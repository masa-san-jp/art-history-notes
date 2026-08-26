# Architecture and responsibility boundary

## Components

| Component | Owns | Does not own |
| --- | --- | --- |
| Repository harness | instructions, task contract, baseline, scope guard, secret scan, fixed checks | Agent process, model, credentials, scheduling |
| External Agent | task interpretation, repository edits, semantic evidence, completion report | bypassing contract or scope |
| Task source | objective, context, requirements, acceptance, checks, non-goals | executable commands or credentials |
| Git workspace | source files, generated files, local session evidence | hidden remote state |
| Optional CI | read-only repetition of local checks | production agent execution or delivery |

## Deliberate non-features

The repository never starts Codex, Claude, another model, or an arbitrary command supplied
by an Issue. It does not poll Issues, hold distributed leases, maintain a run ledger, create
PRs, or push branches. Those are execution-environment or delivery concerns outside this
repository.

## Data boundary

The task parser consumes only the v2 YAML block after the exact task marker. Text outside the
block is untrusted context. Baseline sessions store hashes and paths, not file contents or
environment-variable values. Verification output redacts credential-shaped values and never
prints the detected value.

## Change boundary

The external Agent may change only the task scope. Existing dirty files are recorded before
the task and are preserved as pre-existing state unless the Agent changes them again. A task
cannot grant itself a new command, environment variable, scope, or external write permission.
