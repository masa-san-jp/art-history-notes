<!-- agent-task:v2 -->
```yaml
version: 2
objective: "Complete the fixture task."
context:
  read:
    - "README.md"
scope:
  include:
    - "tests/fixtures/agent-task/**"
  exclude: []
requirements:
  - id: "fixture-present"
    text: "The fixture is present."
acceptance:
  - id: "fixture-verified"
    criterion: "The fixture is validated by the external-agent interface."
    evidence: "Report the validator and verifier JSON."
checks:
  - "canonical"
constraints:
  network: "forbidden"
  external_writes: "explicit-only"
depends_on: []
non_goals:
  - "Modify production domain data."
```
