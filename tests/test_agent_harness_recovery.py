from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from agent_harness.models import RunState
from agent_harness.recovery import recover_stale_runs, stale_runs
from agent_harness.store import RunStore


class RecoveryTests(unittest.TestCase):
    def test_stale_run_is_recovered_with_same_id_and_event(self) -> None:
        directory = tempfile.TemporaryDirectory()
        store = RunStore(Path(directory.name) / "state.sqlite3")
        run = store.create_run(repository="local/repo", issue_number=1, contract_hash="a" * 64, base_sha="b" * 40, branch="agent/1/run", worktree=".agent-harness/worktrees/run", backend="fake")
        store.transition(run.run_id, RunState.CLAIMED)
        store.heartbeat(run.run_id, lease_expires_at="2020-01-01T00:00:00Z")
        now = datetime.now(timezone.utc)
        self.assertEqual(stale_runs(store, now=now, stale_after_seconds=0)[0].run_id, run.run_id)
        recovered = recover_stale_runs(store, now=now, stale_after_seconds=0)[0]
        self.assertEqual(recovered.run_id, run.run_id)
        self.assertEqual(recovered.state, RunState.PREPARING)
        self.assertEqual(store.events(run.run_id)[-1]["event_type"], "run.crash_recovered")
        directory.cleanup()
