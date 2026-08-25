"""Command line interface for the initial agent harness primitives."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import signal
import threading
import time
from typing import Any

import yaml

from .models import RunState, RunStoreError
from .controller import HarnessConfig, HarnessController, doctor
from .github import GhClient, GitHubError
from .ids import new_run_id
from .lease import LeaseManager
from .queue import TaskQueue
from .store import RunStore
from .task_contract import ContractValidationError, load_contract, normalized_json, parse_contract


ROOT = Path(__file__).resolve().parents[1]
LABELS_PATH = ROOT / ".github" / "labels.yml"
DEFAULT_DB = ROOT / ".agent-harness" / "state.sqlite3"


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _validate_file(path: Path) -> int:
    try:
        contract = load_contract(path)
    except ContractValidationError as exc:
        _print_json({"ok": False, "errors": [error.as_dict() for error in exc.errors]})
        return 2
    _print_json({"ok": True, "contract": json.loads(normalized_json(contract))})
    return 0


def _validate_issue(number: int) -> int:
    try:
        result = subprocess.run(
            ["gh", "issue", "view", str(number), "--json", "body"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        _print_json({"ok": False, "error": {"code": "github_unavailable", "message": str(exc)}})
        return 3
    if result.returncode:
        _print_json({"ok": False, "error": {"code": "github_unavailable", "message": result.stderr.strip()}})
        return 3
    try:
        body = json.loads(result.stdout)["body"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        _print_json({"ok": False, "error": {"code": "github_invalid_response", "message": str(exc)}})
        return 3
    try:
        from .task_contract import parse_contract

        contract = parse_contract(body)
    except ContractValidationError as exc:
        _print_json({"ok": False, "issue": number, "errors": [error.as_dict() for error in exc.errors]})
        return 2
    _print_json({"ok": True, "issue": number, "contract": json.loads(normalized_json(contract))})
    return 0


def _load_labels() -> list[dict[str, str]]:
    data = yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(".github/labels.yml must contain a list")
    labels: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("name", "color", "description")):
            raise ValueError("each label requires name, color, description")
        labels.append({key: item[key] for key in ("name", "color", "description")})
    return labels


def _sync_labels(apply: bool) -> int:
    try:
        labels = _load_labels()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        _print_json({"ok": False, "error": {"code": "invalid_labels", "message": str(exc)}})
        return 2
    if not apply:
        _print_json({"ok": True, "dry_run": True, "labels": labels})
        return 0
    failures = []
    for label in labels:
        result = subprocess.run(
            ["gh", "label", "create", label["name"], "--color", label["color"], "--description", label["description"], "--force"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode:
            failures.append({"label": label["name"], "message": result.stderr.strip()})
    if failures:
        _print_json({"ok": False, "error": {"code": "label_sync_failed", "failures": failures}})
        return 3
    _print_json({"ok": True, "dry_run": False, "labels": labels})
    return 0


def _store(args: argparse.Namespace) -> RunStore:
    return RunStore(args.db or DEFAULT_DB)


def _run_output(run: Any, as_json: bool) -> None:
    if as_json:
        _print_json(run.as_dict() if hasattr(run, "as_dict") else run)
        return
    if isinstance(run, list):
        for item in run:
            print(f"{item.run_id} issue=#{item.issue_number} state={item.state.value} attempt={item.attempt}")
    else:
        print(f"{run.run_id} issue=#{run.issue_number} state={run.state.value} attempt={run.attempt}")


def _run_command(args: argparse.Namespace) -> int:
    if args.run_command == "execute":
        return _execute_command(args)
    store = _store(args)
    try:
        if args.run_command == "list":
            runs = store.list_runs(args.state)
            _run_output(runs, args.json)
            return 0
        if args.run_command == "show":
            _run_output(store.get_run(args.run_id), args.json)
            return 0
        if args.run_command == "events":
            events = store.events(args.run_id)
            if args.jsonl:
                for event in events:
                    print(json.dumps(event, ensure_ascii=False, sort_keys=True))
            else:
                _print_json(events)
            return 0
        if args.run_command == "resume":
            _run_output(store.resume(args.run_id, args.reason), args.json)
            return 0
        if args.run_command == "cancel":
            _run_output(store.cancel(args.run_id, args.reason), args.json)
            return 0
    except RunStoreError as exc:
        _print_json({"ok": False, "error": {"code": exc.__class__.__name__, "message": str(exc)}})
        return 4
    return 2


def _execute_command(args: argparse.Namespace) -> int:
    config = HarnessConfig.load(ROOT / "config" / "agent-harness.yaml", root=ROOT)
    if not config.enabled:
        _print_json({"status": "disabled", "reason": "config enabled is false"})
        return 5
    try:
        client = GhClient()
        controller = HarnessController(root=ROOT, client=client, config=config, store=_store(args), owner_id=args.runner_id)
        result = controller.execute_issue(args.issue) if args.issue is not None else controller.execute_run(args.run_id)
        payload: dict[str, Any] = {"status": result.status, "issue_number": result.issue_number, "run_id": result.run_id, "reason": result.reason}
        if result.outcome is not None:
            payload["outcome"] = {"state": result.outcome.state.value, "attempts": result.outcome.attempts, "failure_code": result.outcome.failure_code.value if result.outcome.failure_code else None}
        _print_json(payload)
        return 0 if result.status in {"completed", "recovered", "idle"} and (result.outcome is None or result.outcome.state == RunState.SUCCEEDED) else 4
    except (GitHubError, RunStoreError, OSError, ValueError) as exc:
        _print_json({"status": "blocked", "reason": str(exc)})
        return 4


def _queue_command(args: argparse.Namespace) -> int:
    if args.queue_command == "claim":
        return _queue_claim(args)
    if args.queue_command in {"heartbeat", "release"}:
        return _queue_lease_action(args)
    try:
        decisions = TaskQueue(GhClient()).decisions()
    except GitHubError as exc:
        _print_json({"ok": False, "error": {"code": "github_unavailable", "message": str(exc)}})
        return 3
    values = [{"issue": decision.issue.number, "status": decision.status, "reason": decision.reason, "title": decision.issue.title} for decision in decisions]
    if args.queue_command == "next":
        values = values[:1]
    if args.json:
        _print_json(values)
    else:
        for value in values:
            print(f"#{value['issue']} {value['status']} {value['title']}")
    return 0


def _queue_claim(args: argparse.Namespace) -> int:
    root = ROOT
    config = HarnessConfig.load(root / "config" / "agent-harness.yaml", root=root)
    store = _store(args)
    try:
        client = GhClient()
        issue = client.get_issue(args.issue)
        decision = TaskQueue(client).next([issue])
        if decision is None:
            _print_json({"ok": False, "status": "contended", "issue": args.issue, "reason": "issue is not ready"})
            return 4
        contract = parse_contract(issue.body)
        environment = os.environ.copy()
        environment.pop("GIT_INDEX_FILE", None)
        base = subprocess.run(["git", "rev-parse", f"origin/{config.base_branch}"], cwd=root, env=environment, capture_output=True, text=True, check=False, timeout=10)
        if base.returncode:
            raise GitHubError(base.stderr.strip() or "base branch is unavailable")
        base_sha = base.stdout.strip()
        run_id = new_run_id()
        owner_id = args.runner_id
        manager = LeaseManager(client, owner_id=owner_id, ttl_seconds=config.lease_ttl_seconds)
        lease = manager.acquire(issue_number=issue.number, run_id=run_id, base_sha=base_sha)
        if lease is None:
            _print_json({"ok": False, "status": "contended", "issue": issue.number, "reason": "another runner owns the lease"})
            return 4
        try:
            run = store.create_run(
                repository=client.repository,
                issue_number=issue.number,
                contract_hash=store.hash_contract(normalized_json(contract)),
                base_sha=base_sha,
                branch=f"agent/issue-{issue.number}/{run_id[:8]}",
                worktree=str(config.worktree_root / run_id),
                backend="default",
                run_id=run_id,
            )
            store.record_lease(run_id, owner_id=owner_id, token_hash=lease.token_hash or hashlib.sha256(lease.token.encode()).hexdigest(), acquired_at=lease.acquired_at, heartbeat_at=lease.heartbeat_at, expires_at=lease.expires_at)
            client.add_label(issue.number, "agent-running")
        except Exception:
            manager.release(lease)
            if "run" in locals():
                current = store.get_run(run.run_id)
                if current.state not in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
                    store.transition(run.run_id, RunState.BLOCKED, expected_state=current.state, reason_code="claim_failed", reason_detail="claim side effect could not be completed")
            raise
        _print_json({"ok": True, "status": "claimed", "run": run.as_dict()})
        return 0
    except (GitHubError, OSError, ValueError) as exc:
        _print_json({"ok": False, "error": {"code": "claim_failed", "message": str(exc)}})
        return 3


def _queue_lease_action(args: argparse.Namespace) -> int:
    root = ROOT
    config = HarnessConfig.load(root / "config" / "agent-harness.yaml", root=root)
    store = _store(args)
    try:
        client = GhClient()
        run = store.get_run(args.run_id)
        manager = LeaseManager(client, owner_id=args.runner_id, ttl_seconds=config.lease_ttl_seconds)
        lease = manager.load_owned(issue_number=run.issue_number, run_id=run.run_id)
        if lease is None:
            raise GitHubError("the requested runner does not own the Issue lease")
        token_hash = lease.token_hash or hashlib.sha256(lease.token.encode()).hexdigest()
        if args.queue_command == "heartbeat":
            lease = manager.heartbeat(lease, base_sha=run.base_sha)
            store.heartbeat(run.run_id, lease_expires_at=lease.expires_at)
            store.heartbeat_lease(run.run_id, heartbeat_at=lease.heartbeat_at, expires_at=lease.expires_at)
            _print_json({"ok": True, "status": "heartbeated", "run_id": run.run_id, "expires_at": lease.expires_at})
            return 0
        manager.release(lease)
        store.release_lease(run.run_id, owner_id=args.runner_id, token_hash=token_hash)
        current = store.get_run(run.run_id)
        if current.state not in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
            current = store.transition(run.run_id, RunState.BLOCKED, expected_state=current.state, reason_code="lease_released", reason_detail="lease released by operator")
        _print_json({"ok": True, "status": "released", "run": current.as_dict()})
        return 0
    except (GitHubError, RunStoreError, OSError, ValueError) as exc:
        _print_json({"ok": False, "error": {"code": "lease_action_failed", "message": str(exc)}})
        return 4


def _controller_command(args: argparse.Namespace) -> int:
    root = ROOT
    config = HarnessConfig.load(root / "config" / "agent-harness.yaml", root=root)
    if args.controller_command == "doctor":
        result = doctor(root, config)
        _print_json(result) if args.json else print("ok" if result["ok"] else "failed")
        return 0 if result["ok"] else 5
    if args.controller_command == "finalize":
        try:
            result = GhClient().finalize_merged_pr(args.pr)
        except GitHubError as exc:
            _print_json({"status": "blocked", "reason": str(exc)})
            return 4
        _print_json(result)
        return 0
    if args.controller_command == "reconcile-closed":
        try:
            result = GhClient().finalize_closed_pr(args.pr)
        except GitHubError as exc:
            _print_json({"status": "blocked", "reason": str(exc)})
            return 4
        _print_json(result)
        return 0
    if not config.enabled:
        _print_json({"status": "disabled", "reason": "config enabled is false"})
        return 0
    controller = HarnessController(root=root, client=GhClient(), config=config)
    poll_seconds = getattr(args, "poll_seconds", None)
    stop_requested = threading.Event()
    previous_handlers = {}
    if poll_seconds is not None:
        if poll_seconds < 1:
            print("--poll-seconds must be positive", file=sys.stderr)
            return 2
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, lambda _signum, _frame: stop_requested.set())
    try:
        while True:
            try:
                result = controller.run_once()
            except (GitHubError, OSError, ValueError) as exc:
                _print_json({"status": "blocked", "reason": str(exc)})
                return 4
            _print_json({"status": result.status, "issue_number": result.issue_number, "run_id": result.run_id, "reason": result.reason})
            if args.controller_command == "serve-once" or getattr(args, "once", False) or poll_seconds is None:
                return 0
            if stop_requested.wait(poll_seconds):
                _print_json({"status": "stopped", "reason": "shutdown requested; no new claim will be started"})
                return 0
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent_harness")
    parser.add_argument("--db", type=Path, help="state database path (default: .agent-harness/state.sqlite3)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    task = subparsers.add_parser("task")
    task_subparsers = task.add_subparsers(dest="task_command", required=True)
    validate = task_subparsers.add_parser("validate")
    source = validate.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path)
    source.add_argument("--issue", type=int)

    labels = subparsers.add_parser("labels")
    labels_subparsers = labels.add_subparsers(dest="labels_command", required=True)
    sync = labels_subparsers.add_parser("sync")
    sync.add_argument("--dry-run", action="store_true", help="show intended labels without changing GitHub")
    sync.add_argument("--apply", action="store_true", help="create or update labels in GitHub")

    run = subparsers.add_parser("run")
    run_subparsers = run.add_subparsers(dest="run_command", required=True)
    list_runs = run_subparsers.add_parser("list")
    list_runs.add_argument("--state", choices=[state.value for state in RunState])
    list_runs.add_argument("--json", action="store_true")
    show = run_subparsers.add_parser("show")
    show.add_argument("run_id")
    show.add_argument("--json", action="store_true")
    events = run_subparsers.add_parser("events")
    events.add_argument("run_id")
    events.add_argument("--jsonl", action="store_true")
    for command in ("resume", "cancel"):
        action = run_subparsers.add_parser(command)
        action.add_argument("run_id")
        action.add_argument("--reason", required=True)
        action.add_argument("--json", action="store_true")
    execute = run_subparsers.add_parser("execute")
    execute_source = execute.add_mutually_exclusive_group(required=True)
    execute_source.add_argument("--issue", type=int)
    execute_source.add_argument("--run-id")
    execute.add_argument("--runner-id", default=f"{socket.gethostname()}:{os.getpid()}")
    execute.add_argument("--json", action="store_true")

    queue = subparsers.add_parser("queue")
    queue_subparsers = queue.add_subparsers(dest="queue_command", required=True)
    for command in ("list", "next"):
        action = queue_subparsers.add_parser(command)
        action.add_argument("--json", action="store_true")
    claim = queue_subparsers.add_parser("claim")
    claim.add_argument("issue", type=int)
    claim.add_argument("--runner-id", default=f"{socket.gethostname()}:{os.getpid()}")
    claim.add_argument("--json", action="store_true")
    for command in ("heartbeat", "release"):
        action = queue_subparsers.add_parser(command)
        action.add_argument("run_id")
        action.add_argument("--runner-id", required=True)
        action.add_argument("--json", action="store_true")

    controller = subparsers.add_parser("controller")
    controller_subparsers = controller.add_subparsers(dest="controller_command", required=True)
    serve = controller_subparsers.add_parser("serve")
    serve_group = serve.add_mutually_exclusive_group()
    serve_group.add_argument("--once", action="store_true")
    serve_group.add_argument("--poll-seconds", type=int, default=None)
    controller_subparsers.add_parser("serve-once")
    finalize = controller_subparsers.add_parser("finalize")
    finalize.add_argument("--pr", type=int, required=True)
    reconcile_closed = controller_subparsers.add_parser("reconcile-closed")
    reconcile_closed.add_argument("--pr", type=int, required=True)
    doctor_parser = controller_subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "task" and args.task_command == "validate":
        return _validate_file(args.file) if args.file else _validate_issue(args.issue)
    if args.command == "labels" and args.labels_command == "sync":
        if args.dry_run and args.apply:
            print("--dry-run and --apply are mutually exclusive", file=sys.stderr)
            return 2
        return _sync_labels(args.apply)
    if args.command == "run":
        return _run_command(args)
    if args.command == "queue":
        return _queue_command(args)
    if args.command == "controller":
        return _controller_command(args)
    return 2
