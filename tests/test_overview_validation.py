import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import build_graph


def entity(entity_id, entity_type="movement", **extra):
    value = {
        "id": entity_id,
        "type": entity_type,
        "updated": "2026-08-13",
        "path": f"entities/{entity_type}s/{entity_id.split('/', 1)[1]}.md",
        "relations": [],
        "space": [],
    }
    value.update(extra)
    return value


class OverviewValidationTests(unittest.TestCase):
    def validate(self, text, entities):
        with tempfile.TemporaryDirectory() as directory:
            overview_dir = Path(directory)
            (overview_dir / "sample.md").write_text(text, encoding="utf-8")
            errors = []
            with mock.patch.object(build_graph, "OVERVIEWS", overview_dir):
                build_graph.validate_overviews(entities, errors)
            return errors

    def test_scalar_relation_and_space_assertions_pass(self):
        entities = {
            "movement/a": entity(
                "movement/a",
                kind="retrospective",
                relations=[{"type": "grouped_as", "target": "movement/b"}],
                space=[{"role": "originated_in", "target": "place/x"}],
            ),
            "movement/b": entity("movement/b", kind="retrospective"),
            "place/x": entity("place/x", "place"),
        }
        text = """---
as_of: 2026-08-13
depends_on: [movement/a, movement/b, place/x]
assertions:
  - {subject: movement/a, field: kind, equals: retrospective}
  - {subject: movement/a, relation: grouped_as, target: movement/b}
  - {subject: movement/a, space_role: originated_in, target: place/x}
---

本文
"""
        self.assertEqual([], self.validate(text, entities))

    def test_mismatch_and_missing_dependency_are_reported(self):
        entities = {"movement/a": entity("movement/a", kind="lineage-school")}
        text = """---
as_of: 2026-08-13
depends_on: []
assertions:
  - {subject: movement/a, field: kind, equals: retrospective}
---

本文
"""
        errors = self.validate(text, entities)
        self.assertTrue(any("期待値" in error for error in errors))
        self.assertTrue(any("depends_onに参照先が不足" in error for error in errors))

    def test_coverage_date_must_match_entities(self):
        with tempfile.TemporaryDirectory() as directory:
            overview_dir = Path(directory)
            (overview_dir / "coverage.md").write_text(
                "---\nas_of: 2026-08-12\ndepends_on: []\n---\n"
                "データの最新日: 2026-08-12\n", encoding="utf-8")
            errors = []
            with mock.patch.object(build_graph, "OVERVIEWS", overview_dir):
                build_graph.validate_overviews(
                    {"movement/a": entity("movement/a")}, errors)
            self.assertTrue(any("entityの最新日" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
