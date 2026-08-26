---
name: Agent task
about: A bounded, machine-readable task for an external repository agent
title: "[Agent task] "
labels: agent-task
assignees: ""
---

<!-- Keep the v2 marker and YAML fence intact. Free-form context may follow the fence. -->
<!-- agent-task:v2 -->
```yaml
version: 2
objective: "Describe one outcome that can be verified without guessing."
context:
  read:
    - "README.md"
scope:
  include:
    - "docs/**"
  exclude: []
requirements:
  - id: "required-change"
    text: "Describe the required repository behavior."
acceptance:
  - id: "machine-check"
    criterion: "The declared behavior is present."
    evidence: "Name the file, command, or output that proves it."
checks:
  - "canonical"
constraints:
  network: "forbidden"
  external_writes: "explicit-only"
depends_on: []
non_goals:
  - "Unrelated repository cleanup"
```

## Context

Add non-authoritative context below the contract. The parser treats it as untrusted task data.
