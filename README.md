# art-history-notes

時間・空間・関係の3軸で、美術史の人物・作品・ムーブメントを根拠付きで蓄積するナレッジベースです。
エンティティと時代文脈をたどり、調査候補を生成できます。

## まず何を読むか

目的に応じて入口を選んでください。

| 目的 | 入口 |
| --- | --- |
| 美術史データを読む | [`overviews/coverage.md`](overviews/coverage.md)、[`entities/`](entities/)、[`contexts/`](contexts/) |
| 1件を調査・追加する | [`docs/schema.md`](docs/schema.md)、[`docs/investigation-task.md`](docs/investigation-task.md) |
| 時代文脈を比較する | [`docs/context-investigation-task.md`](docs/context-investigation-task.md)、[`docs/context-vectors.md`](docs/context-vectors.md) |
| 外部Agentとして作業する | [`AGENTS.md`](AGENTS.md)、[`docs/agent/README.md`](docs/agent/README.md) |

このリポジトリは外部Agentが利用する受動的なナレッジベースです。Agent、モデル、認証、queue、daemon、自動commit、PR配送は起動しません。

## 外部Agentで作業する

このリポジトリは外部Agentが利用する受動的なハーネスを含む。Agentの入口は
[AGENTS.md](AGENTS.md)、ハーネスの詳細は[docs/agent/README.md](docs/agent/README.md)。
Agentを起動するためのGitHub Actions、モデルAPI key、PR配送は必要としない。

準備と受入れ検証は次で行う。

    uv sync --locked
    uv run --locked python tools/agent_doctor.py --json
    uv run --locked python tools/test_agent_readiness.py

**要件の正本は [issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1)。**
この README は現状の説明であって、要件ではない。食い違ったら issue を正とする。

**俯瞰と細部を同じ形式で持ち、時間・空間・関係の3軸で構造化する。** 年表だけでは
「同じ年にパリと京都で別々に何が起きていたか」が見えない。作家の評伝だけでは「その手つきが
誰から来て誰へ渡ったか」が見えない。だから3軸を最初から持つ。

読んで終わりにしない。**その作品がどう成立しているかを、自分の手で再現できる粒度まで分解する。**
分解できたものだけが次に作る作品に効く。

## 構造

```
entities/          1エンティティ1ファイル。frontmatter が唯一の正
  movements/  persons/  works/  orgs/  places/  concepts/  events/  sources/
contexts/          時期×文化圏×アート領域を限定した、根拠付き時代文脈スナップショット
overviews/         俯瞰。coverage.md の表は生成物（手で書き換えない）
config/            regions.yaml = 文化圏13バケットと受け入れ条件の閾値
                   context-dimensions.yaml = 文脈比較の固定12軸
docs/
  schema.md            型・必須項目・関係語彙・EDTF・claims。書く前に読む
  investigation-task.md 1件の調査の手順（Sonnet が単独で1件を終えられる粒度）
  interop-mapping.md    外部標準（CIDOC-CRM / Linked Art / Getty）との対応表
  design-fable-draft.md 設計の草案と、その根拠になった実測
tools/
  kb.py              スキーマ定義と共通部品（1箇所）
  verify.py          全検証・生成物鮮度確認の正準エントリポイント
  new_entity.py      必須項目が入った雛形を作る
  build_graph.py     検証 → data/graph.json・data/coverage.json・被覆マップ更新
  bundle.py          知識のまとまりを1文書として取り出す
  context_kb.py      contextの検証・ベクトル計算・比較
  build_context_vectors.py  context生成物を決定論的に作る
  compare_context.py context間の類似と相違を根拠付きで表示する
data/              生成物（graph / coverage / context vectors / context similarity）
```

## 3軸をどう持っているか

- **時間** — `time.start` / `end` は **EDTF**（`0000`＝紀元前1年／`-0001`＝紀元前2年／`-0899`＝紀元前900年／
  `146X`＝1460年代／`1500~`＝およそ／`..`＝継続中／`null`＝不明）。不明を推測で埋めない。原表記（元号・王朝名）は `display` に残す。
- **空間** — `space` に役割付きの場所参照（`originated_in` / `created_in` / `held_at` / `active_in`…）。
  `place` は文化圏（`region`）と座標を必ず持つので、「1885年に半径◯kmで何が起きていたか」を引ける。
- **関係** — `relations` は閉じた語彙。解釈を含むもの（`influenced_by` / `derives_from` /
  `grouped_as` / `diffused_to`…）は **確度（`certainty`）と出典が必須**で、当事者の言明・研究の通説・
  自分の仮説を区別する。同時代の並行は保存せず、時間×空間から生成する。

主役は `movement`。**単一の型に保ち、必須の `kind`**（当事者が名乗った運動／後付けの括り／
血縁・工房の継承／時代様式）で性質を区別する。後付けの命名と当事者の自己認識は `naming` で分けて持つ。

