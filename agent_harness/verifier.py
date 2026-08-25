"""Ordered post-agent verification pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import threading
from typing import Any

from .failure import FailureCode
from .handoff import HandoffError, validate_handoff
from .policy import ExecutionPolicy, PolicyViolation, SecretDetector
from .process_runner import ProcessResult, run_argv
from .task_contract import normalized_json
from .worktree import Worktree, WorktreeManager


@dataclass(frozen=True)
class VerificationStage:
    name: str
    ok: bool
    duration_seconds: float
    returncode: int | None = None
    diagnostic: str = ""
    failure_code: FailureCode | None = None


@dataclass(frozen=True)
class VerificationResult:
    ok: bool
    stages: tuple[VerificationStage, ...]
    manifest: tuple[str, ...] = ()
    handoff: dict[str, Any] | None = None

    @property
    def failure_code(self) -> FailureCode | None:
        return next((stage.failure_code for stage in self.stages if stage.failure_code), None)


class VerificationPipeline:
    def __init__(self, *, worktrees: WorktreeManager, policy: ExecutionPolicy | None = None, canonical_argv: list[str] | None = None) -> None:
        self.worktrees = worktrees
        self.policy = policy or ExecutionPolicy()
        self.canonical_argv = canonical_argv or ["uv", "run", "--locked", "python", "tools/verify.py"]

    def verify(
        self,
        *,
        worktree: Worktree,
        contract: dict[str, Any],
        handoff: dict[str, Any] | None,
        run_canonical: bool = True,
        cancel_event: threading.Event | None = None,
    ) -> VerificationResult:
        stages: list[VerificationStage] = []
        if handoff is None:
            stages.append(VerificationStage("handoff", False, 0.0, diagnostic="missing or malformed handoff", failure_code=FailureCode.BACKEND_FAILED))
            return VerificationResult(False, tuple(stages))
        try:
            normalized_handoff = validate_handoff(handoff)
        except HandoffError as exc:
            stages.append(VerificationStage("handoff", False, 0.0, diagnostic=str(exc), failure_code=FailureCode.BACKEND_FAILED))
            return VerificationResult(False, tuple(stages))
        if normalized_handoff["status"] != "completed":
            stages.append(VerificationStage("handoff", False, 0.0, diagnostic=f"backend handoff status is {normalized_handoff['status']}", failure_code=FailureCode.BACKEND_FAILED))
            return VerificationResult(False, tuple(stages), handoff=normalized_handoff)
        stages.append(VerificationStage("handoff", True, 0.0))

        try:
            manifest = self.worktrees.manifest(worktree, include=contract["scope"]["include"], exclude=contract["scope"].get("exclude", []))
        except PolicyViolation as exc:
            stages.append(VerificationStage("scope", False, 0.0, diagnostic=str(exc), failure_code=FailureCode.POLICY_VIOLATION))
            return VerificationResult(False, tuple(stages), handoff=normalized_handoff)
        stages.append(VerificationStage("scope", True, 0.0))

        secret = self._scan_secrets(worktree, manifest)
        if secret is not None:
            stages.append(VerificationStage("secret_scan", False, 0.0, diagnostic=secret, failure_code=FailureCode.SECRET_DETECTED))
            return VerificationResult(False, tuple(stages), tuple(manifest), normalized_handoff)
        stages.append(VerificationStage("secret_scan", True, 0.0))

        for index, check in enumerate(contract["checks"]):
            result = run_argv(check["argv"], cwd=worktree.path, timeout_seconds=check["timeout_seconds"], max_output_bytes=contract["limits"]["max_output_bytes"], policy=self.policy, cancel_event=cancel_event)
            stage = self._process_stage(f"task_check_{index}", result, FailureCode.TASK_CHECK_FAILED)
            stages.append(stage)
            if not stage.ok:
                return VerificationResult(False, tuple(stages), tuple(manifest), normalized_handoff)

        if run_canonical:
            result = run_argv(
                self.canonical_argv,
                cwd=worktree.path,
                timeout_seconds=contract["limits"]["timeout_minutes"] * 60,
                max_output_bytes=contract["limits"]["max_output_bytes"],
                policy=self.policy,
                cancel_event=cancel_event,
            )
            stage = self._process_stage("canonical_verify", result, FailureCode.CANONICAL_VERIFY_FAILED)
            stages.append(stage)
            if not stage.ok:
                return VerificationResult(False, tuple(stages), tuple(manifest), normalized_handoff)
        stages.append(VerificationStage("final_manifest", True, 0.0, diagnostic=normalized_json({"paths": manifest})))
        return VerificationResult(True, tuple(stages), tuple(manifest), normalized_handoff)

    def _scan_secrets(self, worktree: Worktree, manifest: list[str]) -> str | None:
        detector = SecretDetector(self.policy.secrets)
        for relative in manifest:
            path = worktree.path / relative
            if not path.is_file() or path.is_symlink():
                continue
            try:
                with path.open("rb") as handle:
                    carry = ""
                    while chunk := handle.read(64 * 1024):
                        text = carry + chunk.decode("utf-8", errors="replace")
                        finding = detector.finding(text)
                        if finding:
                            return f"{finding} in {relative}"
                        carry = text[-256:]
            except OSError as exc:
                return f"secret scan could not read {relative}: {exc.__class__.__name__}"
        return None

    @staticmethod
    def _process_stage(name: str, result: ProcessResult, failure: FailureCode) -> VerificationStage:
        diagnostic = (result.stderr or result.stdout).decode("utf-8", errors="replace")[-8192:]
        if result.cancelled:
            return VerificationStage(name, False, result.duration_seconds, result.returncode, diagnostic, FailureCode.CANCELLED)
        if result.timed_out:
            return VerificationStage(name, False, result.duration_seconds, result.returncode, diagnostic, FailureCode.TIMEOUT)
        if result.output_limited:
            return VerificationStage(name, False, result.duration_seconds, result.returncode, diagnostic, FailureCode.OUTPUT_LIMIT)
        return VerificationStage(name, result.returncode == 0, result.duration_seconds, result.returncode, diagnostic, None if result.returncode == 0 else failure)
