"""Vendor-neutral backend protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import threading
from typing import Any, Protocol


@dataclass(frozen=True)
class BackendCapabilities:
    name: str
    version: str
    structured_events: bool
    continuation: bool
    usage: bool


@dataclass(frozen=True)
class BackendRequest:
    run_id: str
    attempt: int
    worktree: Path
    prompt_file: Path
    events_file: Path
    handoff_file: Path
    prompt: str
    timeout_seconds: int
    max_output_bytes: int
    env: dict[str, str] = field(default_factory=dict)
    cancel_event: threading.Event | None = None


@dataclass(frozen=True)
class BackendResult:
    status: str
    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool = False
    cancelled: bool = False
    output_limited: bool = False
    handoff: dict[str, Any] | None = None


class AgentBackend(Protocol):
    def probe(self) -> BackendCapabilities: ...

    def start(self, request: BackendRequest) -> Any: ...

    def wait(self, handle: Any) -> BackendResult: ...

    def cancel(self, handle: Any) -> None: ...
