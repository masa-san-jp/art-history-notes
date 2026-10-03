import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from method_concepts import (classify, load_method_config, method_concept_ids,
                             method_validation_errors, concept_validation_errors)
from kb import build_edges, load_entities


class MethodConceptRulesTest(unittest.TestCase):
    def test_versioned_rules_are_complete(self):
        config = load_method_config()
        self.assertEqual(config["contract_version"], "method-concepts/v2")
        self.assertEqual(set(config["legacy_concept_ids"]), {
            "concept/automatism", "concept/divisionism", "concept/trompe-loeil", "concept/hurufiyya",
            "concept/minhwa", "concept/ukiyo-e", "concept/harmony", "concept/ma", "concept/yohaku"})
        self.assertEqual(config["classification"]["required_method_fields"],
                         ["fixes", "varies", "requires", "origin_domain"])

    def test_configured_method_term_is_concept(self):
        result = classify("fractal", {"exact_label_hits": [], "hits": []})
        self.assertEqual(result["entity_type"], "concept")
        self.assertTrue(result["is_method"])
        self.assertEqual(result["reason"], "configured-method-term")

    def test_style_exclusion_defaults_to_movement_without_existing_hit(self):
        result = classify("ukiyo-e", {"exact_label_hits": [], "hits": []})
        self.assertEqual(result["entity_type"], "movement")
        self.assertFalse(result["is_method"])

    def test_method_shape_rejects_empty_shell(self):
        errors = method_validation_errors({"fixes": [], "varies": [], "requires": [], "origin_domain": "art"})
        self.assertEqual(len(errors), 3)
        self.assertTrue(all("1件以上" in error for error in errors))

    def test_existing_data_has_measurable_method_paths(self):
        entities, _ = load_entities()
        methods = method_concept_ids(entities)
        links = [edge for edge in build_edges(entities)
                 if edge.get("from") in methods and edge.get("type") == "used_by"]
        self.assertGreaterEqual(len(methods), 3)
        self.assertGreaterEqual(len(links), 2)
        self.assertNotIn({"from": "concept/iterated-boundary-generation", "type": "used_by",
                          "to": "movement/computer-art", "derived": True}, links)

    def test_missing_method_cannot_bypass_new_concept_gate(self):
        for status in ("draft", "verified"):
            for method in ("absent", None):
                meta = {"id": "concept/new-method", "type": "concept", "status": status}
                if method is None:
                    meta["method"] = None
                self.assertTrue(concept_validation_errors(meta))
        for eid in load_method_config()["legacy_concept_ids"]:
            self.assertEqual(concept_validation_errors({"id": eid, "type": "concept", "status": "draft"}), [])
        self.assertEqual(concept_validation_errors({"id": "concept/new-method", "type": "concept", "status": "stub"}), [])

    def test_non_concept_does_not_reload_method_config(self):
        from unittest.mock import patch
        with patch("method_concepts.load_method_config", side_effect=AssertionError("unnecessary read")):
            self.assertEqual(concept_validation_errors({"type": "work"}), [])
            self.assertTrue(concept_validation_errors({"type": "work", "method": {}}))

    def test_graph_enforces_method_and_sourced_relation_contract(self):
        import copy
        from build_graph import validate
        from kb import ROOT, load_config
        entities, _ = load_entities()
        config = load_config()
        for field in ("method", "sources"):
            meta = copy.deepcopy(entities["concept/poured-painting"])
            meta.pop(field)
            errors = []
            validate(entities, [(ROOT / meta["path"], meta, "")], config, errors)
            self.assertTrue(errors, field)
        for field in ("source", "certainty"):
            meta = copy.deepcopy(entities["movement/surrealism"])
            meta["relations"] = [copy.deepcopy(meta["relations"][0])]
            meta["relations"][0].pop(field)
            errors = []
            validate(entities, [(ROOT / meta["path"], meta, "")], config, errors)
            self.assertTrue(any("uses_method" in error for error in errors), errors)
        meta = copy.deepcopy(entities["concept/automatism"])
        meta["relations"] = [{"type": "uses_method", "target": "concept/poured-painting",
                              "certainty": "scholarly", "source": meta["sources"][0]["url"]}]
        errors = []
        validate(entities, [(ROOT / meta["path"], meta, "")], config, errors)
        self.assertTrue(any("関係元" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
