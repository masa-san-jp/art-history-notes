# Agent backends

`agent_harness.backends.base.AgentBackend` is the vendor-neutral boundary. A
backend exposes `probe`, `start`, `wait`, and `cancel`; the harness decides
success from the verified worktree and handoff, not from model prose.

The production implementation is the `command` backend. Its argv is loaded
only from `config/agent-harness.yaml`; Issue text cannot add commands or flags.
The only substitutions are `{worktree}`, `{prompt_file}`, `{events_file}`,
`{handoff_file}`, `{attempt}`, and `{run_id}`. The process is started with
`shell=False`, a bounded timeout/output budget, and the contract/repository
environment intersection.

The checked-in example uses:

```yaml
prompt_mode: stdin
argv: [codex, exec, --ephemeral, --ask-for-approval, never, --sandbox, workspace-write, --cd, "{worktree}", -]
```

The final `-` is Codex CLI's stdin prompt mode. The prompt is also saved as a
run artifact for deterministic replay. A backend must atomically write the
validated `handoff.json` before exiting with success.

`fake` is test-only and deterministic. It is used by CI so no model,
credential, or network access is needed to exercise the complete control loop.
