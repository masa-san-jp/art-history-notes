import copy
import contextlib
import io
import unittest
from unittest import mock

from tools import query_spacetime


def place(entity_id, latitude, longitude, region):
    return {
        "id": entity_id,
        "type": "place",
        "label_ja": entity_id.rsplit("/", 1)[1],
        "region": region,
        "coordinates": [latitude, longitude],
        "time": {"start": "0000", "end": ".."},
    }


def movement(entity_id, start, end, place_id=None):
    return {
        "id": entity_id,
        "type": "movement",
        "label_ja": entity_id.rsplit("/", 1)[1],
        "time": {"start": start, "end": end},
        "space": ([{"role": "originated_in", "target": place_id}]
                  if place_id else []),
    }


def fixture_entities():
    entities = {
        "place/paris": place("place/paris", 48.8566, 2.3522, "europe-west"),
        "place/tokyo": place("place/tokyo", 35.6762, 139.6503, "asia-east-japan"),
        "place/center": place("place/center", 0, 0, "europe-west"),
        "place/edge": place("place/edge", 0, 1, "europe-west"),
        "place/far": place("place/far", 0, 2, "europe-west"),
        "place/istanbul": place("place/istanbul", 41.0082, 28.9784, "mena"),
    }
    entities.update(
        {
            "movement/exact": movement("movement/exact", "1884", "1886", "place/paris"),
            "movement/mask": movement("movement/mask", "19XX", "..", "place/tokyo"),
            "movement/approx": movement("movement/approx", "1885~", "1886", "place/paris"),
            "movement/bce": movement("movement/bce", "-0899", "-0800", "place/paris"),
            "movement/ongoing": movement("movement/ongoing", "1880", "..", "place/center"),
            "movement/old": movement("movement/old", "1800", "1850", "place/paris"),
            "movement/unknown-start": movement("movement/unknown-start", None, "..", "place/paris"),
            "movement/unknown-end": movement("movement/unknown-end", "1880", None, "place/paris"),
            "movement/no-place": movement("movement/no-place", "1880", "1890"),
            "movement/distance-edge": movement("movement/distance-edge", "1885", "1885", "place/edge"),
            "movement/distance-far": movement("movement/distance-far", "1885", "1885", "place/far"),
            "movement/historical": movement("movement/historical", "1200", "1500", "place/istanbul"),
        }
    )
    return entities


class SpacetimeQueryTests(unittest.TestCase):
    def setUp(self):
        self.entities = fixture_entities()
        self.history = {
            "place/istanbul": [
                {"start": "0330", "end": "1453", "region": "europe-east"},
                {"start": "1453", "end": "..", "region": "mena"},
            ]
        }

    def query(self, year, **kwargs):
        return query_spacetime.query_entities(
            self.entities,
            (year, year),
            region_history=self.history,
            **kwargs,
        )

    def test_exact_mask_approx_bce_and_open_end_overlap(self):
        payload = self.query(1885)
        ids = {result["id"] for result in payload["results"]}
        self.assertIn("movement/exact", ids)
        self.assertIn("movement/approx", ids)
        self.assertIn("movement/ongoing", ids)
        self.assertNotIn("movement/mask", ids)

        payload = self.query(1950)
        self.assertIn("movement/mask", {result["id"] for result in payload["results"]})

        payload = self.query(-850)
        self.assertIn("movement/bce", {result["id"] for result in payload["results"]})

    def test_unknown_time_and_place_are_reported_without_inference(self):
        payload = self.query(1885)
        excluded = {item["id"]: item["reasons"] for item in payload["excluded"]}
        self.assertIn("unknown-time", excluded["movement/unknown-start"])
        self.assertIn("unknown-time", excluded["movement/unknown-end"])
        self.assertIn("unknown-place", excluded["movement/no-place"])

    def test_historical_region_uses_query_period(self):
        before = self.query(1400)
        before_result = next(result for result in before["results"]
                             if result["id"] == "movement/historical")
        self.assertEqual("europe-east", before_result["region"])

        after = self.query(1500)
        after_result = next(result for result in after["results"]
                            if result["id"] == "movement/historical")
        self.assertEqual("mena", after_result["region"])

    def test_region_and_distance_filters(self):
        payload = self.query(1950, regions=["asia-east-japan"])
        self.assertEqual({"movement/mask"}, {result["id"] for result in payload["results"]})

        boundary = query_spacetime.haversine_km(
            self.entities["place/center"]["coordinates"],
            self.entities["place/edge"]["coordinates"],
        )
        payload = self.query(1885, near="place/center", radius_km=boundary)
        ids = {result["id"] for result in payload["results"]}
        self.assertIn("movement/ongoing", ids)
        self.assertIn("movement/distance-edge", ids)
        self.assertNotIn("movement/distance-far", ids)
        edge = next(result for result in payload["results"]
                    if result["id"] == "movement/distance-edge")
        self.assertEqual(round(boundary, 3), edge["distance_km"])

    def test_type_specific_place_role_and_no_graph_mutation(self):
        before = copy.deepcopy(self.entities)
        payload = self.query(1885, entity_type="place")
        self.assertTrue(all(result["space_role"] == "self" for result in payload["results"]))
        self.assertEqual(before, self.entities)

    def test_json_is_byte_deterministic(self):
        payload = self.query(1885)
        self.assertEqual(query_spacetime.render_json(payload), query_spacetime.render_json(payload))
        self.assertIn('"results": [', query_spacetime.render_json(payload))

    def test_cli_rejects_invalid_time_and_distance_arguments(self):
        invalid = [
            ["--at", "1885", "--from", "1880", "--to", "1890"],
            ["--from", "1880"],
            ["--at", "1885", "--near", "place/paris"],
            ["--at", "1885", "--radius-km", "10"],
            ["--at", "1885", "--near", "place/paris", "--radius-km", "-1"],
        ]
        for argv in invalid:
            with self.subTest(argv=argv), self.assertRaises(SystemExit), \
                    contextlib.redirect_stderr(io.StringIO()):
                query_spacetime.parse_args(argv)

    def test_cli_rejects_unknown_near_id(self):
        with mock.patch.object(query_spacetime, "load_graph", return_value=self.entities), \
                mock.patch.object(query_spacetime, "load_config", return_value={"buckets": {}}), \
                mock.patch.object(query_spacetime, "load_region_history", return_value={}):
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stderr(io.StringIO()):
                    query_spacetime.main([
                        "--at", "1885", "--near", "place/missing", "--radius-km", "1",
                    ])


if __name__ == "__main__":
    unittest.main()
