<!-- agent-task:v2 -->
```yaml
version: 2
objective: "Invalid fixture."
context:
  read: []
scope:
  include:
    - "../outside/**"
  exclude: []
requirements:
  - id: "x"
    text: "x"
acceptance:
  - id: "x"
    criterion: "x"
    evidence: "x"
checks:
  - "canonical"
constraints:
  network: "forbidden"
  external_writes: "explicit-only"
depends_on: []
non_goals:
  - "x"
```
