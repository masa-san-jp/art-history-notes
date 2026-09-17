# テーマ調査サイクル仕様（theme-research-cycle/v1）

作成: 2026-09-17 ／ 状態: 提案（実装前） ／ 対象repo: `masa-san-jp/art-history-notes`（owner側）

目的を一文で言うと——**制作計画の実行1回につき、そのテーマに応じた美術史調査が1回回り、結果がこのKBの
利用者ローカルに根拠付きで残り、次回の実行がそれを参照でき、貯まった分を利用者が任意のタイミングで
共有remoteへ還元できる**、という状態を作る。

## 0. 正本との関係

上位の正本は親repoの AAK-SPEC v1
（`agentic-art-orchestration/docs/20260905-agentic-art-autonomy-and-knowledge-cycle-specification.md`、
参照commit `b0e7c7f8d0a1f756fa708deef4fb380a62e45e0d`）の共通節（principles / storage /
instance-profile / knowledge-cycle / completion）と、このrepoを対象とする **AAK-06**、利用者別
clone/forkを扱う **AAK-04** である。本仕様はそれらを変更せず、AAK-06の実装（Issue #386 → PR #387、
`origin/main` に統合済み）の上に「テーマ起点で調査を1回回す」という運用単位を定義する。
矛盾があればAAK-SPECを優先し、本仕様を改訂する。

本仕様は「何を・どの契約で・どこまで自動で」を決める設計文書であり、実装完了を意味しない。
実装は §9 の順序で、既存の task contract v2（`docs/agent/task-contract.md`）を通して行う。

## 1. 確認した現状（2026-09-17時点、コードから読み取ったもの）

### 1.1 親runは既に「run毎に全ownerへquery→write」を回している

- 親の `tools/run.py --cycle-context …` は、Research requestの `intent.creative_question` を
  `theme_proposal` として確定し（`run.py:89-105`）、8 ownerへpin済みqueryを投げ、`PLAN_READY` 後に
  ownerごとの **write job** を要求する（`tools/knowledge_cycle_run.py:275-320`）。
- write jobは外部JSONで `{action: write | no-new-evidence, inputs, reason}` の3 fieldのみ。
  `no-new-evidence` は inputs 空で、receiptもcommitも捏造しない。
- art-history-notesのnative writeは `tools/research_knowledge_intake.py`、受け付ける入力キーは
  `candidate / source-snapshots / query / scope`（親 `tools/native_knowledge.py:15,26`）。

### 1.2 art-history-notes側の受け口（AAK-06）は `origin/main` に存在する

`tools/research_knowledge_intake.py`（`prepare / validate / commit / index / retrieve / invalidate`）と
`docs/research-knowledge-intake.md` が正本。要点:

- 保存先は利用者ローカルの外部store（`store.json` + bare Git `objects.git`、ref `refs/heads/knowledge`）。
  code checkoutの `entities/` には書かない。creator / collection 単位。
- 入力は `artifact-record/v1` envelope + `art-history-research-intake/v1` payload
  （`classification / target_id / project_id / statement / entity / source_reads / context_body`）。
- `source_reads` は URL→外部snapshot fileのmappingと byte範囲hashを実検証する。**snapshotなしの
  既読宣言は拒否**。intakeは `verified` を付けず、歴史候補は `draft`、本人解釈は `entity: null`。
- commitはCASで競合検知し `knowledge-write-receipt/v1` を返す。remoteへのpush・Issue・PRは行わない。
- 次回参照は `tools/export_signals.py --knowledge-store-root … --query …` が
  `art-history-knowledge-export/v1` でrecord refsを返す（AAK-06-AC3）。

### 1.3 しかし、candidateを作る主体がいない——ここが「使うたびに厚くなる」が起きない原因

- `agentic-art-research` の `tools/` `docs/` `schemas/` `templates/` に
  `art-history-research-intake/v1` を生成するコードも手順も無い（grep結果0件）。
