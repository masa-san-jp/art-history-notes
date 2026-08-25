from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from agent_harness.task_contract import ContractValidationError, load_contract, normalized_json, parse_contract


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "agent-task.md"


class AgentTaskContractTests(unittest.TestCase):
    def test_template_is_valid_and_normalized(self) -> None:
        contract = load_contract(TEMPLATE)
        self.assertEqual(contract["version"], 1)
        self.assertEqual(contract["scope"]["exclude"], [])
        self.assertEqual(contract["permissions"]["allowed_env"], [])
        self.assertEqual(json.loads(normalized_json(contract)), contract)

    def test_marker_reads_only_the_fence_after_marker(self) -> None:
        text = """untrusted ```yaml\nversion: 99\n```\n\n<!-- agent-task:v1 -->\n```yaml\n""" + TEMPLATE.read_text(encoding="utf-8").split("```yaml\n", 1)[1]
        contract = parse_contract(text)
        self.assertEqual(contract["version"], 1)

    def test_unknown_key_is_reported_as_json_pointer(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8").replace("version: 1", "version: 1\nunknown: true", 1)
        with self.assertRaises(ContractValidationError) as context:
            parse_contract(text)
        self.assertIn({"path": "/unknown", "message": "unknown key"}, [error.as_dict() for error in context.exception.errors])

    def test_unsafe_paths_and_shell_string_are_rejected(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8").replace('"docs/**"', '"../secrets/**"', 1)
        with self.assertRaises(ContractValidationError) as context:
            parse_contract(text)
        paths = {error.path for error in context.exception.errors}
        self.assertIn("/scope/include/0", paths)

        shell_text = TEMPLATE.read_text(encoding="utf-8").replace(
            'argv: ["uv", "run", "--locked", "python", "tools/verify.py"]',
            'argv: "uv run --locked python tools/verify.py"',
            1,
        )
        with self.assertRaises(ContractValidationError) as context:
            parse_contract(shell_text)
        self.assertIn("/checks/0/argv", {error.path for error in context.exception.errors})

    def test_duplicate_dependencies_and_bool_version_are_rejected(self) -> None:
        duplicate = TEMPLATE.read_text(encoding="utf-8").replace("dependencies: []", "dependencies: [12, 12]", 1)
        with self.assertRaises(ContractValidationError) as context:
            parse_contract(duplicate)
        self.assertIn("/dependencies", {error.path for error in context.exception.errors})

        bool_version = TEMPLATE.read_text(encoding="utf-8").replace("version: 1", "version: true", 1)
        with self.assertRaises(ContractValidationError) as context:
            parse_contract(bool_version)
        self.assertIn("/version", {error.path for error in context.exception.errors})

    def test_missing_marker_is_rejected(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write("objective: no")
            handle.flush()
            with self.assertRaises(ContractValidationError):
                load_contract(Path(handle.name))
