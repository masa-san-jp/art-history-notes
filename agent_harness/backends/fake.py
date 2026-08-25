"""Deterministic backend for local and CI harness tests."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Callable

from .base import BackendCapabilities, BackendRequest, BackendResult


@dataclass
class FakeHandle:
    request: BackendRequest
    result: BackendResult | None = None


class FakeBackend:
    def __init__(self, behavior: Callable[[BackendRequest], dict[str, Any]] | None = None) -> None:
        self.behavior = behavior or self._success
        self.started = 0

    @staticmethod
    def _success(request: BackendRequest) -> dict[str, Any]:
        return {"status": "completed", "summary": "fake backend completed", "changed_paths": [], "checks_run": [], "remaining_risks": [], "blockers": []}

    def probe(self) -> BackendCapabilities:
        return BackendCapabilities(name="fake", version="1", structured_events=True, continuation=True, usage=False)

    def start(self, request: BackendRequest) -> FakeHandle:
        self.started += 1
        request.prompt_file.parent.mkdir(parents=True, exist_ok=True)
        request.prompt_file.write_text(request.prompt, encoding="utf-8")
        return FakeHandle(request)

    def wait(self, handle: FakeHandle) -> BackendResult:
        request = handle.request
        value = dict(self.behavior(request))
        status = value.pop("status", "completed")
        value = {"version": 1, "status": status, **value}
        request.handoff_file.parent.mkdir(parents=True, exist_ok=True)
        request.handoff_file.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        result = BackendResult(status, 0 if status == "completed" else 1, "fake backend", "", handoff=value)
        handle.result = result
        return result

    def cancel(self, handle: FakeHandle) -> None:
        handle.request.cancel_event and handle.request.cancel_event.set()
