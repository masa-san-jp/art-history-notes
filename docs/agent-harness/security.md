# Agent harness security boundary

Issue bodies are untrusted data. Contracts are parsed from the marked YAML
fence and never evaluated as shell text. Backend and verification commands are
argv arrays, `shell=False`, and run in a dedicated worktree.

The effective environment is the intersection of the repository policy and the
contract's `permissions.allowed_env`. Credential values are never stored in a
contract, prompt, event, artifact, Issue, or PR. Configure only approved
variable names and keep their values in the protected runner environment.

After the handoff is validated, the harness checks that every changed path is
inside `scope.include` and outside `scope.exclude`. `.git`, `.agent-harness`,
credential filenames, absolute paths, `..`, and symlink targets outside the
worktree are rejected. A high-confidence credential pattern or configured
secret in a changed file blocks delivery and emits only a redacted reason.

Process groups are terminated on timeout, cancel, lease loss, or output limit.
The backend allowlist rejects shells and destructive external Git operations.
The canonical repository verification remains the final verification stage.
