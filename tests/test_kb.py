import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from kb import (astronomical_year_to_label, bce_year_to_astronomical, century_of_year,
                edtf_ok, edtf_year_range, human_year_to_astronomical, regions_of)


class KbTimeAndRegionTests(unittest.TestCase):
    def test_bce_edtf(self):
        self.assertTrue(edtf_ok("-0900"))
        self.assertTrue(edtf_ok("-09XX"))
        self.assertEqual((-900, -900), edtf_year_range("-0900"))
        self.assertEqual((-999, -900), edtf_year_range("-09XX"))
        self.assertEqual((-899, -800), edtf_year_range("-08XX"))
        self.assertEqual((0, 0), edtf_year_range("0000"))
        self.assertEqual((-1, -1), edtf_year_range("-0001"))
        self.assertEqual(-10, century_of_year(-900))
        self.assertEqual(-1, century_of_year(-1))
        self.assertEqual(-1, century_of_year(0))
        self.assertEqual(-1, century_of_year(-99))
        self.assertEqual(-2, century_of_year(-100))
        self.assertEqual(1, century_of_year(1))
        self.assertFalse(edtf_ok("-900"))

    def test_astronomical_year_labels_and_conversion(self):
        self.assertEqual("1BCE", astronomical_year_to_label(0))
        self.assertEqual("2BCE", astronomical_year_to_label(-1))
        self.assertEqual("1CE", astronomical_year_to_label(1))
        self.assertEqual(-899, bce_year_to_astronomical(900))
        self.assertEqual(-899, human_year_to_astronomical(900, "BCE"))
        self.assertEqual(2026, human_year_to_astronomical(2026, "CE"))
        with self.assertRaises(ValueError):
            human_year_to_astronomical(0, "BCE")
        with self.assertRaises(ValueError):
            human_year_to_astronomical(1, "BAD")

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
