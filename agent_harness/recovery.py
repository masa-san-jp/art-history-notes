"""Crash recovery inspection for non-terminal runs."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import Run, RunState
from .store import RunStore


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def stale_runs(store: RunStore, *, now: datetime | None = None, stale_after_seconds: int = 900) -> list[Run]:
    current = now or datetime.now(timezone.utc)
    cutoff = current - timedelta(seconds=stale_after_seconds)
    result = []
    for run in store.list_runs():
        if run.state in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
            continue
        heartbeat = run.heartbeat_at or run.updated_at
        if parse_timestamp(heartbeat) < cutoff:
            result.append(run)
    return result


def recover_stale_runs(store: RunStore, *, now: datetime | None = None, stale_after_seconds: int = 900) -> list[Run]:
    recovered = []
    for run in stale_runs(store, now=now, stale_after_seconds=stale_after_seconds):
        recovered.append(store.recover_run(run.run_id, reason="heartbeat expired; process ownership was not live"))
    return recovered
