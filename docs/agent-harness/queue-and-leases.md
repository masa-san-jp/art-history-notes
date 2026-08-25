# Queue and leases

`TaskQueue` reads open Issues with the `agent-task` label, validates their
contract, resolves dependencies, and sorts ready work by risk, creation time,
and Issue number. Status labels are projections; they are not the lock.

The distributed lock is
`refs/heads/agent-harness/leases/issue-<number>`. The ref points to a commit
whose message contains lease metadata and a token hash. Ref creation is the
atomic claim. HTTP 409/422 means another owner won the race. Heartbeat first
re-reads the ref and then advances it; release deletes it only when the current
ref is still owned by that lease.

The default TTL is 600 seconds and the controller heartbeat is 30 seconds.
Stale recovery requires a local stale heartbeat and a successful lease
reacquisition/takeover. An active remote lease is left untouched. The local
SQLite lease row stores only the token hash and audit timestamps.
