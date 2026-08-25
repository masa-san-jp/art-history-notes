from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class HarnessCliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-m", "agent_harness", *arguments], cwd=ROOT, capture_output=True, text=True, check=False, timeout=30)

    def test_public_run_list_is_json_and_uses_requested_db(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("--db", str(Path(directory) / "state.sqlite3"), "run", "list", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), [])

    def test_public_execute_is_safe_while_production_is_disabled(self) -> None:
        result = self.run_cli("run", "execute", "--run-id", "run-not-started")
        self.assertEqual(result.returncode, 5)
        self.assertEqual(json.loads(result.stdout)["status"], "disabled")

    def test_public_help_exposes_operator_operations(self) -> None:
        queue = self.run_cli("queue", "--help")
        run = self.run_cli("run", "--help")
        self.assertIn("claim", queue.stdout)
        self.assertIn("heartbeat", queue.stdout)
        self.assertIn("release", queue.stdout)
        self.assertIn("execute", run.stdout)


if __name__ == "__main__":
    unittest.main()
