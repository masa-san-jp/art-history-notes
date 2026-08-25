# Failure and recovery

Each attempt records backend completion, verification stages, diagnostics, and
artifacts in the append-only run ledger. Verification is fail-fast:

1. handoff schema and completed status;
2. changed-path scope and symlink safety;
3. secret scan;
4. contract checks in declared order;
5. canonical `uv run --locked python tools/verify.py`;
6. final manifest.

Transient backend/GitHub/infrastructure failures and ordinary verification
failures may retry within `limits.max_attempts`, using bounded exponential
backoff. Invalid tasks, policy violations, secret findings, lease loss, and
cancel requests do not retry. A lease loss blocks the run before delivery.

On startup, only runs whose heartbeat is older than `stale_after_seconds` are
considered. The controller reacquires the corresponding GitHub lease before
moving one back to `preparing`; it does not resume a run while another owner
still holds the lease. The run ID, branch, worktree, attempt history, and
artifacts remain available for operator investigation.
