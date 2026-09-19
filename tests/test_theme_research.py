import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from tools import theme_research


def fixture_entities():
    return {
        "movement/mughal-painting": {
            "id": "movement/mughal-painting",
            "type": "movement",
            "label_ja": "ムガル絵画",
            "label_en": "Mughal painting",
            "status": "verified",
            "sources": [{"url": "https://example.org/a"}, {"url": "https://example.org/b"}],
        },
        "movement/kowhaiwhai": {
            "id": "movement/kowhaiwhai",
            "type": "movement",
            "label_ja": "コーワイワイ",
            "label_en": "Kōwhaiwhai",
            "status": "verified",
            "sources": [{"url": "https://example.org/c"}],
        },
    }


GRID = {"asia-south": {"18": 1}}


def budget_file(root, **overrides):
    data = {
        "contract_version": "theme-research-budget/v1",
        "per_run": {"max_passes": 1, "max_theme_terms": 4, "max_candidates": 2,
                    "max_source_fetches": 8, "wall_clock_seconds": 900},
        "on_exhausted": "stop",
    }
    data["per_run"].update(overrides)
    path = Path(root) / "theme-research.yaml"
    import yaml
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    return path


class ThemeResearchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.budget = budget_file(self.temp.name)
        self.logged = []

    def run_main(self, argv, entities, search):
        with mock.patch.object(theme_research, "load_entities", return_value=(entities, [])), \
             mock.patch.object(theme_research, "search_entities", side_effect=search), \
             mock.patch.object(theme_research, "log_query",
                                side_effect=lambda term, hits: self.logged.append((term, hits))), \
             mock.patch.object(theme_research, "load_grid", return_value=GRID), \
             mock.patch("sys.argv", ["theme_research.py", "--budget", str(self.budget), *argv]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = theme_research.main()
        return code, out.getvalue()

    def test_hit_summary_reports_status_and_source_count(self):
        summary = theme_research.hit_summary("movement/mughal-painting", fixture_entities())
        self.assertEqual(summary["status"], "verified")
        self.assertEqual(summary["n_sources"], 2)

    def test_hit_summary_missing_entity_is_safe(self):
        summary = theme_research.hit_summary("movement/does-not-exist", {})
        self.assertIsNone(summary["label_ja"])
        self.assertEqual(summary["n_sources"], 0)

    def test_exact_label_hits_separates_subject_from_passing_mentions(self):
        entities = fixture_entities()
        hits = [theme_research.hit_summary(i, entities) for i in entities]
        self.assertEqual(theme_research.exact_label_hits("ムガル絵画", hits), ["movement/mughal-painting"])
        self.assertEqual(theme_research.exact_label_hits("mughal painting", hits), ["movement/mughal-painting"])
        self.assertEqual(theme_research.exact_label_hits("絵画", hits), [])

    def test_recon_contract_single_theme(self):
        entities = fixture_entities()
        code, out = self.run_main(["--theme", "ムガル絵画", "--json"], entities,
                                  lambda term, ents: ["movement/mughal-painting", "movement/kowhaiwhai"])
        self.assertEqual(code, 0)
        report = json.loads(out)
        self.assertEqual(report["contract_version"], "theme-research-recon/v1")
        self.assertEqual(report["themes"], ["ムガル絵画"])
        self.assertEqual(report["results"][0]["hit_count"], 2)
        self.assertEqual(report["results"][0]["exact_label_hits"], ["movement/mughal-painting"])
        # 後方互換field
        self.assertEqual(report["theme"], "ムガル絵画")
        self.assertEqual(report["hit_count"], 2)
        self.assertEqual(report["coverage_grid"], GRID)
        self.assertEqual(report["budget"]["per_run"]["max_candidates"], 2)
        self.assertEqual(self.logged, [("ムガル絵画", 2)])

    def test_multiple_themes_each_logged_and_truncated_by_budget(self):
        self.budget = budget_file(self.temp.name, max_theme_terms=2)
        code, out = self.run_main(["--theme", "a", "--theme", "b", "--theme", "c", "--json"], {},
                                  lambda term, ents: [])
        self.assertEqual(code, 0)
        report = json.loads(out)
        self.assertEqual(report["themes"], ["a", "b"])
        self.assertEqual(report["truncated_themes"], ["c"])
        self.assertEqual(self.logged, [("a", 0), ("b", 0)])

    def test_miss_is_recorded_and_not_an_error(self):
        code, out = self.run_main(["--theme", "存在しないテーマ"], {}, lambda term, ents: [])
        self.assertEqual(code, 0)
        self.assertEqual(self.logged, [("存在しないテーマ", 0)])
        self.assertIn("該当なし", out)

    def test_budget_rejects_missing_or_non_finite_values(self):
        bad = budget_file(self.temp.name, max_candidates=0)
        with self.assertRaises(ValueError):
            theme_research.load_budget(bad)
        import yaml
        path = Path(self.temp.name) / "no-stop.yaml"
        data = yaml.safe_load(self.budget.read_text(encoding="utf-8"))
        data["on_exhausted"] = "continue"
        path.write_text(yaml.safe_dump(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            theme_research.load_budget(path)

    def test_repository_budget_file_is_valid(self):
        budget = theme_research.load_budget(theme_research.BUDGET_PATH)
        self.assertEqual(budget["per_run"]["max_passes"], 1)

    # --- spec §5 R3: candidate template -------------------------------------

    def template(self, term="ムガル絵画", recon=None):
        from datetime import datetime, timezone
        recon = recon if recon is not None else {"exact_label_hits": ["movement/mughal-painting"]}
        return theme_research.candidate_template(
            term, recon, creator="creator-a", collection="history-a", project_id="project/p1",
            origin_instance_id="instance-a", run_id="run-001", code_commit="0" * 40,
            now=datetime(2026, 9, 17, tzinfo=timezone.utc))

    def test_template_uses_intake_envelope_and_never_guesses_sources(self):
        from tools.research_knowledge_intake import FIELDS, OWNER, POLICY, canonical, digest, key
        out = self.template()
        record, payload = out["candidate"]["record"], out["candidate"]["payload"]
        self.assertEqual(set(record), FIELDS)
        self.assertEqual(record["owner_repository"], OWNER)
        self.assertEqual(record["payload_schema"], POLICY)
        self.assertEqual(record["payload_ref"], "contexts/research-memory/payloads/" + key(record) + ".json")
        self.assertEqual(record["content_sha256"], digest(canonical(payload)))
        self.assertEqual(payload["target_id"], "movement/mughal-painting")
        self.assertEqual(out["existing_target"], "movement/mughal-painting")
        self.assertEqual(payload["statement"], "")
        self.assertEqual(payload["source_reads"], [])
        self.assertIsNone(payload["entity"])
        self.assertTrue(any("statement" in m for m in out["missing"]))

    def test_template_without_existing_target_proposes_safe_new_id_and_flags_dedupe(self):
        out = self.template(term="パタゴニア先住民美術", recon={"exact_label_hits": []})
        target = out["candidate"]["payload"]["target_id"]
        self.assertTrue(target.startswith("movement/theme-"), target)
        self.assertIsNone(out["existing_target"])
        self.assertTrue(any("dedupe" in m for m in out["missing"]))

    def filled_candidate(self):
        from tools.research_knowledge_intake import canonical, digest
        candidate = self.template()["candidate"]
        snapshot = Path(self.temp.name) / "source.txt"
        raw = b"Synthetic catalogue passage. Not an actual historical source."
        snapshot.write_bytes(raw)
        candidate["payload"]["statement"] = "Synthetic observation for the contract test."
        candidate["payload"]["source_reads"] = [{
            "url": "https://example.org/synthetic", "content_sha256": digest(raw),
            "locator": "p.1", "start": 0, "end": 9, "slice_sha256": digest(raw[0:9]),
        }]
        candidate["record"]["consent_ref"] = "consent/synthetic"
        candidate["record"]["content_sha256"] = digest(canonical(candidate["payload"]))
        return candidate, {"https://example.org/synthetic": str(snapshot)}

    def test_validate_candidate_file_reports_ok_and_errors(self):
        candidate, snapshots = self.filled_candidate()
        cpath = Path(self.temp.name) / "candidate.json"; spath = Path(self.temp.name) / "snapshots.json"
        cpath.write_text(json.dumps(candidate, ensure_ascii=False), encoding="utf-8")
        spath.write_text(json.dumps(snapshots), encoding="utf-8")
        ok = theme_research.validate_candidate_file(cpath, spath)
        self.assertTrue(ok["ok"], ok)
        self.assertEqual(ok["target_id"], "movement/mughal-painting")
        # 未読の出典（snapshot 無し）は拒否される
        bad = theme_research.validate_candidate_file(cpath, None)
        self.assertFalse(bad["ok"])
        self.assertTrue(bad["errors"])

    def test_validate_candidate_cli_exit_code(self):
        candidate, snapshots = self.filled_candidate()
        cpath = Path(self.temp.name) / "candidate.json"; spath = Path(self.temp.name) / "snapshots.json"
        cpath.write_text(json.dumps(candidate, ensure_ascii=False), encoding="utf-8")
        spath.write_text(json.dumps(snapshots), encoding="utf-8")
        with mock.patch("sys.argv", ["theme_research.py", "--validate-candidate", str(cpath),
                                     "--source-snapshots", str(spath)]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(theme_research.main(), 0)
        self.assertTrue(json.loads(out.getvalue())["ok"])
        with mock.patch("sys.argv", ["theme_research.py", "--validate-candidate", str(cpath)]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(theme_research.main(), 1)

    def test_filled_template_is_accepted_by_intake_validator(self):
        """穴を埋めれば既存 intake の validate_candidate をそのまま通る（骨格が契約と一致している証拠）。"""
        from tools.research_knowledge_intake import canonical, digest, validate_candidate
        out = self.template()
        candidate = out["candidate"]
        snapshot = Path(self.temp.name) / "source.txt"
        raw = b"Synthetic catalogue passage. Not an actual historical source."
        snapshot.write_bytes(raw)
        candidate["payload"]["statement"] = "Synthetic observation for the contract test."
        candidate["payload"]["source_reads"] = [{
            "url": "https://example.org/synthetic", "content_sha256": digest(raw),
            "locator": "p.1", "start": 0, "end": 9, "slice_sha256": digest(raw[0:9]),
        }]
        candidate["record"]["consent_ref"] = "consent/synthetic"
        candidate["record"]["content_sha256"] = digest(canonical(candidate["payload"]))
        validate_candidate(candidate, creator="creator-a", collection="history-a",
                           snapshots={"https://example.org/synthetic": str(snapshot)})


if __name__ == "__main__":
    unittest.main()
