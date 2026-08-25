"""Command line interface for the initial agent harness primitives."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

import yaml

from .models import RunState, RunStoreError
from .controller import HarnessConfig, HarnessController, doctor
from .github import GhClient, GitHubError
from .queue import TaskQueue
from .store import RunStore
from .task_contract import ContractValidationError, load_contract, normalized_json


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


def _queue_command(args: argparse.Namespace) -> int:
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
    if not config.enabled:
        _print_json({"status": "disabled", "reason": "config enabled is false"})
        return 0
    controller = HarnessController(root=root, client=GhClient(), config=config)
    poll_seconds = getattr(args, "poll_seconds", None)
    while True:
        try:
            result = controller.run_once()
        except (GitHubError, OSError, ValueError) as exc:
            _print_json({"status": "blocked", "reason": str(exc)})
            return 4
        _print_json({"status": result.status, "issue_number": result.issue_number, "run_id": result.run_id, "reason": result.reason})
        if args.controller_command == "serve-once" or getattr(args, "once", False) or poll_seconds is None:
            return 0
        if poll_seconds < 1:
            print("--poll-seconds must be positive", file=sys.stderr)
            return 2
        time.sleep(poll_seconds)


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

    queue = subparsers.add_parser("queue")
    queue_subparsers = queue.add_subparsers(dest="queue_command", required=True)
    for command in ("list", "next"):
        action = queue_subparsers.add_parser(command)
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