- Researchの `docs/research-task-protocol.md` §2 は「`art-history-notes` のbundleを利用できる場合は
  検索する」と読むことだけを定めている。
- したがって現状、毎runの art-history write jobは事実上 `no-new-evidence` になる。read-only adapter
  （`agentic-art-research/tools/art_history_adapter.py`）はpin済み `data/graph.json` を読むだけで、
  新規調査を起動しない。

### 1.4 需要ログはrun内から記録されない

`data/queries.jsonl` へ書くのは `tools/kb.py::log_query` を呼ぶ `tools/bundle.py --search` と
`tools/theme_research.py` だけ。親runのqueryやadapterの読取は記録されない。

### 1.5 本branchはmainの受け口を含んでいない（実装時の注意）

作業branch `docs/ecosystem-readme-20260910` は `de5a3c3`（AAK-SPECの基準commit）で `main` から分岐し、
`origin/main` 側の10 commit（AAK-06実装 #387、AP-04 #391、#390、#393）を取り込んでいない。
本仕様の実装は **mainを取り込んだ後**に行う。取り込み自体は履歴を消さない操作（merge / rebase）に限り、
利用者の指示で行う。

## 2. 目標と非目標

目標:

- G1 **1 runにつき1 pass**: 親runの `theme_proposal.creative_question` から派生したテーマ語で、
  このKBに対する調査passが必ず1回走る（結果が空でもpass自体は記録される）。
- G2 **ローカルに残る**: passの成果は利用者のcollectionへ owner receipt付きで保存され、
  次回runのquery/exportにID付きで返る。
- G3 **任意で還元できる**: 貯まったrecordのうち共有価値のあるものを、利用者が選んで
  共有canonical（`entities/`）へ昇格し、自分の判断でremoteへpush/PRできる。自動ではない。
- G4 **捏造ゼロ**: 出典・snapshotの無い主張、未読原典の既読偽装、本人解釈の歴史的事実化は
  既存intakeが拒否する。空振りは `NO_NEW_EVIDENCE` として正常。

非目標:

- daemon・内蔵agent・自動PR・自動push・Issue自動起票（AGENTS.md、AAK-06 要件5、AAK-04 要件3）。
- 下流adapter（`art_history_adapter.py`）の契約変更。
- 被覆グリッドの100%充足。世紀×地域の空欄を埋めること自体は目的にしない。
- `verified` の自動付与。verified化は既存の根拠付き基準（`tools/verified_movement.py`）のまま。

## 3. 用語

| 語 | 定義 |
|---|---|
| theme | 1 runのテーマ。正本は親runの `theme_proposal.creative_question`。そこから派生した検索語（日本語・英語の複数可）を **theme terms** と呼ぶ |
| pass | theme termsに対する1回の調査単位。recon → 判定 → 調査 → candidate作成 → intake の順で、予算内で1回だけ回る |
| recon | `tools/theme_research.py` による既存被覆の確認と需要ログ記録。調査はしない |
| candidate | `art-history-research-intake/v1` payloadを持つ `artifact-record/v1`。passの生成物 |
| receipt | owner intake `commit` が返す `knowledge-write-receipt/v1` |
| collection | 利用者ローカルstoreの保存区分（AAK-04 instance-profileの `source_collections`） |
| upstream contribution | store内recordを共有canonical `entities/` へ昇格し、利用者がpush/PRする手動工程 |

## 4. 1 runの流れ

