from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from agent_harness.backends.fake import FakeBackend
from agent_harness.delivery import RecordingDelivery
from agent_harness.executor import HarnessExecutor
from agent_harness.models import RunState
from agent_harness.store import RunStore
from agent_harness.verifier import VerificationPipeline
from agent_harness.worktree import WorktreeManager


CONTRACT = {
    "version": 1,
    "objective": "run fake task",
    "deliverables": [{"path": "docs/**", "expected": "docs"}],
    "scope": {"include": ["docs/**"], "exclude": []},
    "non_goals": ["none"],
    "dependencies": [],
    "checks": [{"argv": [sys.executable, "-c", "print('task check')"], "timeout_seconds": 5}],
    "permissions": {"network": "none", "external_write": False, "allowed_env": []},
    "limits": {"timeout_minutes": 1, "max_attempts": 2, "max_output_bytes": 4096},
    "risk": "low",
    "completion": ["done"],
}


class ExecutorTests(unittest.TestCase):
    def test_fake_backend_closes_a_run_through_delivery(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        store = RunStore(root / ".agent-harness" / "state.sqlite3")
        run = store.create_run(repository="local/repo", issue_number=1, contract_hash="a" * 64, base_sha=base, branch="agent/issue-1/run", worktree=str(root / ".agent-harness" / "worktrees" / "run"), backend="fake")
        manager = WorktreeManager(root, root / ".agent-harness" / "worktrees")
        delivery = RecordingDelivery()
        executor = HarnessExecutor(store=store, worktrees=manager, backend=FakeBackend(), verifier=VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "print('canonical')"]), delivery=delivery, repository_root=root)
        outcome = executor.execute(run.run_id, CONTRACT)
        self.assertEqual(outcome.state.value, "succeeded")
        self.assertEqual(len(delivery.calls), 1)
        self.assertEqual(store.get_run(run.run_id).state.value, "succeeded")
        event_types = [event["event_type"] for event in store.events(run.run_id)]
        self.assertIn("backend.finished", event_types)
        self.assertIn("verification.stage", event_types)
        directory.cleanup()

    def test_verification_failure_is_repaired_by_second_attempt(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        store = RunStore(root / ".agent-harness" / "state.sqlite3")
        run = store.create_run(repository="local/repo", issue_number=2, contract_hash="a" * 64, base_sha=base, branch="agent/issue-2/run", worktree=str(root / ".agent-harness" / "worktrees" / "run"), backend="fake")
        manager = WorktreeManager(root, root / ".agent-harness" / "worktrees")

        def repair(request):
            bad = request.worktree / "docs" / "retry.flag"
            bad.parent.mkdir(exist_ok=True)
            if request.attempt == 1:
                bad.write_text("outside\n", encoding="utf-8")
            elif bad.exists():
                bad.unlink()
            return {"summary": "repaired", "changed_paths": [], "checks_run": [], "remaining_risks": [], "blockers": []}

        retry_contract = {**CONTRACT, "checks": [{"argv": [sys.executable, "-c", "from pathlib import Path; import sys; sys.exit(1 if Path('docs/retry.flag').exists() else 0)"], "timeout_seconds": 5}]}

        executor = HarnessExecutor(
            store=store,
            worktrees=manager,
            backend=FakeBackend(repair),
            verifier=VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "print('canonical')"]),
            delivery=RecordingDelivery(),
            repository_root=root,
            retry_sleep=lambda _seconds: None,
        )
        outcome = executor.execute(run.run_id, retry_contract)
        self.assertEqual(outcome.state.value, "succeeded")
        self.assertEqual(outcome.attempts, 2)
        self.assertEqual(store.get_run(run.run_id).attempt, 2)
        directory.cleanup()

    def test_lease_heartbeat_failure_blocks_before_delivery(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        store = RunStore(root / ".agent-harness" / "state.sqlite3")
        run = store.create_run(repository="local/repo", issue_number=3, contract_hash="a" * 64, base_sha=base, branch="agent/issue-3/run", worktree=str(root / ".agent-harness" / "worktrees" / "run"), backend="fake")
        manager = WorktreeManager(root, root / ".agent-harness" / "worktrees")
        delivery = RecordingDelivery()

        def slow_success(request):
            time.sleep(0.05)
            return {"summary": "must not deliver", "changed_paths": [], "checks_run": [], "remaining_risks": [], "blockers": []}

        executor = HarnessExecutor(
            store=store,
            worktrees=manager,
            backend=FakeBackend(slow_success),
            verifier=VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "print('canonical')"]),
            delivery=delivery,
            repository_root=root,
            lease_heartbeat=lambda: (_ for _ in ()).throw(RuntimeError("lease ownership was lost")),
            heartbeat_interval_seconds=0.01,
        )
        outcome = executor.execute(run.run_id, CONTRACT)
        self.assertEqual(outcome.state, RunState.BLOCKED)
        self.assertEqual(outcome.failure_code.value, "lease_lost")
        self.assertEqual(delivery.calls, [])
        directory.cleanup()
