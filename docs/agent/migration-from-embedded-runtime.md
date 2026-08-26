# Migration from the embedded runtime

The former agent-harness runtime treated this repository as an Agent
controller. It started a configured Agent command, polled GitHub Issues,
held leases, stored run state, and created PRs. That execution model is not
part of this repository.

The current model is passive:

- an external Agent owns execution and semantic task interpretation;
- the repository owns instructions, task contract validation, baseline,
  scope and secret checks, fixed verification, and completion evidence;
- the user or external Agent chooses whether to commit, push, or create a PR.

No AGENT_HARNESS_ENABLED variable, GitHub Environment, backend credential,
Agent CLI, scheduler, remote callback, or GitHub write permission is needed
to use the current interface. Existing Issues and historical commits are
retained as history; they are not current runtime specifications.
