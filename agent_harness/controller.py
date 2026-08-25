"""Single-cycle controller for queue -> claim -> execute."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import socket
import subprocess
import sys
import shutil
from typing import Any, Callable

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
from .recovery import stale_runs
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
    backend_prompt_mode: str = "file"
    lease_ttl_seconds: int = 600
    stale_after_seconds: int = 900
    heartbeat_interval_seconds: float = 30.0

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
            backend_prompt_mode=str(backend.get("prompt_mode", "file")),
            lease_ttl_seconds=int(value.get("lease_ttl_seconds", 600)),
            stale_after_seconds=int(value.get("stale_after_seconds", 900)),
            heartbeat_interval_seconds=float(value.get("heartbeat_interval_seconds", 30.0)),
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
        return CommandBackend(list(self.config.backend_argv), prompt_mode=self.config.backend_prompt_mode, policy=self.config.policy, env_names=set(self.config.policy.allowed_env))

    def _executor(self, *, lease_heartbeat: Callable[[], None] | None = None) -> HarnessExecutor:
        verifier = self.verifier or VerificationPipeline(worktrees=self.worktrees, policy=self.config.policy)
        return HarnessExecutor(
            store=self.store,
            worktrees=self.worktrees,
            backend=self.backend,
            verifier=verifier,
            delivery=self.delivery,
            repository_root=self.root,
            base_branch=self.config.base_branch,
            lease_heartbeat=lease_heartbeat,
            heartbeat_interval_seconds=self.config.heartbeat_interval_seconds,
        )

    def _acquire_lease(self, *, issue_number: int, run_id: str, base_sha: str) -> tuple[LeaseManager, Any] | None:
        if not isinstance(self.client, GhClient):
            return None
        manager = LeaseManager(self.client, owner_id=self.owner_id, ttl_seconds=self.config.lease_ttl_seconds)
        lease = manager.acquire(issue_number=issue_number, run_id=run_id, base_sha=base_sha)
        if lease is None:
            lease = manager.takeover_if_expired(issue_number=issue_number, run_id=run_id, base_sha=base_sha)
        if lease is None:
            return None
        return manager, lease

    def _lease_heartbeat(self, manager: LeaseManager, lease_holder: list[Any], *, run_id: str, base_sha: str) -> Callable[[], None]:
        def heartbeat() -> None:
            lease_holder[0] = manager.heartbeat(lease_holder[0], base_sha=base_sha)
            self.store.heartbeat(run_id, lease_expires_at=lease_holder[0].expires_at)
            self.store.heartbeat_lease(run_id, heartbeat_at=lease_holder[0].heartbeat_at, expires_at=lease_holder[0].expires_at)

        return heartbeat

    def execute_issue(self, issue_number: int) -> ControllerResult:
        """Execute one explicitly selected ready Issue."""
        issue = self.client.get_issue(issue_number)
        decision = TaskQueue(self.client).next([issue])
        if decision is None or decision.issue.number != issue_number:
            return ControllerResult("blocked", issue_number=issue_number, reason="issue is not ready")
        contract = parse_contract(issue.body)
        environment = os.environ.copy()
        environment.pop("GIT_INDEX_FILE", None)
        base = subprocess.run(["git", "rev-parse", f"origin/{self.config.base_branch}"], cwd=self.root, env=environment, capture_output=True, text=True, check=False, timeout=10)
        if base.returncode:
            return ControllerResult("blocked", issue_number=issue_number, reason=base.stderr.strip() or "base branch is unavailable")
        base_sha = base.stdout.strip()
        run_id = new_run_id()
        lease_manager = None
        lease_holder: list[Any] = []
        if isinstance(self.client, GhClient):
            acquired = self._acquire_lease(issue_number=issue.number, run_id=run_id, base_sha=base_sha)
            if acquired is None:
                return ControllerResult("contended", issue_number=issue.number, reason="another runner owns the lease")
            lease_manager, lease = acquired
            lease_holder.append(lease)
        try:
            run = self.store.create_run(repository=getattr(self.client, "repository", "local/repository"), issue_number=issue.number, contract_hash=self.store.hash_contract(normalized_json(contract)), base_sha=base_sha, branch=f"agent/issue-{issue.number}/{run_id[:8]}", worktree=str(self.config.worktree_root / run_id), backend="default", run_id=run_id)
            if lease_holder:
                self.store.record_lease(run.run_id, owner_id=lease_holder[0].owner_id, token_hash=lease_holder[0].token_hash or hashlib.sha256(lease_holder[0].token.encode()).hexdigest(), acquired_at=lease_holder[0].acquired_at, heartbeat_at=lease_holder[0].heartbeat_at, expires_at=lease_holder[0].expires_at)
            self.client.add_label(issue.number, "agent-running")
            heartbeat = self._lease_heartbeat(lease_manager, lease_holder, run_id=run.run_id, base_sha=run.base_sha) if lease_manager else None
            outcome = self._executor(lease_heartbeat=heartbeat).execute(run.run_id, contract)
            return ControllerResult("completed", issue.number, run.run_id, outcome)
        except Exception as exc:
            try:
                current = self.store.get_run(run_id)
                if current.state not in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.CANCELLED}:
                    self.store.transition(run_id, RunState.BLOCKED, expected_state=current.state, reason_code="internal_error", reason_detail=str(exc)[:4096])
            except Exception:
                pass
            return ControllerResult("blocked", issue.number, run_id, reason=str(exc))
        finally:
            if lease_manager and lease_holder:
                try:
                    lease_manager.release(lease_holder[0])
                    self.store.release_lease(run_id, owner_id=lease_holder[0].owner_id, token_hash=lease_holder[0].token_hash or hashlib.sha256(lease_holder[0].token.encode()).hexdigest())
                except GitHubError:
                    pass

    def execute_run(self, run_id: str) -> ControllerResult:
        """Execute a previously claimed run while preserving its identity."""
        run = self.store.get_run(run_id)
        if run.state not in {RunState.DISCOVERED, RunState.PREPARING, RunState.RETRY_WAIT}:
            return ControllerResult("blocked", run.issue_number, run_id, reason=f"run state {run.state.value} is not executable")
        issue = self.client.get_issue(run.issue_number)
        contract = parse_contract(issue.body)
        lease_manager = None
        lease_holder: list[Any] = []
        if isinstance(self.client, GhClient):
            lease_manager = LeaseManager(self.client, owner_id=self.owner_id, ttl_seconds=self.config.lease_ttl_seconds)
            lease = lease_manager.load_owned(issue_number=run.issue_number, run_id=run_id)
            if lease is None:
                acquired = self._acquire_lease(issue_number=run.issue_number, run_id=run_id, base_sha=run.base_sha)
                if acquired is None:
                    return ControllerResult("contended", run.issue_number, run_id, reason="another runner owns the lease")
                lease_manager, lease = acquired
            lease_holder.append(lease)
            self.store.record_lease(run_id, owner_id=lease.owner_id, token_hash=lease.token_hash or hashlib.sha256(lease.token.encode()).hexdigest(), acquired_at=lease.acquired_at, heartbeat_at=lease.heartbeat_at, expires_at=lease.expires_at)
        try:
            heartbeat = self._lease_heartbeat(lease_manager, lease_holder, run_id=run_id, base_sha=run.base_sha) if lease_manager else None
            outcome = self._executor(lease_heartbeat=heartbeat).execute(run_id, contract)
            return ControllerResult("completed", run.issue_number, run_id, outcome)
        finally:
            if lease_manager and lease_holder:
                try:
                    lease_manager.release(lease_holder[0])
                    self.store.release_lease(run_id, owner_id=lease_holder[0].owner_id, token_hash=lease_holder[0].token_hash or hashlib.sha256(lease_holder[0].token.encode()).hexdigest())
                except GitHubError:
                    pass

    def run_once(self) -> ControllerResult:
        if not self.config.enabled:
            return ControllerResult("disabled", reason="config enabled is false")
        if isinstance(self.client, GhClient):
            for existing in self.store.list_runs():
                if existing.state in {RunState.SUCCEEDED, RunState.BLOCKED, RunState.FAILED, RunState.DELIVERING}:
                    reconcile_issue(self.client, existing)
        for stale in stale_runs(self.store, stale_after_seconds=self.config.stale_after_seconds):
            lease_manager = None
            lease_holder: list[Any] = []
            if isinstance(self.client, GhClient):
                acquired = self._acquire_lease(issue_number=stale.issue_number, run_id=stale.run_id, base_sha=stale.base_sha)
                if acquired is None:
                    continue
                lease_manager, lease = acquired
                lease_holder.append(lease)
            try:
                run = self.store.recover_run(stale.run_id, reason="heartbeat expired; process ownership was not live")
                self.store.record_lease(run.run_id, owner_id=lease_holder[0].owner_id, token_hash=hashlib.sha256(lease_holder[0].token.encode()).hexdigest(), acquired_at=lease_holder[0].acquired_at, heartbeat_at=lease_holder[0].heartbeat_at, expires_at=lease_holder[0].expires_at) if lease_holder else None
                issue = self.client.get_issue(run.issue_number)
                heartbeat = self._lease_heartbeat(lease_manager, lease_holder, run_id=run.run_id, base_sha=run.base_sha) if lease_manager else None
                outcome = self._executor(lease_heartbeat=heartbeat).execute(run.run_id, parse_contract(issue.body))
                return ControllerResult("recovered", issue.number, run.run_id, outcome)
            finally:
                if lease_manager and lease_holder:
                    try:
                        lease_manager.release(lease_holder[0])
                        self.store.release_lease(stale.run_id, owner_id=lease_holder[0].owner_id, token_hash=hashlib.sha256(lease_holder[0].token.encode()).hexdigest())
                    except GitHubError:
                        pass
        decision = TaskQueue(self.client).next()
        if decision is None:
            return ControllerResult("idle", reason="no ready task")
        return self.execute_issue(decision.issue.number)


def doctor(root: Path, config: HarnessConfig) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    def add(name: str, ok: bool, detail: str, code: str) -> None:
        checks.append({"name": name, "ok": ok, "code": code, "detail": detail})

    environment = os.environ.copy()
    environment.pop("GIT_INDEX_FILE", None)
    for name, command in (("python", [sys.executable, "--version"]), ("uv", ["uv", "--version"]), ("git", ["git", "--version"]), ("gh", ["gh", "--version"])):
        try:
            result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, check=False, timeout=10)
            add(name, result.returncode == 0, (result.stdout or result.stderr).splitlines()[0] if result.stdout or result.stderr else "", f"{name}_unavailable" if result.returncode else f"{name}_ready")
        except (OSError, subprocess.TimeoutExpired) as exc:
            add(name, False, str(exc), f"{name}_unavailable")
    try:
        auth = subprocess.run(["gh", "auth", "status"], cwd=root, env=environment, capture_output=True, text=True, check=False, timeout=10)
        add("github_auth", auth.returncode == 0, (auth.stdout or auth.stderr).splitlines()[0] if auth.stdout or auth.stderr else "", "github_auth_missing" if auth.returncode else "github_auth_ready")
    except (OSError, subprocess.TimeoutExpired) as exc:
        add("github_auth", False, str(exc), "github_auth_missing")
    labels_path = root / ".github" / "labels.yml"
    required_labels = {"agent-task", "agent-running", "agent-review", "agent-blocked", "agent-done"}
    try:
        labels = yaml.safe_load(labels_path.read_text(encoding="utf-8")) or []
        names = {str(item.get("name")) for item in labels if isinstance(item, dict)}
        add("required_labels", required_labels.issubset(names), ", ".join(sorted(required_labels - names)) or "all configured", "required_labels_missing" if not required_labels.issubset(names) else "required_labels_ready")
    except (OSError, yaml.YAMLError, TypeError) as exc:
        add("required_labels", False, str(exc), "required_labels_missing")
    state_parent_ok = root.is_dir() and os.access(root, os.W_OK)
    add("state_db_parent", state_parent_ok, f"{config.state_db.parent} (created on first run)" if state_parent_ok else str(config.state_db.parent), "state_db_parent_missing" if not state_parent_ok else "state_db_parent_ready")
    if config.backend_type == "fake":
        add("backend_config", True, "fake backend", "backend_fake")
    elif config.backend_type == "command":
        argv_ok = bool(config.backend_argv)
        binary = config.backend_argv[0] if config.backend_argv else ""
        binary_ok = bool(shutil.which(binary)) if binary else False
        add("backend_config", argv_ok and binary_ok, binary or "backend argv is empty", "backend_unavailable" if not (argv_ok and binary_ok) else "backend_ready")
        prompt_ok = config.backend_prompt_mode in {"file", "stdin"}
        if config.backend_prompt_mode == "stdin":
            prompt_ok = prompt_ok and "-" in config.backend_argv
        add("backend_prompt_transport", prompt_ok, config.backend_prompt_mode, "backend_prompt_invalid" if not prompt_ok else "backend_prompt_ready")
    else:
        add("backend_config", False, f"unsupported backend type: {config.backend_type}", "backend_type_invalid")
    lease_ok = config.lease_ttl_seconds >= 30 and 0 < config.heartbeat_interval_seconds < config.lease_ttl_seconds and config.stale_after_seconds >= config.lease_ttl_seconds
    add("lease_config", lease_ok, f"ttl={config.lease_ttl_seconds}s stale_after={config.stale_after_seconds}s heartbeat={config.heartbeat_interval_seconds}s", "lease_config_invalid" if not lease_ok else "lease_config_ready")
    try:
        result = subprocess.run(["git", "rev-parse", "--verify", f"refs/remotes/origin/{config.base_branch}"], cwd=root, env=environment, capture_output=True, text=True, check=False, timeout=10)
        add("base_ref", result.returncode == 0, f"origin/{config.base_branch}", "base_ref_missing" if result.returncode else "base_ref_ready")
    except (OSError, subprocess.TimeoutExpired) as exc:
        add("base_ref", False, str(exc), "base_ref_missing")
    add("config_enabled", config.enabled, "production is disabled" if not config.enabled else "production enabled", "production_disabled" if not config.enabled else "production_enabled")
    return {"ok": all(check["ok"] for check in checks if check["name"] != "config_enabled"), "checks": checks}
