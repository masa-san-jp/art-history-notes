from __future__ import annotations

from pathlib import Path
import tempfile
import threading
import unittest

from agent_harness.models import ActiveRunExistsError, InvalidTransitionError, RunState
from agent_harness.store import RunStore


class RunStoreTests(unittest.TestCase):
    def make_store(self) -> RunStore:
        self.tempdir = tempfile.TemporaryDirectory()
        return RunStore(Path(self.tempdir.name) / ".agent-harness" / "state.sqlite3")

    def tearDown(self) -> None:
        if hasattr(self, "tempdir"):
            self.tempdir.cleanup()

    def make_run(self, store: RunStore, issue: int = 1):
        return store.create_run(
            repository="example/repo",
            issue_number=issue,
            contract_hash="a" * 64,
            base_sha="b" * 40,
            branch=f"agent/issue-{issue}/run",
            worktree=f".agent-harness/worktrees/{issue}",
            backend="fake",
        )

    def test_state_machine_and_append_only_events(self) -> None:
        store = self.make_store()
        run = self.make_run(store)
        run = store.transition(run.run_id, RunState.CLAIMED, expected_state=RunState.DISCOVERED)
        run = store.transition(run.run_id, RunState.PREPARING)
        run = store.start_attempt(run.run_id)
        self.assertEqual(run.attempt, 1)
        run = store.transition(run.run_id, RunState.VERIFYING)
        run = store.transition(run.run_id, RunState.RETRY_WAIT, reason_code="canonical_verify_failed")
        run = store.start_attempt(run.run_id)
        self.assertEqual(run.attempt, 2)
        run = store.transition(run.run_id, RunState.BLOCKED, reason_code="policy_violation", reason_detail="scope")
        self.assertEqual(run.state, RunState.BLOCKED)
        with self.assertRaises(InvalidTransitionError):
            store.transition(run.run_id, RunState.PREPARING)
        events = store.events(run.run_id)
        self.assertEqual(events[0]["event_type"], "run.created")
        self.assertEqual(events[-1]["to_state"], "blocked")

    def test_only_one_active_run_per_issue(self) -> None:
        store = self.make_store()
        self.make_run(store)
        with self.assertRaises(ActiveRunExistsError):
            self.make_run(store)

    def test_concurrent_creation_has_one_winner(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        path = Path(self.tempdir.name) / "state.sqlite3"
        results: list[str] = []
        errors: list[type[Exception]] = []
        barrier = threading.Barrier(2)

        def create() -> None:
            store = RunStore(path)
            barrier.wait()
            try:
                self.make_run(store)
                results.append("won")
            except Exception as exc:  # pragma: no cover - asserted below
                errors.append(type(exc))

        threads = [threading.Thread(target=create) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(results, ["won"])
        self.assertEqual(errors, [ActiveRunExistsError])

    def test_cancel_is_idempotent_and_resume_preserves_run_id(self) -> None:
        store = self.make_store()
        run = self.make_run(store)
        store.transition(run.run_id, RunState.CLAIMED)
        cancelled = store.cancel(run.run_id, "operator request")
        self.assertEqual(cancelled.state, RunState.CANCELLED)
        event_count = len(store.events(run.run_id))
        self.assertEqual(store.cancel(run.run_id, "same request").state, RunState.CANCELLED)
        self.assertEqual(len(store.events(run.run_id)), event_count)

        blocked = self.make_run(store, issue=2)
        blocked = store.transition(blocked.run_id, RunState.BLOCKED, reason_code="invalid")
        resumed = store.resume(blocked.run_id, "fixed the contract")
        self.assertEqual(resumed.run_id, blocked.run_id)
        self.assertEqual(resumed.state, RunState.PREPARING)

    def test_heartbeat_and_artifact_are_persisted(self) -> None:
        store = self.make_store()
        run = self.make_run(store)
        store.transition(run.run_id, RunState.CLAIMED)
        heartbeat = store.heartbeat(run.run_id, lease_expires_at="2099-01-01T00:00:00Z")
        self.assertEqual(heartbeat.lease_expires_at, "2099-01-01T00:00:00Z")
        store.record_artifact(run.run_id, kind="prompt", path="runs/x/prompt.txt", content=b"prompt")
        with store._connection() as connection:
            artifact = connection.execute("SELECT sha256, byte_count FROM artifacts WHERE run_id = ?", (run.run_id,)).fetchone()
        self.assertEqual(artifact["byte_count"], 6)
        self.assertEqual(len(artifact["sha256"]), 64)
