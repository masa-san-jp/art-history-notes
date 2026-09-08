# 研究成果のowner intake

AAK-06 / Issue #386の実装入口。要件と受入条件の正本は親repoのAAK-SPEC v1、
依存・検証・再開はAAK-PLAN v1（両方の参照commitは
`b0e7c7f8d0a1f756fa708deef4fb380a62e45e0d`）です。

`tools/research_knowledge_intake.py` は明示された `store.json` と `objects.git` を持つ
AAK-04のowner保存先を使用します。store.jsonはowner=`art-history-notes`、creator、collectionを
照合します。未設定のpath、他人のstore、symlink、dirtyなcode checkoutを自動採用しません。
実行codeは現在のclean checkoutのHEADと `--code-commit` が一致する必要があります。
知識のrefは専用bare Gitの `refs/heads/knowledge`。codeと独立して固定します。

## Owner payload

入力JSONは `record` と `payload` だけを持ちます。recordは共通のclosedな
`artifact-record/v1` envelopeです。owner kindは `art-history-knowledge`、payload_schemaは
`art-history-research-intake/v1`。owner、creator、collection、revision、hash、日時、権利と
producerを検証します。producerはkind（agent/human/tool）、generator_version、code_commit、run_idです。
rightsはknowledge_writeとredistributeを明示し、creator-privateはconsent_refが必要です。

payloadは次の7 fieldだけを持ちます。

| field | 内容 |
|---|---|
| classification | historical / creator-interpretation |
| target_id | 既存canonical IDまたは新候補の安全なentity/context ID |
| project_id | 解釈・調査が発生したproject |
| statement | 固有の観測または解釈。競合案も別recordとして残す |
| entity | 既存schemaに適合するentity/context frontmatter、またはnull |
| source_reads | url、content_sha256、locator、start、end、slice_sha256を持つ読取証拠 |
| context_body | contextの4つの正規見出しを含む本文。それ以外はnull |

payload_refは `contexts/research-memory/payloads/<key>.json`。
keyはorigin_instance_id・owner_repository・record_id・revisionのcanonical JSON配列のSHA-256です。
content_sha256はpayloadのUTF-8 canonical JSON（key sort、非ASCII保持、区切り`,`と`:`）のhashです。
本文、引用、生成物を無差別に保存する入力ではありません。未知field、秘密らしい値を拒否します。
record、payload、操作ledger、必要なcanonical Markdownを同じGit commitへ保存します。

source-snapshots JSONはURLから読取用外部ファイルへのmappingです。入力snapshot全体と
指定byte範囲のhashを実際に確認し、raw bytesを保存しません。snapshotなしの既読宣言を拒否します。
完了済みoperationの同内容replayにはrawの再保存を要求せず、元のcommit receiptを返します。

intakeは `verified` を付けません。本人解釈はentity=nullとし、epistemic_statusを推論・提案・
simulation・unknownのまま保持します。歴史候補のcanonical化はsource読取証拠と既存validatorを
必要とし、draftとして置きます。authority IDで同一entityを照合します。競合する日付・名称・
source注記は既存canonical値を上書きせず、別payloadの記録を保持します。

## 操作

初回保存先の選択・権限はAAK-04の明示setupで行います。以下のpath/SHAは使用環境で設定します。

```bash
uv run --locked python tools/research_knowledge_intake.py prepare \
  --store-root /absolute/external/history-memory --creator creator-a --collection history-a \
  --code-commit CODE_SHA --knowledge-commit KNOWLEDGE_SHA \
  --candidate /absolute/external/candidate.json --source-snapshots /absolute/external/source-map.json
uv run --locked python tools/research_knowledge_intake.py commit \
  --store-root /absolute/external/history-memory --creator creator-a --collection history-a \
  --code-commit CODE_SHA --knowledge-commit KNOWLEDGE_SHA \
  --candidate /absolute/external/candidate.json --source-snapshots /absolute/external/source-map.json \
  --operation-id intake-001 --run-id run-001
```

validateはprepareと同じread-only検証です。commitは期待parentとのCASで競合を検知し、
knowledge-write-receipt/v1を返します。新recordのrevisionは連続させ、同revision異内容を拒否します。
同operation異内容も拒否します。remoteへのpush・Issue・PR作成は行いません。

```bash
uv run --locked python tools/research_knowledge_intake.py index \
  --store-root /absolute/external/history-memory --creator creator-a --collection history-a \
  --code-commit CODE_SHA --knowledge-commit RECEIPT_COMMIT
uv run --locked python tools/export_signals.py --purpose artistic-research \
  --knowledge-store-root /absolute/external/history-memory --creator creator-a --collection history-a \
  --code-commit CODE_SHA --knowledge-commit RECEIPT_COMMIT --query QUERY --at 2026-09-05T00:00:00Z
```

indexは正規graph構成関数とcontext validator/vector builderで外部の再生成可能cacheを更新します。
失敗してもGit commitとreceiptを保持し、indexだけを再実行します。snapshot、query、本人scope、時点を
指定したexportは `art-history-knowledge-export/v1` のrecord refsを返します。従来の引数だけの
research-signal-export/v1は互換経路です。取得だけを再利用とは数えず、実際の判断への採否・影響は
利用側Researchのreuse traceで記録します。

invalidateはinvalidatesを持つ新revision/recordのcommitです。active exportは撤回・期限切れを除外し、
source失効の派生記録も再検証対象にします。indexではそのcanonical上書き層を使わず、独立した
共有baselineを保持します。Git履歴と過去snapshotは消しません。公開projectionは行いません。

合成受入は `tests.test_research_knowledge_intake`。実Masa profile、実owner間の最終統合、
実エージェントによる次回制作への再利用はこのfixtureを代用せず、AAK-02で検証します。
