#!/usr/bin/env python3
"""Create and inspect a non-destructive baseline for one external-agent task."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

try:
    from .agent_task import ContractInvalid, load_contract, normalized_json
    from .agent_support import ROOT, file_states, relative_path
except ImportError:
    from agent_task import ContractInvalid, load_contract, normalized_json
    from agent_support import ROOT, file_states, relative_path


SESSION_VERSION = 1


def task_hash(task: dict[str, Any]) -> str:
    return hashlib.sha256(normalized_json(task).encode("utf-8")).hexdigest()


def _resolve_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    relative = resolved.relative_to(ROOT).as_posix()
    if not (relative == ".agent-local" or relative.startswith(".agent-local/")):
        raise ValueError("session output inside repository must be under .agent-local")
    return resolved


def _git_head() -> str:
    import subprocess
    try:
        from .agent_support import run_git
    except ImportError:
        from agent_support import run_git

    result = run_git(["rev-parse", "HEAD"])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "cannot resolve HEAD")
    return result.stdout.decode("ascii", errors="strict").strip()


def begin(task_file: Path, output: Path) -> dict[str, Any]:
    task = load_contract(task_file, root=ROOT)
    destination = _resolve_output(output)
    if destination.exists():
        raise FileExistsError(f"session output already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    baseline = file_states(ROOT)
    payload = {
        "version": SESSION_VERSION,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "repository_root": str(ROOT),
        "task_hash": task_hash(task),
        "base_sha": _git_head(),
        "baseline_entries": [state.as_dict() for state in sorted(baseline.values(), key=lambda item: item.path)],
    }
    temporary = destination.with_name(destination.name + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return payload


def load_session(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid session: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("version") != SESSION_VERSION:
        raise ValueError("invalid session version")
    required = {"version", "created_at", "repository_root", "task_hash", "base_sha", "baseline_entries"}
    if set(payload) != required:
        raise ValueError("session keys do not match the session schema")
    if (
        not isinstance(payload["created_at"], str)
        or not payload["created_at"].strip()
        or payload["repository_root"] != str(ROOT)
        or not isinstance(payload["task_hash"], str)
        or not re.fullmatch(r"[a-f0-9]{64}", payload["task_hash"])
        or not isinstance(payload["base_sha"], str)
        or not re.fullmatch(r"[a-f0-9]{40,64}", payload["base_sha"])
    ):
        raise ValueError("session repository or hash fields are invalid")
    entries = payload["baseline_entries"]
    if not isinstance(entries, list):
        raise ValueError("baseline_entries must be an array")
    paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "kind", "content_sha256"}:
            raise ValueError("invalid baseline entry")
        if not isinstance(entry["path"], str) or not isinstance(entry["kind"], str):
            raise ValueError("invalid baseline entry fields")
        try:
            relative_path(entry["path"])
        except ValueError as exc:
            raise ValueError("invalid baseline entry path") from exc
        if entry["path"] in paths or entry["kind"] not in {"file", "symlink", "missing"}:
            raise ValueError("invalid or duplicate baseline entry")
        paths.add(entry["path"])
        content_hash = entry["content_sha256"]
        if content_hash is not None and (not isinstance(content_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", content_hash)):
            raise ValueError("invalid baseline content hash")
        if entry["kind"] == "missing" and content_hash is not None:
            raise ValueError("missing baseline entries cannot have content hashes")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent_session")
    sub = parser.add_subparsers(dest="command", required=True)
    begin_parser = sub.add_parser("begin")
    begin_parser.add_argument("--task-file", required=True, type=Path)
    begin_parser.add_argument("--output", required=True, type=Path)
    show_parser = sub.add_parser("show")
    show_parser.add_argument("--session", required=True, type=Path)
    show_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "begin":
            payload = begin(args.task_file, args.output)
        else:
            payload = load_session(args.session)
    except (ContractInvalid, FileExistsError, OSError, ValueError, RuntimeError) as exc:
        print(f"agent_session: {exc}", file=sys.stderr)
        return 2
    if args.command == "show" and not args.json:
        print(f"session: {args.session}")
        print(f"base_sha: {payload['base_sha']}")
        print(f"task_hash: {payload['task_hash']}")
        print(f"baseline_entries: {len(payload['baseline_entries'])}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
