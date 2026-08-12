import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from build_graph import render_coverage, validate_coverage_reviews


class CoverageReviewTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {"buckets": {"oceania": {"label_ja": "オセアニア", "west": False}}}

    def test_reviewed_empty_cell_is_valid(self):
        reviews = [{
            "region": "oceania", "century": "20", "status": "no-known-grouping",
            "note": "調査範囲では該当する括りを確認できない",
            "sources": ["https://www.nma.gov.au/"],
        }]
        errors = []
        validate_coverage_reviews(reviews, self.cfg, {"grid": {}}, errors)
        self.assertEqual([], errors)

    def test_review_cannot_hide_an_existing_movement(self):
        reviews = [{
            "region": "oceania", "century": "20", "status": "no-known-grouping",
            "note": "調査範囲では該当する括りを確認できない",
            "sources": ["https://www.nma.gov.au/"],
        }]
        errors = []
        validate_coverage_reviews(reviews, self.cfg, {"grid": {"oceania": {"20": 1}}}, errors)
        self.assertTrue(any("movement が存在するセル" in error for error in errors))

    def test_render_marks_reviewed_cell_as_empty_set(self):
        cov = {
            "as_of": "2026-08-12", "movement_total": 0, "movement_stub_excluded": 0,
            "by_status": {}, "grid": {}, "per_bucket": {"oceania": 0},
            "origin_unknown": [], "origin_multiple": [], "isolated": [],
            "no_known_grouping": [{
                "region": "oceania", "century": "20", "status": "no-known-grouping",
                "note": "調査範囲では該当する括りを確認できない",
                "sources": ["https://www.nma.gov.au/"],
            }],
            "progress": {},
        }
        rendered = render_coverage(cov, self.cfg, {})
        self.assertIn("| oceania（オセアニア） ※非西洋 | ∅ |", rendered)
        self.assertIn("`no-known-grouping`", rendered)


if __name__ == "__main__":
    unittest.main()
