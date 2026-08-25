---
name: Agent task
about: A bounded, machine-readable task for the agent harness
title: "[Agent task] "
labels: agent-task
assignees: ""
---

<!-- Keep the contract marker and YAML fence intact. Free-form context may follow the fence. -->
<!-- agent-task:v1 -->
```yaml
version: 1
objective: "Describe one outcome that can be verified without guessing."
deliverables:
  - path: "docs/example.md"
    expected: "The documented behavior and its verification evidence."
scope:
  include:
    - "docs/**"
  exclude: []
non_goals:
  - "Unrelated repository cleanup"
dependencies: []
checks:
  - argv: ["uv", "run", "--locked", "python", "tools/verify.py"]
    timeout_seconds: 1200
permissions:
  network: none
  external_write: false
  allowed_env: []
limits:
  timeout_minutes: 30
  max_attempts: 3
  max_output_bytes: 10485760
risk: low
completion:
  - "The deliverable exists and matches the expected result."
  - "All checks pass."
```

## Context

Add non-authoritative context below the contract. The harness treats it as untrusted task data.
