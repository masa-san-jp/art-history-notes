# art-history-notes

美術史のナレッジベース。aiko-art（私）が書き、積む。

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
overviews/         俯瞰。coverage.md の表は生成物（手で書き換えない）
config/            regions.yaml = 文化圏13バケットと受け入れ条件の閾値
docs/
  schema.md            型・必須項目・関係語彙・EDTF・claims。書く前に読む
  investigation-task.md 1件の調査の手順（Sonnet が単独で1件を終えられる粒度）
  interop-mapping.md    外部標準（CIDOC-CRM / Linked Art / Getty）との対応表
  design-fable-draft.md 設計の草案と、その根拠になった実測
tools/
  kb.py              スキーマ定義と共通部品（1箇所）
  new_entity.py      必須項目が入った雛形を作る
  build_graph.py     検証 → data/graph.json・data/coverage.json・被覆マップ更新
  bundle.py          知識のまとまりを1文書として取り出す
data/              生成物（graph.json / coverage.json）
```

## 3軸をどう持っているか

- **時間** — `time.start` / `end` は **EDTF**（`146X`＝1460年代／`1500~`＝およそ／`..`＝継続中／
  `null`＝不明）。不明を推測で埋めない。原表記（元号・王朝名）は `display` に残す。
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

```bash
python3 tools/new_entity.py movement kano-school --ja 狩野派 --en "Kanō school"
python3 tools/build_graph.py --check     # 検証だけ（CI 用）
python3 tools/build_graph.py             # 検証 + グラフ・被覆マップの生成
python3 tools/bundle.py --search 調和               # 語で探す（IDを知らなくていい）
python3 tools/bundle.py movement/kano-school        # 1件とその周辺を1文書で
python3 tools/bundle.py --region asia-east-japan    # 文化圏でまとめて
python3 tools/bundle.py --century 19                # 世紀でまとめて
```

1件の調査は [docs/investigation-task.md](docs/investigation-task.md) の手順だけで終わる。

**他の人格（アイコたち）が読むときは [docs/for-other-personas.md](docs/for-other-personas.md) から。**
このKBの使い手はアイコたちで、引用してよい記述とだめな記述の区別がそこに書いてある。

## 書くときの規律

- 出典URLを本文に置く。手元の知識だけで書いた行は書かない。
- 一次情報を優先する（所蔵館 API・本人の手紙・カタログ）。二次情報は二次と書く。
- 実物を見ていない作品は「実物未見」と明記する。
- 確定できないことは `未確認` として残す。空欄で隠さない。
- 俯瞰を書いたら、根拠になる個別エンティティを1つ以上張る。張れないなら書く段階にない。

詳細は [docs/schema.md](docs/schema.md)。

## いま入っているもの

`python3 tools/build_graph.py` の出力が正確な現在地（件数をここに書き写すと必ず古くなる）。
空白の全体像は [overviews/coverage.md](overviews/coverage.md)。

## 制作との接続

当面の制作締切は AIアートグランプリ5「調和」（2026-09-15・**1名1作品のみ**）と
AIクリエイターズマーケット2026（2026-11-07）。だから最初に深く掘るのは
[concept/harmony](entities/concepts/harmony.md)。ただしこのKBは締切のための資料置き場ではなく、
締切が変わっても残る蓄積として作る。
