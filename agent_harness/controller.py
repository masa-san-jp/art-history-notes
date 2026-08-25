"""Single-cycle controller for queue -> claim -> execute."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import socket
import subprocess
import sys
from typing import Any

import yaml

from .backends.command import CommandBackend
from .backends.fake import FakeBackend
from .delivery import GitHubDelivery, RecordingDelivery
from .executor import ExecutionOutcome, HarnessExecutor
from .github import GhClient, GitHubClient, GitHubError
from .lease import LeaseManager
from .models import RunState
from .policy import ExecutionPolicy
from .queue import TaskQueue
from .reconcile import reconcile_issue
from .recovery import recover_stale_runs
from .store import RunStore
from .ids import new_run_id
from .task_contract import normalized_json, parse_contract
from .verifier import VerificationPipeline
from .worktree import WorktreeManager


@dataclass(frozen=True)
class HarnessConfig:
    enabled: bool
    base_branch: str
    worktree_root: Path
    state_db: Path
    backend_type: str
    backend_argv: tuple[str, ...]
    policy: ExecutionPolicy

    @classmethod
    def load(cls, path: Path, *, root: Path) -> "HarnessConfig":
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        policy_value = value.get("policy", {})
        backends = value.get("backends", {})
        backend = backends.get("default", {})
        return cls(
            enabled=bool(value.get("enabled", False)),
            base_branch=str(value.get("base_branch", "main")),
            worktree_root=(root / str(value.get("worktree_root", ".agent-harness/worktrees"))).resolve(),
            state_db=(root / str(value.get("state_db", ".agent-harness/state.sqlite3"))).resolve(),
            backend_type=str(backend.get("type", "command")),
            backend_argv=tuple(str(part) for part in backend.get("argv", [])),
            policy=ExecutionPolicy(
                allowed_commands=frozenset(str(item) for item in policy_value.get("allowed_commands", ["git", "python", "python3", "uv", "codex", "claude"])),
                max_timeout_seconds=int(policy_value.get("max_timeout_seconds", 14400)),
                max_output_bytes=int(policy_value.get("max_output_bytes", 10 * 1024 * 1024)),
                allowed_env=frozenset(str(item) for item in policy_value.get("allowed_env", [])),
            ),
        )


@dataclass(frozen=True)
class ControllerResult:
    status: str
    issue_number: int | None = None
    run_id: str | None = None
    outcome: ExecutionOutcome | None = None
    reason: str | None = None


class HarnessController:
    def __init__(self, *, root: Path, client: GitHubClient, config: HarnessConfig, store: RunStore | None = None, backend: Any | None = None, delivery: Any | None = None, verifier: Any | None = None, owner_id: str | None = None) -> None:
        self.root = root.resolve()
        self.client = client
        self.config = config
        self.store = store or RunStore(config.state_db)
        self.worktrees = WorktreeManager(self.root, config.worktree_root)
        self.backend = backend or self._make_backend()
        self.delivery = delivery or GitHubDelivery(self.root, client)
        self.verifier = verifier
        self.owner_id = owner_id or f"{socket.gethostname()}:{os.getpid()}"

    def _make_backend(self) -> Any:
        if self.config.backend_type == "fake":
            return FakeBackend()
        return CommandBackend(list(self.config.backend_argv), policy=self.config.policy, env_names=set(self.config.policy.allowed_env))

    def _executor(self) -> HarnessExecutor:
        verifier = self.verifier or VerificationPipeline(worktrees=self.worktrees, policy=self.config.policy)
        return HarnessExecutor(store=self.store, worktrees=self.worktrees, backend=self.backend, verifier=verifier, delivery=self.delivery, repository_root=self.root, base_branch=self.config.base_branch)

    def run_once(self) -> ControllerResult:
        if not self.config.enabled:
            return ControllerResult("disabled", reason="config enabled is false")
        if isinstance(self.client, GhClient):
            for existing in self.store.list_runs():
                if existing.state in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.DELIVERING}:
                    reconcile_issue(self.client, existing)
        recovered = recover_stale_runs(self.store)
        if recovered:
            run = recovered[0]
            issue = self.client.get_issue(run.issue_number)
            outcome = self._executor().execute(run.run_id, parse_contract(issue.body))
            return ControllerResult("recovered", issue.number, run.run_id, outcome)
        decision = TaskQueue(self.client).next()
        if decision is None:
            return ControllerResult("idle", reason="no ready task")
        issue = decision.issue
        contract = parse_contract(issue.body)
        environment = os.environ.copy()
        environment.pop("GIT_INDEX_FILE", None)
        base_sha = subprocess.check_output(["git", "rev-parse", f"origin/{self.config.base_branch}"], cwd=self.root, text=True, env=environment).strip()
        run_id = new_run_id()
        lease = None
        if isinstance(self.client, GhClient):
            lease = LeaseManager(self.client, owner_id=self.owner_id).acquire(issue_number=issue.number, run_id=run_id, base_sha=base_sha)
            if lease is None:
                lease = LeaseManager(self.client, owner_id=self.owner_id).takeover_if_expired(issue_number=issue.number, run_id=run_id, base_sha=base_sha)
                if lease is None:
                    return ControllerResult("contended", issue_number=issue.number, reason="another runner owns the lease")
        branch = f"agent/issue-{issue.number}/{run_id[:8]}"
        worktree_path = self.config.worktree_root / run_id
        try:
            run = self.store.create_run(repository=getattr(self.client, "repository", "local/repository"), issue_number=issue.number, contract_hash=self.store.hash_contract(normalized_json(contract)), base_sha=base_sha, branch=branch, worktree=str(worktree_path), backend="default", run_id=run_id)
            self.client.add_label(issue.number, "agent-running")
            outcome = self._executor().execute(run.run_id, contract)
            return ControllerResult("completed", issue.number, run.run_id, outcome)
        except Exception as exc:
            if run_id:
                try:
                    current = self.store.get_run(run_id)
                    if current.state not in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
                        self.store.transition(run_id, RunState.BLOCKED, expected_state=current.state, reason_code="internal_error", reason_detail=str(exc)[:4096])
                except Exception:
                    pass
            return ControllerResult("blocked", issue.number, run_id, reason=str(exc))
        finally:
            if lease is not None:
                try:
                    LeaseManager(self.client, owner_id=self.owner_id).release(lease)
                except GitHubError:
                    pass


def doctor(root: Path, config: HarnessConfig) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for name, command in (("python", [sys.executable, "--version"]), ("git", ["git", "--version"]), ("gh", ["gh", "--version"])):
        try:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False, timeout=10)
            checks.append({"name": name, "ok": result.returncode == 0, "detail": (result.stdout or result.stderr).splitlines()[0] if result.stdout or result.stderr else ""})
        except (OSError, subprocess.TimeoutExpired) as exc:
            checks.append({"name": name, "ok": False, "detail": str(exc)})
    checks.append({"name": "config_enabled", "ok": config.enabled, "detail": "production is disabled" if not config.enabled else "production enabled"})
    return {"ok": all(check["ok"] for check in checks if check["name"] != "config_enabled"), "checks": checks}
