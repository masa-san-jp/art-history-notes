from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)


class AgentReadinessE2ETests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name) / "repo"
        ignored = shutil.ignore_patterns(".git", ".agent-local", "__pycache__", ".venv")
        shutil.copytree(ROOT, self.repo, ignore=ignored)
        fixture_bin = Path(self.tempdir.name) / "bin"
        fixture_bin.mkdir()
        fixture_uv = fixture_bin / "uv"
        fixture_uv.write_text("#!/bin/sh\nprintf 'uv fixture\\n'\nexit 0\n", encoding="utf-8")
        fixture_uv.chmod(0o755)
        self.environment = os.environ.copy()
        self.environment["PATH"] = str(fixture_bin) + os.pathsep + self.environment.get("PATH", "")
        (self.repo / "config" / "agent-checks.yaml").write_text(
            'checks:\n  canonical:\n    description: "fixture check"\n    argv: [uv, run, --locked, python, tools/verify.py]\n    timeout_seconds: 10\n',
            encoding="utf-8",
        )
        self.task = self.repo / "tests" / "fixtures" / "agent-task" / "complete.md"
        self.assertEqual(run_git(self.repo, "init").returncode, 0)
        self.assertEqual(run_git(self.repo, "config", "user.email", "test@example.invalid").returncode, 0)
        self.assertEqual(run_git(self.repo, "config", "user.name", "Agent readiness test").returncode, 0)
        self.assertEqual(run_git(self.repo, "add", ".").returncode, 0)
        self.assertEqual(run_git(self.repo, "commit", "-m", "fixture baseline").returncode, 0)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def command(self, script: str, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.repo / "tools" / script), *args],
            cwd=self.repo,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
            env=self.environment,
        )

    def test_public_cli_handles_fresh_and_dirty_worktrees(self) -> None:
        doctor = self.command("agent_doctor.py", "--json")
        self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
        self.assertTrue(json.loads(doctor.stdout)["ok"])
        validated = self.command("agent_task.py", "validate", "--file", str(self.task), "--json")
        self.assertEqual(validated.returncode, 0, validated.stderr)

        (self.repo / "README.md").write_text((self.repo / "README.md").read_text(encoding="utf-8") + "\npre-existing\n", encoding="utf-8")
        (self.repo / "pre-existing.txt").write_text("owned before task\n", encoding="utf-8")
        session = self.repo / ".agent-local" / "session.json"
        begun = self.command("agent_session.py", "begin", "--task-file", str(self.task), "--output", str(session))
        self.assertEqual(begun.returncode, 0, begun.stderr)

        first = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertEqual(json.loads(first.stdout)["manifest"], [])

        target = self.repo / "tests" / "fixtures" / "agent-task" / "result.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("verified fixture\n", encoding="utf-8")
        success = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(success.returncode, 0, success.stdout)
        manifest = json.loads(success.stdout)["manifest"]
        self.assertEqual(manifest, ["tests/fixtures/agent-task/result.md"])

        outside = self.repo / "outside.txt"
        outside.write_text("outside scope\n", encoding="utf-8")
        scope_failure = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(scope_failure.returncode, 1)
        self.assertEqual(json.loads(scope_failure.stdout)["scope"]["failures"], [{"path": "outside.txt", "code": "outside_scope"}])
        outside.unlink()

        forbidden_local = self.repo / ".agent-local" / "unauthorized.txt"
        forbidden_local.write_text("must be rejected\n", encoding="utf-8")
        local_failure = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(local_failure.returncode, 1)
        self.assertEqual(json.loads(local_failure.stdout)["scope"]["failures"], [{"path": ".agent-local/unauthorized.txt", "code": "forbidden_path"}])
        forbidden_local.unlink()

        link = self.repo / "tests" / "fixtures" / "agent-task" / "escape"
        link.symlink_to(self.repo / "README.md")
        symlink_failure = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(symlink_failure.returncode, 1)
        self.assertEqual(json.loads(symlink_failure.stdout)["scope"]["failures"], [{"path": "tests/fixtures/agent-task/escape", "code": "symlink_forbidden"}])
        link.unlink()

        secret = "ghp_" + "A" * 24
        secret_path = self.repo / "tests" / "fixtures" / "agent-task" / "secret.txt"
        secret_path.write_text(secret, encoding="utf-8")
        secret_failure = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(secret_failure.returncode, 1)
        self.assertNotIn(secret, secret_failure.stdout)
        self.assertEqual(json.loads(secret_failure.stdout)["secrets"]["failures"], [{"path": "tests/fixtures/agent-task/secret.txt", "code": "secret_detected"}])
        secret_path.unlink()

    def test_tampered_session_is_rejected(self) -> None:
        session = self.repo / ".agent-local" / "session.json"
        begun = self.command("agent_session.py", "begin", "--task-file", str(self.task), "--output", str(session))
        self.assertEqual(begun.returncode, 0, begun.stderr)
        payload = json.loads(session.read_text(encoding="utf-8"))
        payload["task_hash"] = "0" * 64
        session.write_text(json.dumps(payload), encoding="utf-8")
        result = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["code"], "task_changed")

    def test_dirty_overlap_is_rejected(self) -> None:
        readme = self.repo / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\npre-existing\n", encoding="utf-8")
        pre_existing = self.repo / "pre-existing.txt"
        pre_existing.write_text("owned before task\n", encoding="utf-8")
        session = self.repo / ".agent-local" / "dirty-overlap.json"
        begun = self.command("agent_session.py", "begin", "--task-file", str(self.task), "--output", str(session))
        self.assertEqual(begun.returncode, 0, begun.stderr)
        readme.write_text(readme.read_text(encoding="utf-8") + "changed by task\n", encoding="utf-8")
        result = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["scope"]["failures"], [{"path": "README.md", "code": "outside_scope"}])

    def test_scope_mutation_modes_are_rejected(self) -> None:
        task = self.repo / "mutation-task.md"
        task.write_text(
            self.task.read_text(encoding="utf-8").replace('    - "README.md"', '    - "tools/verify.py"', 1),
            encoding="utf-8",
        )
        readme = self.repo / "README.md"
        original = readme.read_bytes()
        try:
            operations = ("modify", "delete", "rename")
            for operation in operations:
                with self.subTest(operation=operation):
                    session = self.repo / ".agent-local" / f"{operation}.json"
                    begun = self.command("agent_session.py", "begin", "--task-file", str(task), "--output", str(session))
                    self.assertEqual(begun.returncode, 0, begun.stderr)
                    if operation == "modify":
                        readme.write_bytes(original + b"changed\n")
                    elif operation == "delete":
                        readme.unlink()
                    else:
                        readme.rename(self.repo / "README.renamed")
                    result = self.command("agent_verify.py", "--task-file", str(task), "--session", str(session), "--json")
                    self.assertEqual(result.returncode, 1, result.stdout)
                    failures = json.loads(result.stdout)["scope"]["failures"]
                    self.assertTrue(failures)
                    self.assertTrue(all(item["code"] == "outside_scope" for item in failures))
                    if (self.repo / "README.renamed").exists():
                        (self.repo / "README.renamed").rename(readme)
                    if not readme.exists():
                        readme.write_bytes(original)
                    else:
                        readme.write_bytes(original)
        finally:
            if (self.repo / "README.renamed").exists():
                (self.repo / "README.renamed").rename(readme)
            readme.write_bytes(original)

    def test_failed_check_still_runs_canonical_last(self) -> None:
        (self.repo / "config" / "agent-checks.yaml").write_text(
            f"""checks:
  preflight:
    description: \"Intentional fixture failure.\"
    argv: [{json.dumps(sys.executable)}, -c, \"import sys; sys.exit(3)\"]
    timeout_seconds: 10
  canonical:
    description: \"fixture check\"
    argv: [uv, run, --locked, python, tools/verify.py]
    timeout_seconds: 10
""",
            encoding="utf-8",
        )
        task = self.repo / "failure-task.md"
        task.write_text(
            self.task.read_text(encoding="utf-8")
            .replace('    - "README.md"', '    - "tools/verify.py"', 1)
            .replace('  - "canonical"', '  - "preflight"', 1),
            encoding="utf-8",
        )
        session = self.repo / ".agent-local" / "failure.json"
        begun = self.command("agent_session.py", "begin", "--task-file", str(task), "--output", str(session))
        self.assertEqual(begun.returncode, 0, begun.stderr)
        result = self.command("agent_verify.py", "--task-file", str(task), "--session", str(session), "--json")
        self.assertEqual(result.returncode, 1, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual([item["id"] for item in payload["checks"]], ["preflight", "canonical"])
        self.assertEqual([item["code"] for item in payload["checks"]], ["check_failed", "ok"])

    def test_completion_json_has_stable_fields(self) -> None:
        session = self.repo / ".agent-local" / "completion.json"
        begun = self.command("agent_session.py", "begin", "--task-file", str(self.task), "--output", str(session))
        self.assertEqual(begun.returncode, 0, begun.stderr)
        result = self.command("agent_verify.py", "--task-file", str(self.task), "--session", str(session), "--json")
        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(
            set(payload),
            {"schema_version", "ok", "task_hash", "base_sha", "manifest", "scope", "secrets", "checks", "acceptance"},
        )
        self.assertEqual(payload["manifest"], [])
        self.assertEqual(payload["checks"][-1]["id"], "canonical")
