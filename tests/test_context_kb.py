import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_context_vectors
from build_context_vectors import build_payloads
from context_kb import (compare_vectors, compute_context_vector, compute_input_digest,
                        load_contexts, validate_contexts)


BODY = """# Context

## 範囲
限定範囲。
## 根拠の読み方
出典の範囲で読む。
## 反対証拠・内部差
内部差を記録する。
## 未確認
未確認事項。
"""


def config():
    got = yaml.safe_load((ROOT / "config" / "context-dimensions.yaml").read_text(encoding="utf-8"))
    got["regions"] = ["europe-west", "asia-east-japan"]
    return got


def signal(number=1, dimension="technology_stance", direction=1, source=None,
           holders=None, certainty="attested", salience=2):
    return {
        "id": f"s{number:03d}",
        "dimension": dimension,
        "direction": direction,
        "salience": salience,
        "holders": holders or ["participants", "critics"],
        "claim": f"signal {number} の主張",
        "certainty": certainty,
        "source": source or f"https://example.org/{number}",
        "note": "この資料の対象を越えて一般化しない",
    }


def context(context_id="context/example", kind="current", signals=None):
    signals = signals if signals is not None else [signal()]
    return {
        "id": context_id,
        "label_ja": context_id,
        "kind": kind,
        "scope": {
            "start": "2026" if kind == "current" else "1909",
            "end": "2026" if kind == "current" else "1914",
            "regions": ["asia-east-japan" if kind == "current" else "europe-west"],
            "domain": "art",
            "topics": ["test-topic"],
        },
        "about": [] if kind == "current" else ["movement/example"],
        "signals": signals,
        "sources": list(dict.fromkeys(item["source"] for item in signals)),
        "status": "draft",
        "updated": "2026-08-10",
        "_path": ROOT / "contexts" / f"{context_id.split('/', 1)[1]}.md",
        "_relative_path": f"contexts/{context_id.split('/', 1)[1]}.md",
        "_body": BODY,
    }


ENTITIES = {
    "movement/example": {"type": "movement"},
    "source/example": {"type": "source"},
}


