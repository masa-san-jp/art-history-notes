import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools import build_graph, bundle, detail_baseline
from tools.kb import build_edges, load_config, load_entities, load_region_history
from test_semantic_validation import valid_meta


def related_fixture():
    movement = valid_meta()
    person = copy.deepcopy(valid_meta("person/example"))
    person.update({"type": "person", "path": "entities/persons/example.md"})
    person.pop("kind", None)
    person.pop("naming", None)
    work = copy.deepcopy(valid_meta("work/example"))
    work.update({"type": "work", "path": "entities/works/example.md"})
    work.pop("kind", None)
    work.pop("naming", None)
    work["relations"] = [{"type": "belongs_to", "target": movement["id"]}]
    work["_test_body"] = "## どう成立しているか\n"
    movement["relations"] = [
        {"type": "influenced_by", "target": person["id"],
         "certainty": "scholarly", "source": "https://example.test/relation"},
    ]
    movement["sources"].append({"url": "https://example.test/relation", "kind": "reference"})
    return movement, person, work


class EvidenceValidationTests(unittest.TestCase):
    def validate(self, movement, *others):
        entities = {meta["id"]: meta for meta in (movement, *others)}
        records = [(Path(meta["path"]), meta, "") for meta in entities.values()]
        errors = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for meta in entities.values():
                path = root / meta["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                body = meta.pop("_test_body", "")
                path.write_text(f"---\n---\n{body}", encoding="utf-8")
            with mock.patch.object(build_graph, "ROOT", root), \
                    mock.patch.object(build_graph, "load_region_history", return_value={}):
                build_graph.validate(entities, records, {"buckets": {"test"}}, errors)
        return errors

    def test_evidence_accepts_existing_person_and_work_relations(self):
        movement, person, work = related_fixture()
        movement["evidence"] = [
            {"target": person["id"], "supports": ["naming", "relation"]},
            {"target": work["id"], "supports": ["kind", "time", "visual-character"]},
        ]
        self.assertEqual([], self.validate(movement, person, work))

    def test_evidence_rejects_missing_target_wrong_type_unknown_support_and_missing_relation(self):
        movement, person, work = related_fixture()
        place = valid_meta("place/example", "place")
        movement["evidence"] = [
            {"target": "person/missing", "supports": ["kind"]},
            {"target": place["id"], "supports": ["kind"]},
            {"target": person["id"], "supports": ["not-a-support"]},
        ]
        errors = self.validate(movement, person, work, place)
        self.assertTrue(any("存在するperson/work ID" in error for error in errors))
        self.assertTrue(any("語彙外" in error for error in errors))

        movement, person, work = related_fixture()
        movement["evidence"] = [{"target": work["id"], "supports": ["kind"]}]
        work["relations"] = []
        self.assertTrue(any("既存relation" in error for error in self.validate(movement, person, work)))

    def test_visual_character_requires_work_heading(self):
        movement, person, work = related_fixture()
        movement["evidence"] = [{"target": work["id"], "supports": ["visual-character"]}]
        work["_test_body"] = "## 事実\n"
        self.assertTrue(any("どう成立しているか" in error
                            for error in self.validate(movement, person, work)))

    def test_manifest_recomputes_to_thirteen_regions(self):
        entities, _ = load_entities()
        config = load_config()
        selected = detail_baseline.select_baseline(entities, config, load_region_history())
        self.assertEqual(set(config["buckets"]), set(selected))
        self.assertEqual([], detail_baseline.validate_manifest(entities, config))

    def test_bundle_includes_evidence_block(self):
        entities, _ = load_entities()
        text = bundle.render(
            ["movement/nanga"], entities, build_edges(entities), "E2E")
        self.assertIn("証拠接続:", text)
        self.assertIn("work/group-pilgrimage-jizo-ike-taiga", text)


if __name__ == "__main__":
    unittest.main()
