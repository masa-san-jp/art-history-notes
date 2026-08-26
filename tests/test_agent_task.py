from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from tools.agent_task import ContractInvalid, load_contract, normalized_json, parse_contract


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "agent-task.md"
DOC_EXAMPLE = ROOT / "docs" / "agent" / "task-contract.md"


class AgentTaskTests(unittest.TestCase):
    def test_template_is_valid_v2_and_normalized(self) -> None:
        contract = load_contract(TEMPLATE, root=ROOT)
        self.assertEqual(contract["version"], 2)
        self.assertEqual(json.loads(normalized_json(contract)), contract)

    def test_documented_example_is_valid(self) -> None:
        self.assertEqual(load_contract(DOC_EXAMPLE, root=ROOT)["version"], 2)

    def test_marker_outside_contract_is_not_parsed(self) -> None:
        fence = chr(96) * 3
        source = TEMPLATE.read_text(encoding="utf-8")
        text = "untrusted " + fence + "yaml\nversion: 99\n" + fence + "\n" + source[source.index("<!-- agent-task:v2 -->"):]
        contract = parse_contract(text, root=ROOT)
        self.assertEqual(contract["version"], 2)

    def test_unknown_key_and_unsafe_path_are_reported(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8").replace("version: 2", "version: 2\nunknown: true", 1).replace('"docs/**"', '"../secrets/**"', 1)
        with self.assertRaises(ContractInvalid) as context:
            parse_contract(text, root=ROOT)
        errors = {(error.code, error.path) for error in context.exception.errors}
        self.assertIn(("unknown_key", "/unknown"), errors)
        self.assertIn(("unsafe_path", "/scope/include/0"), errors)

    def test_unsafe_contract_shapes_are_rejected(self) -> None:
        cases = (
            ("<!-- agent-task:v1 -->", "unsupported_version"),
            ('read:\n    - "docs/**"', "context_glob"),
            ('checks:\n  - "missing"', "unknown_check"),
            ('checks:\n  - "canonical"\n  - "canonical"', "duplicate_value"),
            ('include:\n    - "../outside/**"', "unsafe_path"),
        )
        source = TEMPLATE.read_text(encoding="utf-8")
        for replacement, expected in cases:
            with self.subTest(expected=expected):
                if replacement.startswith("<!--"):
                    text = source.replace("<!-- agent-task:v2 -->", replacement, 1)
                elif replacement.startswith("read:"):
                    text = source.replace('    - "README.md"', '    - "docs/**"', 1)
                elif replacement.startswith("checks:"):
                    check_value = '  - "canonical"\n  - "canonical"' if "canonical\"\n" in replacement else '  - "missing"'
                    text = source.replace('  - "canonical"', check_value, 1)
                else:
                    text = source.replace('    - "docs/**"', '    - "../outside/**"', 1)
                with self.assertRaises(ContractInvalid) as context:
                    parse_contract(text, root=ROOT)
                self.assertIn(expected, {error.code for error in context.exception.errors})

    def test_file_and_stdin_cli_outputs_are_machine_readable(self) -> None:
        command = [sys.executable, "tools/agent_task.py", "validate", "--file", str(TEMPLATE), "--json"]
        file_result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(file_result.returncode, 0, file_result.stderr)
        self.assertTrue(json.loads(file_result.stdout)["ok"])
        stdin_result = subprocess.run(
            [sys.executable, "tools/agent_task.py", "validate", "--stdin", "--json"],
            cwd=ROOT,
            input=TEMPLATE.read_text(encoding="utf-8"),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(stdin_result.returncode, 0, stdin_result.stderr)
        self.assertEqual(json.loads(stdin_result.stdout)["task"], json.loads(file_result.stdout)["task"])

    def test_invalid_yaml_is_an_input_error(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/agent_task.py", "validate", "--stdin", "--json"],
            cwd=ROOT,
            input="<!-- agent-task:v2 -->\n```yaml\nversion: [\n```",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["code"], "invalid_yaml")

    def test_checked_in_fixtures_have_expected_validity(self) -> None:
        valid = ROOT / "tests" / "fixtures" / "agent-task" / "valid.md"
        self.assertEqual(load_contract(valid, root=ROOT)["version"], 2)
        for invalid in sorted((ROOT / "tests" / "fixtures" / "agent-task" / "invalid").glob("*.md")):
            with self.subTest(path=invalid):
                with self.assertRaises(ContractInvalid):
                    load_contract(invalid, root=ROOT)
