from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from agent_harness.delivery import GitHubDelivery
from agent_harness.models import Run
from agent_harness.worktree import WorktreeManager


class FakeDeliveryClient:
    def __init__(self) -> None:
        self.pr_calls = 0
        self.sync_calls = 0

    def find_or_create_pr(self, run, *, objective, base_branch):
        self.pr_calls += 1
        return {"number": 42, "url": "https://example.test/pr/42", "body": "marker"}

    def sync_issue(self, number, *, status, pr, message):
        self.sync_calls += 1


class DeliveryTests(unittest.TestCase):
    def test_retry_after_delivery_timeout_reuses_run_marked_commit(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        manager = WorktreeManager(root, root / ".agent-harness" / "worktrees")
        worktree = manager.create(run_id="run", branch="agent/issue-1/run", base_sha=base)
        (worktree.path / "docs").mkdir()
        (worktree.path / "docs" / "result.md").write_text("result\n", encoding="utf-8")
        run = Run("run", "local/repository", 1, "a" * 64, base, "agent/issue-1/run", str(worktree.path), "fake", __import__("agent_harness.models", fromlist=["RunState"]).RunState.DELIVERING, 1, None, None, None, None, None, False, "now", "now")
        client = FakeDeliveryClient()
        delivery = GitHubDelivery(root, client, auto_push=False)
        first = delivery.deliver(run, objective="write result", manifest=["docs/result.md"], worktree=worktree.path, base_branch="main")
        commit_after_first = subprocess.check_output(["git", "-C", str(worktree.path), "rev-parse", "HEAD"], text=True).strip()
        second = delivery.deliver(run, objective="write result", manifest=["docs/result.md"], worktree=worktree.path, base_branch="main")
        commit_after_second = subprocess.check_output(["git", "-C", str(worktree.path), "rev-parse", "HEAD"], text=True).strip()
        self.assertEqual(first.commit_sha, second.commit_sha)
        self.assertEqual(commit_after_first, commit_after_second)
        self.assertEqual(client.pr_calls, 2)
        self.assertEqual(client.sync_calls, 2)
        manager.cleanup(worktree, allow=True)
        directory.cleanup()
