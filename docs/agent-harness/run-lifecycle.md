# Agent harness run lifecycle

The local run ledger is `.agent-harness/state.sqlite3`; it is runtime state,
not repository content. Every state change is an append-only event and is
committed in the same SQLite transaction as the run update.

The normal path is:

```text
discovered -> claimed -> preparing -> running -> verifying -> delivering -> succeeded
```

`running` and `verifying` may enter `retry_wait` before a later attempt returns
to `running`. Any non-terminal state can become `blocked`, `failed`, or
`cancelled`. Terminal states cannot be changed. `run resume` is the explicit
operator action that moves a `blocked` or `failed` run to `preparing` while
keeping the original run ID.

Retry waits use bounded exponential delays (`2, 4, 8, ...` seconds, capped by
policy), while the current run heartbeat remains active. Lease loss or a
cancel request stops backend/verification work before delivery.

The ledger stores the Issue number, contract hash, base SHA, branch, worktree,
backend, attempt, heartbeat, lease deadline, reason, pull request number, and
all event/artifact references. A partial unique index prevents more than one
non-terminal run for the same repository and Issue.

## Commands

```bash
uv run --locked python -m agent_harness run list --json
uv run --locked python -m agent_harness run show RUN_ID --json
uv run --locked python -m agent_harness run events RUN_ID --jsonl
uv run --locked python -m agent_harness run resume RUN_ID --reason "operator confirmed the dependency"
uv run --locked python -m agent_harness run cancel RUN_ID --reason "stop the deployment"
uv run --locked python -m agent_harness run execute --run-id RUN_ID --runner-id RUNNER_ID
uv run --locked python -m agent_harness run execute --issue ISSUE_NUMBER --runner-id RUNNER_ID
```