```text
親 run.py ── theme_proposal.creative_question ──┐
                                                ▼
[A] recon      tools/theme_research.py --theme "<term>" --json   （read-only + queries.jsonl追記）
                                                │
[B] 判定       hitsに主題そのものの verified entity がある → NO_NEW_EVIDENCE（理由を記録）
               hitsが無い／stub・draftのみ／出典が薄い → [C]へ
                                                │
[C] 調査       外部エージェントが出典を取得（network: allowed、§5 R4の予算内）
               URL→外部snapshot file + sha256 = source-snapshots.json
               candidate.json（historical: entity frontmatter付き draft／creator-interpretation: entity null）
                                                │
[D] intake     research_knowledge_intake.py prepare/validate （read-only検証）
               親の write job = {action: write, inputs: {candidate, source-snapshots}, reason}
               親が native commit → receipt → index
                                                │
[E] 次回参照   export_signals.py --knowledge-store-root … --query … が新recordをID付きで返す
                                                │
[F] 還元(任意) 利用者がrecordを選び、task contract v2 で canonical entities/ へ昇格
               build_graph → audit → verify → 自分でcommit → 自分の判断で push / PR
```

[A]〜[E]は1 runの中で閉じる。[F]はrunの外、利用者の任意のタイミング。

## 5. owner（art-history-notes）側の要件

### R1 recon契約 `theme-research-recon/v1`

`tools/theme_research.py --theme <term> --json` の出力を契約として固定する。

```json
{
  "contract_version": "theme-research-recon/v1",
  "theme": "<term>",
  "hits": [{"id": "movement/mughal-painting", "label_ja": "ムガル絵画", "type": "movement",
            "status": "verified", "n_sources": 12}],
  "hit_count": 1,
  "coverage_grid": {"<region>": {"<century>": <count>}},
  "next_step": "<日本語の案内文>"
}
```

- 現行実装（2026-09-17）は `contract_version` を持たない。追加する（後方互換）。
- `--theme` は複数回指定可能にし、1回の起動でterm数分のrecon結果を配列で返す（1 runのtheme termsが
  日英で複数になるため）。各termは個別に `data/queries.jsonl` へ記録する。
- exit codeは常に0。該当なしは失敗ではない。
- `search_entities` は本文全体の部分一致であり関連度順ではない（`tools/kb.py:326-335`）。
  「主題そのもの」の判定は、`label_ja` / `label_en` がtermに一致するhitがあるかでエージェントが行う。
  将来 `exact_label_hits` を別fieldで返す改善は許すが、v1の必須ではない。

### R2 手順書の2経路化

`docs/agent/theme-research-task.md` は現在、canonical `entities/` へ直接書く経路（§4 [F]相当）だけを
書いている。次の2経路を明示する。

- **経路A（run内 / 標準）**: candidate → intake → store。code checkoutは変更しない。
  この経路が「使うたびに厚くなる」を担う。
- **経路B（手動 / 還元）**: store内recordを canonical `entities/` へ昇格。
  `.github/ISSUE_TEMPLATE/theme-research-task.md` のcontractはこの経路用。

### R3 candidate雛形の生成（新規・任意機能）

`tools/theme_research.py --emit-candidate-template --theme <term> --creator <id> --collection <id> --project-id <id>`
で、recon結果から candidate.json の骨格を出す。

- envelopeの固定field（`contract_version`, `owner_repository`, `kind`, `payload_schema`, `producer.kind` 等）と、
  payloadの `target_id` 候補（既存canonical IDとの照合結果、無ければ安全な新ID案）を埋める。
- `statement`, `source_reads`, `entity`, `context_body` は空のまま出す。**ここを埋めるのはエージェント**であり、
  雛形は出典やhashを推測しない。
- 雛形は既存 `validate_candidate`（`research_knowledge_intake.py:49`）を通らない状態で出してよいが、
  「何が未充足か」を `missing` 配列で併記する。

### R4 予算（有限値をconfigに置く）

`config/theme-research.yaml`（新規、`theme-research-budget/v1`）:

```yaml
contract_version: theme-research-budget/v1
per_run:
  max_passes: 1            # 1 runにつき1 pass。増やさない
  max_theme_terms: 4       # creative_questionから派生させる検索語の上限
  max_candidates: 3        # 1 passで起票するcandidateの上限
  max_source_fetches: 12   # 取得する出典URLの上限（snapshot化するもの）
  wall_clock_seconds: 1200
on_exhausted: stop         # 上限到達で停止し、未完了分は書かない（捏造しない）
```

