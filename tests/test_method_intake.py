"""Method candidate -> real owner Git intake; synthetic snapshots, no network."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import research_knowledge_intake as intake
from tools.agent_support import resolve_code_commit
from tools.theme_research import candidate_template


class MethodIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # The production clean-code guard stays active even when the main worktree is dirty.
        code = self.root / "code"
        code.mkdir()
        subprocess.run(["git", "init", "-q", str(code)], check=True)
        subprocess.run(["git", "-C", str(code), "-c", "user.name=Fixture", "-c",
                        "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "Fixture"], check=True)
        self.code = resolve_code_commit(code)
        self.addCleanup(patch.stopall)
        patch.object(intake, "ROOT", code).start()
        # Explicit root: the resolver's default argument otherwise binds the source checkout.
        patch.object(intake, "resolve_code_commit", side_effect=lambda root: resolve_code_commit(root)).start()
        store = self.root / "owner"
        store.mkdir()
        (store / "store.json").write_text(json.dumps({"owner": intake.OWNER,
                                                      "creator": "fixture", "collection": "methods"}))
        gitdir = store / "objects.git"
        subprocess.run(["git", "init", "--bare", "-q", str(gitdir)], check=True)
        tree = subprocess.check_output(["git", "--git-dir", str(gitdir), "mktree"], input=b"").decode().strip()
        head = subprocess.check_output(["git", "--git-dir", str(gitdir), "-c", "user.name=Fixture", "-c",
                                        "user.email=fixture@example.invalid", "commit-tree", tree], input=b"Fixture").decode().strip()
        subprocess.run(["git", "--git-dir", str(gitdir), "update-ref", "refs/heads/knowledge", head], check=True)
        self.store = intake.KnowledgeStore(store, "fixture", "methods", self.code)
        self.raw = b"Synthetic method catalogue fixture; not a historical claim."
        snapshot = self.root / "snapshot.txt"
        snapshot.write_bytes(self.raw)
        self.url = "https://example.org/synthetic-method"
        self.snapshots = {self.url: str(snapshot)}
        self.method = {"fixes": ["synthetic operation"], "varies": ["synthetic input"],
                       "requires": ["synthetic material"], "origin_domain": "computation"}

    def candidate(self):
        result = candidate_template("Synthetic Iterated Method", {"exact_label_hits": [], "hits": []},
                                    creator="fixture", collection="methods", project_id="test",
                                    origin_instance_id="fixture", run_id="test", code_commit=self.code,
                                    entity_kind="method", method=copy.deepcopy(self.method))
        candidate = result["candidate"]
        payload, record = candidate["payload"], candidate["record"]
        payload["statement"] = "A synthetic operation read from a fixture, not a historical assertion."
        payload["entity"] = {"id": payload["target_id"], "uri": "urn:ahn:" + payload["target_id"],
            "type": "concept", "label_ja": "合成手法", "label_en": "Synthetic Iterated Method",
            "authority": {"none_reason": "synthetic fixture"}, "time": {"start": None, "end": None},
            "space": [], "relations": [], "method": copy.deepcopy(self.method),
            "sources": [{"url": self.url, "kind": "institutional"}], "status": "draft", "updated": "2026-10-03"}
        payload["source_reads"] = [{"url": self.url, "content_sha256": intake.digest(self.raw),
            "locator": "fixture", "start": 0, "end": len(self.raw), "slice_sha256": intake.digest(self.raw)}]
        record.update(lifecycle="accepted", consent_ref="synthetic-test-consent")
        self.rehash(candidate)
        return candidate

    def rehash(self, candidate):
        candidate["record"]["content_sha256"] = intake.digest(intake.canonical(candidate["payload"]))

    def test_candidate_template_to_intake_to_concept(self):
        candidate = self.candidate()
        receipt = self.store.commit(candidate, self.store.head(), "method-test", "test", self.snapshots)
        self.assertEqual(receipt["status"], "COMMITTED")
        target = candidate["payload"]["target_id"]
        self.assertEqual(self.store.entities(receipt["target_commit"])[target]["method"], self.method)
        saved = self.store.records(receipt["target_commit"])[0]
        self.assertEqual(saved["applicability"]["method_classification"],
                         candidate["record"]["applicability"]["method_classification"])
        paths = self.store.git("ls-tree", "-r", "--name-only", receipt["target_commit"]).decode()
        self.assertIn("entities/concepts/synthetic-iterated-method.md", paths)
        self.assertNotIn("snapshot", paths)

    def test_method_empty_and_type_mismatch_rejected_before_writes(self):
        for mutation in ("empty-payload", "empty-entity", "wrong-type", "no-method", "no-declaration"):
            candidate = self.candidate()
            if mutation == "empty-payload": candidate["payload"]["method"] = {}
            if mutation == "empty-entity": candidate["payload"]["entity"]["method"] = {}
            if mutation == "wrong-type": candidate["payload"]["entity"]["type"] = "movement"
            if mutation == "no-method": candidate["payload"]["entity"].pop("method")
            if mutation == "no-declaration": candidate["payload"].pop("entity_kind")
            self.rehash(candidate)
            parent = self.store.head()
            with self.subTest(mutation=mutation), self.assertRaises(intake.IntakeError):
                self.store.commit(candidate, parent, mutation, "test", self.snapshots)
            self.assertEqual(parent, self.store.head())

    def test_decision_closed_vocabulary_and_provenance_required(self):
        for field, value in (("reason", "unverified-guess"), ("rule_version", "method-concepts/v0"),
                             ("entity_type", "movement"), ("is_method", "true"), ("extra", "unknown")):
            candidate = self.candidate()
            candidate["record"]["applicability"]["method_classification"][field] = value
            with self.subTest(field=field), self.assertRaises(intake.IntakeError):
                intake.validate_candidate(candidate, creator="fixture", collection="methods", snapshots=self.snapshots)
        candidate = self.candidate()
        candidate["record"]["applicability"].pop("method_classification")
        with self.assertRaises(intake.IntakeError):
            intake.validate_candidate(candidate, creator="fixture", collection="methods", snapshots=self.snapshots)

    def test_unmarked_new_concept_is_not_a_legacy_escape(self):
        candidate = self.candidate()
        candidate["payload"].pop("entity_kind")
        candidate["payload"].pop("method")
        candidate["payload"]["entity"].pop("method")
        candidate["record"]["applicability"].pop("method_classification")
        self.rehash(candidate)
        with self.assertRaises(intake.IntakeError):
            intake.validate_candidate(candidate, creator="fixture", collection="methods", snapshots=self.snapshots)
