"""Dedicated git worktrees and diff manifest helpers."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess

from .policy import PolicyViolation, validate_scope


class WorktreeError(RuntimeError):
    """A worktree cannot be created, inspected, or removed safely."""


def _git_environment() -> dict[str, str]:
    environment = os.environ.copy()
    # git commit hooks expose their temporary index to child processes. A
    # harness subprocess may operate on a separate repository/worktree and
    # must use that repository's own index instead.
    environment.pop("GIT_INDEX_FILE", None)
    return environment


def _git(args: list[str], *, cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True, timeout=timeout, env=_git_environment())
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorktreeError(f"git command failed to start: {exc}") from exc
    if result.returncode:
        raise WorktreeError(result.stderr.strip() or f"git command failed: {' '.join(args)}")
    return result


@dataclass(frozen=True)
class Worktree:
    path: Path
    branch: str
    base_sha: str


class WorktreeManager:
    def __init__(self, repository: Path, root: Path) -> None:
        self.repository = repository.resolve()
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, *, run_id: str, branch: str, base_sha: str) -> Worktree:
        if "/" not in branch or branch.startswith("-"):
            raise WorktreeError("branch must be a namespaced non-option ref")
        path = (self.root / run_id).resolve()
        if self.root not in path.parents:
            raise WorktreeError("worktree path escapes configured root")
        if path.exists():
            current = _git(["rev-parse", "HEAD"], cwd=path).stdout.strip()
            if current != base_sha:
                raise WorktreeError("existing worktree does not match recorded base SHA")
            return Worktree(path, branch, base_sha)
        _git(["worktree", "add", "-b", branch, str(path), base_sha], cwd=self.repository)
        return Worktree(path, branch, base_sha)

    def changed_paths(self, worktree: Worktree) -> list[str]:
        tracked = _git(["diff", "--name-only", "-z", worktree.base_sha, "--"], cwd=worktree.path).stdout
        untracked = _git(["ls-files", "--others", "--exclude-standard", "-z"], cwd=worktree.path).stdout
        values = [item for item in (tracked + untracked).split("\x00") if item]
        if any("\x00" in item or os.path.isabs(item) or ".." in Path(item).parts for item in values):
            raise PolicyViolation("git returned an unsafe changed path")
        return sorted(set(values))

    def manifest(self, worktree: Worktree, *, include: list[str], exclude: list[str]) -> list[str]:
        return validate_scope(self.changed_paths(worktree), include, exclude)

    def cleanup(self, worktree: Worktree, *, allow: bool) -> None:
        if not allow:
            raise WorktreeError("cleanup requires an explicit terminal-run permission")
        path = worktree.path.resolve()
        if self.root not in path.parents:
            raise WorktreeError("refusing to remove worktree outside configured root")
        _git(["worktree", "remove", "--force", str(path)], cwd=self.repository)
