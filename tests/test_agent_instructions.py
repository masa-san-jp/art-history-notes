from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AgentInstructionTests(unittest.TestCase):
    def test_entrypoint_has_required_sections_and_commands(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        headings = [
            "# Repository mission",
            "# Instruction precedence",
            "# Start here",
            "# Task workflow",
            "# Domain rules",
            "# Generated files",
            "# Verification",
            "# Git and external side effects",
            "# Completion report",
        ]
        positions = [text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        for relative in (
            "tools/agent_doctor.py",
            "tools/agent_task.py",
            "tools/agent_session.py",
            "tools/agent_verify.py",
            "tools/test_agent_readiness.py",
        ):
            self.assertIn(relative, text)
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_readme_reaches_agent_documentation(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[AGENTS.md](AGENTS.md)", text)
        self.assertIn("[docs/agent/README.md](docs/agent/README.md)", text)
        architecture = (ROOT / "docs" / "agent" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("The repository never starts", architecture)

    def test_workflow_is_read_only_and_does_not_start_an_agent(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "agent-readiness.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("issues: write", workflow)
        self.assertNotIn("pull-requests: write", workflow)
        self.assertNotIn("codex", workflow.lower())
        self.assertNotIn("claude", workflow.lower())
