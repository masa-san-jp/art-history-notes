from __future__ import annotations

from pathlib import Path
import tempfile
import sys
import threading
import unittest

from agent_harness.policy import ExecutionPolicy, PolicyViolation, Redactor, path_in_scope, validate_scope
from agent_harness.process_runner import run_argv


ROOT = Path(__file__).resolve().parents[1]


class PolicyTests(unittest.TestCase):
    def test_scope_and_forbidden_paths(self) -> None:
        self.assertTrue(path_in_scope("docs/a.md", ["docs/**"], []))
        self.assertFalse(path_in_scope(".git/config", ["**"], []))
        self.assertFalse(path_in_scope(".env", ["**"], []))
        with self.assertRaises(PolicyViolation):
            validate_scope(["src/a.py", "docs/a.md"], ["docs/**"], [])

    def test_argv_rejects_shell_and_unallowlisted_commands(self) -> None:
        policy = ExecutionPolicy()
        with self.assertRaises(PolicyViolation):
            policy.validate_argv(["sh", "-c", "echo unsafe"])
        with self.assertRaises(PolicyViolation):
            policy.validate_argv(["curl", "https://example.com"])

    def test_redactor_replaces_longest_secret_first(self) -> None:
        redactor = Redactor(["secret", "secret-value"])
        self.assertEqual(redactor.text("secret-value secret"), "[REDACTED] [REDACTED]")

    def test_process_runner_bounds_output_and_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_argv(
                [sys.executable, "-c", "print('x' * 10000)"],
                cwd=Path(directory),
                timeout_seconds=5,
                max_output_bytes=128,
            )
            self.assertTrue(result.output_limited)
            self.assertLessEqual(len(result.stdout) + len(result.stderr), 128)

            result = run_argv(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                cwd=Path(directory),
                timeout_seconds=1,
                max_output_bytes=128,
            )
            self.assertTrue(result.timed_out)

    def test_process_runner_can_be_cancelled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            event = threading.Event()
            event.set()
            result = run_argv(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                cwd=Path(directory),
                timeout_seconds=5,
                max_output_bytes=128,
                cancel_event=event,
            )
            self.assertTrue(result.cancelled)
