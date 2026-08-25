"""Atomic Git reference leases for distributed GitHub runners."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import secrets
from typing import Any

from .github import GhClient, GitHubError


@dataclass(frozen=True)
class Lease:
    repository: str
    issue_number: int
    run_id: str
    owner_id: str
    token: str
    ref: str
    commit_sha: str
    acquired_at: str
    heartbeat_at: str
    expires_at: str


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


class LeaseManager:
    def __init__(self, client: GhClient, *, owner_id: str, ttl_seconds: int = 600) -> None:
        if ttl_seconds < 30:
            raise ValueError("lease TTL must be at least 30 seconds")
        self.client = client
        self.owner_id = owner_id
        self.ttl_seconds = ttl_seconds

    def acquire(self, *, issue_number: int, run_id: str, base_sha: str) -> Lease | None:
        acquired = _now()
        expires = acquired + timedelta(seconds=self.ttl_seconds)
        token = secrets.token_urlsafe(32)
        ref = f"refs/heads/agent-harness/leases/issue-{issue_number}"
        tree = self.client.get_commit_tree(base_sha)
        message = json.dumps({"version": 1, "issue": issue_number, "run_id": run_id, "owner_id": self.owner_id, "token_sha256": hashlib.sha256(token.encode()).hexdigest(), "acquired_at": _stamp(acquired), "heartbeat_at": _stamp(acquired), "expires_at": _stamp(expires), "base_sha": base_sha}, sort_keys=True)
        commit_sha = self.client.create_commit(message=message, tree=tree, parent=base_sha)
        try:
            self.client.create_ref(ref, commit_sha)
        except GitHubError as exc:
            if exc.status in {409, 422} or "already exists" in str(exc).lower():
                return None
            raise
        return Lease(self.client.repository, issue_number, run_id, self.owner_id, token, ref, commit_sha, _stamp(acquired), _stamp(acquired), _stamp(expires))

    def takeover_if_expired(self, *, issue_number: int, run_id: str, base_sha: str) -> Lease | None:
        ref = f"refs/heads/agent-harness/leases/issue-{issue_number}"
        current = self.client.get_ref(ref)
        if not current:
            return self.acquire(issue_number=issue_number, run_id=run_id, base_sha=base_sha)
        sha = current.get("object", {}).get("sha")
        if not sha:
            return None
        try:
            payload = json.loads(self.client.get_commit_message(sha))
            expires_at = datetime.fromisoformat(str(payload["expires_at"]).replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return None
        if expires_at >= _now():
            return None
        confirmation = self.client.get_ref(ref)
        if not confirmation or confirmation.get("object", {}).get("sha") != sha:
            return None
        self.client.delete_ref(ref)
        return self.acquire(issue_number=issue_number, run_id=run_id, base_sha=base_sha)

    def heartbeat(self, lease: Lease, *, base_sha: str) -> Lease:
        current = self.client.get_ref(lease.ref)
        if not current or current.get("object", {}).get("sha") != lease.commit_sha:
            raise GitHubError("lease ownership was lost")
        now = _now()
        expires = now + timedelta(seconds=self.ttl_seconds)
        tree = self.client.get_commit_tree(base_sha)
        message = json.dumps({"version": 1, "issue": lease.issue_number, "run_id": lease.run_id, "owner_id": lease.owner_id, "token_sha256": hashlib.sha256(lease.token.encode()).hexdigest(), "acquired_at": lease.acquired_at, "heartbeat_at": _stamp(now), "expires_at": _stamp(expires), "base_sha": base_sha}, sort_keys=True)
        commit_sha = self.client.create_commit(message=message, tree=tree, parent=lease.commit_sha)
        self.client.update_ref(lease.ref, commit_sha, force=False)
        return Lease(lease.repository, lease.issue_number, lease.run_id, lease.owner_id, lease.token, lease.ref, commit_sha, lease.acquired_at, _stamp(now), _stamp(expires))

    def release(self, lease: Lease) -> None:
        current = self.client.get_ref(lease.ref)
        if current and current.get("object", {}).get("sha") == lease.commit_sha:
            self.client.delete_ref(lease.ref)
