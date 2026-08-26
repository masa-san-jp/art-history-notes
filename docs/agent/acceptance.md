# Agent readiness acceptance

The completion command is:

    uv run --locked python tools/test_agent_readiness.py

It runs the public-interface tests and then the repository's canonical
verification. The suite does not start an Agent, call a model, access GitHub,
or require a credential.

| Requirement | Evidence |
| --- | --- |
| Read the repository entrypoint | tests/test_agent_instructions.py |
| Validate a task contract | tests/test_agent_task.py |
| Detect local prerequisites | tests/test_agent_doctor.py |
| Preserve pre-existing dirty work | tests/test_agent_session.py and tests/test_agent_readiness_e2e.py |
| Guard scope and secrets | tests/test_agent_verify.py and tests/test_agent_readiness_e2e.py |
| Run fixed checks only | tests/test_agent_verify.py |
| Complete from a fresh clone | tests/test_agent_readiness_e2e.py |
| Complete without delivery side effects | tests/test_agent_readiness_e2e.py and workflow permissions |
| Preserve domain correctness | tools/verify.py |

## Epic scenario traceability

The seven-step user scenario in Issue #378 is covered as follows.

| Step | Scenario | Evidence |
| --- | --- | --- |
| 1 | Open the repository and read the entrypoint | `tests/test_agent_instructions.py` |
| 2 | Run setup and doctor | `tests/test_agent_doctor.py` and `uv sync --locked` |
| 3 | Validate the task contract | `tests/test_agent_task.py` |
| 4 | Record a baseline without changing existing work | `tests/test_agent_session.py` and E2E dirty-tree case |
| 5 | Edit only the permitted scope and use generators | `tests/test_agent_readiness_e2e.py` in-scope case |
| 6 | Verify scope, secrets, fixed checks, and canonical checks | `tests/test_agent_verify.py` and E2E failure cases |
| 7 | Report machine-readable evidence without delivery | verifier JSON and read-only workflow permissions |

The twelve E2E scenarios from Issue #383 are mapped to the public test suite.

| # | Scenario | Test evidence |
| --- | --- | --- |
| 1 | Fresh-clone equivalent | `AgentReadinessE2ETests.test_public_cli_handles_fresh_and_dirty_worktrees` |
| 2 | No change | same test, first verification |
| 3 | Dirty preservation | same test, pre-existing README and untracked file |
| 4 | Dirty overlap | `AgentReadinessE2ETests.test_dirty_overlap_is_rejected` |
| 5 | Invalid marker, version, path, and check | `AgentTaskTests.test_unsafe_contract_shapes_are_rejected` |
| 6 | Add, modify, delete, rename, and symlink scope escapes | `AgentReadinessE2ETests.test_scope_mutation_modes_are_rejected` |
| 7 | Secret detection without value disclosure | same public E2E test, secret case |
| 8 | Failed check followed by canonical check | `AgentReadinessE2ETests.test_failed_check_still_runs_canonical_last` |
| 9 | Stale and tampered session | `AgentVerifyTests.test_tampered_session_fields_are_rejected` |
| 10 | Timeout and cancel without a child process left running | `AgentVerifyTests.test_timeout_terminates_the_process_group` and `test_cancel_file_terminates_the_process_group` |
| 11 | Completion JSON shape | `AgentReadinessE2ETests.test_completion_json_has_stable_fields` |
| 12 | Instruction integrity | `tests/test_agent_instructions.py` |

The E2E creates a temporary local git repository, invokes public tools as
subprocesses, and uses a fixture check registry. The source repository's
canonical registry and canonical verification are exercised by the final
step of the completion command.
