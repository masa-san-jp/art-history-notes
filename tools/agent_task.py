#!/usr/bin/env python3
"""Parse and validate the external-agent task contract v2."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- agent-task:v2 -->"
_FENCE = re.compile(
    re.escape(MARKER) + r"[ \t]*\r?\n" + (chr(96) * 3) + "yaml" +
    r"\r?\n(?P<body>.*?)\r?\n" + (chr(96) * 3),
    re.DOTALL,
)
_ID = re.compile(r"^[a-z0-9-]+$")
_DANGEROUS = {"", ".", ".."}
_TOP_KEYS = {
    "version", "objective", "context", "scope", "requirements", "acceptance",
    "checks", "constraints", "depends_on", "non_goals",
}


@dataclass(frozen=True)
class ContractError:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


class ContractInvalid(ValueError):
    def __init__(self, errors: list[ContractError]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(f"{e.path}: {e.message}" for e in errors))


def _pointer(path: str, key: str | int) -> str:
    escaped = str(key).replace("~", "~0").replace("/", "~1")
    return f"{path}/{escaped}" if path else f"/{escaped}"


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def _keys(value: Any, allowed: set[str], path: str, errors: list[ContractError]) -> None:
    if not isinstance(value, dict):
        errors.append(ContractError("type", path, "must be an object"))
        return
    for key in value:
        if key not in allowed:
            errors.append(ContractError("unknown_key", _pointer(path, key), "unknown key"))


def _path_pattern(value: Any, path: str, errors: list[ContractError]) -> None:
    if not _string(value) or value.startswith("/") or "\\" in value:
        errors.append(ContractError("unsafe_path", path, "must be a relative POSIX path pattern"))
        return
    if any(part in _DANGEROUS for part in value.split("/")):
        errors.append(ContractError("unsafe_path", path, "must not contain empty, '.' or '..' components"))


def _id(value: Any, path: str, errors: list[ContractError]) -> None:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        errors.append(ContractError("invalid_id", path, "must match ^[a-z0-9-]+$"))


def _strings(value: Any, path: str, errors: list[ContractError], minimum: int = 0) -> None:
    if not isinstance(value, list):
        errors.append(ContractError("type", path, "must be an array"))
        return
    if len(value) < minimum:
        errors.append(ContractError("missing", path, f"must contain at least {minimum} item(s)"))
    for index, item in enumerate(value):
        if not _string(item):
            errors.append(ContractError("invalid_string", _pointer(path, index), "must be a non-empty string"))


def _unique_ids(items: Any, path: str, errors: list[ContractError]) -> None:
    if not isinstance(items, list):
        return
    ids = [item.get("id") for item in items if isinstance(item, dict) and isinstance(item.get("id"), str)]
    if len(ids) != len(set(ids)):
        errors.append(ContractError("duplicate_id", path, "ids must be unique"))


def _check_ids(root: Path, checks: Any, errors: list[ContractError]) -> None:
    registry = root / "config" / "agent-checks.yaml"
    try:
        loaded = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
        check_definitions = loaded.get("checks") if isinstance(loaded, dict) else None
        known = set(check_definitions.keys()) if isinstance(check_definitions, dict) else set()
        if not isinstance(check_definitions, dict):
            raise ValueError("check registry must contain an object named checks")
    except (OSError, yaml.YAMLError) as exc:
        errors.append(ContractError("check_registry_invalid", "/checks", str(exc)))
        return
    except ValueError as exc:
        errors.append(ContractError("check_registry_invalid", "/checks", str(exc)))
        return
    if isinstance(checks, list):
        for index, check in enumerate(checks):
            if isinstance(check, str) and check not in known:
                errors.append(ContractError("unknown_check", _pointer("/checks", index), f"unknown check: {check}"))
        check_ids = [check for check in checks if isinstance(check, str)]
        if len(check_ids) != len(set(check_ids)):
            errors.append(ContractError("duplicate_value", "/checks", "check IDs must be unique"))


def validate_contract(value: Any, *, root: Path | None = None) -> list[ContractError]:
    errors: list[ContractError] = []
    if not isinstance(value, dict):
        return [ContractError("type", "", "contract must be an object")]
    _keys(value, _TOP_KEYS, "", errors)
    for key in sorted(_TOP_KEYS - set(value)):
        errors.append(ContractError("required", _pointer("", key), "is required"))
    if value.get("version") != 2 or isinstance(value.get("version"), bool):
        errors.append(ContractError("unsupported_version", "/version", "must be integer 2"))
    if not _string(value.get("objective")):
        errors.append(ContractError("required", "/objective", "must be a non-empty string"))

    context = value.get("context")
    _keys(context, {"read"}, "/context", errors)
    if isinstance(context, dict):
        reads = context.get("read")
        _strings(reads, "/context/read", errors)
        if isinstance(reads, list):
            for index, item in enumerate(reads):
                _path_pattern(item, _pointer("/context/read", index), errors)
                if isinstance(item, str) and any(character in item for character in "*?["):
                    errors.append(ContractError("context_glob", _pointer("/context/read", index), "context.read must name one existing file"))
                if root is not None and isinstance(item, str) and not (root / item).is_file():
                    errors.append(ContractError("missing_context", _pointer("/context/read", index), "file does not exist"))

    scope = value.get("scope")
    _keys(scope, {"include", "exclude"}, "/scope", errors)
    if isinstance(scope, dict):
        include, exclude = scope.get("include"), scope.get("exclude")
        _strings(include, "/scope/include", errors, minimum=1)
        _strings(exclude, "/scope/exclude", errors)
        if isinstance(include, list):
            for index, item in enumerate(include):
                _path_pattern(item, _pointer("/scope/include", index), errors)
        if isinstance(exclude, list):
            for index, item in enumerate(exclude):
                _path_pattern(item, _pointer("/scope/exclude", index), errors)
        if isinstance(include, list) and isinstance(exclude, list):
            overlap = set(include) & set(exclude)
            if overlap:
                errors.append(ContractError("scope_overlap", "/scope", f"include and exclude overlap: {sorted(overlap)}"))

    requirements = value.get("requirements")
    if not isinstance(requirements, list) or len(requirements) < 1:
        errors.append(ContractError("missing", "/requirements", "must contain at least one item"))
    elif isinstance(requirements, list):
        for index, item in enumerate(requirements):
            path = _pointer("/requirements", index)
            _keys(item, {"id", "text"}, path, errors)
            if isinstance(item, dict):
                _id(item.get("id"), _pointer(path, "id"), errors)
                if not _string(item.get("text")):
                    errors.append(ContractError("required", _pointer(path, "text"), "must be a non-empty string"))
        _unique_ids(requirements, "/requirements", errors)

    acceptance = value.get("acceptance")
    if not isinstance(acceptance, list) or len(acceptance) < 1:
        errors.append(ContractError("missing", "/acceptance", "must contain at least one item"))
    elif isinstance(acceptance, list):
        for index, item in enumerate(acceptance):
            path = _pointer("/acceptance", index)
            _keys(item, {"id", "criterion", "evidence"}, path, errors)
            if isinstance(item, dict):
                _id(item.get("id"), _pointer(path, "id"), errors)
                for key in ("criterion", "evidence"):
                    if not _string(item.get(key)):
                        errors.append(ContractError("required", _pointer(path, key), "must be a non-empty string"))
        _unique_ids(acceptance, "/acceptance", errors)

    checks = value.get("checks")
    _strings(checks, "/checks", errors, minimum=1)
    if isinstance(checks, list):
        for index, item in enumerate(checks):
            _id(item, _pointer("/checks", index), errors)
    if root is not None:
        _check_ids(root, checks, errors)

    constraints = value.get("constraints")
    _keys(constraints, {"network", "external_writes"}, "/constraints", errors)
    if isinstance(constraints, dict):
        if constraints.get("network") not in {"forbidden", "read-only", "allowed"}:
            errors.append(ContractError("invalid_value", "/constraints/network", "must be forbidden, read-only, or allowed"))
        if constraints.get("external_writes") not in {"forbidden", "explicit-only"}:
            errors.append(ContractError("invalid_value", "/constraints/external_writes", "must be forbidden or explicit-only"))

    depends = value.get("depends_on")
    if not isinstance(depends, list):
        errors.append(ContractError("type", "/depends_on", "must be an array"))
    elif any(not isinstance(item, int) or isinstance(item, bool) or item < 1 for item in depends):
        errors.append(ContractError("invalid_value", "/depends_on", "must contain positive integers"))
    elif len(depends) != len(set(depends)):
        errors.append(ContractError("duplicate_value", "/depends_on", "must not contain duplicates"))

    _strings(value.get("non_goals"), "/non_goals", errors, minimum=1)
    return errors


def _extract(text: str) -> dict[str, Any]:
    matches = list(_FENCE.finditer(text))
    if len(matches) != 1:
        if not matches and "<!-- agent-task:v1 -->" in text:
            code = "unsupported_version"
        else:
            code = "missing_marker" if not matches else "multiple_contracts"
        raise ContractInvalid([ContractError(code, "", "exactly one v2 contract marker and YAML fence is required")])
    try:
        value = yaml.safe_load(matches[0].group("body"))
    except yaml.YAMLError as exc:
        raise ContractInvalid([ContractError("invalid_yaml", "", str(exc))]) from exc
    return value


def parse_contract(text: str, *, root: Path | None = None) -> dict[str, Any]:
    value = _extract(text)
    errors = validate_contract(value, root=root)
    if errors:
        raise ContractInvalid(errors)
    return normalize(value)


def load_contract(path: Path, *, root: Path | None = None) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ContractInvalid([ContractError("input_error", "", str(exc))]) from exc
    return parse_contract(text, root=root or ROOT)


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def normalized_json(value: dict[str, Any]) -> str:
    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _read_input(args: argparse.Namespace) -> str:
    if bool(args.file) == bool(args.stdin):
        raise ValueError("exactly one of --file or --stdin is required")
    if args.stdin:
        return sys.stdin.read()
    return Path(args.file).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent_task")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "extract"):
        command = sub.add_parser(name)
        command.add_argument("--file")
        command.add_argument("--stdin", action="store_true")
        command.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        text = _read_input(args)
        value = parse_contract(text, root=ROOT)
    except ContractInvalid as exc:
        payload = {"schema_version": 2, "ok": False, "errors": [error.as_dict() for error in exc.errors], "task": None}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            for error in exc.errors:
                print(f"{error.code} {error.path}: {error.message}", file=sys.stderr)
        return 2 if any(error.code == "invalid_yaml" for error in exc.errors) else 1
    except (OSError, UnicodeError, ValueError) as exc:
        payload = {"schema_version": 2, "ok": False, "errors": [{"code": "input_error", "path": "", "message": str(exc)}], "task": None}
        if getattr(args, "json", False):
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(str(exc), file=sys.stderr)
        return 2
    if args.command == "validate":
        payload = {"schema_version": 2, "ok": True, "errors": [], "task": value}
    else:
        payload = {"schema_version": 2, "task": value}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
