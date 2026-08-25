"""Stable data types and state transitions for harness runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class RunState(StrEnum):
    DISCOVERED = "discovered"
    CLAIMED = "claimed"
    PREPARING = "preparing"
    RUNNING = "running"
    VERIFYING = "verifying"
    RETRY_WAIT = "retry_wait"
    DELIVERING = "delivering"
    SUCCEEDED = "succeeded"
    BLOCKED = "blocked"
    FAILED = "failed"
    CANCELLED = "cancelled"


TERMINAL_STATES = frozenset({RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED})


def _non_terminal_targets(*states: RunState) -> frozenset[RunState]:
    return frozenset({*states, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED})


ALLOWED_TRANSITIONS: dict[RunState, frozenset[RunState]] = {
    RunState.DISCOVERED: _non_terminal_targets(RunState.CLAIMED),
    RunState.CLAIMED: _non_terminal_targets(RunState.PREPARING),
    RunState.PREPARING: _non_terminal_targets(RunState.RUNNING),
    RunState.RUNNING: _non_terminal_targets(RunState.VERIFYING, RunState.RETRY_WAIT),
    RunState.VERIFYING: _non_terminal_targets(RunState.DELIVERING, RunState.RETRY_WAIT),
    RunState.RETRY_WAIT: _non_terminal_targets(RunState.RUNNING, RunState.PREPARING),
    RunState.DELIVERING: _non_terminal_targets(RunState.SUCCEEDED),
    RunState.SUCCEEDED: frozenset(),
    RunState.BLOCKED: frozenset(),
    RunState.FAILED: frozenset(),
    RunState.CANCELLED: frozenset(),
}


@dataclass(frozen=True)
class Run:
    run_id: str
    repository: str
    issue_number: int
    contract_hash: str
    base_sha: str
    branch: str
    worktree: str
    backend: str
    state: RunState
    attempt: int
    heartbeat_at: str | None
    lease_expires_at: str | None
    reason_code: str | None
    reason_detail: str | None
    pr_number: int | None
    cancel_requested: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: Any) -> "Run":
        return cls(
            run_id=row["run_id"],
            repository=row["repository"],
            issue_number=row["issue_number"],
            contract_hash=row["contract_hash"],
            base_sha=row["base_sha"],
            branch=row["branch"],
            worktree=row["worktree"],
            backend=row["backend"],
            state=RunState(row["state"]),
            attempt=row["attempt"],
            heartbeat_at=row["heartbeat_at"],
            lease_expires_at=row["lease_expires_at"],
            reason_code=row["reason_code"],
            reason_detail=row["reason_detail"],
            pr_number=row["pr_number"],
            cancel_requested=bool(row["cancel_requested"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "repository": self.repository,
            "issue_number": self.issue_number,
            "contract_hash": self.contract_hash,
            "base_sha": self.base_sha,
            "branch": self.branch,
            "worktree": self.worktree,
            "backend": self.backend,
            "state": self.state.value,
            "attempt": self.attempt,
            "heartbeat_at": self.heartbeat_at,
            "lease_expires_at": self.lease_expires_at,
            "reason_code": self.reason_code,
            "reason_detail": self.reason_detail,
            "pr_number": self.pr_number,
            "cancel_requested": self.cancel_requested,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class RunStoreError(RuntimeError):
    """Base class for durable state errors."""


class RunNotFoundError(RunStoreError):
    """The requested run does not exist."""


class InvalidTransitionError(RunStoreError):
    """A requested state transition is not legal."""


class ActiveRunExistsError(RunStoreError):
    """Another non-terminal run already owns the repository/Issue pair."""


class StateConflictError(RunStoreError):
    """The caller supplied an obsolete expected state."""
