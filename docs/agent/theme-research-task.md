# Theme research task

Purpose: give any caller — a downstream repository (`agentic-art-research` generating a
production plan), a human, or an interactive Agent session — a single, repeatable unit of
work: *"run one research pass on this theme against art-history-notes."* Every run should
either extend the KB with genuine, sourced content, or record a demand signal that nothing
was there yet. Either outcome is valid; a logged query with no new entity is not a failure.

This is the local, offline half of a two-repository handoff. The other half —
`agentic-art-research`'s `tools/art_history_adapter.py` — pulls already-committed,
pinned-commit signals out of this KB read-only. It does not trigger new research here.
Making the KB "thicker" over repeated use is this repository's job, done by whoever holds a
local clone; nothing here changes the adapter's pinned, read-only contract on the other side.

## What "one research pass" means

1. **Reconnaissance (always).**

       uv run --locked python tools/theme_research.py --theme "テーマ" [--json]

   This logs the query to `data/queries.jsonl` (a miss is recorded too — see
   `tools/kb.py::log_query`) and prints the existing hits plus the full
   `data/coverage.json` region×century grid. It does not do any research itself; it only
   tells you what is already here.

2. **Judge whether there is a real gap.** A hit list full of entities that merely mention
   the theme in passing (see `tools/kb.py::search_entities` — it is a literal substring
   match over the whole body, not a relevance ranking) is not coverage. Look for an entity
   whose `label_ja`/`label_en` is the theme itself, check its `status` and source count. If
   one already exists and is `verified` with real sources, stop here — the recon step is
   the whole task.

3. **If there is a genuine gap, follow the same workflow used throughout this repository's
   history** (see any commit that adds a `movement`/`place` pair for the pattern):
   - Grep `entities/` across **every** type, not just the one you plan to create, for the
     same subject. See [`feedback_check_for_duplicates`](../schema.md) discipline — a
     duplicate entity is worse than a missing one.
   - Research with real sources (Wikipedia, Wikidata, museum collection pages, scholarly
     essays). Verify any Wikidata QID by fetching the item, not by guessing from a search
     snippet.
   - Scaffold with `tools/new_entity.py`, fill every required field per
     [`docs/schema.md`](../schema.md), and write claims/relations only where a real URL
     backs them.
   - If a movement has no genuine cross-region connection, do not invent one. Record
     `status: no-documented-cross-region-relation` in `config/cross-region-reviews.yaml`
     (≥2 sources, ≥2 distinct hostnames, all already present in the entity's own
     `sources:` list) and add the movement id to `config/cross-region-baseline-v1.yaml`.
   - Validate, then regenerate, in this order:

         uv run --locked python tools/build_graph.py --check
         uv run --locked python tools/build_graph.py
         uv run --locked python tools/audit.py
         uv run --locked python tools/verify.py

4. **Stop at a local commit.** `git add` and `git commit` the result so the accumulated
   knowledge survives in the local clone. Do **not** `git push`, open a PR, or update an
   Issue — this repository's standing policy (see the root `README.md`, "外部Agentで作業する")
   is that delivery side effects only happen when the user explicitly asks for them. Pushing
   a locally-accumulated clone's history to the shared remote later is a deliberate, manual
   choice by whoever holds that clone, not something this task automates.

## Using the GitHub issue template

[`.github/ISSUE_TEMPLATE/theme-research-task.md`](../../.github/ISSUE_TEMPLATE/theme-research-task.md)
is a ready-to-fill agent-task v2 contract for this exact loop. Replace every `{{theme}}`
placeholder, then validate before starting:

    uv run --locked python tools/agent_task.py validate --file TASK --json

Its `constraints.network` is `allowed` (unlike the generic template's `forbidden`) because
step 3 needs to fetch real sources. `constraints.external_writes` stays `explicit-only` —
the harness never pushes or opens a PR on its own.
