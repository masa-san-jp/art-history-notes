import contextlib
import io
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import export_signals


def movement(status="draft", space=None):
    return {
        "id": "movement/example",
        "path": "entities/movements/example.md",
        "type": "movement",
        "kind": "retrospective",
        "label_ja": "例",
        "label_en": "Example",
        "status": status,
        "time": {"start": "1900", "end": ".."},
        "space": space or [{"role": "originated_in", "target": "place/a"}],
        "relations": [{
            "type": "influenced_by",
            "target": "movement/other",
            "certainty": "scholarly",
            "source": "https://example.test/source",
        }],
    }


class ExportSignalsTests(unittest.TestCase):
    def test_unverified_status_is_preserved_as_unknown_validity(self):
        record = export_signals.build_record(
            movement("draft"),
            {"place/a": {"region": "europe-west"}},
            "a" * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            "artistic-research",
        )
        self.assertEqual("unknown", record["validity"]["status"])
        self.assertTrue(any("draft" in item for item in record["unknowns"]))

    def test_multiple_origin_regions_are_not_reduced_to_first(self):
        record = export_signals.build_record(
            movement(space=[
                {"role": "originated_in", "target": "place/a"},
                {"role": "originated_in", "target": "place/b"},
            ]),
            {
                "place/a": {"region": "europe-west"},
                "place/b": {"region": "asia-east-japan"},
            },
            "a" * 40,
            datetime(2026, 8, 14, tzinfo=timezone.utc),
            "artistic-research",
        )
        self.assertEqual("europe-west,asia-east-japan", record["geo"])
        self.assertTrue(any("place/a" in item and "place/b" in item for item in record["unknowns"]))

    def test_unknown_entity_returns_clean_error(self):
        stderr = io.StringIO()
        with mock.patch.object(sys, "argv", ["export_signals.py", "--purpose", "test", "--entity", "movement/missing"]), contextlib.redirect_stderr(stderr):
            self.assertEqual(1, export_signals.main())
        self.assertIn("そのIDは無い", stderr.getvalue())

    def test_dirty_checkout_is_not_used_as_commit_provenance(self):
        with mock.patch.object(export_signals.subprocess, "run") as run:
            run.return_value = mock.Mock(stdout=" M entities/example.md\n")
            with self.assertRaisesRegex(RuntimeError, "dirty"):
                export_signals._head_commit()
        self.assertEqual(1, run.call_count)


if __name__ == "__main__":
    unittest.main()
