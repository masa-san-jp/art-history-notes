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

Configure the backend argv in `config/agent-harness.yaml`. Keep credentials in
the protected environment or an approved environment variable; never put them
in an Issue, config file, prompt, or artifact. Production remains disabled
until `AGENT_HARNESS_ENABLED=true` is set as a repository variable.

## Observe and operate

```bash
uv run --locked python -m agent_harness queue list --json
uv run --locked python -m agent_harness run list --json
uv run --locked python -m agent_harness run show RUN_ID --json
uv run --locked python -m agent_harness run events RUN_ID --jsonl
uv run --locked python -m agent_harness run resume RUN_ID --reason "operator resolution"
uv run --locked python -m agent_harness run cancel RUN_ID --reason "stop execution"
```

`blocked` and `failed` runs are retained for evidence. Resume preserves the
run ID and creates a new attempt. Do not delete the SQLite database while a
runner is active.

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
