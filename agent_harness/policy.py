"""Execution policy, diff scope checking, and streaming redaction."""

from __future__ import annotations

from dataclasses import dataclass, field
import fnmatch
import os
from pathlib import PurePosixPath
import re
from typing import Iterable


class PolicyViolation(RuntimeError):
    """An execution request exceeds the configured safety policy."""


_SHELLS = {"sh", "bash", "zsh", "fish", "dash", "ksh", "cmd", "cmd.exe", "powershell", "pwsh"}
_ALWAYS_FORBIDDEN = (".git", ".agent-harness")
_SECRET_PATHS = {".env", ".env.local", ".env.production", "credentials.json", "token.json"}


@dataclass(frozen=True)
class ExecutionPolicy:
    allowed_commands: frozenset[str] = frozenset({"git", "python", "python3", "uv", "codex", "claude"})
    max_output_bytes: int = 10 * 1024 * 1024
    max_timeout_seconds: int = 4 * 60 * 60
    allowed_env: frozenset[str] = frozenset()
    secrets: tuple[str, ...] = field(default_factory=tuple)

    def validate_argv(self, argv: list[str] | tuple[str, ...]) -> None:
        if not argv or any(not isinstance(part, str) or not part or "\x00" in part for part in argv):
            raise PolicyViolation("argv must be a non-empty NUL-free string sequence")
        executable = os.path.basename(argv[0])
        if executable in _SHELLS:
            raise PolicyViolation("shell execution is forbidden")
        if executable not in self.allowed_commands:
            raise PolicyViolation(f"command is not allowlisted: {executable}")
        if executable == "git" and any(part in {"reset", "clean", "push", "checkout"} for part in argv[1:]):
            raise PolicyViolation("destructive or external git operations are forbidden for task processes")

    def validate_timeout(self, seconds: int) -> None:
        if not 1 <= seconds <= self.max_timeout_seconds:
            raise PolicyViolation(f"timeout must be between 1 and {self.max_timeout_seconds} seconds")


def _safe_path(path: str) -> bool:
    if not path or "\x00" in path or path.startswith("/") or "\\" in path:
        return False
    parts = PurePosixPath(path).parts
    return ".." not in parts and "." not in parts


def path_in_scope(path: str, include: Iterable[str], exclude: Iterable[str]) -> bool:
    """Match repository-relative POSIX paths against contract glob patterns."""

    if not _safe_path(path):
        return False
    parts = PurePosixPath(path).parts
    if parts and parts[0] in _ALWAYS_FORBIDDEN:
        return False
    if PurePosixPath(path).name in _SECRET_PATHS:
        return False
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in include) and not any(
        fnmatch.fnmatchcase(path, pattern) for pattern in exclude
    )


def validate_scope(paths: Iterable[str], include: Iterable[str], exclude: Iterable[str]) -> list[str]:
    violations = sorted({path for path in paths if not path_in_scope(path, include, exclude)})
    if violations:
        raise PolicyViolation("changed paths outside contract scope: " + ", ".join(violations))
    return sorted(set(paths))


class Redactor:
    """Streaming-friendly replacement of configured secret values."""

    def __init__(self, secrets: Iterable[str] = ()) -> None:
        self._secrets = tuple(sorted({secret for secret in secrets if secret}, key=len, reverse=True))

    def text(self, value: str) -> str:
        for secret in self._secrets:
            value = value.replace(secret, "[REDACTED]")
        return value

    def bytes(self, value: bytes) -> bytes:
        return self.text(value.decode("utf-8", errors="replace")).encode("utf-8")


def collect_allowed_environment(source: dict[str, str], names: Iterable[str]) -> dict[str, str]:
    allowed = set(names)
    return {key: value for key, value in source.items() if key in allowed}
