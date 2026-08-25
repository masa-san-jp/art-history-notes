"""Configured argv-template backend."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import threading
from typing import Any

from ..handoff import HandoffError, load_handoff
from ..policy import ExecutionPolicy, Redactor, collect_allowed_environment
from ..process_runner import ProcessResult, run_argv
from .base import AgentBackend, BackendCapabilities, BackendRequest, BackendResult


_PLACEHOLDERS = {"worktree", "prompt_file", "events_file", "handoff_file", "attempt", "run_id"}
_PLACEHOLDER_PATTERN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


@dataclass
class CommandHandle:
    request: BackendRequest
    result: ProcessResult | None = None


class CommandBackend:
    def __init__(self, argv_template: list[str], *, policy: ExecutionPolicy | None = None, env_names: set[str] | None = None, secrets: list[str] | None = None) -> None:
        self.argv_template = tuple(argv_template)
        self.policy = policy or ExecutionPolicy()
        self.env_names = env_names or set()
        self.redactor = Redactor(secrets or self.policy.secrets)
        if not self.argv_template:
            raise ValueError("backend argv template must not be empty")

    def probe(self) -> BackendCapabilities:
        return BackendCapabilities(name="command", version=os.path.basename(self.argv_template[0]), structured_events=True, continuation=False, usage=False)

    def _argv(self, request: BackendRequest) -> list[str]:
        values = {
            "worktree": str(request.worktree),
            "prompt_file": str(request.prompt_file),
            "events_file": str(request.events_file),
            "handoff_file": str(request.handoff_file),
            "attempt": str(request.attempt),
            "run_id": request.run_id,
        }
        result: list[str] = []
        for part in self.argv_template:
            formatted = part
            for key, value in values.items():
                formatted = formatted.replace("{" + key + "}", value)
            unknown = [match.group(1) for match in _PLACEHOLDER_PATTERN.finditer(formatted) if match.group(1) not in _PLACEHOLDERS]
            if unknown:
                raise ValueError(f"unknown backend placeholder in {part!r}: {unknown[0]}")
            result.append(formatted)
        return result

    def start(self, request: BackendRequest) -> CommandHandle:
        request.prompt_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = request.prompt_file.with_suffix(request.prompt_file.suffix + ".tmp")
        temporary.write_text(request.prompt, encoding="utf-8")
        temporary.replace(request.prompt_file)
        return CommandHandle(request)

    def wait(self, handle: CommandHandle) -> BackendResult:
        request = handle.request
        environment = collect_allowed_environment(os.environ, self.env_names)
        result = run_argv(
            self._argv(request),
            cwd=request.worktree,
            timeout_seconds=request.timeout_seconds,
            max_output_bytes=request.max_output_bytes,
            policy=self.policy,
            env=environment,
            redactor=self.redactor,
            cancel_event=request.cancel_event,
        )
        handle.result = result
        handoff = None
        if request.handoff_file.exists():
            try:
                handoff = load_handoff(request.handoff_file)
            except HandoffError:
                handoff = None
        status = "completed" if result.returncode == 0 and not result.timed_out and not result.cancelled and not result.output_limited and handoff else "failed"
        if result.cancelled:
            status = "cancelled"
        elif result.timed_out:
            status = "timeout"
        elif result.output_limited:
            status = "output_limit"
        return BackendResult(status, result.returncode, result.stdout.decode("utf-8", errors="replace"), result.stderr.decode("utf-8", errors="replace"), result.timed_out, result.cancelled, result.output_limited, handoff)

    def cancel(self, handle: CommandHandle) -> None:
        if handle.request.cancel_event is not None:
            handle.request.cancel_event.set()
