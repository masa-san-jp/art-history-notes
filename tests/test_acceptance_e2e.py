import copy
import itertools
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from tools import bundle, build_context_vectors, compare_context, context_kb
from tools import query_spacetime
from tools.kb import (ROOT, build_edges, century_of_year, edtf_year_range, load_config,
                      load_entities, load_region_history, regions_of)


MARKER_RE = re.compile(r"^`([^`]+)` — [^\n]+$", re.MULTILINE)


class AcceptanceE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entities, cls.records = load_entities()
        cls.edges = build_edges(cls.entities)
        cls.config = load_config()
        cls.region_history = load_region_history()
        cls.coverage = json.loads((ROOT / "data" / "coverage.json").read_text(encoding="utf-8"))

    def render_bundle(self, ids):
        return bundle.render(ids, self.entities, self.edges, "E2E")

    def assert_bundle_integrity(self, ids, text):
        self.assertEqual(text, self.render_bundle(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("## 出典（このバンドル全体）", text)
        for entity_id in ids:
            meta = self.entities[entity_id]
            marker = f"`{entity_id}` — {meta['path']}"
            self.assertEqual(1, text.count(marker), entity_id)
            self.assertIn(meta.get("status"), text)
            time = meta.get("time") or {}
            span = "–".join(str(value) for value in (time.get("start"), time.get("end")) if value)
            self.assertIn(span or "年代未確認", text)
        selected = set(ids)
        for edge in self.edges:
            if edge.get("derived") or not ({edge["from"], edge["to"]} & selected):
                continue
            if edge["from"] in selected:
                self.assertIn(f"- {edge['type']} →", text)
            else:
                self.assertIn(f"— {edge['type']} →", text)
            if edge.get("source"):
                self.assertIn(edge["source"], text.split("## 出典（このバンドル全体）", 1)[1])

    def bundle_ids_from_text(self, text):
        return [match.group(1) for match in MARKER_RE.finditer(text)]

    def test_non_stub_movement_bundles_are_complete_and_deterministic(self):
        for entity_id, meta in sorted(self.entities.items()):
            if meta.get("type") != "movement" or meta.get("status") == "stub":
                continue
            text = self.render_bundle([entity_id])
            self.assert_bundle_integrity([entity_id], text)

    def test_all_region_and_used_century_bundles_match_graph_conditions(self):
        movements = {
            entity_id: meta for entity_id, meta in self.entities.items()
            if meta.get("type") == "movement"
        }
        for region in self.config["buckets"]:
            expected = sorted(
                entity_id for entity_id in movements
                if region in regions_of(entity_id, self.entities, self.region_history)
            )
            self.assertTrue(expected, region)
            text = self.render_bundle(expected)
            self.assertEqual(expected, self.bundle_ids_from_text(text), region)
            self.assert_bundle_integrity(expected, text)

        used_centuries = {
            century for row in self.coverage["grid"].values()
            for century, count in row.items() if count and century != "unknown"
        }
        for century_text in sorted(used_centuries, key=int):
            century = int(century_text)
            expected = []
            for entity_id, meta in movements.items():
                start, _ = edtf_year_range((meta.get("time") or {}).get("start"))
                if start is not None and century_of_year(start) == century:
                    expected.append(entity_id)
            expected.sort()
            self.assertTrue(expected, century_text)
            text = self.render_bundle(expected)
            self.assertEqual(expected, self.bundle_ids_from_text(text), century_text)
            self.assert_bundle_integrity(expected, text)

    def test_spacetime_fixed_fixture_and_graph_immutability(self):
        fixture = {
            "place/paris": {
                "id": "place/paris", "type": "place", "label_ja": "パリ",
                "region": "europe-west", "coordinates": [48.8566, 2.3522],
            },
            "movement/impressionism": {
                "id": "movement/impressionism", "type": "movement", "label_ja": "印象派",
                "time": {"start": "1874", "end": "1886"},
                "space": [{"role": "originated_in", "target": "place/paris"}],
            },
            "movement/unknown": {
                "id": "movement/unknown", "type": "movement", "label_ja": "不明派",
                "time": {"start": None, "end": ".."},
                "space": [{"role": "originated_in", "target": "place/paris"}],
            },
        }
        before = copy.deepcopy(fixture)
        payload = query_spacetime.query_entities(fixture, (1885, 1885))
        self.assertEqual(["movement/impressionism"], [row["id"] for row in payload["results"]])
        self.assertEqual([{"id": "movement/unknown", "reasons": ["unknown-time"]}],
                         payload["excluded"])
        self.assertEqual(before, fixture)

    def test_all_context_vectors_and_comparable_pairs_have_sources(self):
        config = build_context_vectors.load_context_config()
        contexts = context_kb.load_contexts(build_context_vectors.CONTEXTS_DIR, ROOT)
        digest = context_kb.compute_input_digest(
            build_context_vectors.CONFIG_PATH, build_context_vectors.CONTEXTS_DIR)
        graph_before = (ROOT / "data" / "graph.json").read_bytes()
        vectors_payload, similarity_payload = build_context_vectors.build_payloads(
            contexts, config, digest)
        self.assertEqual(set(contexts), set(vectors_payload["contexts"]))

        expected_pairs = []
        for first, second in itertools.combinations(sorted(contexts), 2):
            pair = context_kb.compare_vectors(contexts[first], contexts[second], config)
            if pair is not None:
                expected_pairs.append(pair)
        self.assertEqual(expected_pairs, similarity_payload["pairs"])
        for pair in similarity_payload["pairs"]:
            candidate = compare_context.candidate_object(
                pair["a"], pair, vectors_payload["contexts"], contexts)
            for axis in candidate["aligned"] + candidate["divergent"]:
                self.assertTrue(axis["sources"], (pair, axis))
        self.assertEqual(graph_before, (ROOT / "data" / "graph.json").read_bytes())

    def test_readme_cli_smoke_runs_in_isolated_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            copy_root = Path(directory) / "repo"
            shutil.copytree(
                ROOT,
                copy_root,
                ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"),
            )
            commands = [
                ["tools/build_graph.py", "--check"],
                ["tools/build_graph.py"],
                ["tools/bundle.py", "--region", "asia-east-japan"],
                ["tools/bundle.py", "--century", "19"],
                ["tools/bundle.py", "--search", "調和"],
                ["tools/query_spacetime.py", "--at", "1885", "--format", "json"],
                ["tools/build_context_vectors.py", "--check"],
                ["tools/build_context_vectors.py"],
                ["tools/compare_context.py", "context/ai-art-japan-2026-h2",
                 "--kind", "historical", "--top", "3"],
                ["tools/audit.py"],
                ["tools/new_entity.py", "movement", "e2e-smoke", "--ja", "E2E smoke"],
            ]
            for command in commands:
                with self.subTest(command=command):
                    result = subprocess.run(
                        [sys.executable, *command],
                        cwd=copy_root,
                        capture_output=True,
                        text=True,
                        timeout=90,
                    )
                    self.assertEqual(0, result.returncode, result.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
