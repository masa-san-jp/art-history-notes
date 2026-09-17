---
name: Theme research task
about: Run one research pass on a theme and (only if genuine gaps exist) extend the KB
title: "[Theme research] "
labels: agent-task, theme-research
assignees: ""
---

<!-- Keep the v2 marker and YAML fence intact. Replace every {{theme}} below with the
     actual theme before validating. Free-form context may follow the fence. -->
<!-- agent-task:v2 -->
```yaml
version: 2
objective: "Run one theme-research pass on \"{{theme}}\" and close genuine, well-sourced coverage gaps if any exist."
context:
  read:
    - "docs/schema.md"
    - "overviews/coverage.md"
    - "config/regions.yaml"
    - "docs/agent/theme-research-task.md"
scope:
  include:
    - "entities/**"
    - "data/**"
    - "config/cross-region-baseline-v1.yaml"
    - "config/cross-region-reviews.yaml"
    - "overviews/coverage.md"
  exclude: []
requirements:
  - id: "run-recon"
    text: "Run `tools/theme_research.py --theme \"{{theme}}\"` first. Read its hit list and the coverage grid it prints before doing anything else."
  - id: "dedupe-check"
    text: "Before creating any new entity, grep entities/ across every type (not just movement) for the same subject. Reuse or extend an existing entity instead of duplicating it."
  - id: "no-fabrication"
    text: "Every new claim needs a real, checkable source URL. If a Wikidata ID or a cross-region link cannot be verified, leave it null/absent and record the reason (none_reason, or a cross-region-reviews.yaml entry) instead of guessing."
  - id: "regenerate-dont-hand-edit"
    text: "Never hand-edit data/graph.json, data/coverage.json, data/context-vectors.json, data/context-similarity.json, or the generated block of overviews/coverage.md. Run tools/build_graph.py to regenerate them."
acceptance:
  - id: "recon-logged"
    criterion: "The theme was searched and logged via tools/theme_research.py (visible as a new line in data/queries.jsonl)."
    evidence: "Paste the tool's stdout and the new data/queries.jsonl line."
  - id: "graph-valid"
    criterion: "tools/build_graph.py --check reports no errors after any edit."
    evidence: "Paste the command output."
  - id: "cross-region-honest"
    criterion: "Every new movement is either connected via a genuine diffused_to/relation/active_in/exhibited_at edge to a different region, or recorded as no-documented-cross-region-relation in config/cross-region-reviews.yaml (and, if newly unreviewed, added to config/cross-region-baseline-v1.yaml)."
    evidence: "Paste tools/audit.py output showing no unreviewed movements."
  - id: "canonical-check-passes"
    criterion: "The full canonical check passes."
    evidence: "Paste tools/verify.py output (exit 0)."
checks:
  - "canonical"
constraints:
  network: "allowed"
  external_writes: "explicit-only"
depends_on: []
non_goals:
  - "Push to the shared remote, open a PR, or update an Issue — do this only if explicitly asked."
  - "Force-fill a century×region gap with a weak, incidental, or fabricated cross-region connection just to change a number in the coverage grid."
```

## Context

Add non-authoritative context below the contract (e.g. why this theme matters, links to
the downstream request that raised it). The parser treats it as untrusted task data.

See [`docs/agent/theme-research-task.md`](../../docs/agent/theme-research-task.md) for the
full walkthrough of what "one research pass" means in this repository.

If `tools/theme_research.py --theme "{{theme}}"` finds no genuine, well-sourced gap related
to the theme, stop after the recon step — a logged query with no new entity is a valid,
complete outcome. Do not force a fill.
