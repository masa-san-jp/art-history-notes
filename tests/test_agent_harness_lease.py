from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import unittest

from agent_harness.github import GitHubError
from agent_harness.lease import LeaseManager, _stamp


class FakeLeaseClient:
    repository = "local/repository"

    def __init__(self) -> None:
        self.refs: dict[str, dict[str, str]] = {}
        self.messages: dict[str, str] = {}
        self.counter = 0

    def get_commit_tree(self, sha):
        return "tree"

    def create_commit(self, *, message, tree, parent):
        self.counter += 1
        sha = f"sha-{self.counter}"
        self.messages[sha] = message
        return sha

    def create_ref(self, ref, sha):
        if ref in self.refs:
            raise GitHubError("already exists", status=422)
        self.refs[ref] = {"object": {"sha": sha}}

    def get_ref(self, ref):
        return self.refs.get(ref)

    def get_commit_message(self, sha):
        return self.messages[sha]

    def update_ref(self, ref, sha, *, force=False):
        self.refs[ref] = {"object": {"sha": sha}}

    def delete_ref(self, ref):
        self.refs.pop(ref, None)


class LeaseTests(unittest.TestCase):
    def test_active_lease_blocks_second_owner(self) -> None:
        client = FakeLeaseClient()
        first = LeaseManager(client, owner_id="one").acquire(issue_number=1, run_id="run-1", base_sha="base")
        second = LeaseManager(client, owner_id="two").acquire(issue_number=1, run_id="run-2", base_sha="base")
        self.assertIsNotNone(first)
        self.assertIsNone(second)

    def test_expired_lease_is_taken_over_only_after_same_ref_confirmation(self) -> None:
        client = FakeLeaseClient()
        ref = "refs/heads/agent-harness/leases/issue-1"
        expired = datetime.now(timezone.utc) - timedelta(minutes=5)
        client.messages["old"] = json.dumps({"expires_at": _stamp(expired)})
        client.refs[ref] = {"object": {"sha": "old"}}
        lease = LeaseManager(client, owner_id="new").takeover_if_expired(issue_number=1, run_id="run-2", base_sha="base")
        self.assertEqual(lease.run_id, "run-2")
        self.assertNotEqual(lease.commit_sha, "old")
