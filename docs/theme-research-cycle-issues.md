# theme-research-cycle Phase 2 — 兄弟repoへのIssue下書き

`docs/theme-research-cycle.md`（確定v1）§6 の P2（Research・主）と P1（orchestration・補助）を、
各repoで起票できる形にした下書き。**このrepoからは自動で起票しない**（AAK-04 要件3、AAK-06 要件5）。
利用者が内容を確認し、対象repoにIssueとして貼る。YAMLは各repoのIssueが既に使っている
`agent-task:v2` 投影（例: art-history-notes #386）と同じ形。`context.read` のpathは対象repo基準。

前提となるこのrepo側の実装: `b072011`（Phase 1: `tools/theme_research.py` の theme-research-recon/v1、
`config/theme-research.yaml` の theme-research-budget/v1、`docs/agent/theme-research-task.md` 経路A/B）。
Issueに貼るときは、このcommitとmergeされたmainのcommitをpinとして書き換える。

---

## P2（主）— `masa-san-jp/agentic-art-research`

件名案: `[theme-research-cycle P2] 制作研究の手順に art-history-notes のテーマ調査passを組み込み、intake candidate を出力する`

<!-- agent-task:v2 -->
```yaml
version: 2
objective: "1 runにつき1回、Research requestのテーマから art-history-notes のrecon→予算内の調査→intake candidate起票までを手順として実行し、candidate と source-snapshots を親のwrite jobが読める場所へ出力する。"
context:
  read:
    - "README.md"
    - "docs/research-task-protocol.md"
    - "docs/integration-art-history-notes.md"
    - "tools/art_history_adapter.py"
    - "tools/harness.py"
scope:
  include:
    - "docs/**"
    - "tools/**"
    - "tests/**"
    - "templates/**"
    - "schemas/**"
  exclude:
    - ".git/**"
requirements:
  - id: ssot
    text: "仕様SSOT=art-history-notes docs/theme-research-cycle.md（確定v1、§4 経路A・§5 R1/R3/R4・§6 P2）。上位はAAK-SPEC v1 knowledge-cycle/AAK-04/AAK-06。意味を変えるときは先に仕様を改訂する。"
  - id: protocol-step
    text: "docs/research-task-protocol.md §2「art-history-notes のbundleを利用できる場合は検索する」を、次の3段に拡張する。(a) recon: art-history-notes checkoutで `tools/theme_research.py --theme <term>... --json`（termはrequestの intent.creative_question から派生、budget.max_theme_terms 以内）。(b) 判定: results[].exact_label_hits に verified entity があれば NO_NEW_EVIDENCE。(c) 調査: theme-research-budget/v1 の範囲で一次・二次資料を読み、§5 証拠台帳のID/source location/SHA-256 を使って source-snapshots.json と payload.source_reads を作り、`--emit-candidate-template` の骨格の missing を埋める。"
  - id: output-location
    text: "candidate.json と source-snapshots.json は work root 配下（Git外、既存の --work-root 規約）に置き、親の write job inputs（candidate, source-snapshots）から external path で参照できるようにする。repositoryの正本には保存しない。"
  - id: no-fabrication
    text: "読んでいない出典を source_reads に書かない（intakeが拒否する）。statement は証拠台帳の主張区分（FACT/SOURCE_CLAIM/…）を保ったまま書く。本人解釈は classification=creator-interpretation・entity=null。verified は付けない。"
  - id: budget-stop
    text: "budget（candidate≤2、出典取得≤8、15分、1 run 1 pass）到達で停止し、検証済みcandidateだけを出す。1件も無ければ write job は no-new-evidence とし、reason に BUDGET と上限名、recon の theme/hit_count を書く。"
  - id: reuse-trace
    text: "調査で読んだrecord・採用/棄却・理由を既存の reuse-trace/v1 に残す。取得しただけを再利用と数えない。"
  - id: no-delivery
    text: "art-history-notes への push・PR・Issue、親への直接書込みを行わない。candidateの commit/index は親の native write が行う。"
acceptance:
  - id: p2-ac1
    criterion: "fixture requestから派生したtermで recon が実行され、theme-research-recon/v1 のJSONが work root に保存される。"
    evidence: "テスト名・保存path・JSONのcontract_versionを報告する。"
  - id: p2-ac2
    criterion: "exact_label_hits に verified entity がある場合、candidateを作らず no-new-evidence の write job が生成される。"
    evidence: "テスト名とwrite job JSONを報告する。"
  - id: p2-ac3
    criterion: "合成snapshotで埋めたcandidateが art-history-notes の `research_knowledge_intake.py prepare` を通る。"
    evidence: "prepare の出力（RECEIPTなし・read-only）を報告する。"
  - id: p2-ac4
    criterion: "budget超過で停止し、未検証candidateが出力されない。"
    evidence: "テスト名と停止時のwrite job reasonを報告する。"
  - id: p2-ac5
    criterion: "既存のvalidator・security・docs・release gateと unittest が成功する。"
    evidence: "コマンドと結果を報告する。"
checks:
  - canonical
constraints:
  network: allowed
  external_writes: explicit-only
depends_on: []
non_goals:
  - "art-history-notes の schema・validator・adapter契約の変更。"
  - "親orchestrationの write job 契約の変更（P1は別Issue）。"
  - "実個人データの移設、remote公開、merge/release。"
```