class ValidationTests(unittest.TestCase):
    def errors(self, item):
        return validate_contexts({item["id"]: item}, ENTITIES, config())

    def assert_error(self, item, fragment):
        self.assertTrue(any(fragment in error for error in self.errors(item)), self.errors(item))

    def test_valid_current_allows_empty_about(self):
        self.assertEqual([], self.errors(context()))

    def test_valid_historical(self):
        self.assertEqual([], self.errors(context(kind="historical")))

    def test_frontmatter_missing_is_collected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contexts_dir = root / "contexts"
            contexts_dir.mkdir()
            (contexts_dir / "bad.md").write_text("# no frontmatter\n", encoding="utf-8")
            loaded = load_contexts(contexts_dir, root)
            self.assertIn("frontmatter がない", "\n".join(validate_contexts(loaded, ENTITIES, config())))

    def test_id_must_match_filename(self):
        item = context()
        item["_path"] = ROOT / "contexts" / "different.md"
        self.assert_error(item, "id とファイル名")

    def test_duplicate_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contexts_dir = root / "contexts"
            contexts_dir.mkdir()
            text = (ROOT / "tests" / "fixtures" / "contexts" / "valid-current.md").read_text(encoding="utf-8")
            (contexts_dir / "a.md").write_text(text.replace("context/valid-current", "context/same"), encoding="utf-8")
            (contexts_dir / "b.md").write_text(text.replace("context/valid-current", "context/same"), encoding="utf-8")
            loaded = load_contexts(contexts_dir, root)
            self.assertIn("id が重複", "\n".join(validate_contexts(loaded, ENTITIES, config())))

    def test_required_field(self):
        item = context()
        del item["label_ja"]
        self.assert_error(item, "必須フィールド label_ja")

    def test_vocabularies(self):
        item = context()
        item["kind"] = "unknown"
        item["status"] = "unknown"
        item["signals"][0]["certainty"] = "unknown"
        item["signals"][0]["holders"] = ["society"]
        joined = "\n".join(self.errors(item))
        for fragment in ("kind が語彙外", "status が語彙外", "certainty が語彙外", "holder が語彙外"):
            self.assertIn(fragment, joined)

    def test_domain_is_art(self):
        item = context()
        item["scope"]["domain"] = "music"
        self.assert_error(item, "scope.domain は art")

    def test_regions_nonempty_and_known(self):
        item = context()
        item["scope"]["regions"] = []
        self.assert_error(item, "scope.regions")
        item["scope"]["regions"] = ["unknown"]
        self.assert_error(item, "未知の region")

    def test_edtf(self):
        item = context()
        item["scope"]["start"] = "not-a-date"
        self.assert_error(item, "scope.start が EDTF")

    def test_historical_requires_about(self):
        item = context(kind="historical")
        item["about"] = []
        self.assert_error(item, "historical context は about")

    def test_unknown_entity_reference(self):
        item = context(kind="historical")
        item["about"] = ["movement/missing"]
        self.assert_error(item, "参照先が存在しない")

    def test_signal_id_format_and_duplicate(self):
        item = context(signals=[signal(1), signal(2)])
        item["signals"][0]["id"] = "bad"
        item["signals"][1]["id"] = "bad"
        joined = "\n".join(self.errors(item))
        self.assertIn("s + 3桁", joined)
        self.assertIn("signal id が重複", joined)

    def test_direction_range_and_bool(self):
        item = context()
        item["signals"][0]["direction"] = True
        self.assert_error(item, "direction は整数")
        item["signals"][0]["direction"] = 3
        self.assert_error(item, "direction は整数")

    def test_direction_zero_is_valid(self):
        item = context()
        item["signals"][0]["direction"] = 0
        self.assertEqual([], self.errors(item))

    def test_salience_range_and_bool(self):
        item = context()
        item["signals"][0]["salience"] = False
        self.assert_error(item, "salience は整数")

    def test_holders_nonempty(self):
        item = context()
        item["signals"][0]["holders"] = []
        self.assert_error(item, "holders は1件以上")

    def test_claim_and_note_nonempty(self):
        item = context()
        item["signals"][0]["claim"] = ""
        item["signals"][0]["note"] = ""
        joined = "\n".join(self.errors(item))
        self.assertIn("claim は空", joined)
        self.assertIn("note は空", joined)

    def test_source_must_be_url_or_source_entity(self):
        item = context()
        item["signals"][0]["source"] = "source/missing"
        item["sources"] = ["source/missing"]
        self.assert_error(item, "既存 source ID")
        item["signals"][0]["source"] = "source/example"
        item["sources"] = ["source/example"]
        self.assertEqual([], self.errors(item))

    def test_signal_source_must_be_listed(self):
        item = context()
        item["sources"] = ["https://example.org/other"]
        self.assert_error(item, "context の sources にない")

    def test_duplicate_signal_claim(self):
        first, second = signal(1), signal(2)
        second.update(dimension=first["dimension"], source=first["source"], claim=first["claim"])
        item = context(signals=[first, second])
        self.assert_error(item, "signal が重複")

    def test_fixed_headings_and_todo(self):
        item = context()
        item["_body"] = "TODO\n"
        joined = "\n".join(self.errors(item))
        self.assertIn("固定見出し", joined)
        self.assertIn("TODO が残っている", joined)

    def test_draft_requires_signal_and_source(self):
        item = context(signals=[])
        item["sources"] = []
        joined = "\n".join(self.errors(item))
        self.assertIn("signal が1件以上", joined)
        self.assertIn("source が1件以上", joined)

    def test_verified_conditions(self):
        item = context()
        item["status"] = "verified"
        joined = "\n".join(self.errors(item))
        for fragment in ("signal が12件", "8軸以上", "source が6件", "holders が3役割"):
            self.assertIn(fragment, joined)

    def test_verified_rejects_hypothesis(self):
        dimensions = [item["id"] for item in config()["dimensions"][:8]]
        signals = [signal(i + 1, dimensions[i % 8], certainty="hypothesis" if i == 0 else "attested",
                          holders=["participants", "critics", "researchers"])
                   for i in range(12)]
        item = context(signals=signals)
        item["status"] = "verified"
        self.assert_error(item, "hypothesis signal")

    def test_verified_opposing_signals_must_be_noted(self):
        dimensions = [item["id"] for item in config()["dimensions"][:8]]
        signals = [signal(i + 1, dimensions[i % 8], direction=-1 if i == 0 else 1,
                          holders=["participants", "critics", "researchers"])
                   for i in range(12)]
        item = context(signals=signals)
        item["status"] = "verified"
        self.assert_error(item, "正負 signal ID")


