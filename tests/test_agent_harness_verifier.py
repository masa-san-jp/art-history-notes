from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from agent_harness.failure import FailureCode, retry_allowed, retry_delay_seconds
from agent_harness.verifier import VerificationPipeline
from agent_harness.worktree import Worktree, WorktreeManager


CONTRACT = {
    "version": 1,
    "objective": "verify",
    "deliverables": [{"path": "docs/**", "expected": "docs"}],
    "scope": {"include": ["docs/**"], "exclude": []},
    "non_goals": ["none"],
    "dependencies": [],
    "checks": [{"argv": [sys.executable, "-c", "print('ok')"], "timeout_seconds": 5}],
    "permissions": {"network": "none", "external_write": False, "allowed_env": []},
    "limits": {"timeout_minutes": 1, "max_attempts": 3, "max_output_bytes": 4096},
    "risk": "low",
    "completion": ["done"],
}


class VerifierTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, WorktreeManager, Worktree]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        manager = WorktreeManager(root, root / ".agent-harness" / "worktrees")
        worktree = manager.create(run_id="run", branch="agent/issue-1/run", base_sha=base)
        return directory, root, manager, worktree

    def test_success_requires_canonical_verify(self) -> None:
        directory, root, manager, worktree = self.make_repo()
        try:
            (worktree.path / "docs").mkdir()
            (worktree.path / "docs" / "test.md").write_text("ok\n", encoding="utf-8")
            handoff = {"version": 1, "status": "completed", "summary": "ok", "changed_paths": ["docs/test.md"], "checks_run": [], "remaining_risks": [], "blockers": []}
            pipeline = VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "print('canonical')"])
            result = pipeline.verify(worktree=worktree, contract=CONTRACT, handoff=handoff)
            self.assertTrue(result.ok)
            self.assertEqual(result.stages[-1].name, "final_manifest")
        finally:
            manager.cleanup(worktree, allow=True)
            directory.cleanup()

    def test_scope_violation_blocks_before_checks(self) -> None:
        directory, root, manager, worktree = self.make_repo()
        try:
            (worktree.path / "secret.txt").write_text("bad\n", encoding="utf-8")
            handoff = {"version": 1, "status": "completed", "summary": "bad", "changed_paths": ["secret.txt"], "checks_run": [], "remaining_risks": [], "blockers": []}
            result = VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "raise SystemExit(1)"]).verify(worktree=worktree, contract=CONTRACT, handoff=handoff)
            self.assertFalse(result.ok)
            self.assertEqual(result.failure_code, FailureCode.POLICY_VIOLATION)
            self.assertEqual([stage.name for stage in result.stages], ["handoff", "scope"])
        finally:
            manager.cleanup(worktree, allow=True)
            directory.cleanup()

    def test_secret_scan_blocks_before_checks_without_recording_value(self) -> None:
        directory, root, manager, worktree = self.make_repo()
        try:
            (worktree.path / "docs").mkdir()
            (worktree.path / "docs" / "secret.txt").write_text("api_key=0123456789abcdef0123\n", encoding="utf-8")
            handoff = {"version": 1, "status": "completed", "summary": "secret", "changed_paths": ["docs/secret.txt"], "checks_run": [], "remaining_risks": [], "blockers": []}
            pipeline = VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "raise SystemExit(1)"])
            result = pipeline.verify(worktree=worktree, contract=CONTRACT, handoff=handoff)
            self.assertFalse(result.ok)
            self.assertEqual(result.failure_code, FailureCode.SECRET_DETECTED)
            self.assertEqual([stage.name for stage in result.stages], ["handoff", "scope", "secret_scan"])
            self.assertNotIn("0123456789abcdef0123", result.stages[-1].diagnostic)
        finally:
            manager.cleanup(worktree, allow=True)
            directory.cleanup()

    def test_symlink_escape_is_rejected(self) -> None:
        directory, root, manager, worktree = self.make_repo()
        outside = Path(directory.name).parent / f"outside-{worktree.branch.replace('/', '-')}.txt"
        try:
            outside.write_text("outside\n", encoding="utf-8")
            (worktree.path / "docs").mkdir()
            (worktree.path / "docs" / "escape.txt").symlink_to(outside)
            handoff = {"version": 1, "status": "completed", "summary": "escape", "changed_paths": [], "checks_run": [], "remaining_risks": [], "blockers": []}
            result = VerificationPipeline(worktrees=manager, canonical_argv=[sys.executable, "-c", "print('canonical')"]).verify(worktree=worktree, contract=CONTRACT, handoff=handoff)
            self.assertFalse(result.ok)
            self.assertEqual(result.failure_code, FailureCode.POLICY_VIOLATION)
        finally:
            manager.cleanup(worktree, allow=True)
            outside.unlink(missing_ok=True)
            directory.cleanup()

    def test_retry_policy_is_finite(self) -> None:
        self.assertTrue(retry_allowed(FailureCode.CANONICAL_VERIFY_FAILED, attempt=1, max_attempts=3))
        self.assertFalse(retry_allowed(FailureCode.POLICY_VIOLATION, attempt=1, max_attempts=3))
        self.assertFalse(retry_allowed(FailureCode.CANONICAL_VERIFY_FAILED, attempt=3, max_attempts=3))
        self.assertEqual(retry_delay_seconds(3), 8.0)
