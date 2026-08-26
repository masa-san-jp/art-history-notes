"""Small repository-local safety primitives for the external-agent interface."""

from __future__ import annotations

from dataclasses import dataclass
import fnmatch
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_ROOTS = {".git", ".agent-local"}
FORBIDDEN_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "token.json",
    "id_rsa",
    "id_ed25519",
}
SECRET_PATTERNS = (
    re.compile(rb"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    re.compile(rb"\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", re.IGNORECASE),
)


@dataclass(frozen=True)
class FileState:
    path: str
    kind: str
    content_sha256: str | None

    def as_dict(self) -> dict[str, str | None]:
        return {"path": self.path, "kind": self.kind, "content_sha256": self.content_sha256}


def run_git(args: list[str], *, root: Path = ROOT) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def relative_path(path: str) -> str:
    if not path or "\x00" in path or path.startswith("/") or "\\" in path:
        raise ValueError("path must be a non-empty relative POSIX path")
    pure = PurePosixPath(path)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError("path must stay inside the repository")
    return pure.as_posix()


def content_sha(path: Path) -> str | None:
    if path.is_symlink():
        return hashlib.sha256(("symlink:" + os.readlink(path)).encode("utf-8", errors="surrogateescape")).hexdigest()
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _status_paths(root: Path) -> list[tuple[str, str]]:
    result = run_git(["status", "--porcelain=v1", "--untracked-files=all", "-z"], root=root)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git status failed")
    fields = result.stdout.split(b"\0")
    paths: list[tuple[str, str]] = []
    index = 0
    while index < len(fields):
        raw = fields[index]
        index += 1
        if not raw:
            continue
        text = raw.decode("utf-8", errors="surrogateescape")
        if len(text) < 4:
            continue
        status, path = text[:2], text[3:]
        paths.append((path, status))
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            if index < len(fields) and fields[index]:
                paths.append((fields[index].decode("utf-8", errors="surrogateescape"), "rename-source"))
                index += 1
    return paths


def _diff_paths(root: Path, base_sha: str) -> list[str]:
    result = run_git(["diff", "--no-renames", "--name-only", "-z", base_sha, "--"], root=root)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace").strip() or "git diff failed")
    return [field.decode("utf-8", errors="surrogateescape") for field in result.stdout.split(b"\0") if field]


def _local_paths(root: Path) -> set[str]:
    local_root = root / ".agent-local"
    if not local_root.exists() or local_root.is_symlink():
        return {".agent-local"} if local_root.is_symlink() else set()
    paths: set[str] = set()
    for current, directories, files in os.walk(local_root, followlinks=False):
        current_path = Path(current)
        for name in (*directories, *files):
            candidate = current_path / name
            try:
                paths.add(relative_path(candidate.relative_to(root).as_posix()))
            except ValueError:
                continue
        directories[:] = [name for name in directories if not (current_path / name).is_symlink()]
    return paths


def file_states(root: Path = ROOT, *, base_sha: str | None = None) -> dict[str, FileState]:
    paths = {path for path, _ in _status_paths(root)}
    paths.update(_local_paths(root))
    if base_sha is not None:
        paths.update(_diff_paths(root, base_sha))
    states: dict[str, FileState] = {}
    for raw_path in paths:
        try:
            path = relative_path(raw_path)
        except ValueError:
            continue
        candidate = root / path
        kind = "symlink" if candidate.is_symlink() else "file" if candidate.is_file() else "missing"
        states[path] = FileState(path, kind, content_sha(candidate))
    return states


def secret_finding(data: bytes) -> str | None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(data):
            return "credential-shaped value detected"
    return None


def path_forbidden(path: str) -> str | None:
    try:
        clean = relative_path(path)
    except ValueError:
        return "unsafe_path"
    parts = PurePosixPath(clean).parts
    if parts and parts[0] in FORBIDDEN_ROOTS:
        return "forbidden_path"
    name = PurePosixPath(clean).name
    if name in FORBIDDEN_NAMES or name.startswith(".env.") or name.endswith((".pem", ".key")):
        return "secret_path"
    return None


def symlink_component(root: Path, path: str) -> bool:
    """Return whether the path or one of its parents is a symlink."""

    clean = relative_path(path)
    candidate = root
    for part in PurePosixPath(clean).parts:
        candidate /= part
        if candidate.is_symlink():
            return True
    return False


def path_in_scope(path: str, include: Iterable[str], exclude: Iterable[str]) -> bool:
    if path_forbidden(path) is not None:
        return False
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in include) and not any(
        fnmatch.fnmatchcase(path, pattern) for pattern in exclude
    )
