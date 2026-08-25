"""One-run execution loop joining ledger, backend, verification, and delivery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import threading
from typing import Any

from .backends.base import AgentBackend, BackendRequest
from .context import build_context
from .delivery import DeliveryAdapter, DeliveryError, DeliveryResult
from .failure import FailureCode, retry_allowed
from .models import RunState
from .store import RunStore
from .verifier import VerificationPipeline
from .worktree import WorktreeManager


@dataclass(frozen=True)
class ExecutionOutcome:
    run_id: str
    state: RunState
    attempts: int
    failure_code: FailureCode | None = None
    delivery: DeliveryResult | None = None


class HarnessExecutor:
    def __init__(self, *, store: RunStore, worktrees: WorktreeManager, backend: AgentBackend, verifier: VerificationPipeline, delivery: DeliveryAdapter, repository_root: Path, base_branch: str = "main") -> None:
        self.store = store
        self.worktrees = worktrees
        self.backend = backend
        self.verifier = verifier
        self.delivery = delivery
        self.repository_root = repository_root
        self.base_branch = base_branch

    def execute(self, run_id: str, contract: dict[str, Any]) -> ExecutionOutcome:
        run = self.store.get_run(run_id)
        if run.state == RunState.DISCOVERED:
            run = self.store.transition(run_id, RunState.CLAIMED, expected_state=RunState.DISCOVERED)
        if run.state == RunState.CLAIMED:
            run = self.store.transition(run_id, RunState.PREPARING, expected_state=RunState.CLAIMED)
        if run.state not in {RunState.PREPARING, RunState.RETRY_WAIT}:
            return ExecutionOutcome(run_id, run.state, run.attempt)
        worktree = self.worktrees.create(run_id=run.run_id, branch=run.branch, base_sha=run.base_sha)
        previous_failure: dict[str, Any] | None = None
        max_attempts = contract["limits"]["max_attempts"]
        while True:
            run = self.store.get_run(run_id)
            if run.state == RunState.RETRY_WAIT:
                run = self.store.start_attempt(run_id)
            else:
                run = self.store.start_attempt(run_id)
            cancel_event = threading.Event()
            try:
                context = build_context(root=self.repository_root, contract=contract, run_id=run.run_id, attempt=run.attempt, base_sha=run.base_sha, previous_failure=previous_failure)
                prompt_file = self.repository_root / ".agent-harness" / "runs" / run.run_id / f"attempt-{run.attempt}" / "prompt.txt"
                events_file = prompt_file.with_name("events.jsonl")
                handoff_file = prompt_file.with_name("handoff.json")
                self.store.record_artifact(run.run_id, kind="prompt", path=str(prompt_file), attempt=run.attempt, content=context.text.encode("utf-8"))
                request = BackendRequest(run.run_id, run.attempt, worktree.path, prompt_file, events_file, handoff_file, context.text, contract["limits"]["timeout_minutes"] * 60, contract["limits"]["max_output_bytes"], cancel_event=cancel_event)
                result = self.backend.wait(self.backend.start(request))
                if result.status != "completed" or result.handoff is None:
                    code = FailureCode.CANCELLED if result.cancelled else FailureCode.TIMEOUT if result.timed_out else FailureCode.OUTPUT_LIMIT if result.output_limited else FailureCode.BACKEND_FAILED
                    previous_failure = {"code": code.value, "diagnostic": result.stderr[-4096:]}
                    self.store.finish_attempt(run_id, failure_code=code.value, failure_detail=previous_failure["diagnostic"])
                    if self._retry_or_finish(run_id, code, run.attempt, max_attempts):
                        continue
                    return ExecutionOutcome(run_id, self.store.get_run(run_id).state, run.attempt, code)
                self.store.transition(run_id, RunState.VERIFYING, expected_state=RunState.RUNNING)
                verification = self.verifier.verify(worktree=worktree, contract=contract, handoff=result.handoff)
                if not verification.ok:
                    code = verification.failure_code or FailureCode.INTERNAL_ERROR
                    previous_failure = {"code": code.value, "stages": [stage.__dict__ for stage in verification.stages]}
                    self.store.finish_attempt(run_id, failure_code=code.value, failure_detail=str(previous_failure)[-4096:])
                    if self._retry_or_finish(run_id, code, run.attempt, max_attempts):
                        continue
                    return ExecutionOutcome(run_id, self.store.get_run(run_id).state, run.attempt, code)
                self.store.finish_attempt(run_id)
                self.store.transition(run_id, RunState.DELIVERING, expected_state=RunState.VERIFYING)
                try:
                    delivery = self.delivery.deliver(self.store.get_run(run_id), objective=contract["objective"], manifest=list(verification.manifest), worktree=worktree.path, base_branch=self.base_branch)
                    if delivery.pr_number is not None:
                        self.store.set_pr_number(run_id, delivery.pr_number)
                except DeliveryError as exc:
                    code = FailureCode.GITHUB_TRANSIENT
                    previous_failure = {"code": code.value, "diagnostic": str(exc)}
                    if self._retry_or_finish(run_id, code, run.attempt, max_attempts, current_state=RunState.DELIVERING):
                        continue
                    return ExecutionOutcome(run_id, self.store.get_run(run_id).state, run.attempt, code)
                terminal = RunState.SUCCEEDED if delivery.status in {"done", "review"} else RunState.BLOCKED
                self.store.transition(run_id, terminal, expected_state=RunState.DELIVERING, reason_code="completed" if terminal == RunState.SUCCEEDED else "delivery_blocked")
                return ExecutionOutcome(run_id, terminal, run.attempt, delivery=delivery)
            finally:
                cancel_event.set() if self.store.get_run(run_id).cancel_requested else None

    def _retry_or_finish(self, run_id: str, code: FailureCode, attempt: int, max_attempts: int, *, current_state: RunState | None = None) -> bool:
        state = current_state or self.store.get_run(run_id).state
        if retry_allowed(code, attempt=attempt, max_attempts=max_attempts):
            self.store.transition(run_id, RunState.RETRY_WAIT, expected_state=state, reason_code=code.value)
            return True
        terminal = RunState.BLOCKED if code in {FailureCode.POLICY_VIOLATION, FailureCode.TASK_INVALID, FailureCode.SECRET_DETECTED, FailureCode.LEASE_LOST, FailureCode.CANCELLED} else RunState.FAILED
        self.store.transition(run_id, terminal, expected_state=state, reason_code=code.value)
        return False
