# art-history-notes

時間・空間・関係の3軸で、美術史のムーブメントを根拠付きで蓄積するナレッジベースです。
個別の人物・作品・場所・組織などを `entities/` に、時期×文化圏×領域のスナップショットを
`contexts/` に保存し、関係をたどったり、時間と場所から調査候補を生成したりできます。

このリポジトリには、外部Agentが安全に作業するための受動的なハーネスも含まれます。
リポジトリ自身はAgent、モデル、認証、queue、daemon、自動commit、PR配送を起動しません。

## まず何を読むか

目的に応じて入口を選んでください。

| 目的 | 入口 |
| --- | --- |
| 美術史データを読む | [`overviews/coverage.md`](overviews/coverage.md)、[`entities/`](entities/)、[`contexts/`](contexts/) |
| 1件のエンティティを調査・追加する | [`docs/schema.md`](docs/schema.md)、[`docs/investigation-task.md`](docs/investigation-task.md) |
| 時代文脈を調査・比較する | [`docs/context-investigation-task.md`](docs/context-investigation-task.md)、[`docs/context-vectors.md`](docs/context-vectors.md) |
| 外部Agentとして作業する | [AGENTS.md](AGENTS.md)、[docs/agent/README.md](docs/agent/README.md) |
| 外部標準へ対応付ける | [`docs/interop-mapping.md`](docs/interop-mapping.md) |

要件の正本は [Issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1)、データ形式の正本は
[`docs/schema.md`](docs/schema.md) です。このREADMEは利用方法の案内であり、仕様と食い違う場合は正本を優先します。

## 兄弟リポジトリと関係

