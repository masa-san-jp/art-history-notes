import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from cross_region import audit_cross_region, validate_baseline, validate_reviews


def place(entity_id, region):
    return {"id": entity_id, "type": "place", "region": region, "space": []}


def movement(entity_id, origin="place/paris", relations=None, space=None):
    return {
        "id": entity_id,
        "type": "movement",
        "time": {"start": "1900", "end": ".."},
        "space": [{"role": "originated_in", "target": origin}] + (space or []),
        "relations": relations or [],
    }


class CrossRegionAuditTests(unittest.TestCase):
    def test_all_four_routes_are_reported_with_edges_and_destination_regions(self):
        entities = {
            "movement/example": movement(
                "movement/example",
                relations=[
                    {"type": "influenced_by", "target": "movement/asia",
                     "certainty": "scholarly", "source": "https://example.test/movement"},
                    {"type": "diffused_to", "target": "place/new-york-city",
                     "certainty": "scholarly", "source": "https://example.test/diffusion"},
                    {"type": "exhibited_at", "target": "event/asia",
                     "certainty": "scholarly", "source": "https://example.test/exhibition"},
                ],
                space=[{"role": "active_in", "target": "place/tokyo"}],
            ),
            "movement/asia": movement("movement/asia", origin="place/tokyo"),
            "place/paris": place("place/paris", "europe-west"),
            "place/tokyo": place("place/tokyo", "asia-east-japan"),
            "place/new-york-city": place("place/new-york-city", "americas-north"),
            "event/asia": {
                "id": "event/asia", "type": "event", "time": {"start": "1900", "end": ".."},
                "space": [{"role": "held_at", "target": "place/tokyo"}],
            },
        }
        result = audit_cross_region(entities)
        row = next(item for item in result["movements"] if item["movement_id"] == "movement/example")
        self.assertEqual("connected", row["status"])
        self.assertEqual({"movement-relation", "diffused-to-place", "active-in-place", "exhibited-at-place"},
                         {route["kind"] for route in row["routes"]})
        for route in row["routes"]:
            self.assertTrue(route["edges"])
            self.assertTrue(route["destination_regions"])

    def test_person_and_work_edges_do_not_count_as_cross_region(self):
        entities = {
            "movement/example": movement(
                "movement/example",
                relations=[
                    {"type": "created_by", "target": "person/example"},
                    {"type": "depicts", "target": "work/example"},
                ],
            ),
            "place/paris": place("place/paris", "europe-west"),
            "person/example": {"id": "person/example", "type": "person"},
            "work/example": {"id": "work/example", "type": "work"},
        }
        result = audit_cross_region(entities)
        self.assertEqual(["movement/example"], result["unreviewed"])
        self.assertEqual([], next(iter(result["movements"]))["routes"])

    def test_categories_are_exclusive_and_reviews_are_validated(self):
        entities = {
            "movement/connected": movement(
                "movement/connected",
                relations=[{"type": "diffused_to", "target": "place/new-york-city"}],
            ),
            "movement/reviewed": dict(
                movement("movement/reviewed"),
                sources=[
                    {"url": "https://example.test/a", "kind": "reference"},
                    {"url": "https://example.org/b", "kind": "reference"},
                ],
            ),
            "movement/unreviewed": movement("movement/unreviewed"),
            "place/paris": place("place/paris", "europe-west"),
            "place/new-york-city": place("place/new-york-city", "americas-north"),
        }
        reviews = [{
            "movement_id": "movement/reviewed",
            "status": "no-documented-cross-region-relation",
            "checked": "2026-08-25",
            "note": "対象範囲の資料では域外接続を確認できない",
            "sources": ["https://example.test/a", "https://example.org/b"],
        }]
        result = audit_cross_region(entities, reviews=reviews)
        errors = validate_reviews(reviews, entities, result)
        self.assertEqual([], errors)
        self.assertEqual({"connected": 1, "reviewed-no-documented-link": 1, "unreviewed": 1}, result["counts"])
        self.assertEqual(3, sum(result["counts"].values()))

        bad = [dict(reviews[0]), dict(reviews[0])]
        bad[0]["sources"] = ["not-a-url"]
        bad_result = audit_cross_region(entities, reviews=bad)
        errors = "\n".join(validate_reviews(bad, entities, bad_result))
        self.assertIn("movement_idが重複", errors)
        self.assertIn("sourcesはhttp(s) URL 2件以上", errors)

        connected_review = [dict(reviews[0], movement_id="movement/connected")]
        connected_result = audit_cross_region(entities, reviews=connected_review)
        self.assertIn("既にconnected", "\n".join(validate_reviews(connected_review, entities, connected_result)))

    def test_baseline_rejects_duplicates_unknown_ids_and_new_unreviewed_ids(self):
        entities = {
            "movement/one": movement("movement/one"),
            "movement/two": movement("movement/two"),
            "place/paris": place("place/paris", "europe-west"),
        }
        audit = audit_cross_region(entities)
        baseline = {
            "schema_version": 1,
            "source_commit": "a" * 40,
            "movement_count": 1,
            "movement_ids": ["movement/one"],
        }
        errors = validate_baseline(baseline, entities, audit)
        self.assertIn("baselineにない未調査movement", "\n".join(errors))

        bad = dict(baseline, movement_count=3,
                   movement_ids=["movement/one", "movement/one"])
        errors = "\n".join(validate_baseline(bad, entities))
        self.assertIn("件数が不一致", errors)
        self.assertIn("重複", errors)

        unknown = dict(baseline, movement_count=1, movement_ids=["movement/missing"])
        self.assertIn("存在しないmovement_id", "\n".join(validate_baseline(unknown, entities)))


if __name__ == "__main__":
    unittest.main()
