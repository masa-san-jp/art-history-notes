import copy
import math
import unittest
from pathlib import Path
from unittest import mock

from tools import build_graph


def valid_meta(entity_id="movement/example", entity_type="movement"):
    directory = {
        "movement": "movements",
        "place": "places",
    }[entity_type]
    meta = {
        "id": entity_id,
        "uri": f"urn:ahn:{entity_id}",
        "type": entity_type,
        "label_ja": "例",
        "label_en": "Example",
        "authority": {
            "wikidata": None,
            "aat": None,
            "ulan": None,
            "tgn": None,
            "ndl": None,
            "jpsearch": None,
            "none_reason": "独立典拠IDを未確認",
        },
        "time": {"start": "1900", "end": "..", "display": "1900年以降"},
        "relations": [],
        "space": [],
        "claims": [],
        "sources": ["https://example.test/source"],
        "status": "draft",
        "updated": "2026-08-13",
        "aliases": [],
    }
    if entity_type == "movement":
        meta.update(
            {
                "kind": "retrospective",
                "naming": {
                    "self_identified": False,
                    "named_by": None,
                    "named_when": None,
                    "original_label": "Example",
                    "note": "命名の経緯を調査中",
                },
            }
        )
    else:
        meta.update({"region": "test", "coordinates": [35.0, 139.0]})
    meta["path"] = f"entities/{directory}/{entity_id.split('/', 1)[1]}.md"
    return meta


class SemanticValidationTests(unittest.TestCase):
    def validate(self, *metas, buckets=None):
        entities = {meta["id"]: meta for meta in metas}
        records = [
            (Path(meta["path"]), meta, "")
            for meta in metas
        ]
        errors = []
        with mock.patch.object(build_graph, "load_region_history", return_value={}):
            build_graph.validate(
                entities,
                records,
                {"buckets": buckets or {"test"}},
                errors,
            )
        return errors

    def test_valid_movement_and_place_pass(self):
        self.assertEqual([], self.validate(valid_meta(), valid_meta("place/tokyo", "place")))

    def test_coordinates_reject_shape_nonfinite_and_range(self):
        place = valid_meta("place/example", "place")
        del place["coordinates"]
        self.assertTrue(any("2要素配列" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = [math.nan, 0]
        self.assertTrue(any("有限の数値" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = [math.inf, 0]
        self.assertTrue(any("有限の数値" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = ["35", 139]
        self.assertTrue(any("有限の数値" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = [True, 139]
        self.assertTrue(any("有限の数値" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = [91, 0]
        self.assertTrue(any("範囲外" in error for error in self.validate(place)))

        place = valid_meta("place/example", "place")
        place["coordinates"] = [35]
        self.assertTrue(any("2要素配列" in error for error in self.validate(place)))

    def test_time_rejects_open_start_and_reverse_range_but_allows_ambiguous_range(self):
        movement = valid_meta()
        movement["time"] = {"start": "..", "end": "1900"}
        self.assertTrue(any("time.start に開いた端" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["time"] = {"start": "2000", "end": "1900"}
        self.assertTrue(any("start がtime.endより後" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["time"] = {"start": "19XX", "end": "2000"}
        self.assertFalse(any("start がtime.endより後" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["time"] = {"start": 1900, "end": ".."}
        self.assertTrue(any("time.start" in error for error in self.validate(movement)))

    def test_naming_requires_edtf_original_label_and_named_by_target(self):
        movement = valid_meta()
        movement["naming"]["self_identified"] = "false"
        self.assertTrue(any("self_identified はbool" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["naming"]["named_when"] = "999"
        self.assertTrue(any("named_when" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["naming"]["original_label"] = None
        movement["naming"]["note"] = ""
        self.assertTrue(any("original_label=null" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["naming"]["named_by"] = "person/missing"
        self.assertTrue(any("named_by" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["naming"]["original_label"] = ""
        self.assertTrue(any("original_label は空でない" in error for error in self.validate(movement)))

    def test_authority_requires_known_ids_or_reason(self):
        movement = valid_meta()
        movement["authority"]["wikidata"] = "not-a-qid"
        movement["authority"]["none_reason"] = None
        errors = self.validate(movement)
        self.assertTrue(any("authority.wikidata" in error for error in errors))
        self.assertTrue(any("典拠が1つも無い" in error for error in errors))

        movement = valid_meta()
        movement["authority"]["ulan"] = "500123456"
        movement["authority"]["none_reason"] = "検索メモ"
        self.assertTrue(any("none_reasonはnull" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["authority"]["unknown"] = "value"
        self.assertTrue(any("未知のkey" in error for error in self.validate(movement)))

    def test_authority_accepts_all_supported_identifiers(self):
        movement = valid_meta()
        movement["authority"].update(
            {
                "wikidata": "Q123",
                "aat": "300123456",
                "ulan": "500123456",
                "tgn": "7012345",
                "ndl": "12345678",
                "jpsearch": "https://jpsearch.go.jp/123",
                "none_reason": None,
            }
        )
        self.assertEqual([], self.validate(movement))

    def test_authority_rejects_each_bad_identifier_format(self):
        bad_values = {
            "wikidata": "P123",
            "aat": "12345678",
            "ulan": "12345678",
            "tgn": "123456",
            "ndl": "1234567",
        }
        for key, value in bad_values.items():
            with self.subTest(key=key):
                movement = valid_meta()
                movement["authority"][key] = value
                self.assertTrue(any(f"authority.{key}" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["authority"]["jpsearch"] = ""
        self.assertTrue(any("authority.jpsearch" in error for error in self.validate(movement)))

    def test_updated_alias_and_claim_rules(self):
        movement = valid_meta()
        movement["updated"] = "2026-02-30"
        self.assertTrue(any("updated" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["aliases"] = ["movement/Bad-Slug"]
        self.assertTrue(any("型付きalias" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["aliases"] = [""]
        self.assertTrue(any("alias は空でない" in error for error in self.validate(movement)))

        movement = valid_meta()
        movement["aliases"] = ["movement/other"]
        other = valid_meta("movement/other")
        self.assertTrue(any("既存の id と衝突" in error for error in self.validate(movement, other)))

        movement = valid_meta()
        other = valid_meta("movement/other")
        movement["aliases"] = ["旧称"]
        other["aliases"] = ["旧称"]
        self.assertTrue(any("alias 旧称 が重複" in error for error in self.validate(movement, other)))

        movement = valid_meta()
        claim = {"field": "time", "source": "https://example.test", "certainty": "scholarly"}
        movement["claims"] = [copy.deepcopy(claim), copy.deepcopy(claim)]
        self.assertTrue(any("完全重複" in error for error in self.validate(movement)))

        for field, value in (
            ("field", ""),
            ("source", ""),
            ("certainty", "unknown"),
        ):
            with self.subTest(field=field):
                movement = valid_meta()
                invalid_claim = copy.deepcopy(claim)
                invalid_claim[field] = value
                movement["claims"] = [invalid_claim]
                errors = self.validate(movement)
                self.assertTrue(errors, (field, errors))


if __name__ == "__main__":
    unittest.main()
