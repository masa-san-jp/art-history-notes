#!/usr/bin/env python3
"""Owner-local research intake; immutable Git receipts and conservative evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime

import yaml

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from kb import (ROOT, DIR_FOR_TYPE, URI_PREFIX, load_config, load_entities, source_validation_errors,
                read_frontmatter, normalized_meta, build_edges)
from build_graph import validate as validate_entities
from agent_support import SECRET_PATTERNS

OWNER = "art-history-notes"
POLICY = "art-history-research-intake/v1"
FIELDS = set("contract_version record_id revision origin_instance_id creator_id owner_repository collection_id kind payload_schema payload_ref content_sha256 sources derived_from epistemic_status lifecycle applicability rights access_scope consent_ref created_at reviewed_at valid_until producer supersedes invalidates".split())


class IntakeError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def key(record):
    return digest(canonical([record[k] for k in ("origin_instance_id", "owner_repository", "record_id", "revision")]))


def validate_candidate(candidate, *, creator, collection, snapshots=None):
    """Read source snapshots without storing raw text or claiming unobserved reads."""
    if not isinstance(candidate, dict) or set(candidate) != {"record", "payload"}:
        raise IntakeError("candidate must contain record and payload only")
    record, payload = candidate["record"], candidate["payload"]
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise IntakeError("closed artifact-record/v1 envelope required")
    if record["contract_version"] != "artifact-record/v1" or record["payload_schema"] != POLICY:
        raise IntakeError("unknown contract/schema version")
    if record["kind"] != "art-history-knowledge" or not isinstance(record["applicability"], dict):
        raise IntakeError("owner kind and applicability required")
    producer = record["producer"]
    if not isinstance(producer, dict) or set(producer) != {"kind", "generator_version", "code_commit", "run_id"}:
        raise IntakeError("explicit producer kind/version/code/run required")
    if producer["kind"] not in {"agent", "human", "tool"} or not producer["generator_version"] or not producer["run_id"] or not re.fullmatch(r"[0-9a-f]{40}", str(producer["code_commit"])):
        raise IntakeError("invalid producer provenance")
    if record["owner_repository"] != OWNER or record["creator_id"] != creator or record["collection_id"] != collection:
        raise IntakeError("owner/creator/collection mismatch")
    if not isinstance(record["revision"], int) or isinstance(record["revision"], bool) or record["revision"] < 1:
        raise IntakeError("revision must be positive")
    for name in ("record_id", "origin_instance_id", "creator_id", "collection_id"):
        if not isinstance(record[name], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", record[name]):
            raise IntakeError("invalid record identity")
    for name in ("sources", "derived_from", "supersedes", "invalidates"):
        if not isinstance(record[name], list) or any(not isinstance(x, dict) for x in record[name]):
            raise IntakeError("references must be object arrays")
    for reference in record["derived_from"] + record["supersedes"] + record["invalidates"]:
        if not all(k in reference for k in ("origin_instance_id", "owner_repository", "record_id", "revision")):
            raise IntakeError("record reference must carry complete origin identity")
        if key(reference) == key(record): raise IntakeError("self-referential provenance forbidden")
    for name in ("created_at", "reviewed_at", "valid_until"):
        value = record[name]
        if value is None and name != "created_at":
            continue
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None: raise ValueError()
        except (AttributeError, TypeError, ValueError) as exc:
            raise IntakeError("timestamp must be explicit and timezone-aware") from exc
    if record["epistemic_status"] not in {"observed", "externally-supported", "inferred", "proposed", "simulated", "unknown"}:
        raise IntakeError("invalid epistemic status")
    if record["lifecycle"] not in {"candidate", "accepted", "rejected", "superseded", "revoked"}:
        raise IntakeError("invalid lifecycle")
    if record["access_scope"] not in {"public", "creator-private"} or record["rights"] != {"knowledge_write": True, "redistribute": record["access_scope"] == "public"}:
        raise IntakeError("explicit knowledge write and redistribution rights required")
    if record["access_scope"] == "creator-private" and (not isinstance(record["consent_ref"], str) or not record["consent_ref"]):
        raise IntakeError("private creator knowledge requires explicit consent reference")
    if not isinstance(payload, dict) or set(payload) != {"classification", "target_id", "project_id", "statement", "entity", "source_reads", "context_body"}:
        raise IntakeError("closed owner payload required")
    if payload["classification"] not in {"historical", "creator-interpretation"}:
        raise IntakeError("unknown knowledge classification")
    for name in ("target_id", "project_id", "statement"):
        if not isinstance(payload[name], str) or not payload[name].strip():
            raise IntakeError("target, project and substantive statement required")
    if payload["classification"] == "creator-interpretation" and (payload["entity"] is not None or record["epistemic_status"] not in {"inferred", "proposed", "simulated", "unknown"}):
        raise IntakeError("creator interpretation cannot become canonical historical fact")
    if record["content_sha256"] != digest(canonical(payload)):
        raise IntakeError("payload hash mismatch")
    expected_path = "contexts/research-memory/payloads/" + key(record) + ".json"
    if record["payload_ref"] != expected_path:
        raise IntakeError("payload ref must be the owner-derived safe path")
    if any(pattern.search(canonical(candidate)) for pattern in SECRET_PATTERNS):
        raise IntakeError("secret-like content rejected")
    reads = payload["source_reads"]
    if not isinstance(reads, list): raise IntakeError("source reads must be an array")
    verified_urls = set()
    for proof in reads:
        if not isinstance(proof, dict) or set(proof) != {"url", "content_sha256", "locator", "start", "end", "slice_sha256"}:
            raise IntakeError("closed source-read proof required")
        source_path = (snapshots or {}).get(proof["url"])
        if not source_path:
            raise IntakeError("source marked read without an available snapshot")
        raw = Path(source_path).read_bytes()
        start, end = proof["start"], proof["end"]
        if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(raw):
            raise IntakeError("source passage range invalid")
        if not proof["locator"] or digest(raw) != proof["content_sha256"] or digest(raw[start:end]) != proof["slice_sha256"]:
            raise IntakeError("source snapshot/passage hash mismatch")
        verified_urls.add(proof["url"])
    entity = payload["entity"]
    if payload["context_body"] is not None and not isinstance(payload["context_body"], str):
        raise IntakeError("context body must be explicit text or null")
    if entity is not None:
        if not isinstance(entity, dict) or entity.get("id") != payload["target_id"]:
            raise IntakeError("canonical target mismatch")
        if entity.get("status") == "verified":
            raise IntakeError("research intake cannot assign verified; owner review required")
        allowed = set("id uri type label_ja label_en authority time space relations sources status updated kind naming claims evidence aliases former_names founding_control control_changes images region role place_type about scope signals".split())
        if set(entity) - allowed: raise IntakeError("unrecognized canonical payload fields")
        if not verified_urls or any(s.get("url") not in verified_urls for s in entity.get("sources", [])):
            raise IntakeError("canonical candidate requires read source snapshots")
        if record["epistemic_status"] not in {"externally-supported", "observed"}:
            raise IntakeError("canonical candidate requires external evidence")
        errors = source_validation_errors(entity.get("sources"), "candidate")
        if errors: raise IntakeError("; ".join(errors))
    return candidate


class KnowledgeStore:
    """Compatible with the explicit AAK-04 owner store binding; never pushes."""
    def __init__(self, root, creator, collection, code_commit):
        self.root = Path(root)
        if not self.root.is_absolute() or self.root == ROOT or ROOT in self.root.parents:
            raise IntakeError("explicit external store required")
        if self.root.is_symlink() or any(p.is_symlink() for p in self.root.parents):
            raise IntakeError("symlink store forbidden")
        self.creator, self.collection, self.code_commit = creator, collection, code_commit
        if not re.fullmatch(r"[0-9a-f]{40}", code_commit): raise IntakeError("code commit must be fixed")
        actual_code = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        dirty_code = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT, capture_output=True, text=True)
        if actual_code.returncode or dirty_code.returncode or actual_code.stdout.strip() != code_commit or dirty_code.stdout.strip():
            raise IntakeError("execute from the clean isolated checkout at the declared code commit")
        self.git_dir = self.root / "objects.git"
        marker = self.root / "store.json"
        expected = {"owner": OWNER, "creator": creator, "collection": collection}
        if not marker.is_file() or marker.is_symlink() or json.loads(marker.read_text()) != expected:
            raise IntakeError("AAK-04 owner store setup required; no implicit adoption")
        if self.git_dir.is_symlink(): raise IntakeError("symlink Git store forbidden")
        self.ref = "refs/heads/knowledge"
        self.head()

    def git(self, *args, body=None, index=None, check=True):
        env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_AUTHOR_NAME="art-history-owner", GIT_AUTHOR_EMAIL="local@example.invalid",
            GIT_COMMITTER_NAME="art-history-owner", GIT_COMMITTER_EMAIL="local@example.invalid",
            GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        if index: env["GIT_INDEX_FILE"] = str(index)
        r = subprocess.run(["git", "--git-dir", str(self.git_dir), *args], input=body, capture_output=True, env=env)
        if check and r.returncode: raise IntakeError("local Git operation failed: " + args[0])
        return r.stdout if check else r

    def head(self): return self.git("rev-parse", self.ref).decode().strip()

    def read(self, commit, path):
        r = self.git("show", commit + ":" + path, check=False)
        return r.stdout if not r.returncode else None

    def entities(self, commit):
        entities, _ = load_entities()
        blocked_targets = self.blocked_targets(commit)
        for name in self.git("ls-tree", "-r", "--name-only", commit, "entities/").decode().splitlines():
            text = self.read(commit, name).decode()
            meta = yaml.safe_load(text.split("---\n", 2)[1]); meta["path"] = name
            if meta["id"] in blocked_targets: continue
            entities[meta["id"]] = meta
        return entities

    def context_files(self, commit):
        files = {p.name: p.read_bytes() for p in (ROOT / "contexts").glob("*.md")}
        blocked_targets = self.blocked_targets(commit)
        for path in self.git("ls-tree", "-r", "--name-only", commit, "contexts/").decode().splitlines():
            if path.endswith(".md") and len(Path(path).parts) == 2:
                if "context/" + Path(path).stem in blocked_targets: continue
                files[Path(path).name] = self.read(commit, path)
        return files

    def context_payloads(self, commit, overrides=None):
        from context_kb import load_contexts, validate_contexts, compute_input_digest
        from build_context_vectors import load_context_config, build_payloads
        files = self.context_files(commit); files.update(overrides or {})
        with tempfile.TemporaryDirectory(dir=self.root) as td:
            base = Path(td); contexts = base / "contexts"; contexts.mkdir()
            config = base / "config"; config.mkdir()
            config_file = config / "context-dimensions.yaml"
            config_file.write_bytes((ROOT / "config/context-dimensions.yaml").read_bytes())
            for name, raw in files.items(): (contexts / name).write_bytes(raw)
            loaded = load_contexts(contexts, base); cfg = load_context_config()
            errors = validate_contexts(loaded, self.entities(commit), cfg)
            if errors: raise IntakeError("; ".join(errors))
            return build_payloads(loaded, cfg, compute_input_digest(config_file, contexts))

    def records(self, commit):
        if not re.fullmatch(r"[0-9a-f]{40}", commit): raise IntakeError("snapshot must be a full commit")
        self.git("merge-base", "--is-ancestor", commit, self.head())
        names = self.git("ls-tree", "-r", "--name-only", commit, "records/").decode().splitlines()
        return [json.loads(self.read(commit, path)) for path in names]

    def active_state(self, commit):
        records = self.records(commit); latest = {}
        for record in records:
            identity = (record["origin_instance_id"], record["record_id"])
            if identity not in latest or record["revision"] > latest[identity]["revision"]: latest[identity] = record
        invalid = {key(ref) for record in records for ref in record["invalidates"]}
        changed = True
        while changed:
            changed = False
            for record in records:
                if key(record) not in invalid and any(key(ref) in invalid for ref in record["derived_from"] if "record_id" in ref):
                    invalid.add(key(record)); changed = True
        return records, latest, invalid

    def blocked_targets(self, commit):
        _, latest, invalid = self.active_state(commit)
        targets = set()
        for record in latest.values():
            if record["lifecycle"] != "accepted" or key(record) in invalid:
                payload = json.loads(self.read(commit, record["payload_ref"]))
                binding = self.read(commit, "contexts/research-memory/bindings/" + key(record) + ".json")
                targets.add(json.loads(binding)["canonical_id"] if binding else payload["target_id"])
        return targets

    def commit(self, candidate, parent, operation, run_id, snapshots=None, *, dry_run=False):
        record, payload = candidate["record"], candidate["payload"]
        operation_path = "operations/" + digest(operation.encode()) + ".json"
        head = self.head()
        ledger = self.read(head, operation_path)
        if ledger:
            saved = json.loads(ledger)
            if saved["candidate_hash"] != digest(canonical(candidate)) or saved["parent"] != parent:
                raise IntakeError("OPERATION_CONFLICT")
            original = self.git("log", "-1", "--format=%H", head, "--", operation_path).decode().strip()
            return self.receipt(record, operation, run_id, parent, original, "ALREADY_APPLIED")
        validate_candidate(candidate, creator=self.creator, collection=self.collection, snapshots=snapshots)
        if head != parent: raise IntakeError("PARENT_CONFLICT")
        prior = self.records(head)
        prior_keys = {key(r) for r in prior}
        for reference in record["derived_from"] + record["supersedes"] + record["invalidates"]:
            if reference["owner_repository"] == OWNER and key(reference) not in prior_keys:
                raise IntakeError("local provenance must resolve an existing immutable revision")
        record_path = "records/" + key(record) + ".json"
        previous = self.read(head, record_path)
        if previous and previous != canonical(record): raise IntakeError("REVISION_CONFLICT")
        if previous: return self.receipt(record, operation, run_id, parent, parent, "NO_CHANGE")
        revisions = [r["revision"] for r in prior if r["record_id"] == record["record_id"] and r["origin_instance_id"] == record["origin_instance_id"]]
        if record["revision"] != max(revisions, default=0) + 1:
            raise IntakeError("REVISION_CONFLICT")
        writes = {record_path: canonical(record), record["payload_ref"]: canonical(payload)}
        entity = payload["entity"]
        if entity is not None and record["lifecycle"] == "accepted" and not payload["target_id"].startswith("context/"):
            entities = self.entities(head)
            target = payload["target_id"]
            # Authority identity resolves aliases without generating duplicate entities.
            authority = entity.get("authority") or {}
            matches = [eid for eid, meta in entities.items() if any(v and k != "none_reason" and (meta.get("authority") or {}).get(k) == v for k,v in authority.items())]
            if len(set(matches)) > 1: raise IntakeError("AMBIGUOUS_CANONICAL_ID")
            target = matches[0] if matches else target
            existing = entities.get(target)
            merged = copy.deepcopy(existing or entity)
            merged["id"], merged["uri"] = target, URI_PREFIX + target
            merged["status"] = "draft"
            if existing:
                # Keep contested dates, context and labels intact; alternatives remain in payload history.
                for field in ("sources", "relations"):
                    values = list(merged.get(field) or [])
                    for value in entity.get(field) or []:
                        if field == "sources" and any(v.get("url") == value.get("url") for v in values): continue
                        if value not in values: values.append(value)
                    merged[field] = values
            etype, slug = target.split("/", 1)
            if etype not in DIR_FOR_TYPE or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                raise IntakeError("unsafe canonical entity ID")
            path = "entities/" + DIR_FOR_TYPE[etype] + "/" + slug + ".md"
            merged["path"] = path
            entities[target] = merged
            errors = []
            validate_entities(entities, [(ROOT / path, merged, "")], load_config(), errors)
            if errors: raise IntakeError("; ".join(errors))
            merged.pop("path", None)
            old_bytes = self.read(head, path)
            body = old_bytes.decode().split("---\n", 2)[2] if old_bytes else (read_frontmatter(ROOT / path)[1] if (ROOT / path).exists() else "\nResearch intake; competing interpretations remain in immutable owner payloads.\n")
            writes[path] = ("---\n" + yaml.safe_dump(merged, allow_unicode=True, sort_keys=False) + "---\n" + body).encode()
            writes["contexts/research-memory/bindings/" + key(record) + ".json"] = canonical({"canonical_id": target})
        elif entity is not None and record["lifecycle"] == "accepted":
            target = payload["target_id"]
            if not re.fullmatch(r"context/[a-z0-9]+(?:-[a-z0-9]+)*", target): raise IntakeError("unsafe context ID")
            name = target.split("/", 1)[1] + ".md"
            current = self.context_files(head).get(name)
            if current:
                _, meta_text, body = current.decode().split("---\n", 2)
                merged = yaml.safe_load(meta_text)
                for field, identity_field in (("sources", "url"), ("signals", "id")):
                    values = list(merged.get(field) or [])
                    identities = {v[identity_field] for v in values}
                    values.extend(v for v in entity.get(field, []) if v[identity_field] not in identities)
                    merged[field] = values
                merged["status"] = "draft"
            else:
                merged, body = copy.deepcopy(entity), payload["context_body"]
                if not body: raise IntakeError("new context requires its owner-authored body sections")
            raw = ("---\n" + yaml.safe_dump(merged, allow_unicode=True, sort_keys=False) + "---\n" + body).encode()
            self.context_payloads(head, {name: raw})
            writes["contexts/" + name] = raw
        writes[operation_path] = canonical({"candidate_hash": digest(canonical(candidate)), "parent": parent, "record_id": record["record_id"]})
        if dry_run:
            return {"status": "VALID", "candidate_hash": digest(canonical(candidate)),
                    "target_parent": parent, "planned_paths": sorted(writes)}
        with tempfile.TemporaryDirectory(dir=self.root) as td:
            index = Path(td) / "index"
            self.git("read-tree", parent, index=index)
            for path, raw in sorted(writes.items()):
                sha = self.git("hash-object", "-w", "--stdin", body=raw).decode().strip()
                self.git("update-index", "--add", "--cacheinfo", "100644," + sha + "," + path, index=index)
            tree = self.git("write-tree", index=index).decode().strip()
            commit = self.git("commit-tree", tree, "-p", parent, body=canonical({"operation": operation, "run": run_id})).decode().strip()
            self.git("update-ref", self.ref, commit, parent)
        return self.receipt(record, operation, run_id, parent, commit, "COMMITTED")

    def receipt(self, record, operation, run, parent, commit, status):
        return {"contract_version": "knowledge-write-receipt/v1", "operation_id": operation, "run_id": run,
            "owner": OWNER, "collection": self.collection, "target_parent": parent, "target_commit": commit,
            "accepted_ids": [record["record_id"]], "rejected_ids": [], "schema_version": POLICY,
            "policy_version": POLICY, "index_commit": None, "index_hash": None, "status": status,
            "reason": "Owner-validated immutable knowledge; index remains a separate resumable step"}

    def index(self, commit):
        records = self.records(commit)
        entities = self.entities(commit)
        vectors, similarities = self.context_payloads(commit)
        result = {"commit": commit, "records": records, "context_vectors": vectors, "context_similarity": similarities,
                  "revalidation_required": sorted(self.blocked_targets(commit)),
                  "graph": {"entities": {eid: normalized_meta(meta) for eid,meta in entities.items()}, "edges": build_edges(entities)}}
        path = self.root / "research-index.json"
        if path.is_symlink(): raise IntakeError("symlink index forbidden")
        # Canonical graph construction functions; cache is regenerated, never committed as knowledge.
        raw = json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str).encode()
        with tempfile.NamedTemporaryFile(dir=self.root, delete=False) as handle:
            handle.write(raw); temporary = Path(handle.name)
        temporary.replace(path)
        return {"index_commit": commit, "index_hash": digest(raw), "records": len(records)}

    def retrieve(self, commit, query, scope, at):
        records, latest, invalid = self.active_state(commit)
        hits = []
        for record in latest.values():
            if record["creator_id"] != self.creator or record["collection_id"] != self.collection: continue
            if record["lifecycle"] != "accepted" or record["access_scope"] not in {scope, "public"} or key(record) in invalid: continue
            if record["valid_until"] and datetime.fromisoformat(record["valid_until"].replace("Z", "+00:00")) <= at: continue
            payload = json.loads(self.read(commit, record["payload_ref"]))
            if digest(canonical(payload)) != record["content_sha256"]: raise IntakeError("stored payload hash mismatch")
            if query.casefold() not in (payload["statement"] + " " + payload["target_id"]).casefold(): continue
            binding = self.read(commit, "contexts/research-memory/bindings/" + key(record) + ".json")
            target_id = json.loads(binding)["canonical_id"] if binding else payload["target_id"]
            hits.append({"record_id": record["record_id"], "revision": record["revision"],
                "origin_instance_id": record["origin_instance_id"], "creator_id": record["creator_id"],
                "owner_repository": OWNER, "knowledge_commit": commit, "code_commit": self.code_commit,
                "target_id": target_id, "payload_ref": record["payload_ref"],
                "epistemic_status": record["epistemic_status"], "classification": payload["classification"],
                "reason": "query matched owner knowledge; retrieval alone is not reuse"})
        return {"status": "FOUND" if hits else ("EMPTY_HISTORY" if not records else "NOT_APPLICABLE"), "records": hits}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "validate", "commit", "index", "retrieve", "invalidate"])
    parser.add_argument("--store-root", type=Path, required=True)
    parser.add_argument("--creator", required=True); parser.add_argument("--collection", required=True)
    parser.add_argument("--code-commit", required=True); parser.add_argument("--knowledge-commit", required=True)
    parser.add_argument("--candidate", type=Path); parser.add_argument("--source-snapshots", type=Path)
    parser.add_argument("--operation-id"); parser.add_argument("--run-id")
    parser.add_argument("--query", default=""); parser.add_argument("--scope", choices=["public", "creator-private"], default="creator-private")
    parser.add_argument("--at")
    args = parser.parse_args()
    try:
        store = KnowledgeStore(args.store_root, args.creator, args.collection, args.code_commit)
        if args.command == "index": result = store.index(args.knowledge_commit)
        elif args.command == "retrieve":
            at = datetime.fromisoformat(args.at.replace("Z", "+00:00"))
            if at.tzinfo is None: raise IntakeError("explicit query time required")
            result = store.retrieve(args.knowledge_commit, args.query, args.scope, at)
        else:
            if not args.candidate: raise IntakeError("candidate required")
            candidate = json.loads(args.candidate.read_text())
            snapshots = json.loads(args.source_snapshots.read_text()) if args.source_snapshots else {}
            if args.command in {"prepare", "validate"}:
                result = store.commit(candidate, args.knowledge_commit,
                    "validation-" + digest(canonical(candidate)), "validation", snapshots, dry_run=True)
            else:
                if not args.operation_id or not args.run_id: raise IntakeError("operation/run ID required")
                if args.command == "invalidate" and not candidate["record"]["invalidates"]: raise IntakeError("invalidation target required")
                result = store.commit(candidate, args.knowledge_commit, args.operation_id, args.run_id, snapshots)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result = {"status": "INDEX_PENDING" if args.command == "index" else "REJECTED", "reason": str(exc)}
        if args.command == "index": result["target_commit"] = args.knowledge_commit
        print(json.dumps(result, ensure_ascii=False)); return 1


if __name__ == "__main__": raise SystemExit(main())
