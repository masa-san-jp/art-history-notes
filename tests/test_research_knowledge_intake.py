import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from tools.research_knowledge_intake import (KnowledgeStore, IntakeError, OWNER, POLICY,
    canonical, digest, key, validate_candidate, ROOT)

NOW = datetime(2026, 9, 5, tzinfo=timezone.utc)


class ResearchIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store_root = self.root / "memory"; self.store_root.mkdir()
        self.code = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        gitdir = self.store_root / "objects.git"
        subprocess.run(["git", "init", "--bare", "-q", str(gitdir)], check=True)
        (self.store_root / "store.json").write_text(json.dumps({"owner": OWNER, "creator": "creator-a", "collection": "history-a"}))
        # Seed the same empty Git owner binding used by AAK-04, without remote effects.
        tree = subprocess.check_output(["git", "--git-dir", str(gitdir), "mktree"], input=b"").decode().strip()
        commit = subprocess.check_output(["git", "--git-dir", str(gitdir), "-c", "user.name=Synthetic", "-c", "user.email=synthetic@example.invalid", "commit-tree", tree], input=b"synthetic setup").decode().strip()
        subprocess.run(["git", "--git-dir", str(gitdir), "update-ref", "refs/heads/knowledge", commit], check=True)
        self.store = KnowledgeStore(self.store_root, "creator-a", "history-a", self.code)
        self.snapshot = self.root / "source.txt"; self.snapshot.write_bytes(b"Synthetic catalogue passage. Not an actual historical source.")
        self.snapshots = {"https://example.org/synthetic": str(self.snapshot)}

    def candidate(self, record_id="observation", revision=1):
        raw = self.snapshot.read_bytes()
        entity = {"id": "concept/synthetic-study", "uri": "urn:ahn:concept/synthetic-study", "type": "concept",
            "label_ja": "合成研究概念", "label_en": "Synthetic study", "authority": {"none_reason": "synthetic fixture"},
            "sources": [{"url": "https://example.org/synthetic", "kind": "institutional", "note": "synthetic fixture"}],
            "status": "draft", "updated": "2026-09-05", "relations": [], "time": {"start": "1900", "end": "1901"}}
        payload = {"classification": "historical", "target_id": entity["id"], "project_id": "synthetic-project",
            "context_body": None,
            "statement": "Synthetic research decision grounded in a read fixture.", "entity": entity,
            "source_reads": [{"url": "https://example.org/synthetic", "content_sha256": digest(raw), "locator": "paragraph-1",
                "start": 0, "end": len(raw), "slice_sha256": digest(raw)}]}
        record = {"contract_version": "artifact-record/v1", "record_id": record_id, "revision": revision,
            "origin_instance_id": "instance-a", "creator_id": "creator-a", "owner_repository": OWNER,
            "collection_id": "history-a", "kind": "art-history-knowledge", "payload_schema": POLICY,
            "payload_ref": "", "content_sha256": digest(canonical(payload)), "sources": [], "derived_from": [],
            "epistemic_status": "externally-supported", "lifecycle": "accepted", "applicability": {"medium": "unknown"},
            "rights": {"knowledge_write": True, "redistribute": False}, "access_scope": "creator-private", "consent_ref": "synthetic-consent",
            "created_at": "2026-09-05T00:00:00Z", "reviewed_at": None, "valid_until": None,
            "producer": {"kind": "agent", "generator_version": POLICY, "code_commit": self.code, "run_id": "synthetic"}, "supersedes": [], "invalidates": []}
        record["payload_ref"] = "contexts/research-memory/payloads/" + key(record) + ".json"
        return {"record": record, "payload": payload}

    def commit(self, candidate, operation="one"):
        return self.store.commit(candidate, self.store.head(), operation, "synthetic-run", self.snapshots)

    def rehash(self, candidate):
        candidate["record"]["content_sha256"] = digest(canonical(candidate["payload"]))

    def test_aak_06_ac1_replay_and_competing_interpretations_preserved(self):
        candidate = self.candidate(); parent = self.store.head()
        receipt = self.commit(candidate)
        replay = self.store.commit(candidate, parent, "one", "synthetic-run", self.snapshots)
        self.assertEqual(receipt["target_commit"], replay["target_commit"])
        self.assertEqual("ALREADY_APPLIED", replay["status"])
        conflict = self.candidate("competing")
        conflict["payload"]["entity"]["time"]["start"] = "1800"
        conflict["payload"]["statement"] = "A competing dated interpretation remains separately attributable."
        self.rehash(conflict); self.commit(conflict, "two")
        paths = self.store.git("ls-tree", "-r", "--name-only", self.store.head(), "entities/").decode().splitlines()
        self.assertEqual(["entities/concepts/synthetic-study.md"], paths)
        self.assertEqual("1900", self.store.entities(self.store.head())["concept/synthetic-study"]["time"]["start"])
        self.assertEqual(2, len(self.store.records(self.store.head())))
        saved = json.loads(self.store.read(self.store.head(), conflict["record"]["payload_ref"]))
        self.assertEqual("1800", saved["entity"]["time"]["start"])

    def test_aak_06_ac2_unread_and_falsified_sources_and_verified_rejected(self):
        candidate = self.candidate(); parent = self.store.head()
        with self.assertRaises(IntakeError): self.store.commit(candidate, parent, "one", "run", {})
        candidate["payload"]["source_reads"][0]["slice_sha256"] = "0" * 64; self.rehash(candidate)
        with self.assertRaises(IntakeError): self.commit(candidate)
        candidate = self.candidate(); candidate["payload"]["entity"]["status"] = "verified"; self.rehash(candidate)
        with self.assertRaises(IntakeError): self.commit(candidate)
        candidate = self.candidate(); candidate["payload"]["classification"] = "creator-interpretation"; self.rehash(candidate)
        with self.assertRaises(IntakeError): self.commit(candidate)
        self.assertEqual(parent, self.store.head())

    def test_aak_06_ac3_git_reopen_index_rebuild_and_canonical_export_cli(self):
        receipt = self.commit(self.candidate())
        self.store = KnowledgeStore(self.store_root, "creator-a", "history-a", self.code)
        index = self.store.index(receipt["target_commit"])
        (self.store_root / "research-index.json").unlink()
        self.assertEqual(index, self.store.index(receipt["target_commit"]))
        command = [sys.executable, "tools/export_signals.py", "--purpose", "artistic-research", "--knowledge-store-root", str(self.store_root),
            "--creator", "creator-a", "--collection", "history-a", "--code-commit", self.code, "--knowledge-commit", receipt["target_commit"],
            "--query", "Synthetic", "--at", NOW.isoformat()]
        r = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(0, r.returncode, r.stderr)
        result = json.loads(r.stdout)
        self.assertEqual("observation", result["records"][0]["record_id"])
        self.assertEqual("concept/synthetic-study", result["records"][0]["target_id"])
        self.assertEqual(receipt["target_commit"], result["knowledge_commit"])

    def test_aak_06_ac4_origin_and_existing_body_survive_update(self):
        first = self.commit(self.candidate())
        path = "entities/concepts/synthetic-study.md"
        body = self.store.read(first["target_commit"], path).decode().split("---\n", 2)[2]
        self.commit(self.candidate("second"), "two")
        self.assertEqual(body, self.store.read(self.store.head(), path).decode().split("---\n", 2)[2])
        refs = self.store.retrieve(self.store.head(), "", "creator-private", NOW)["records"]
        self.assertTrue(all(r["origin_instance_id"] == "instance-a" and r["creator_id"] == "creator-a" for r in refs))
        with self.assertRaises(IntakeError): KnowledgeStore(self.store_root, "creator-b", "history-a", self.code)
        self.assertEqual(b"", self.store.git("remote"))

    def test_stale_parent_revision_conflict_and_path_escape_fail_closed(self):
        candidate = self.candidate(); old = self.store.head(); self.commit(candidate)
        changed = self.candidate(); changed["payload"]["statement"] = "different"; self.rehash(changed)
        with self.assertRaises(IntakeError): self.commit(changed, "two")
        with self.assertRaises(IntakeError): self.store.commit(self.candidate("second"), old, "two", "run", self.snapshots)
        escaped = self.candidate("escape"); escaped["record"]["payload_ref"] = "../raw.json"
        with self.assertRaises(IntakeError): self.commit(escaped, "escape")

    def test_creator_interpretation_is_separate_and_revocation_preserves_old_snapshot(self):
        candidate = self.candidate(); candidate["payload"].update(classification="creator-interpretation", entity=None, source_reads=[])
        candidate["record"]["epistemic_status"] = "proposed"; self.rehash(candidate)
        first = self.commit(candidate)
        self.assertEqual(b"", self.store.git("ls-tree", "-r", "--name-only", first["target_commit"], "entities/"))
        withdrawn = copy.deepcopy(candidate); withdrawn["record"]["revision"] = 2; withdrawn["record"]["lifecycle"] = "revoked"
        withdrawn["record"]["payload_ref"] = "contexts/research-memory/payloads/" + key(withdrawn["record"]) + ".json"
        second = self.commit(withdrawn, "withdraw")
        self.assertEqual([], self.store.retrieve(second["target_commit"], "", "creator-private", NOW)["records"])
        self.assertEqual(1, len(self.store.retrieve(first["target_commit"], "", "creator-private", NOW)["records"]))

    def test_context_intake_uses_existing_validator_and_vector_builder(self):
        self.commit(self.candidate())
        before, _ = self.store.context_payloads(self.store.head())
        candidate = self.candidate("context-observation")
        source = candidate["payload"]["entity"]["sources"]
        candidate["payload"]["entity"] = {"id": "context/synthetic-context", "label_ja": "合成時代文脈",
            "kind": "current", "scope": {"start": "2026", "end": "2026", "regions": ["europe-west"], "domain": "art", "topics": ["synthetic"]},
            "about": ["concept/synthetic-study"], "sources": source, "status": "draft", "updated": "2026-09-05",
            "signals": [{"id": "s001", "dimension": "temporal_orientation", "direction": 1, "salience": 1,
                "holders": ["researchers"], "claim": "Synthetic scoped observation", "certainty": "hypothesis",
                "source": source[0]["url"], "note": "Synthetic evidence, no historical assertion"}]}
        candidate["payload"].update(target_id="context/synthetic-context", context_body="\n## 範囲\n合成条件のみ\n## 根拠の読み方\n合成snapshot\n## 反対証拠・内部差\n未観測\n## 未確認\n実世界は未検証\n")
        self.rehash(candidate); receipt = self.commit(candidate, "context")
        self.store.index(receipt["target_commit"])
        after = json.loads((self.store_root / "research-index.json").read_text())["context_vectors"]
        self.assertIn("context/synthetic-context", after["contexts"])
        for context, vector in before["contexts"].items(): self.assertEqual(vector, after["contexts"][context])

    def test_prepare_checks_canonical_domain_without_writing_knowledge(self):
        parent = self.store.head()
        candidate = self.candidate()
        result = self.store.commit(candidate, parent, "validate", "validation", self.snapshots, dry_run=True)
        self.assertEqual("VALID", result["status"])
        self.assertEqual(parent, self.store.head())
        self.assertEqual([], self.store.records(parent))
        candidate["payload"]["entity"]["type"] = "invalid-owner-type"
        self.rehash(candidate)
        with self.assertRaises(IntakeError):
            self.store.commit(candidate, parent, "validate", "validation", self.snapshots, dry_run=True)
        self.assertEqual(parent, self.store.head())

    def test_index_failure_keeps_commit_and_can_resume_without_raw(self):
        receipt = self.commit(self.candidate())
        victim = self.root / "unchanged.txt"; victim.write_text("unchanged")
        index = self.store_root / "research-index.json"; index.symlink_to(victim)
        self.snapshot.unlink()
        command = [sys.executable, str(ROOT / "tools/research_knowledge_intake.py"), "index",
            "--store-root", str(self.store_root), "--creator", "creator-a", "--collection", "history-a",
            "--code-commit", self.code, "--knowledge-commit", receipt["target_commit"]]
        failed = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(1, failed.returncode)
        self.assertEqual("INDEX_PENDING", json.loads(failed.stdout)["status"])
        self.assertEqual(receipt["target_commit"], self.store.head())
        self.assertEqual("unchanged", victim.read_text())
        index.unlink()
        resumed = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(0, resumed.returncode, resumed.stderr)
        self.assertEqual(receipt["target_commit"], json.loads(resumed.stdout)["index_commit"])

    def test_completed_operation_replay_does_not_need_raw_snapshot_retention(self):
        candidate = self.candidate(); parent = self.store.head(); first = self.commit(candidate)
        self.snapshot.unlink()
        replay = self.store.commit(candidate, parent, "one", "synthetic-run", {})
        self.assertEqual(first["target_commit"], replay["target_commit"])

    def test_canonical_overlay_and_dependents_are_removed_from_active_index_on_revocation(self):
        first_candidate = self.candidate(); first = self.commit(first_candidate)
        derived = self.candidate("dependent")
        derived["payload"].update(entity=None, classification="creator-interpretation", source_reads=[])
        derived["record"]["epistemic_status"] = "inferred"
        ref = {k: first_candidate["record"][k] for k in ("origin_instance_id", "owner_repository", "record_id", "revision")}
        derived["record"]["derived_from"] = [ref]; self.rehash(derived); self.commit(derived, "derived")
        revoked = self.candidate("revocation")
        revoked["payload"].update(entity=None, classification="creator-interpretation", source_reads=[])
        revoked["record"].update(epistemic_status="proposed", lifecycle="revoked", invalidates=[ref])
        self.rehash(revoked); last = self.commit(revoked, "revoke")
        self.assertEqual([], self.store.retrieve(last["target_commit"], "", "creator-private", NOW)["records"])
        self.assertNotIn("concept/synthetic-study", self.store.entities(last["target_commit"]))
        self.assertIn("concept/synthetic-study", self.store.entities(first["target_commit"]))


if __name__ == "__main__": unittest.main()
