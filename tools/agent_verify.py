#!/usr/bin/env python3
"""Verify one external-agent task without starting an Agent or writing remotely."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
from typing import Callable
import time
from typing import Any

import yaml

try:
    from .agent_session import load_session, task_hash
    from .agent_task import ContractInvalid, load_contract
    from .agent_support import ROOT, file_states, path_forbidden, path_in_scope, run_git, secret_finding, symlink_component
except ImportError:
    from agent_session import load_session, task_hash
    from agent_task import ContractInvalid, load_contract
    from agent_support import ROOT, file_states, path_forbidden, path_in_scope, run_git, secret_finding, symlink_component


MAX_OUTPUT_BYTES = 1024 * 1024
SHELLS = {"sh", "bash", "zsh", "fish", "dash", "ksh", "cmd", "cmd.exe", "powershell", "pwsh"}
CHECK_ENV_NAMES = {"PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "VIRTUAL_ENV", "UV_CACHE_DIR"}
_CANCEL_REQUESTED = False


def _terminate(process: subprocess.Popen[bytes], *, force: bool = False) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL if force else signal.SIGTERM)
            return
        except (ProcessLookupError, PermissionError):
            pass
    try:
        (process.kill if force else process.terminate)()
    except ProcessLookupError:
        pass


def run_check(
    argv: list[str],
    timeout_seconds: int,
    *,
    is_cancelled: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    if not argv or any(not isinstance(part, str) or not part or "\x00" in part for part in argv):
        return {"id": "", "argv": argv, "exit_code": None, "duration_seconds": 0, "code": "invalid_argv"}
    if Path(argv[0]).name in SHELLS:
        return {"id": "", "argv": argv, "exit_code": None, "duration_seconds": 0, "code": "shell_forbidden"}
    environment = {key: value for key, value in os.environ.items() if key in CHECK_ENV_NAMES}
    environment.setdefault("PATH", os.defpath)
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            argv,
            cwd=ROOT,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=os.name == "posix",
        )
    except OSError as exc:
        return {"id": "", "argv": argv, "exit_code": None, "duration_seconds": round(time.monotonic() - started, 3), "code": "start_failed", "detail": str(exc)}
    selector = selectors.DefaultSelector()
    assert process.stdout is not None
    assert process.stderr is not None
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    reason: str | None = None
    finish_deadline: float | None = None
    force_sent = False
    try:
        while selector.get_map():
            now = time.monotonic()
            if process.poll() is None and reason is None:
                if is_cancelled is not None and is_cancelled():
                    reason = "cancelled"
                    _terminate(process)
                    finish_deadline = now + 1
                elif now - started >= timeout_seconds:
                    reason = "timeout"
                    _terminate(process)
                    finish_deadline = now + 1
            if process.poll() is not None:
                finish_deadline = finish_deadline or now + 0.5
            if finish_deadline is not None and now >= finish_deadline and process.poll() is None and not force_sent:
                _terminate(process, force=True)
                force_sent = True
                finish_deadline = now + 1
            if finish_deadline is not None and now >= finish_deadline and process.poll() is not None:
                for key in list(selector.get_map().values()):
                    selector.unregister(key.fileobj)
                break
            wait_for = 0.05 if reason is not None else min(0.1, max(0.0, timeout_seconds - (now - started)))
            for key, _ in selector.select(timeout=wait_for):
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    selector.unregister(key.fileobj)
                    continue
                room = MAX_OUTPUT_BYTES - len(buffers[key.data])
                if room <= 0:
                    if reason is None:
                        reason = "output_limit"
                        _terminate(process)
                        finish_deadline = time.monotonic() + 1
                    continue
                if len(data) > room:
                    if reason is None:
                        reason = "output_limit"
                        _terminate(process)
                        finish_deadline = time.monotonic() + 1
                buffers[key.data].extend(data[:room])
        try:
            returncode = process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            _terminate(process, force=True)
            try:
                returncode = process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                returncode = None
    finally:
        selector.close()
        if process.poll() is None:
            _terminate(process, force=True)
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                pass
        process.stdout.close()
        process.stderr.close()
    code = reason or ("ok" if returncode == 0 else "check_failed")
    return {
        "id": "",
        "argv": argv,
        "exit_code": returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "code": code,
    }


def _load_registry() -> dict[str, Any]:
    try:
        value = yaml.safe_load((ROOT / "config" / "agent-checks.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"invalid check registry: {exc}") from exc
    checks = value.get("checks") if isinstance(value, dict) else None
    if not isinstance(checks, dict):
        raise ValueError("check registry must contain an object named checks")
    for check_id, definition in checks.items():
        if not isinstance(check_id, str) or not isinstance(definition, dict):
            raise ValueError("check registry entries are invalid")
        if set(definition) != {"description", "argv", "timeout_seconds"}:
            raise ValueError(f"invalid fields for check {check_id}")
        if not isinstance(definition["description"], str) or not definition["description"].strip():
            raise ValueError(f"invalid description for check {check_id}")
        argv = definition.get("argv")
        timeout = definition.get("timeout_seconds")
        if not isinstance(argv, list) or not argv or any(not isinstance(part, str) or not part or "\x00" in part for part in argv):
            raise ValueError(f"invalid argv for check {check_id}")
        if Path(argv[0]).name in SHELLS:
            raise ValueError(f"shell is forbidden for check {check_id}")
        if not isinstance(timeout, int) or timeout < 1:
            raise ValueError(f"invalid timeout for check {check_id}")
    return checks


def _git_revision_exists(sha: str) -> bool:
    if not isinstance(sha, str) or not sha:
        return False
    return run_git(["cat-file", "-e", f"{sha}^{{commit}}"]).returncode == 0


def _session_entries(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["path"]: entry for entry in payload["baseline_entries"]}


def _changed_paths(session: dict[str, Any], session_file: Path) -> tuple[list[str], dict[str, str]]:
    baseline = _session_entries(session)
    current = file_states(ROOT, base_sha=session["base_sha"])
    try:
        session_relative = session_file.expanduser().resolve().relative_to(ROOT).as_posix()
    except ValueError:
        session_relative = None
    if session_relative is not None:
        current.pop(session_relative, None)
        baseline.pop(session_relative, None)
    paths = sorted(set(baseline) | set(current))
    changed = [path for path in paths if baseline.get(path) != (current[path].as_dict() if path in current else None)]
    kinds = {
        path: current[path].kind if path in current else str(baseline[path].get("kind", "missing"))
        for path in changed
    }
    return changed, kinds


def _scope_failures(paths: list[str], task: dict[str, Any], kinds: dict[str, str]) -> list[dict[str, str]]:
    include = task["scope"]["include"]
    exclude = task["scope"]["exclude"]
    failures = []
    for path in paths:
        reason = path_forbidden(path)
        if reason is None and (kinds.get(path) == "symlink" or symlink_component(ROOT, path)):
            reason = "symlink_forbidden"
        if reason is None and not path_in_scope(path, include, exclude):
            reason = "outside_scope"
        if reason is not None:
            failures.append({"path": path, "code": reason})
    return failures


def _secret_failures(paths: list[str]) -> list[dict[str, str]]:
    failures = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            continue
        try:
            finding = secret_finding(path.read_bytes())
        except OSError:
            finding = "file_unreadable"
        if finding:
            failures.append({"path": relative, "code": "secret_detected"})
    return failures


def verify(task_file: Path, session_file: Path, *, cancel_file: Path | None = None) -> tuple[int, dict[str, Any]]:
    try:
        task = load_contract(task_file, root=ROOT)
        session = load_session(session_file)
    except (ContractInvalid, OSError, ValueError) as exc:
        return 2, {"schema_version": 1, "ok": False, "errors": [{"code": "input_invalid", "message": str(exc)}]}
    errors: list[dict[str, str]] = []
    if session["task_hash"] != task_hash(task):
        errors.append({"code": "task_changed", "message": "session task hash does not match task file"})
    if not _git_revision_exists(session["base_sha"]):
        errors.append({"code": "base_missing", "message": "session base SHA is not a commit in this repository"})
    if errors:
        return 2, {"schema_version": 1, "ok": False, "errors": errors, "task_hash": task_hash(task), "base_sha": session.get("base_sha")}

    changed, kinds = _changed_paths(session, session_file)
    scope_failures = _scope_failures(changed, task, kinds)
    secret_failures = _secret_failures(changed)
    check_results: list[dict[str, Any]] = []
    if not scope_failures and not secret_failures:
        try:
            registry = _load_registry()
        except ValueError as exc:
            return 2, {"schema_version": 1, "ok": False, "errors": [{"code": "check_registry_invalid", "message": str(exc)}]}
        check_ids = [check_id for check_id in task["checks"] if check_id != "canonical"] + ["canonical"]
        for check_id in check_ids:
            definition = registry.get(check_id)
            if definition is None:
                check_results.append({"id": check_id, "argv": [], "exit_code": None, "duration_seconds": 0, "code": "unknown_check"})
                continue
            result = run_check(
                definition["argv"],
                definition["timeout_seconds"],
                is_cancelled=lambda: _CANCEL_REQUESTED or (cancel_file is not None and cancel_file.exists()),
            )
            result["id"] = check_id
            check_results.append(result)

    ok = not scope_failures and not secret_failures and all(item["code"] == "ok" for item in check_results)
    payload = {
        "schema_version": 1,
        "ok": ok,
        "task_hash": task_hash(task),
        "base_sha": session["base_sha"],
        "manifest": changed,
        "scope": {"ok": not scope_failures, "failures": scope_failures},
        "secrets": {"ok": not secret_failures, "failures": secret_failures},
        "checks": check_results,
        "acceptance": [item["id"] for item in task["acceptance"]],
    }
    return (0 if ok else 1), payload


def _request_cancel(signum: int, frame: Any) -> None:
    del signum, frame
    global _CANCEL_REQUESTED
    _CANCEL_REQUESTED = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent_verify")
    parser.add_argument("--task-file", required=True, type=Path)
    parser.add_argument("--session", required=True, type=Path)
    parser.add_argument("--cancel-file", type=Path, help="cancel the current check when this file exists")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    previous_handlers = {}
    for signum in (signal.SIGINT, signal.SIGTERM):
        previous_handlers[signum] = signal.signal(signum, _request_cancel)
    code, payload = verify(args.task_file, args.session, cancel_file=args.cancel_file)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    else:
        print("verified" if payload.get("ok") else "not verified")
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
