from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from tools.agent_doctor import checks


ROOT = Path(__file__).resolve().parents[1]


class AgentDoctorTests(unittest.TestCase):
    def test_checks_are_local_and_read_only(self) -> None:
        result = checks(ROOT)
        self.assertTrue(all(item["ok"] for item in result), result)
        names = {item["name"] for item in result}
        self.assertIn("AGENTS.md", names)
        self.assertIn("task_schema", names)
        self.assertNotIn("github_auth", names)
        self.assertNotIn("agent_cli", names)

    def test_json_cli_is_machine_readable(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/agent_doctor.py", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(list(payload), ["ok", "checks"])