上限到達時のwrite jobは、それまでに検証済みのcandidateだけを `write` するか、1件も無ければ
`no-new-evidence` を選ぶ。`reason` に `BUDGET` と到達した上限名を書く。上限の緩和は
AAK-SPEC「現在の上限を未検証で増やして通さない」に従い、本configの改訂と根拠を伴う。

### R5 重複と競合（既存intakeの機能に委ねる）

- 既存canonical IDとの照合はauthority ID（Wikidata等）と `target_id` で行う（intake既存）。
- 同一主題の再passは新entityを作らず、競合する根拠は別payloadとして併記する（AAK-06-AC1）。
- canonical `entities/` 側に既に `verified` がある主題は §4 [B]で `NO_NEW_EVIDENCE` とし、
  passの成果は `data/queries.jsonl` の1行のみでよい。

### R6 記録

- owner側に残るのは receipt、`data/queries.jsonl`、candidate内の `producer.run_id` / operation_id。
- 「参照した／採用した」の区別（reuse-trace/v1）はResearch側の責務であり、ownerは持たない。

### R7 upstream contribution（経路B）の契約

1. 対象は利用者が選ぶ。自動選定しない。
2. `.github/ISSUE_TEMPLATE/theme-research-task.md` を写経したtaskを **ローカルファイル**として作り、
   `tools/agent_task.py validate` → `agent_session.py begin` → 編集 → `agent_verify.py`。
   Issueとして起票するかは利用者の任意。
3. 昇格したentityの `status` は `draft`。`verified` は既存基準を満たしたときだけ。
4. **origin保持**: 昇格entityの `sources[].note` に、元recordの `record_id` / `revision` /
   `origin_instance_id` / `collection_id` を書く。schemaへ専用fieldを足すかは別途 `docs/schema.md`
   改訂で判断し、v1では `note` 記載を必須とする（AAK-06 要件4「fork/upstream差分でもorigin IDを維持する」）。
5. `build_graph.py --check` → `build_graph.py` → `audit.py` → `verify.py` を通し、利用者自身がcommitする。
6. push / PR / Issue更新は利用者の明示操作。fork利用者は自分のremoteのみを対象にし、
   元remoteへ自動送信しない（AAK-04 要件3）。
7. 昇格がmainへmergeされるまで、下流のpinned adapterには出ない。それまでの参照は経路A（store経由の
   export）だけである、と手順書に明記する。

### R8 下流adapterとの整合

`art_history_adapter.py` は変更しない。ただし同adapterは `git rev-parse HEAD` との一致しか見ず、
dirty worktreeを検出しない（`_source_commit`）。経路Bで `entities/` を編集した直後にpinを更新する
場合は、**commit後のHEAD**でpinすることを手順書に書く。

## 6. 親（orchestration）・Research側への提案（本repoの外。各repoでIssue化する）

これらは本仕様の完成に必要だが、本repoの権限外である。自動でIssueを送らず、利用者が各repoに起票する。

- P1（orchestration）`knowledge_cycle_run.py:281` の art-history write job要求 `do` 文言に、
  「`theme_research.py` のreconを行い、theme-research-budget/v1 の範囲でcandidateを起票するか、
  recon hashを理由に添えて `no-new-evidence` を選ぶ」を追加する。あわせて `query_inputs['art-history-notes']`
  の `query` を `theme_proposal.creative_question` 由来のterm群から生成できる補助を検討する
  （現状は利用者手書きの外部JSON）。
- P2（research）`docs/research-task-protocol.md` §2 の「bundleを利用できる場合は検索する」を、
  「recon → 予算内で調査 → candidate起票」に拡張し、`art-history-research-intake/v1` のcandidateを
  出力する場所（work root配下、Git外）を定める。
- P3（両方）`no-new-evidence` の `reason` に recon結果のhash（theme terms・hit_count）を含め、
  「調べなかった」と「調べたが無かった」を区別する。

