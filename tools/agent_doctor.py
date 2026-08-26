#!/usr/bin/env python3
"""Read-only readiness checks for an external agent working in this repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

import yaml

try:
    from .agent_support import ROOT
except ImportError:
    from agent_support import ROOT


def _check(name: str, ok: bool, code: str, detail: str) -> dict[str, Any]:
    return {"name": name, "ok": ok, "code": code, "detail": detail}


def _command_version(command: str, root: Path) -> tuple[bool, str]:
    path = shutil.which(command)
    if path is None:
        return False, f"{command} is not on PATH"
    try:
        result = subprocess.run([command, "--version"], cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{command} cannot be probed: {exc}"
    return result.returncode == 0, result.stdout.decode("utf-8", errors="replace").splitlines()[0][:200]


def checks(root: Path = ROOT) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    root_ok = (root / ".git").exists()
    result.append(_check("repository_root", root_ok, "repository_root_ready" if root_ok else "repository_root_missing", str(root)))
    python_ok = sys.version_info >= (3, 12) and sys.version_info < (3, 13)
    result.append(_check("python", python_ok, "python_version_invalid" if not python_ok else "python_ready", sys.version.split()[0]))
    for command in ("uv", "git"):
        ok, detail = _command_version(command, root)
        result.append(_check(command, ok, f"{command}_unavailable" if not ok else f"{command}_ready", detail))
    required_files = (
        "uv.lock",
        "AGENTS.md",
        "config/agent-task.schema.json",
        "config/agent-session.schema.json",
        "config/agent-checks.yaml",
        "tools/verify.py",
        "tools/agent_task.py",
        "tools/agent_session.py",
        "tools/agent_verify.py",
    )
    for relative in required_files:
        exists = (root / relative).is_file()
        result.append(_check(relative, exists, "required_file_missing" if not exists else "required_file_present", relative))
    try:
        schema = json.loads((root / "config" / "agent-task.schema.json").read_text(encoding="utf-8"))
        schema_ok = schema.get("title", "").endswith("v2") and schema.get("properties", {}).get("version", {}).get("const") == 2
        result.append(_check("task_schema", schema_ok, "task_schema_invalid" if not schema_ok else "task_schema_ready", "version 2"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result.append(_check("task_schema", False, "task_schema_invalid", str(exc)))
    try:
        registry = yaml.safe_load((root / "config" / "agent-checks.yaml").read_text(encoding="utf-8")) or {}
        definitions = registry.get("checks") if isinstance(registry, dict) else None
        canonical = definitions.get("canonical") if isinstance(definitions, dict) else None
        registry_ok = (
            isinstance(canonical, dict)
            and set(canonical) == {"description", "argv", "timeout_seconds"}
            and isinstance(canonical["description"], str)
            and bool(canonical["description"].strip())
            and canonical["argv"] == ["uv", "run", "--locked", "python", "tools/verify.py"]
            and isinstance(canonical["timeout_seconds"], int)
            and canonical["timeout_seconds"] >= 1
        )
        result.append(_check("check_registry", registry_ok, "check_registry_invalid" if not registry_ok else "check_registry_ready", "canonical"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        result.append(_check("check_registry", False, "check_registry_invalid", str(exc)))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent_doctor")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    check_results = checks()
    result = {"ok": all(item["ok"] for item in check_results), "checks": check_results}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=False))
    else:
        for item in result["checks"]:
            mark = "ok" if item["ok"] else "FAIL"
            print(f"[{mark}] {item['name']}: {item['detail']} ({item['code']})")
        print("ready" if result["ok"] else "not ready")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
