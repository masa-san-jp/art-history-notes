import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from verified_movement import audit_manifest, validate_transition


def source(url="https://museum.example/art"):
    return [{"url": url, "kind": "institutional"}]


def movement(entity_id, status="draft"):
    return {
        "id": entity_id,
        "type": "movement",
        "status": status,
        "time": {"start": "1900", "end": ".."},
        "space": [{"role": "originated_in", "target": "place/example"}],
        "claims": [
            {"field": "time", "source": "https://museum.example/art", "certainty": "scholarly"},
            {"field": "originated_in", "source": "https://museum.example/art", "certainty": "scholarly"},
            {"field": "kind", "source": "https://museum.example/art", "certainty": "scholarly"},
        ],
        "sources": source(),
    }


class VerifiedMovementTests(unittest.TestCase):
    def test_false_reports_incomplete_and_allows_manifest_external_draft(self):
        entities = {
            "movement/one": movement("movement/one", "verified"),
            "movement/two": movement("movement/two", "draft"),
            "movement/external": movement("movement/external", "draft"),
            "place/example": {"type": "place", "region": "europe-west"},
        }
        manifest = {
            "schema_version": 1,
            "source_commit": "a" * 40,
            "movement_count": 2,
            "enforce_complete": False,
            "movement_ids": ["movement/one", "movement/two"],
        }
        report, errors = audit_manifest(manifest, entities)
        self.assertEqual([], errors)
        self.assertEqual(1, report["verified"])
        self.assertEqual(["movement/two"], report["incomplete"])

    def test_true_requires_every_manifest_movement_verified(self):
        entities = {
            "movement/one": movement("movement/one", "verified"),
            "movement/two": movement("movement/two", "draft"),
            "place/example": {"type": "place", "region": "europe-west"},
        }
        manifest = {
            "schema_version": 1,
            "source_commit": "a" * 40,
            "movement_count": 2,
            "enforce_complete": True,
            "movement_ids": ["movement/one", "movement/two"],
        }
        _report, errors = audit_manifest(manifest, entities)
        self.assertIn("未完了", "\n".join(errors))

    def test_complete_gate_cannot_regress(self):
        previous = {"enforce_complete": True}
        self.assertEqual([], validate_transition(previous, {"enforce_complete": True}))
        self.assertIn("退行", "\n".join(validate_transition(previous, {"enforce_complete": False})))


if __name__ == "__main__":
    unittest.main()