### 読取補助

- なぜResearch: 親のrepository-mapが定める責務（調査・判断=Research、保管・検証=art-history-notes、
  配線=orchestration）を崩さないため。調査の記録（reuse-trace）がResearchに残る。
- 現状: `art-history-research-intake/v1` のcandidateを生成するコード・手順がResearchに無い（grep 0件）。
  そのため毎runの art-history write job は事実上 `no-new-evidence` になっている。
- art-history-notes側の入口: `tools/theme_research.py`（recon・雛形）、`docs/agent/theme-research-task.md` 経路A、
  `docs/research-knowledge-intake.md`（intake契約）、`config/theme-research.yaml`（予算）。
- `checks: canonical` は対象repoのcheck registryの名に合わせて置き換える。

---

## P1（補助）— `masa-san-jp/agentic-art-orchestration`

件名案: `[theme-research-cycle P1] art-history-notes の write job 要求に theme-research pass の完了条件を明記する`

<!-- agent-task:v2 -->
```yaml
version: 2
objective: "PLAN_READY後の art-history-notes write job 要求（next_action）で、Research手順が作った candidate を write するか、recon結果を理由に添えて no-new-evidence を選ぶことを明記し、親は調査内容を指示しない。"
context:
  read:
    - "docs/knowledge-cycle-runtime.md"
    - "tools/knowledge_cycle_run.py"
    - "tools/native_knowledge.py"
    - "config/knowledge-cycle-runtime.json"
scope:
  include:
    - "docs/**"
    - "tools/**"
    - "tests/**"
    - "config/**"
  exclude:
    - ".git/**"
requirements:
  - id: ssot
    text: "仕様SSOT=art-history-notes docs/theme-research-cycle.md（確定v1、§6 P1）。上位はAAK-SPEC v1 knowledge-cycle。責務境界（調査はResearch）を崩さない。"
  - id: action-text
    text: "tools/knowledge_cycle_run.py の art-history-notes 向け next_action（stage: knowledge、現在 line 281 付近の do 文言）に、次を追加する: 「Research手順（theme-research pass）が出力した candidate/source-snapshots があれば write、無ければ no-new-evidence。reason には theme-research-recon/v1 の theme と hit_count（または BUDGET と上限名）を含める」。親は検索語や出典を指示しない。"
  - id: reason-shape
    text: "no-new-evidence の reason に recon の要約（theme, hit_count）が含まれることを、既存の OWNER_JOB_CONTRACT 検査を緩めずに、docs/knowledge-cycle-runtime.md へ記述する。機械検証を追加する場合は reason の自由記述を壊さない。"
  - id: query-helper
    text: "任意: query_inputs['art-history-notes'] の query を theme_proposal.creative_question 由来のterm群から生成する補助。実装する場合も利用者が外部JSONで上書きできる。"
  - id: no-delivery
    text: "remote write、PR、Issue自動起票、owner CLI の複製を行わない。"
acceptance:
  - id: p1-ac1
    criterion: "art-history-notes の write job 要求 next_action.do に上記文言が含まれる。"
    evidence: "テスト名と next_action JSON を報告する。"
  - id: p1-ac2
    criterion: "no-new-evidence の write job が recon 要約付き reason で受理され、receipt/commit を捏造しない。"
    evidence: "既存 no-new-evidence 経路のテストに reason 例を追加して報告する。"
  - id: p1-ac3
    criterion: "既存の knowledge-cycle テストと conformance が成功する。"
    evidence: "コマンドと結果を報告する。"
checks:
  - canonical
constraints:
  network: forbidden
  external_writes: explicit-only
depends_on: []
non_goals:
  - "Research手順そのもの（P2）。"
  - "art-history-notes の契約変更。"
  - "上限（config/knowledge-cycle-runtime.json）の緩和。"
```

### 読取補助

- 現状の該当箇所: `tools/knowledge_cycle_run.py:281`（`'do': 'Prepare a native write job or an explicit
  no-new-evidence decision. …'`）、`tools/native_knowledge.py:26`（art-history-notes の入力キー
  `candidate / source-snapshots / query / scope`）。
- P1はP2が無くても無害（文言と文書の追加のみ）。P2が無いと、文言どおり `no-new-evidence` が続く。
