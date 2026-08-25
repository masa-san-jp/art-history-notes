from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from agent_harness.backends.fake import FakeBackend
from agent_harness.controller import HarnessConfig, HarnessController
from agent_harness.delivery import RecordingDelivery
from agent_harness.github import Issue
from agent_harness.policy import ExecutionPolicy
from agent_harness.store import RunStore
from agent_harness.verifier import VerificationPipeline


BODY = f'''<!-- agent-task:v1 -->
```yaml
version: 1
objective: controller test
deliverables:
  - path: docs/**
    expected: docs
scope:
  include: [docs/**]
non_goals: [none]
dependencies: []
checks:
  - argv: [{sys.executable}, -c, "print('check')"]
    timeout_seconds: 5
permissions:
  network: none
  external_write: false
limits:
  timeout_minutes: 1
  max_attempts: 1
  max_output_bytes: 4096
risk: low
completion: [done]
```'''


class FakeGitHub:
    repository = "local/repository"

    def __init__(self, issue: Issue) -> None:
        self.issue = issue
        self.labels: list[tuple[int, str]] = []

    def list_open_issues(self):
        return [self.issue]

    def get_issue(self, number):
        return self.issue

    def add_label(self, number, label):
        self.labels.append((number, label))

    def remove_label(self, number, label):
        return None

    def comment_issue(self, number, body):
        return None


class ControllerTests(unittest.TestCase):
    def test_queue_creates_and_executes_one_run_with_fake_github(self) -> None:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
        (root / "README.md").write_text("test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
        base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        subprocess.run(["git", "-C", str(root), "update-ref", "refs/remotes/origin/main", base], check=True)
        issue = Issue(1, "test", BODY, "open", frozenset({"agent-task"}), "2026-01-01T00:00:00Z")
        client = FakeGitHub(issue)
        config = HarnessConfig(True, "main", root / ".agent-harness" / "worktrees", root / ".agent-harness" / "state.sqlite3", "fake", (), ExecutionPolicy(allowed_commands=frozenset({"git", Path(sys.executable).name}), max_output_bytes=4096))
        store = RunStore(config.state_db)
        from agent_harness.worktree import WorktreeManager

        manager = WorktreeManager(root, config.worktree_root)
        controller = HarnessController(
            root=root,
            client=client,
            config=config,
            store=store,
            backend=FakeBackend(),
            delivery=RecordingDelivery(),
            verifier=VerificationPipeline(worktrees=manager, policy=config.policy, canonical_argv=[sys.executable, "-c", "print('canonical')"]),
        )
        result = controller.run_once()
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.outcome.state.value, "succeeded")
        self.assertEqual(client.labels, [(1, "agent-running")])
        directory.cleanup()
