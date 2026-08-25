# Agent harness

The harness turns a bounded `agent-task` Issue into one resumable run. The
public entrypoint is:

```bash
uv run --locked python -m agent_harness --help
uv run --locked python -m agent_harness task validate --file .github/ISSUE_TEMPLATE/agent-task.md
uv run --locked python -m agent_harness controller doctor --json
uv run --locked python -m agent_harness controller serve --once
```

Production is disabled by default in `config/agent-harness.yaml`. Enable it
only after the backend command, `PATH`, GitHub permissions, required labels,
and protected `agent-harness` environment have been configured.

The runtime database, worktrees, prompts, handoffs, and logs live below
`.agent-harness/` and are intentionally not committed. The canonical
repository check remains:

```bash
uv run --locked python tools/verify.py
```

The `agent-harness-ci` workflow runs local harness tests with no model or
secret. The production workflow requires the repository variable
`AGENT_HARNESS_ENABLED=true` and uses one dispatcher concurrency group plus
the per-Issue Git lease.