## 7. データ契約一覧

| 契約 | 所在 | 状態 |
|---|---|---|
| theme-research-recon/v1 | `tools/theme_research.py --json` | 既存出力に `contract_version` を追加 |
| theme-research-budget/v1 | `config/theme-research.yaml` | 新規 |
| artifact-record/v1 + art-history-research-intake/v1 | `docs/research-knowledge-intake.md`（origin/main） | 既存・変更なし |
| owner write job `{action, inputs, reason}` | 親 `knowledge_cycle_run.py` | 既存・変更なし |
| knowledge-write-receipt/v1 | `tools/research_knowledge_intake.py` | 既存・変更なし |
| art-history-knowledge-export/v1 | `tools/export_signals.py`（origin/main） | 既存・変更なし |
| agent-task v2（経路B） | `.github/ISSUE_TEMPLATE/theme-research-task.md` | 既存（2026-09-17追加） |

## 8. 受入条件

- TR-AC1 recon: `theme_research.py --theme X --json` が契約通りのJSONを返し、`data/queries.jsonl` に
  termごとに1行追加される。該当なしでもexit 0。（`tests/test_theme_research.py` を拡張）
- TR-AC2 経路A通し（synthetic）: theme → candidate（fixture）→ `prepare` → `commit` → `index` →
  `export_signals.py --knowledge-store-root … --query <theme>` が新record IDを返す。
  （`tests/test_research_knowledge_intake.py` にtheme起点fixtureを追加）
- TR-AC3 空振り: 同テーマの `verified` entityが既にある場合、passは重複entityを作らず、
  write jobは `no-new-evidence` になる。
- TR-AC4 予算: `max_candidates` 到達で停止し、検証済み分だけが `write` される。未検証分は書かれない。
- TR-AC5 経路B: 昇格taskが `canonical` check（`tools/verify.py`）を通り、昇格entityの `sources[].note`
  に元record refが残る。
- TR-AC6 副作用なし: いずれの経路でも `git push` / PR / Issue APIを呼ばない（既存harnessテストと
  同じ方式で確認）。
- TR-AC7 実エージェント: synthetic合格を実運用の合格と混同しない。実エージェントによる1 run通しは
  AAK-02の live acceptance の枠で別途記録する。

## 9. 実装順序

1. **Phase 0 — mainへの追従**: `docs/ecosystem-readme-20260910` に `origin/main` を取り込む
   （AAK-06実装を得るため）。方法は利用者が決める。
2. **Phase 1 — owner側（本repo）**: R1（`contract_version`・複数term）、R2（手順書2経路化）、
   R4（config）、R3（雛形、任意）、TR-AC1〜AC6のテスト。task contract v2で実施。
3. **Phase 2 — 他repoへの提案**: §6 P1〜P3を各repoに起票（利用者操作）。
4. **Phase 3 — 実runでの確認**: 実エージェントで1 run通し、receiptと次回exportの証拠を残す（TR-AC7）。

## 10. 未確認・リスク

- `search_entities` の部分一致ノイズ（「ムガル絵画」で24件ヒットの大半が本文中の比較言及）。
  R1の `exact_label_hits` で軽減できるが、v1では判定をエージェントに委ねる。
- theme termsの日英揺れと表記揺れ（例: 「クメール」「Khmer」「Angkor」）。R4の `max_theme_terms` で
  上限を切るが、派生規則は未定義。
- 親の `query_inputs` が利用者手書きの外部JSONである点（P1で補助を提案）。
- 外部storeの絶対path・creator・collectionはAAK-04のsetupに依存する。未設定なら経路Aは動かず、
  `SETUP_REQUIRED` を返すべきで、cwdや他人のprofileから推測しない（AAK-04 要件4）。
- adapterのdirty worktree非検出（R8）。
- 本仕様は2026-09-17時点の `origin/main`（`d5e6a48`）と本branch（`41f5189`）のコードを根拠にしている。
  実装時に再確認する。
