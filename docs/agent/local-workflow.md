# Local workflow for an external Agent

The repository is the harness; the Agent is started outside it. The Agent can
be Codex, Claude, another product, or a human. No product credential is part
of this workflow.

## Before editing

    git status --short
    uv sync --locked
    uv run --locked python tools/agent_doctor.py --json
    uv run --locked python tools/agent_task.py validate --file TASK --json
    uv run --locked python tools/agent_session.py begin --task-file TASK --output .agent-local/SESSION.json

The session records the task hash, starting HEAD, and hashes of pre-existing
dirty paths. It never stages, stashes, restores, or deletes a user change.
Do not reuse a session for another task.

## Edit and verify

Read the contract's context and domain documents. Modify only scope.include
minus scope.exclude. Do not edit generated files directly; run their existing
generator.

    uv run --locked python tools/agent_verify.py --task-file TASK --session .agent-local/SESSION.json --json

To cancel a running check, send SIGINT/SIGTERM to the verifier or pass a
local cancel-file path and create that file from the outside:

    uv run --locked python tools/agent_verify.py --task-file TASK --session .agent-local/SESSION.json --cancel-file .agent-local/CANCEL --json

The verifier compares the current worktree to the baseline, rejects forbidden
paths and credential-shaped content, runs the fixed checks from the registry,
and runs canonical verification last. A no-change task is valid when every
check passes and manifest is empty.

## Report

Report changed paths, every check and exit code, evidence for every acceptance
ID, and remaining risks. Say 「なし」 when no risk remains. Do not commit,
push, create a PR, or update an Issue unless the user explicitly requests it.
