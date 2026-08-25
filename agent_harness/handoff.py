"""Validation for the structured result an agent leaves behind."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class HandoffError(ValueError):
    """The backend handoff is absent, malformed, or incomplete."""


REQUIRED = {"version", "status", "summary", "changed_paths", "checks_run", "remaining_risks", "blockers"}
STATUSES = {"completed", "blocked", "failed"}


def validate_handoff(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise HandoffError("handoff must be an object")
    missing = sorted(REQUIRED - value.keys())
    if missing:
        raise HandoffError("handoff missing: " + ", ".join(missing))
    if value["version"] != 1 or isinstance(value["version"], bool):
        raise HandoffError("handoff version must be integer 1")
    if value["status"] not in STATUSES:
        raise HandoffError("handoff status is invalid")
    if not isinstance(value["summary"], str) or not value["summary"].strip():
        raise HandoffError("handoff summary must be non-empty")
    for key in ("changed_paths", "checks_run", "remaining_risks", "blockers"):
        if not isinstance(value[key], list) or any(not isinstance(item, (str, dict)) for item in value[key]):
            raise HandoffError(f"handoff {key} must be an array of strings or objects")
    unknown = set(value) - REQUIRED
    if unknown:
        raise HandoffError("handoff unknown keys: " + ", ".join(sorted(unknown)))
    return {key: value[key] for key in sorted(value)}


def load_handoff(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HandoffError(f"cannot read handoff: {exc}") from exc
    return validate_handoff(value)
