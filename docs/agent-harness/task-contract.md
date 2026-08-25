# Agent task contract v1

An eligible task is a GitHub Issue with the `agent-task` label and one
`<!-- agent-task:v1 -->` marker followed immediately by a YAML fence. The
runtime validator is `agent_harness.task_contract`; the interoperability
schema is `config/agent-task.schema.json`.

Validate an Issue or a local template with:

```bash
uv run --locked python -m agent_harness task validate --issue NUMBER
uv run --locked python -m agent_harness task validate --file PATH
```

The output is stable normalized JSON. Exit code 0 means valid, 2 means a
contract violation, and 3 means the GitHub source could not be read.
