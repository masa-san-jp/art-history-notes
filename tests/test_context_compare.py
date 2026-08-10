import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import compare_context


PYTHON = sys.executable
TARGET = "context/ai-art-japan-2026-h2"


class CompareCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [PYTHON, "tools/compare_context.py", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_markdown_output_has_required_explanation(self):
        result = self.run_cli(TARGET, "--kind", "historical", "--top", "3")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("類似上位3軸", result.stdout)
        self.assertIn("相違上位3軸", result.stdout)
        self.assertIn("方向", result.stdout)
        self.assertIn("顕著性", result.stdout)
        self.assertIn("分極", result.stdout)
        self.assertIn("信頼度", result.stdout)
        self.assertIn(compare_context.NOTICE, result.stdout)

    def test_json_output_parses(self):
        result = self.run_cli(TARGET, "--kind", "historical", "--top", "3", "--format", "json")
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(TARGET, payload["target"])
        self.assertEqual(3, len(payload["candidates"]))
        self.assertEqual(compare_context.NOTICE, payload["notice"])

    def test_unknown_context_is_exit_two(self):
        result = self.run_cli("context/missing")
        self.assertEqual(2, result.returncode)
        self.assertIn("未知の context ID", result.stderr)

    def test_invalid_top_is_exit_two(self):
        result = self.run_cli(TARGET, "--top", "0")
        self.assertEqual(2, result.returncode)
        self.assertIn("1〜100", result.stderr)

    def test_missing_generated_file_is_exit_two(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            with mock.patch.object(compare_context, "VECTORS_PATH", missing):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    code = compare_context.main([TARGET])
            self.assertEqual(2, code)
            self.assertIn("生成物がない", stderr.getvalue())

    def test_digest_mismatch_is_exit_two(self):
        stderr = io.StringIO()
        with mock.patch.object(compare_context, "compute_input_digest", return_value="stale"):
            with contextlib.redirect_stderr(stderr):
                code = compare_context.main([TARGET])
        self.assertEqual(2, code)
        self.assertIn("生成物が入力と一致しない", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
