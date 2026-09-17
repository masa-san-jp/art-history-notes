import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from tools import theme_research


def fixture_entities():
    return {
        "movement/mughal-painting": {
            "id": "movement/mughal-painting",
            "type": "movement",
            "label_ja": "ムガル絵画",
            "status": "verified",
            "sources": [{"url": "https://example.org/a"}, {"url": "https://example.org/b"}],
        },
        "movement/kowhaiwhai": {
            "id": "movement/kowhaiwhai",
            "type": "movement",
            "label_ja": "コーワイワイ",
            "status": "verified",
            "sources": [{"url": "https://example.org/c"}],
        },
    }


class ThemeResearchTest(unittest.TestCase):
    def test_hit_summary_reports_status_and_source_count(self):
        entities = fixture_entities()
        summary = theme_research.hit_summary("movement/mughal-painting", entities)
        self.assertEqual(summary["status"], "verified")
        self.assertEqual(summary["n_sources"], 2)

    def test_hit_summary_missing_entity_is_safe(self):
        summary = theme_research.hit_summary("movement/does-not-exist", {})
        self.assertIsNone(summary["label_ja"])
        self.assertEqual(summary["n_sources"], 0)

    def test_main_logs_query_and_reports_hits(self):
        entities = fixture_entities()
        logged = []
        with mock.patch.object(theme_research, "load_entities", return_value=(entities, [])), \
             mock.patch.object(theme_research, "search_entities",
                                return_value=["movement/mughal-painting"]), \
             mock.patch.object(theme_research, "log_query",
                                side_effect=lambda term, hits: logged.append((term, hits))), \
             mock.patch.object(theme_research, "load_grid", return_value={"asia-south": {"18": 1}}), \
             mock.patch("sys.argv", ["theme_research.py", "--theme", "ムガル絵画", "--json"]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                exit_code = theme_research.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(logged, [("ムガル絵画", 1)])
        report = json.loads(out.getvalue())
        self.assertEqual(report["theme"], "ムガル絵画")
        self.assertEqual(report["hit_count"], 1)
        self.assertEqual(report["hits"][0]["id"], "movement/mughal-painting")
        self.assertEqual(report["coverage_grid"], {"asia-south": {"18": 1}})

    def test_main_reports_miss_without_error(self):
        logged = []
        with mock.patch.object(theme_research, "load_entities", return_value=({}, [])), \
             mock.patch.object(theme_research, "search_entities", return_value=[]), \
             mock.patch.object(theme_research, "log_query",
                                side_effect=lambda term, hits: logged.append((term, hits))), \
             mock.patch.object(theme_research, "load_grid", return_value={}), \
             mock.patch("sys.argv", ["theme_research.py", "--theme", "存在しないテーマ"]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                exit_code = theme_research.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(logged, [("存在しないテーマ", 0)])
        self.assertIn("該当なし", out.getvalue())


if __name__ == "__main__":
    unittest.main()
