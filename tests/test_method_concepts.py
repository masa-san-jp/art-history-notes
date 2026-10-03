import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from method_concepts import classify, load_method_config, method_concept_ids, method_validation_errors
from kb import build_edges, load_entities


class MethodConceptRulesTest(unittest.TestCase):
    def test_versioned_rules_are_complete(self):
        config = load_method_config()
        self.assertEqual(config["contract_version"], "method-concepts/v1")
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
        self.assertEqual(len(methods), 3)
        self.assertEqual(len(links), 3)


if __name__ == "__main__":
    unittest.main()
