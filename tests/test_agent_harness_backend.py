from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

from agent_harness.backends.command import CommandBackend
from agent_harness.backends.fake import FakeBackend
from agent_harness.backends.base import BackendRequest
from agent_harness.context import build_context
from agent_harness.handoff import HandoffError, validate_handoff
from agent_harness.policy import ExecutionPolicy


CONTRACT = {
    "version": 1,
    "objective": "test",
    "deliverables": [{"path": "docs/**", "expected": "docs"}],
    "scope": {"include": ["docs/**"], "exclude": []},
    "non_goals": ["none"],
    "dependencies": [],
    "checks": [{"argv": ["python", "-V"], "timeout_seconds": 5}],
    "permissions": {"network": "none", "external_write": False, "allowed_env": []},
    "limits": {"timeout_minutes": 1, "max_attempts": 1, "max_output_bytes": 4096},
    "risk": "low",
    "completion": ["test passes"],
}


class BackendTests(unittest.TestCase):
    def request(self, directory: str) -> BackendRequest:
        root = Path(directory)
        return BackendRequest("01900000-0000-7000-8000-000000000000", 1, root, root / "prompt.txt", root / "events.jsonl", root / "handoff.json", "prompt", 5, 4096)

    def test_context_is_deterministic_and_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = build_context(root=root, contract=CONTRACT, run_id="run", attempt=1, base_sha="base")
            second = build_context(root=root, contract=CONTRACT, run_id="run", attempt=1, base_sha="base")
            self.assertEqual(first.sha256, second.sha256)
            self.assertEqual(first.text, second.text)
            with self.assertRaises(ValueError):
                build_context(root=root, contract=CONTRACT, run_id="run", attempt=1, base_sha="base", max_bytes=10)

    def test_fake_backend_writes_valid_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = self.request(directory)
            backend = FakeBackend()
            result = backend.wait(backend.start(request))
            self.assertEqual(result.status, "completed")
            self.assertEqual(result.handoff["version"], 1)

    def test_command_backend_uses_argv_template_and_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = self.request(directory)
            command = [sys.executable, "-c", "import json; json.dump({'version': 1, 'status': 'completed', 'summary': 'ok', 'changed_paths': [], 'checks_run': [], 'remaining_risks': [], 'blockers': []}, open(r'{handoff_file}', 'w'))"]
            backend = CommandBackend(command, policy=ExecutionPolicy(allowed_commands=frozenset({Path(sys.executable).name}), max_output_bytes=4096))
            result = backend.wait(backend.start(request))
            self.assertEqual(result.status, "completed")
            self.assertEqual(result.handoff["summary"], "ok")

    def test_command_backend_can_feed_prompt_via_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = self.request(directory)
            command = [
                sys.executable,
                "-c",
                "import json,sys; assert sys.stdin.read() == 'prompt'; json.dump({'version': 1, 'status': 'completed', 'summary': 'stdin', 'changed_paths': [], 'checks_run': [], 'remaining_risks': [], 'blockers': []}, open(r'{handoff_file}', 'w'))",
            ]
            backend = CommandBackend(command, prompt_mode="stdin", policy=ExecutionPolicy(allowed_commands=frozenset({Path(sys.executable).name}), max_output_bytes=4096))
            result = backend.wait(backend.start(request))
            self.assertEqual(result.status, "completed")
            self.assertEqual(result.handoff["summary"], "stdin")

    def test_handoff_rejects_unknown_or_missing_keys(self) -> None:
        with self.assertRaises(HandoffError):
            validate_handoff({"version": 1})
        with self.assertRaises(HandoffError):
            validate_handoff({"version": 1, "status": "completed", "summary": "ok", "changed_paths": [], "checks_run": [], "remaining_risks": [], "blockers": [], "extra": 1})
