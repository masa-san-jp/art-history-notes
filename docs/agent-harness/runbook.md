# Agent harness runbook

## Setup

```bash
uv sync --frozen
uv run --locked python -m agent_harness labels sync --dry-run
uv run --locked python -m agent_harness controller doctor --json
```

Set up the five `agent-*` labels with the explicit apply command only after
reviewing the dry-run output:

```bash
uv run --locked python -m agent_harness labels sync --apply
```

Configure the backend argv and its prompt transport in `config/agent-harness.yaml`.
The checked-in Codex backend uses `codex exec ... -` with `prompt_mode: stdin`;
the final `-` is required because Codex reads the prompt from standard input.
Keep credentials in the protected environment or an explicitly approved
environment variable name; never put credential values in an Issue, config
file, prompt, or artifact. Production remains disabled until
`AGENT_HARNESS_ENABLED=true` is set as a repository variable.

`doctor --json` checks the executable, GitHub authentication, required labels,
stdin transport, lease timing, runtime DB parent, and `origin/<base_branch>`.
Each check has a stable `code`; its top-level `ok` intentionally ignores the
separate `config_enabled` gate, so a disabled harness can still be validated
before activation. Do not activate until every prerequisite check is green and
the backend authentication has been installed in the protected environment.

## Observe and operate

```bash
uv run --locked python -m agent_harness queue list --json
uv run --locked python -m agent_harness run list --json
uv run --locked python -m agent_harness run show RUN_ID --json
uv run --locked python -m agent_harness run events RUN_ID --jsonl
uv run --locked python -m agent_harness run resume RUN_ID --reason "operator resolution"
uv run --locked python -m agent_harness run cancel RUN_ID --reason "stop execution"
```

For a local polling controller, use `controller serve --poll-seconds 60`.
SIGINT/SIGTERM finishes the current cycle and emits a stopped result; it does
not claim another Issue. The durable run heartbeat and lease determine whether
the next controller may recover the run.

`blocked` and `failed` runs are retained for evidence. Resume preserves the
run ID and creates a new attempt. Do not delete the SQLite database while a
runner is active.

While an attempt is running, the controller refreshes both the local run
heartbeat and the GitHub per-Issue lease. If lease ownership is lost, the
backend is cancelled and the run becomes `blocked` without delivery. A stale
run is only recovered after the controller reacquires or safely takes over its
expired GitHub lease; an active lease leaves the run untouched for its owner.

## Incident stop and recovery

Set `AGENT_HARNESS_ENABLED=false` before investigating a production incident.
The dispatcher will finish no new claim. Inspect stale leases and run
heartbeats, then use the recorded worktree path and run ID. A stale lease must
be reclaimed only after the documented TTL and ownership check. Preserve the
failed worktree until the Issue report is complete.

SQLite backups must be taken while the controller is stopped. Apply migrations
by starting the versioned harness against the backup copy first. Rotate
backend credentials in the protected environment, then run `doctor --json`.

## Uninstall

Disable the workflow and remove the repository variable. Retain `.agent-harness`
for incident evidence until all runs are terminal; remove only the explicit
runtime directory after evidence retention is complete.
