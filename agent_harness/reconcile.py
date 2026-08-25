"""Idempotent external-state projection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .models import Run, RunState


class ProjectionClient(Protocol):
    def sync_issue(self, number: int, *, status: str, pr: dict[str, Any] | None, message: str) -> None: ...


@dataclass(frozen=True)
class Projection:
    status: str
    message: str
    pr: dict[str, Any] | None = None


def projection_for(run: Run) -> Projection:
    if run.state == RunState.SUCCEEDED:
        return Projection("done", f"Run {run.run_id} completed and was verified.")
    if run.state == RunState.DELIVERING:
        return Projection("review", f"Run {run.run_id} is reconciling delivery.", {"number": run.pr_number} if run.pr_number else None)
    if run.state in {RunState.BLOCKED, RunState.FAILED}:
        return Projection("blocked", f"Run {run.run_id} is {run.state.value}: {run.reason_code or 'unknown reason'}.")
    return Projection("running", f"Run {run.run_id} is {run.state.value}.")


def reconcile_issue(client: ProjectionClient, run: Run) -> Projection:
    projection = projection_for(run)
    client.sync_issue(run.issue_number, status=projection.status, pr=projection.pr, message=projection.message)
    return projection