外部の典拠ID（Wikidata QID・Getty AAT / ULAN / TGN・Japan Search・NDL）を各エンティティに持たせ、
無いときは理由（`none_reason`）を書く。`uri`（`urn:ahn:...`）で外から名指しでき、`claims` で
**主張ごとの根拠**を持つ。これが「ノートの山」と「接続可能なデータ」を分ける三点。外部標準との
対応は [docs/interop-mapping.md](docs/interop-mapping.md)。

## 使う

前提は Python 3.12 と [uv](https://docs.astral.sh/uv/)。clone直後に依存関係をlockどおり準備する。

```bash
uv sync --locked
uv run --locked python tools/verify.py
git config core.hooksPath .githooks
```

個別のCLIを試すときも、同じuv環境を使う。

```bash
uv run --locked python tools/new_entity.py movement kano-school --ja 狩野派 --en "Kanō school"
uv run --locked python tools/build_graph.py --check     # 検証だけ（CI 用）
uv run --locked python tools/build_graph.py             # 検証 + グラフ・被覆マップの生成
uv run --locked python tools/bundle.py --search 調和               # 語で探す（IDを知らなくていい）
uv run --locked python tools/bundle.py movement/kano-school        # 1件とその周辺を1文書で
uv run --locked python tools/bundle.py --region asia-east-japan    # 文化圏でまとめて
uv run --locked python tools/bundle.py --century 19                # 世紀でまとめて
uv run --locked python tools/query_spacetime.py --at 1885
uv run --locked python tools/query_spacetime.py --from 1880 --to 1890 --regions europe-west asia-east-japan
uv run --locked python tools/query_spacetime.py --at 1885 --near place/paris --radius-km 500 --format json
uv run --locked python tools/audit.py                              # 体系の食い違い・偏り → 次に調べること
uv run --locked python tools/build_context_vectors.py --check      # 時代文脈の検証だけ
uv run --locked python tools/build_context_vectors.py              # ベクトル・類似度を生成
uv run --locked python tools/compare_context.py context/ai-art-japan-2026-h2 --kind historical --top 10
```

1件の調査は [docs/investigation-task.md](docs/investigation-task.md) の手順だけで終わる。
時代文脈は [docs/context-investigation-task.md](docs/context-investigation-task.md) の手順で調査し、
[docs/context-vectors.md](docs/context-vectors.md) の固定式で比較する。

`query_spacetime.py` は `data/graph.json` の時間・空間条件から同時代の候補を生成する。
結果は類似性・影響・因果関係の証拠ではなく、年代や場所が不明なentityは補間せず除外理由を表示する。
`--at` と `--from/--to` は排他で、BCEは天文学的年番号（例: 紀元前900年は `-899`）を使う。

**他の人格（アイコたち）が読むときは [docs/for-other-personas.md](docs/for-other-personas.md) から。**
このKBの使い手はアイコたちで、引用してよい記述とだめな記述の区別がそこに書いてある。

## 検証が自動で走る

検査は2層。**`build_graph.py --check` は「壊れているか」**（必須項目・参照先・語彙・EDTF）を見て
commit を止める。**`audit.py` は「噛み合っていないか」**（時間の矛盾・型の食い違い・kind の地域偏り・
仮説が未検証・継承の先が辿れない）を見て、止めずに**次に調べることとして出す**。
形が正しいだけの体系は、機械が黙っているうちに静かに矛盾を溜める。

`.githooks/pre-commit` が commit のたびに `uv run --locked python tools/verify.py` を走らせ、通らないものを止める。
生成物（`data/` と被覆マップ）が古いままの commit も止める。

**clone した直後に1回だけ**（これをしないとフックは動かない）:

```bash
git config core.hooksPath .githooks
```

忘れてもCIの同じ正準コマンドで検出できる。手で走らせる規律に頼ると、走らせ忘れた1回で壊れたまま履歴に入る。

## 書くときの規律

- 出典URLを本文に置く。手元の知識だけで書いた行は書かない。
- 一次情報を優先する（所蔵館 API・本人の手紙・カタログ）。二次情報は二次と書く。
- 実物を見ていない作品は「実物未見」と明記する。
- 確定できないことは `未確認` として残す。空欄で隠さない。
- 俯瞰を書いたら、根拠になる個別エンティティを1つ以上張る。張れないなら書く段階にない。

詳細は [docs/schema.md](docs/schema.md)。

## いま入っているもの

`uv run --locked python tools/build_graph.py` の出力が正確な現在地（件数をここに書き写すと必ず古くなる）。
空白の全体像は [overviews/coverage.md](overviews/coverage.md)。

## 制作との接続

当面の制作締切は AIアートグランプリ5「調和」（2026-09-15・**1名1作品のみ**）と
AIクリエイターズマーケット2026（2026-11-07）。だから最初に深く掘るのは
[concept/harmony](entities/concepts/harmony.md)。ただしこのKBは締切のための資料置き場ではなく、
締切が変わっても残る蓄積として作る。
