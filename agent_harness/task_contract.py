"""Parsing and validation for the machine-readable agent-task contract.

The contract is intentionally validated without a third-party JSON Schema
runtime.  The checked-in JSON Schema is the documentation/interoperability
artifact; this module is the runtime validator used by the CLI.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml


MARKER = "<!-- agent-task:v1 -->"
_FENCE = re.compile(re.escape(MARKER) + r"\s*```yaml\s*\n(?P<body>.*?)\n```", re.DOTALL)
_ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")
_DANGEROUS_PATH_PARTS = {"", ".", ".."}
_CONTRACT_KEYS = {
    "version",
    "objective",
    "deliverables",
    "scope",
    "non_goals",
    "dependencies",
    "checks",
    "permissions",
    "limits",
    "risk",
    "completion",
}
_SCOPE_KEYS = {"include", "exclude"}
_DELIVERABLE_KEYS = {"path", "expected"}
_CHECK_KEYS = {"argv", "timeout_seconds"}
_PERMISSION_KEYS = {"network", "external_write", "allowed_env"}
_LIMIT_KEYS = {"timeout_minutes", "max_attempts", "max_output_bytes"}


@dataclass(frozen=True)
class ContractError:
    """One machine-readable contract validation error."""

    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"path": self.path, "message": self.message}


class ContractValidationError(ValueError):
    """Raised when an Issue does not contain a valid task contract."""

    def __init__(self, errors: list[ContractError]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(f"{e.path}: {e.message}" for e in errors))


def _pointer(path: str, key: str | int) -> str:
    escaped = str(key).replace("~", "~0").replace("/", "~1")
    return f"{path}/{escaped}" if path else f"/{escaped}"


def _is_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_keys(value: Any, allowed: set[str], path: str, errors: list[ContractError]) -> None:
    if not isinstance(value, dict):
        errors.append(ContractError(path, "must be an object"))
        return
    for key in value:
        if key not in allowed:
            errors.append(ContractError(_pointer(path, key), "unknown key"))


def _validate_relative_pattern(value: Any, path: str, errors: list[ContractError]) -> None:
    if not _is_string(value):
        errors.append(ContractError(path, "must be a non-empty string"))
        return
    if "\x00" in value or "\\" in value or value.startswith("/"):
        errors.append(ContractError(path, "must be a relative POSIX path pattern"))
        return
    parts = value.split("/")
    if any(part in _DANGEROUS_PATH_PARTS for part in parts):
        errors.append(ContractError(path, "must not contain empty, '.' or '..' path components"))


def _validate_repo_path(value: Any, path: str, errors: list[ContractError]) -> None:
    _validate_relative_pattern(value, path, errors)
    if isinstance(value, str):
        try:
            resolved = PurePosixPath(value)
            if resolved.is_absolute() or ".." in resolved.parts:
                errors.append(ContractError(path, "must stay inside the repository"))
        except Exception:
            errors.append(ContractError(path, "must be a valid POSIX path"))


def _validate_string_list(value: Any, path: str, errors: list[ContractError], *, min_items: int = 0) -> None:
    if not isinstance(value, list):
        errors.append(ContractError(path, "must be an array"))
        return
    if len(value) < min_items:
        errors.append(ContractError(path, f"must contain at least {min_items} item(s)"))
    for index, item in enumerate(value):
        if not _is_string(item):
            errors.append(ContractError(_pointer(path, index), "must be a non-empty string"))


def _validate_contract(value: Any) -> list[ContractError]:
    errors: list[ContractError] = []
    if not isinstance(value, dict):
        return [ContractError("", "contract must be an object")]

    _validate_keys(value, _CONTRACT_KEYS, "", errors)
    required = {
        "version",
        "objective",
        "deliverables",
        "scope",
        "non_goals",
        "checks",
        "permissions",
        "limits",
        "risk",
        "completion",
    }
    for key in sorted(required - value.keys()):
        errors.append(ContractError(_pointer("", key), "is required"))

    if value.get("version") != 1 or isinstance(value.get("version"), bool):
        errors.append(ContractError("/version", "must be integer 1"))
    if not _is_string(value.get("objective")):
        errors.append(ContractError("/objective", "must be a non-empty string"))

    deliverables = value.get("deliverables")
    if not isinstance(deliverables, list):
        errors.append(ContractError("/deliverables", "must be an array"))
    else:
        if not deliverables:
            errors.append(ContractError("/deliverables", "must contain at least one item"))
        for index, item in enumerate(deliverables):
            item_path = _pointer("/deliverables", index)
            _validate_keys(item, _DELIVERABLE_KEYS, item_path, errors)
            if not isinstance(item, dict) or "path" not in item or "expected" not in item:
                errors.append(ContractError(item_path, "requires path and expected"))
                continue
            _validate_repo_path(item["path"], _pointer(item_path, "path"), errors)
            if not _is_string(item["expected"]):
                errors.append(ContractError(_pointer(item_path, "expected"), "must be a non-empty string"))

    scope = value.get("scope")
    _validate_keys(scope, _SCOPE_KEYS, "/scope", errors)
    if isinstance(scope, dict):
        include = scope.get("include")
        exclude = scope.get("exclude", [])
        _validate_string_list(include, "/scope/include", errors, min_items=1)
        if isinstance(include, list):
            for index, item in enumerate(include):
                _validate_relative_pattern(item, _pointer("/scope/include", index), errors)
        _validate_string_list(exclude, "/scope/exclude", errors)
        if isinstance(exclude, list):
            for index, item in enumerate(exclude):
                _validate_relative_pattern(item, _pointer("/scope/exclude", index), errors)

    _validate_string_list(value.get("non_goals"), "/non_goals", errors)

    dependencies = value.get("dependencies", [])
    if not isinstance(dependencies, list):
        errors.append(ContractError("/dependencies", "must be an array"))
    else:
        if any(dependencies[left] == dependencies[right] for left in range(len(dependencies)) for right in range(left)):
            errors.append(ContractError("/dependencies", "must not contain duplicates"))
        for index, item in enumerate(dependencies):
            if not isinstance(item, int) or isinstance(item, bool) or item <= 0:
                errors.append(ContractError(_pointer("/dependencies", index), "must be a positive integer"))

    checks = value.get("checks")
    if not isinstance(checks, list):
        errors.append(ContractError("/checks", "must be an array"))
    else:
        if not checks:
            errors.append(ContractError("/checks", "must contain at least one item"))
        for index, item in enumerate(checks):
            item_path = _pointer("/checks", index)
            _validate_keys(item, _CHECK_KEYS, item_path, errors)
            if not isinstance(item, dict):
                continue
            argv = item.get("argv")
            if not isinstance(argv, list) or not argv or any(not isinstance(part, str) or not part for part in argv):
                errors.append(ContractError(_pointer(item_path, "argv"), "must be a non-empty string array"))
            elif any("\x00" in part for part in argv):
                errors.append(ContractError(_pointer(item_path, "argv"), "must not contain NUL"))
            timeout = item.get("timeout_seconds")
            if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 7200:
                errors.append(ContractError(_pointer(item_path, "timeout_seconds"), "must be an integer from 1 to 7200"))

    permissions = value.get("permissions")
    _validate_keys(permissions, _PERMISSION_KEYS, "/permissions", errors)
    if isinstance(permissions, dict):
        if permissions.get("network") not in {"none", "read", "write"}:
            errors.append(ContractError("/permissions/network", "must be none, read, or write"))
        if not isinstance(permissions.get("external_write"), bool):
            errors.append(ContractError("/permissions/external_write", "must be boolean"))
        allowed_env = permissions.get("allowed_env", [])
        _validate_string_list(allowed_env, "/permissions/allowed_env", errors)
        if isinstance(allowed_env, list):
            for index, item in enumerate(allowed_env):
                if isinstance(item, str) and not _ENV_NAME.fullmatch(item):
                    errors.append(ContractError(_pointer("/permissions/allowed_env", index), "must be an uppercase environment variable name"))

    limits = value.get("limits")
    _validate_keys(limits, _LIMIT_KEYS, "/limits", errors)
    if isinstance(limits, dict):
        ranges = {
            "timeout_minutes": (1, 240),
            "max_attempts": (1, 5),
            "max_output_bytes": (1024, 104857600),
        }
        for key, (minimum, maximum) in ranges.items():
            number = limits.get(key)
            if not isinstance(number, int) or isinstance(number, bool) or not minimum <= number <= maximum:
                errors.append(ContractError(_pointer("/limits", key), f"must be an integer from {minimum} to {maximum}"))

    if value.get("risk") not in {"low", "medium", "high"}:
        errors.append(ContractError("/risk", "must be low, medium, or high"))
    _validate_string_list(value.get("completion"), "/completion", errors, min_items=1)
    return errors


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def parse_contract(text: str) -> dict[str, Any]:
    """Extract, validate, and normalize the marker contract from Issue text."""

    match = _FENCE.search(text)
    if not match:
        raise ContractValidationError([ContractError("", f"missing {MARKER} followed by a yaml fence")])
    try:
        value = yaml.safe_load(match.group("body"))
    except yaml.YAMLError as exc:
        raise ContractValidationError([ContractError("", f"invalid YAML: {exc}")]) from exc
    errors = _validate_contract(value)
    if errors:
        raise ContractValidationError(errors)
    return _normalize(_with_defaults(value))


def _with_defaults(value: dict[str, Any]) -> dict[str, Any]:
    """Apply only defaults explicitly defined by contract v1."""

    result = dict(value)
    scope = dict(result["scope"])
    scope.setdefault("exclude", [])
    result["scope"] = scope
    result.setdefault("dependencies", [])
    permissions = dict(result["permissions"])
    permissions.setdefault("allowed_env", [])
    result["permissions"] = permissions
    return result


def normalized_json(contract: dict[str, Any]) -> str:
    """Return the stable JSON representation used for hashing and output."""

    return json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_contract(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractValidationError([ContractError("", f"cannot read file: {exc}")]) from exc
    return parse_contract(text)
