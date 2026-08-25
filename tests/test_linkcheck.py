import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import linkcheck


class LinkcheckTests(unittest.TestCase):
    def test_report_has_deterministic_results_and_blocked_categories(self):
        found = {
            "https://example.test/ok": ["entities/a.md"],
            "https://example.test/dead": ["entities/b.md"],
            "https://example.test/gone": ["entities/c.md"],
            "https://example.test/rate-limited": ["entities/d.md"],
            "https://example.test/timeout": ["entities/e.md"],
        }
        payload = linkcheck.report(
            found,
            {
                "https://example.test/ok": 200,
                "https://example.test/dead": 404,
                "https://example.test/gone": 410,
                "https://example.test/rate-limited": 429,
                "https://example.test/timeout": 0,
            },
            checked_at="2026-08-25T00:00:00Z",
        )
        self.assertEqual({"ok": 1, "dead": 2, "blocked": 2}, payload["counts"])
        dead = next(item for item in payload["results"] if item["http_status"] == 404)
        self.assertEqual("dead", dead["result"])
        self.assertEqual(404, dead["http_status"])
        self.assertIsNone(payload["results"][-1]["http_status"])
        other = linkcheck.report(
            found,
            {
                "https://example.test/ok": 200,
                "https://example.test/dead": 404,
                "https://example.test/gone": 410,
                "https://example.test/rate-limited": 429,
                "https://example.test/timeout": 0,
            },
            checked_at="2026-08-26T00:00:00Z",
        )
        payload.pop("checked_at")
        other.pop("checked_at")
        self.assertEqual(payload, other)

    def test_output_json_and_404_410_exit_nonzero(self):
        found = {
            "https://example.test/ok": ["entities/a.md"],
            "https://example.test/dead": ["entities/b.md"],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "linkcheck.json"
            with mock.patch.object(linkcheck, "collect", return_value=found), \
                    mock.patch.object(linkcheck, "status", side_effect=[200, 410]), \
                    mock.patch.object(sys, "argv", ["linkcheck.py", "--output", str(output)]):
                self.assertEqual(1, linkcheck.main())
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(1, payload["counts"]["dead"])
        self.assertIn("checked_at", payload)


if __name__ == "__main__":
    unittest.main()
