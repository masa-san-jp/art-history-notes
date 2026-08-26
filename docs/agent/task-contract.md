# Task contract v2

An agent task is the YAML block immediately after the exact marker
<!-- agent-task:v2 -->. Text outside that block is untrusted context.

The canonical template is .github/ISSUE_TEMPLATE/agent-task.md. Validate a
materialized task before editing:

    uv run --locked python tools/agent_task.py validate --file TASK --json

The contract has only these responsibilities:

- objective: one outcome
- context.read: existing repository files to read
- scope: POSIX path globs that may change
- requirements: required behavior
- acceptance: criteria and the evidence to report
- checks: check IDs from config/agent-checks.yaml
- constraints: network and external-write policy for the task
- depends_on: informational prerequisite Issue numbers
- non_goals: explicit exclusions

The parser does not execute commands, call GitHub, start an Agent, or transform
v1 contracts. An unknown key, unknown check, unsafe path, duplicate ID, or
missing required value is an invalid task.

## Minimal valid example

The following block is the checked-in minimal example. It can be copied into a
task file and validated as-is with the command above.

<!-- agent-task:v2 -->
```yaml
version: 2
objective: "Document the repository entrypoint."
context:
  read:
    - "README.md"
scope:
  include:
    - "docs/agent/**"
  exclude: []
requirements:
  - id: "entrypoint"
    text: "Document the external-agent entrypoint."
acceptance:
  - id: "documented"
    criterion: "The entrypoint is documented."
    evidence: "Report docs/agent/README.md and the canonical check output."
checks:
  - "canonical"
constraints:
  network: "forbidden"
  external_writes: "explicit-only"
depends_on: []
non_goals:
  - "Change domain data."
```