class VectorTests(unittest.TestCase):
    def test_missing_dimension_is_null(self):
        vector = compute_context_vector(context(), config())
        self.assertIsNone(vector["vector"][0])
        self.assertIsNone(vector["dimensions"]["temporal_orientation"])

    def test_certainty_weight_formula(self):
        signals = [signal(1, direction=2, certainty="attested"),
                   signal(2, direction=-2, certainty="hypothesis")]
        vector = compute_context_vector(context(signals=signals), config())
        self.assertEqual(0.6, vector["dimensions"]["technology_stance"]["value"])

    def test_source_and_holder_counts_are_unique(self):
        one = signal(1, holders=["participants", "participants"])
        two = signal(2, source=one["source"], holders=["participants"])
        vector = compute_context_vector(context(signals=[one, two]), config())
        dimension = vector["dimensions"]["technology_stance"]
        self.assertEqual(1, dimension["source_count"])
        self.assertEqual(1, dimension["holder_count"])

    def test_opposite_signals_increase_polarization(self):
        flat = compute_context_vector(context(signals=[signal(1, direction=1), signal(2, direction=1)]), config())
        split = compute_context_vector(context(signals=[signal(1, direction=-1), signal(2, direction=1)]), config())
        self.assertGreater(split["dimensions"]["technology_stance"]["polarization"],
                           flat["dimensions"]["technology_stance"]["polarization"])

    def test_signal_order_does_not_change_json(self):
        signals = [signal(1), signal(2, direction=-1)]
        a = compute_context_vector(context(signals=signals), config())
        b = compute_context_vector(context(signals=list(reversed(signals))), config())
        self.assertEqual(json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False))

    def test_context_order_does_not_change_payload(self):
        a, b = context("context/a"), context("context/b")
        one = build_payloads({"context/a": a, "context/b": b}, config(), "x")
        two = build_payloads({"context/b": b, "context/a": a}, config(), "x")
        self.assertEqual(one, two)

    def test_less_than_four_axes_is_not_comparable(self):
        dims = [item["id"] for item in config()["dimensions"][:3]]
        a = context("context/a", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        b = context("context/b", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        self.assertIsNone(compare_vectors(a, b, config()))

    def test_eight_axes_have_full_coverage_factor(self):
        dims = [item["id"] for item in config()["dimensions"][:8]]
        a = context("context/a", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        b = context("context/b", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        self.assertEqual(1, compare_vectors(a, b, config())["coverage_factor"])

    def test_ties_use_dimension_index(self):
        dims = [item["id"] for item in config()["dimensions"][:4]]
        a = context("context/a", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        b = context("context/b", signals=[signal(i + 1, dim) for i, dim in enumerate(dims)])
        self.assertEqual(dims[:3], compare_vectors(a, b, config())["aligned"])

    def test_hypothesis_has_low_confidence(self):
        got = compute_context_vector(context(signals=[signal(certainty="hypothesis")]), config())
        self.assertLess(got["dimensions"]["technology_stance"]["confidence"], 0.25)

    def test_digest_is_content_based_and_ordered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config").mkdir()
            (root / "contexts").mkdir()
            config_path = root / "config" / "context-dimensions.yaml"
            config_path.write_text("version: 1\n", encoding="utf-8")
            (root / "contexts" / "b.md").write_text("b\n", encoding="utf-8")
            (root / "contexts" / "a.md").write_text("a\n", encoding="utf-8")
            before = compute_input_digest(config_path, root / "contexts")
            (root / "contexts" / "a.md").write_text("changed\n", encoding="utf-8")
            self.assertNotEqual(before, compute_input_digest(config_path, root / "contexts"))

    def test_generator_is_byte_stable_across_two_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            vectors_path = Path(directory) / "context-vectors.json"
            similarity_path = Path(directory) / "context-similarity.json"
            with mock.patch.object(build_context_vectors, "VECTORS_PATH", vectors_path), \
                    mock.patch.object(build_context_vectors, "SIMILARITY_PATH", similarity_path), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, build_context_vectors.main([]))
                before = (vectors_path.read_bytes(), similarity_path.read_bytes())
                self.assertEqual(0, build_context_vectors.main([]))
                after = (vectors_path.read_bytes(), similarity_path.read_bytes())
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
