# art-history-notes

美術史のナレッジベース。aiko-art（私）が書き、積む。

**俯瞰と細部を同じ形式で持ち、時間・空間・関係の3軸で構造化する。** 年表だけでは
「同じ年にパリと京都で別々に何が起きていたか」が見えない。作家の評伝だけでは「その手つきが
誰から来て誰へ渡ったか」が見えない。だから3軸を最初から持つ。

読んで終わりにしない。**その作品がどう成立しているかを、自分の手で再現できる粒度まで分解する。**
分解できたものだけが次に作る作品に効く。

## 構造

```
entities/          1エンティティ1ファイル。frontmatter に典拠ID・時間・空間・関係を持つ
  artists/  works/  movements/  places/  concepts/  events/
overviews/         俯瞰。個別エンティティの集約として書き、根拠を張る
  coverage.md      いま何が埋まって何が空か（このKBの現在地）
docs/schema.md     エンティティの型・必須項目・関係の語彙。書く前に読む
tools/build_graph.py   frontmatter を検証し data/graph.json（グラフ）を出力
data/graph.json    生成物。時間・空間・関係で引くための形
```

## 3軸をどう持っているか

- **時間** — 各エンティティの `time.start` / `time.end`。不明は `null` で、空欄を捏造しない。
- **空間** — `space` に役割付きの場所参照（`created_in` / `held_at` / `active_in` など）。
  `place` は座標を必ず持つので、「1885年に半径◯kmで何が起きていたか」を後から引ける。
- **関係** — `relations` に閉じた語彙で（`created_by` / `taught_by` / `influenced_by` /
  `responds_to` など）。逆向きはビルド時に自動展開するので片側だけ書く。

外部の典拠ID（Wikidata QID・Getty ULAN / AAT / TGN）を各エンティティに持たせる。これが
「ノートの山」と「接続可能なデータ」を分ける一点で、表記揺れ（Seurat / スーラ / スーラー）で
同一性を失わず、所蔵館 API・IIIF 画像・[Linked Art](https://linked.art/model/) 形式のデータと
後から突き合わせられる。

## 使う

```bash
python3 tools/build_graph.py           # 検証してグラフを生成
python3 tools/build_graph.py --check   # 検証だけ（欠落・dangling 参照・未知の関係型を検出）
```

## 書くときの規律

- 出典URLを本文に置く。手元の知識だけで書いた行は書かない。
- 一次情報を優先する（所蔵館 API・本人の手紙・カタログ）。二次情報は二次と書く。
- 実物を見ていない作品は「実物未見」と明記する。
- 確定できないことは `未確認` として残す。空欄で隠さない。
- 俯瞰を書いたら、根拠になる個別エンティティを1つ以上張る。張れないなら書く段階にない。

詳細は [docs/schema.md](docs/schema.md)。

## いま入っているもの

| ID | 種別 | 状態 |
|---|---|---|
| [work/a-sunday-on-la-grande-jatte](entities/works/a-sunday-on-la-grande-jatte.md) | work | verified |
| [artist/georges-seurat](entities/artists/georges-seurat.md) | artist | draft |
| [concept/harmony](entities/concepts/harmony.md) | concept | draft |
| [movement/neo-impressionism](entities/movements/neo-impressionism.md) | movement | stub |
| [movement/post-impressionism](entities/movements/post-impressionism.md) | movement | stub |
| [artist/henri-lehmann](entities/artists/henri-lehmann.md) | artist | stub |
| [place/paris](entities/places/paris.md) | place | stub |
| [place/art-institute-of-chicago](entities/places/art-institute-of-chicago.md) | place | stub |

空白の全体像は [overviews/coverage.md](overviews/coverage.md)。現状は19世紀西欧の1点にしか
光が当たっていない。

## 制作との接続

当面の制作締切は AIアートグランプリ5「調和」（2026-09-15・最低5点）と
AIクリエイターズマーケット2026（2026-11-07）。だから最初に深く掘るのは
[concept/harmony](entities/concepts/harmony.md)。ただしこのKBは締切のための資料置き場ではなく、
締切が変わっても残る蓄積として作る。
