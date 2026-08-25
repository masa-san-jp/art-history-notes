"""Idempotent local git delivery and GitHub result projection."""

from __future__ import annotations

from dataclasses import dataclass
import re
import os
from pathlib import Path
import subprocess
from typing import Any, Protocol

from .github import GitHubClient
from .models import Run


class DeliveryError(RuntimeError):
    """A verified run cannot be delivered safely."""


@dataclass(frozen=True)
class DeliveryResult:
    status: str
    commit_sha: str | None = None
    pr_number: int | None = None
    message: str = ""


class DeliveryAdapter(Protocol):
    def deliver(self, run: Run, *, objective: str, manifest: list[str], worktree: Path, base_branch: str) -> DeliveryResult: ...


def _git(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("GIT_INDEX_FILE", None)
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False, timeout=120, env=environment)
    if result.returncode:
        raise DeliveryError(result.stderr.strip() or "git delivery command failed")
    return result


def _safe_subject(objective: str) -> str:
    compact = re.sub(r"\s+", " ", objective.replace("\n", " ")).strip()
    return compact[:72] or "completed task"


def _commit_for_run(run: Run, *, worktree: Path) -> str | None:
    message = _git(["log", "-1", "--format=%B"], cwd=worktree).stdout
    if f"Agent-Run-ID: {run.run_id}" not in message:
        return None
    if _git(["status", "--porcelain=v2", "--untracked-files=all"], cwd=worktree).stdout.strip():
        raise DeliveryError("run-marked commit exists but worktree is dirty")
    return _git(["rev-parse", "HEAD"], cwd=worktree).stdout.strip()


class GitHubDelivery:
    def __init__(self, repository: Path, client: Any, *, auto_push: bool = True) -> None:
        self.repository = repository
        self.client = client
        self.auto_push = auto_push

    def deliver(self, run: Run, *, objective: str, manifest: list[str], worktree: Path, base_branch: str) -> DeliveryResult:
        manifest = sorted(set(manifest))
        if manifest:
            commit_sha = _commit_for_run(run, worktree=worktree)
            if commit_sha is None:
                _git(["add", "--", *manifest], cwd=worktree)
                staged_raw = _git(["diff", "--cached", "--name-only", "-z", "--"], cwd=worktree).stdout
                staged = sorted(item for item in staged_raw.split("\x00") if item)
                if staged != manifest:
                    raise DeliveryError("staged files differ from verified manifest")
                subject = f"agent(issue #{run.issue_number}): {_safe_subject(objective)}"
                body = f"Agent-Run-ID: {run.run_id}\nAgent-Issue: #{run.issue_number}\nAgent-Base-SHA: {run.base_sha}"
                _git(["-c", "user.name=agent-harness", "-c", "user.email=agent-harness@localhost", "commit", "-m", subject, "-m", body], cwd=worktree)
                commit_sha = _git(["rev-parse", "HEAD"], cwd=worktree).stdout.strip()
            if self.auto_push:
                remote = _git(["ls-remote", "--heads", "origin", run.branch], cwd=worktree).stdout.strip()
                if remote:
                    remote_sha = remote.split()[0]
                    if remote_sha != commit_sha:
                        raise DeliveryError("remote branch exists at a different commit; refusing to overwrite")
                else:
                    _git(["push", "--set-upstream", "origin", run.branch], cwd=worktree)
            pr = self.client.find_or_create_pr(run, objective=objective, base_branch=base_branch)
            self.client.sync_issue(run.issue_number, status="review", pr=pr, message=f"Verified run {run.run_id} delivered in PR #{pr['number']}.")
            return DeliveryResult("review", commit_sha, int(pr["number"]), "PR ready for review")
        self.client.sync_issue(run.issue_number, status="done", pr=None, message=f"Verified run {run.run_id} completed with no changes.")
        return DeliveryResult("done", None, None, "verified no-change completion")


class RecordingDelivery:
    """Deterministic adapter for unit and CI E2E tests."""

    def __init__(self, *, fail_once: bool = False) -> None:
        self.calls: list[tuple[str, list[str]]] = []
        self.fail_once = fail_once

    def deliver(self, run: Run, *, objective: str, manifest: list[str], worktree: Path, base_branch: str) -> DeliveryResult:
        self.calls.append((run.run_id, list(manifest)))
        if self.fail_once and len(self.calls) == 1:
            raise DeliveryError("transient delivery failure")
        return DeliveryResult("done", "0" * 40, None, "recorded")
