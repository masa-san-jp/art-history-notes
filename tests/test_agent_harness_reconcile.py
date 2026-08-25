from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from agent_harness.models import RunState
from agent_harness.reconcile import reconcile_issue
from agent_harness.store import RunStore


class FakeProjectionClient:
    def __init__(self) -> None:
        self.calls = []

    def sync_issue(self, number, *, status, pr, message):
        self.calls.append((number, status, pr, message))


class ReconcileTests(unittest.TestCase):
    def test_projection_is_repeatable(self) -> None:
        directory = tempfile.TemporaryDirectory()
        store = RunStore(Path(directory.name) / "state.sqlite3")
        run = store.create_run(repository="local/repo", issue_number=1, contract_hash="a" * 64, base_sha="b" * 40, branch="agent/1/run", worktree="worktree", backend="fake")
        store.transition(run.run_id, RunState.BLOCKED, reason_code="policy_violation")
        run = store.get_run(run.run_id)
        client = FakeProjectionClient()
        first = reconcile_issue(client, run)
        second = reconcile_issue(client, run)
        self.assertEqual(first, second)
        self.assertEqual(client.calls[0], client.calls[1])
        directory.cleanup()
