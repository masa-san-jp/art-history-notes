from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from tools.agent_session import begin, load_session


ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / ".github" / "ISSUE_TEMPLATE" / "agent-task.md"


class AgentSessionTests(unittest.TestCase):
    def test_begin_records_hashes_without_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "session.json"
            payload = begin(TASK, output)
            self.assertEqual(payload["version"], 1)
            self.assertEqual(payload["repository_root"], str(ROOT))
            self.assertEqual(len(payload["task_hash"]), 64)
            self.assertTrue(payload["base_sha"])
            self.assertTrue(all(set(entry) == {"path", "kind", "content_sha256"} for entry in payload["baseline_entries"]))
            self.assertEqual(load_session(output), payload)

    def test_existing_session_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "session.json"
            begin(TASK, output)
            with self.assertRaises(FileExistsError):
                begin(TASK, output)
