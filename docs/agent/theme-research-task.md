# Theme research task

Specification: `docs/theme-research-cycle.md` (theme-research-cycle/v1) defines the full
per-run cycle this task belongs to — reconnaissance → investigation → owner intake (local
knowledge store) → next-run export → optional manual upstream contribution. This page is the
walkthrough for the canonical-`entities/` path ("経路B" in that spec); the run-internal
store path ("経路A") is documented in `docs/research-knowledge-intake.md` on `main`.

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

## 経路A — run内: candidate → owner intake（利用者ローカルのstoreへ）

制作計画のrunの中で回す標準経路。code checkoutの `entities/` には書かない。手順の正本は
`docs/research-knowledge-intake.md`（AAK-06）。ここでは theme research との接続だけを書く。

1. recon: `tools/theme_research.py --theme "<term>" [--theme "<term2>"] --json`。
   `results[].exact_label_hits` が空でなく、その entity が `verified` なら **NO_NEW_EVIDENCE**。
   親の write job は `{action: no-new-evidence, inputs: {}, reason: "<recon の theme と hit_count>"}`。
2. 骨格: `--emit-candidate-template --creator … --collection … --project-id … --origin-instance-id … --run-id …`
   を付けると `candidate_templates[]` に candidate.json の骨格と `missing` が出る。
   骨格は出典・hash・主張を推測しない。`missing` を全部埋めるのはエージェント。
3. 調査: `config/theme-research.yaml` の予算内で出典を読み、URL→外部snapshot fileの対応
   （`source-snapshots.json`）と `payload.source_reads`（byte範囲hash）を作る。読んでいない出典を
   `source_reads` に書かない（intakeが拒否する）。
4. 検証: `tools/research_knowledge_intake.py prepare …`（read-only）。通らなければ candidate を直す。
   予算到達で1件も通らなければ `no-new-evidence`（reason に `BUDGET` と上限名）。
5. 親の write job: `{action: write, inputs: {candidate: <path>, source-snapshots: <path>}, reason: …}`。
   commit / index は親が native CLI で行い、receipt を検証する。エージェントは push しない。
6. 次回: `tools/export_signals.py --knowledge-store-root … --query <theme>` に新record が ID 付きで返る。

## 経路B — 手動: store の record を canonical `entities/` へ昇格（このページの残り）

貯まった record のうち共有価値のあるものを、利用者が選んで共有リポジトリへ返す経路。
自動ではない。昇格した entity には **元 record への参照** を必ず残す（spec §5 R7-4、Phase 1の形式）:

```yaml
sources:
  - url: "https://example.org/read-source"
    kind: reference
    note: "origin: record_id=<record_id>; revision=<n>; origin_instance_id=<instance>; collection_id=<collection>"
```

`derived_from` 専用field への移行は別task（spec §5 R7-4）。それまでは上の `note` 形式を必須とする。

## Using the GitHub issue template

[`.github/ISSUE_TEMPLATE/theme-research-task.md`](../../.github/ISSUE_TEMPLATE/theme-research-task.md)
is a ready-to-fill agent-task v2 contract for this exact loop. Replace every `{{theme}}`
placeholder, then validate before starting:

    uv run --locked python tools/agent_task.py validate --file TASK --json

Its `constraints.network` is `allowed` (unlike the generic template's `forbidden`) because
step 3 needs to fetch real sources. `constraints.external_writes` stays `explicit-only` —
the harness never pushes or opens a PR on its own.