このrepoは、複数の正本を横断するシステムの一部です。各repoは独立して管理され、データを一つのrepoへ
コピーして統合しません。横断利用が必要な場合は、[`agentic-art-orchestration`](https://github.com/masa-san-jp/agentic-art-orchestration)
がsource commit、manifest、依存関係、境界形式を管理します。

8リポジトリの全体図と、各repoの正本・受け渡し・公開境界は、親repoの [repository map](https://github.com/masa-san-jp/agentic-art-orchestration/blob/main/docs/repository-map.md) にまとめています。ここではart-history-notesから見た接続だけを説明します。

```text
input KBs: self-model / art-history / marketing / viewer-response
                              │
                              │ source commit + 境界形式
                              ▼
                 agentic-art-orchestration
                              │
                              ▼
                   agentic-art-research
                              │
                              ▼
                  agentic-art-production
```

| リポジトリ | 役割 | art-history-notesとの関係 |
| --- | --- | --- |
| [self-model-notes](https://github.com/masa-san-jp/self-model-notes) | 同意範囲と不確実性を保持するSelf Model入力KB | 並列の入力KB。人物・観測データをこのrepoへコピーしません |
| [marketing-trends-notes](https://github.com/masa-san-jp/marketing-trends-notes) | 時間・チャネル・関係で蓄積するマーケティング変化KB | 同じMarkdown + Git型の入力KB。構造の基礎はこのrepoをもとにしていますが、鮮度・vendor根拠などは固有です |
| [agentic-art-research](https://github.com/masa-san-jp/agentic-art-research) | 複数入力から証拠を整理し、研究判断と制作handoffへ変換するrepo | 下流の研究実行側。美術史の正本を読み替えず、境界形式で参照します |
| [agentic-art-production](https://github.com/masa-san-jp/agentic-art-production) | research handoffから制作計画・実行・結果記録を扱うrepo | researchのさらに下流。実作品やproduction projectはこのrepoに保存しません |
| [viewer-response-notes](https://github.com/masa-san-jp/viewer-response-notes) | viewer反応のprivacy-safeな集計と保守的な制作要件評価 | 横断的なfeedback入力。生回答やPIIをこのrepoへ持ち込みません |
| [agentic-art-orchestration](https://github.com/masa-san-jp/agentic-art-orchestration) | 上記repoをsource commit固定で横断利用するcontrol plane | 親のデータベースではありません。各repoの正本性を保ったまま接続します |
| [agentic-art-project](https://github.com/masa-san-jp/agentic-art-project) | 公開制作プラン、作品、制作記録のカタログ | art-historyのentity本文を直接公開せず、Research・Production・Orchestrationの検証済み境界を経た成果だけが公開されます |

このrepo単体で美術史データの閲覧・検索・検証・追記は完結します。横断的な調査や制作handoffが必要な
場合だけ、orchestrationのrunbookと各repoのREADMEを参照してください。

## 最短手順

前提は Python 3.12 と [uv](https://docs.astral.sh/uv/) です。Python本体や依存パッケージを直接呼ばず、
リポジトリ内のPythonコマンドは次の形式で実行してください。

```bash
uv sync --locked
uv run --locked python tools/agent_doctor.py --json
uv run --locked python tools/test_agent_readiness.py
```

`test_agent_readiness.py` は外部Agent向けのunit/integration/E2Eと、最後に正準検証をまとめて実行します。
データだけを検証する場合は次を使います。

```bash
uv run --locked python tools/verify.py
```

commit前にも同じ検証を自動実行するには、cloneごとに一度だけhookを有効化します。

```bash
git config core.hooksPath .githooks
```

## よく使う操作

### データを読む・探す

```bash
# キーワード、型、関係を含むまとまりを読む
uv run --locked python tools/bundle.py --search 調和
uv run --locked python tools/bundle.py movement/kano-school

# 時間・地域・距離から同時代の候補を探す
uv run --locked python tools/query_spacetime.py --at 1885
uv run --locked python tools/query_spacetime.py --at 1885 --near place/paris --radius-km 500 --format json

# 文脈間の類似と相違を比較する
uv run --locked python tools/compare_context.py context/ai-art-japan-2026-h2 --kind historical --top 10
```

`query_spacetime.py` の結果は年代や場所が一致する候補です。類似性・影響・因果関係の証拠ではありません。
`--at` と `--from/--to` は排他で、BCEは天文学的年番号（紀元前900年は `-899`）を使います。

### データを書く・生成する

1. [`docs/schema.md`](docs/schema.md) と該当する調査手順を読む。
2. 出典URL付きのMarkdown entity/contextを編集する。確定できないことは `未確認` として残す。
3. 必要なら雛形を作る。

```bash
uv run --locked python tools/new_entity.py movement kano-school --ja 狩野派 --en "Kanō school"
```

4. 入力から生成物を更新する。

```bash
uv run --locked python tools/build_graph.py
uv run --locked python tools/build_context_vectors.py
```

生成物を直接編集しないでください。`data/graph.json`、`data/coverage.json`、
`data/context-vectors.json`、`data/context-similarity.json`、`overviews/coverage.md` は生成物です。
検証だけを行う場合は `tools/build_graph.py --check` または `tools/build_context_vectors.py --check` を使います。

## データの基本ルール

- 1 entity 1ファイル。frontmatterが正本です。
- すべての調査記述に出典URLを置き、一次情報を優先します。
- `movement`、`person`、`work`、`place` などの型と関係語彙は [`docs/schema.md`](docs/schema.md) に従います。
- 時間はEDTF、空間は役割付きの場所参照、解釈を含む関係は確度と出典を持ちます。
- 外部典拠IDがない場合は、理由を `none_reason` に残します。
- 実物を見ていない作品は「実物未見」、確認できない事項は「未確認」と明記します。

## リポジトリの構成

```text
entities/       人物・作品・ムーブメント・場所などの正本
contexts/       根拠付きの時代文脈スナップショット
overviews/      俯瞰資料（coverage.mdは生成物）
config/         文化圏、検証閾値、task/check schemaの設定
docs/           schema、調査手順、Agent向け手順、標準対応表
tools/          検証、検索、生成、Agent向けローカルCLI
data/           検証・生成された機械可読データ
tests/          domain検証とAgent interfaceのテスト
```

## 外部Agentで作業する

Agentの入口は [AGENTS.md](AGENTS.md) です。task contractがある場合は、contractをvalidateしてから
作業前baselineを記録し、許可されたscopeだけを変更し、最後にtask verifyを実行します。
詳細な手順、責務境界、受入れ証跡は [`docs/agent/README.md`](docs/agent/README.md) を読んでください。

このハーネスは、Agentを選定・起動・ホストする仕組みではありません。GitHub Actionsも検証だけを行い、
Agent executable、モデルAPI、GitHub write権限、repository secretを要求しません。
commit、push、PR、Issue更新は利用者が明示的に依頼した場合だけ行います。

## 検証とCI

正準検証は次の1コマンドです。

```bash
uv run --locked python tools/verify.py
```

この検証は必須項目、参照先、関係語彙、EDTF、生成物の鮮度、時間・空間・関係の整合性を確認します。
`tools/audit.py` は検証を止めずに、偏りや未調査事項を「次に調べること」として報告します。

GitHub Actionsには、正準検証用の `validate.yml` と、Agent interface全体を検証する
`agent-readiness.yml` があります。いずれもAgentを起動せず、read-onlyの検証だけを行います。

## 関連ドキュメント

- [`AGENTS.md`](AGENTS.md)：作業時の指示と完了報告の正本
- [`docs/schema.md`](docs/schema.md)：型、必須項目、関係語彙、EDTF、claims
- [`docs/investigation-task.md`](docs/investigation-task.md)：1件の調査手順
- [`docs/context-investigation-task.md`](docs/context-investigation-task.md)：時代文脈の調査手順
- [`docs/agent/acceptance.md`](docs/agent/acceptance.md)：Agent interfaceとE2Eの対応表
- [`docs/for-other-personas.md`](docs/for-other-personas.md)：他の人格が読むときの扱い
