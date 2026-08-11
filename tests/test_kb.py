import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from kb import century_of_year, edtf_ok, edtf_year_range, regions_of


class KbTimeAndRegionTests(unittest.TestCase):
    def test_bce_edtf(self):
        self.assertTrue(edtf_ok("-0900"))
        self.assertTrue(edtf_ok("-09XX"))
        self.assertEqual((-900, -900), edtf_year_range("-0900"))
        self.assertEqual((-999, -900), edtf_year_range("-09XX"))
        self.assertEqual(-10, century_of_year(-900))
        self.assertEqual(-1, century_of_year(-1))
        self.assertEqual(1, century_of_year(1))
        self.assertFalse(edtf_ok("-900"))

    def test_region_history_uses_movement_start(self):
        entities = {
            "movement/byzantine": {
                "type": "movement",
                "time": {"start": "1200", "end": ".."},
                "space": [{"role": "originated_in", "target": "place/istanbul"}],
            },
            "movement/ottoman": {
                "type": "movement",
                "time": {"start": "146X", "end": ".."},
                "space": [{"role": "originated_in", "target": "place/istanbul"}],
            },
            "place/istanbul": {"type": "place", "region": "mena"},
        }
        history = {
            "place/istanbul": [
                {"start": "0330", "end": "1453", "region": "europe-east"},
                {"start": "1453", "end": "..", "region": "mena"},
            ]
        }
        self.assertEqual(["europe-east"], regions_of("movement/byzantine", entities, history))
        self.assertEqual(["mena"], regions_of("movement/ottoman", entities, history))

    def test_ambiguous_start_keeps_both_regions(self):
        entities = {
            "movement/uncertain": {
                "type": "movement",
                "time": {"start": "14XX", "end": ".."},
                "space": [{"role": "originated_in", "target": "place/istanbul"}],
            },
            "place/istanbul": {"type": "place", "region": "mena"},
        }
        history = {
            "place/istanbul": [
                {"start": "0330", "end": "1453", "region": "europe-east"},
                {"start": "1453", "end": "..", "region": "mena"},
            ]
        }
        self.assertEqual(["europe-east", "mena"], regions_of("movement/uncertain", entities, history))


if __name__ == "__main__":
    unittest.main()
