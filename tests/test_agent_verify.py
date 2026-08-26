from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from tools.agent_session import begin
from tools.agent_verify import _scope_failures, run_check, verify
from tools.agent_task import load_contract


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / ".github" / "ISSUE_TEMPLATE" / "agent-task.md"


class AgentVerifyTests(unittest.TestCase):
    def test_no_change_task_is_verified_without_remote_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            session = Path(directory) / "session.json"
            begin(TASK, session)
            with patch("tools.agent_verify.run_check", return_value={"id": "", "argv": [], "exit_code": 0, "duration_seconds": 0, "code": "ok"}):
                code, payload = verify(TASK, session)
            self.assertEqual(code, 0, payload)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["manifest"], [])
            self.assertEqual(payload["checks"][-1]["id"], "canonical")

    def test_scope_failure_is_machine_readable(self) -> None:
        task = load_contract(TASK, root=ROOT)
        failures = _scope_failures(["outside/file.txt"], task, {"outside/file.txt": "file"})
        self.assertEqual(failures, [{"path": "outside/file.txt", "code": "outside_scope"}])
        self.assertEqual(_scope_failures([".git/config"], task, {".git/config": "file"}), [{"path": ".git/config", "code": "forbidden_path"}])

    def test_timeout_terminates_the_process_group(self) -> None:
        started = time.monotonic()
        result = run_check([sys.executable, "-c", "while True: pass"], 1)
        self.assertEqual(result["code"], "timeout")
        self.assertLess(time.monotonic() - started, 5)

    def test_output_limit_terminates_the_process_group(self) -> None:
        result = run_check([sys.executable, "-c", "print('x' * 2_000_000)"], 10)
        self.assertEqual(result["code"], "output_limit")

    def test_cancel_file_terminates_the_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cancel = Path(directory) / "CANCEL"
            cancel.touch()
            result = run_check(
                [sys.executable, "-c", "while True: pass"],
                10,
                is_cancelled=cancel.exists,
            )
        self.assertEqual(result["code"], "cancelled")

    def test_tampered_session_fields_are_rejected(self) -> None:
        for field, value, expected in (
            ("base_sha", "0" * 40, "base_missing"),
            ("repository_root", "/tmp/other-repository", "input_invalid"),
            ("version", 99, "input_invalid"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                session = Path(directory) / "session.json"
                begin(TASK, session)
                payload = json.loads(session.read_text(encoding="utf-8"))
                payload[field] = value
                session.write_text(json.dumps(payload), encoding="utf-8")
                code, result = verify(TASK, session)
                self.assertEqual(code, 2)
                if field == "base_sha":
                    self.assertEqual(result["errors"][0]["code"], expected)
                else:
                    self.assertEqual(result["errors"][0]["code"], expected)
