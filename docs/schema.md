# スキーマ — このナレッジベースの骨格

## 何のためにこの形にするか

美術史は3つの軸で同時に動く。**時間**（いつ）・**空間**（どこ）・**関係**（誰から誰へ、何に応えて）。
年表だけでは「同じ年にパリとロンドンと京都で何が別々に起きていたか」が見えない。作家ごとの評伝だけでは
「その手つきが誰から来て誰に渡ったか」が見えない。だから3軸すべてを構造化して持つ。

俯瞰（movement / period の面）と細部（1作品の分解）を**同じ形式で**書き、相互に張る。
俯瞰は細部の集約として検証でき、細部は俯瞰の中に位置づけられる。片方だけを書き足す運用にしない。

## エンティティ

1エンティティ = 1ファイル。`entities/<型>/<slug>.md`。

| 型 | 置き場 | 何を書くか |
|---|---|---|
| `artist` | `entities/artists/` | 人。生没・活動地・師弟・所属運動 |
| `work` | `entities/works/` | 作品。素材・寸法・所蔵・構造の分解 |
| `movement` | `entities/movements/` | 運動・様式。始点と終点、中心地、担い手 |
| `place` | `entities/places/` | 都市・施設。座標を持たせて空間軸の結節点にする |
| `concept` | `entities/concepts/` | 概念・技法・主題（調和・点描・遠近法など） |
| `event` | `entities/events/` | 展覧会・サロン・断絶。時間軸の目印 |

`slug` は `<姓>-<名>` / `<作品名>` のケバブケース。ID は `<型>/<slug>`（例 `artist/georges-seurat`）。
**ID は変えない。** 名前の表記を変えたいときは `label_*` を直す。

## frontmatter（必須）

```yaml
---
id: work/a-sunday-on-la-grande-jatte   # <型>/<slug>。ファイルパスと一致させる
type: work
label_ja: グランド・ジャット島の日曜日の午後
label_en: A Sunday Afternoon on the Island of La Grande Jatte
authority:                 # 外部の典拠ID。分かるものだけ書く
  wikidata: Q1044742
  ulan: null               # 人・組織は Getty ULAN
  aat: null                # 概念・様式・技法は Getty AAT
  tgn: null                # 場所は Getty TGN
time:
  start: 1884              # 年（不明なら null）
  end: 1886
  note: 額縁の彩色は1888–89年に追加
space:
  - {role: created_in, target: place/paris}
  - {role: held_at, target: place/art-institute-of-chicago}
relations:
  - {type: created_by, target: artist/georges-seurat}
  - {type: belongs_to, target: movement/neo-impressionism}
sources:                   # 本文で使った出典URL。1本以上必須
  - https://api.artic.edu/api/v1/artworks/27992
status: verified           # stub | draft | verified
updated: 2026-08-08
---
```

**典拠IDを付ける理由**: Wikidata / Getty の ID を持たせておけば、後から所蔵館の API・IIIF 画像・
Linked Art 形式のデータと突き合わせられる。名前の表記揺れ（Seurat / スーラ / スーラー）で
同一性を失わない。これがこの蓄積を「ノートの山」ではなく接続可能なデータにする一点。

参照: [Linked Art](https://linked.art/model/)（CIDOC-CRM 7.1.3 + Getty Vocabularies + JSON-LD の
実装プロファイル。美術館データの事実上の標準）／[Getty Vocabularies](https://www.getty.edu/research/tools/vocabularies/)

## 関係の語彙（この閉じたリストから選ぶ）

| type | 意味 | 主体 → 対象 |
|---|---|---|
| `created_by` | 制作した | work → artist |
| `belongs_to` | 属する運動・様式 | work / artist → movement |
| `taught_by` | 師事した | artist → artist |
| `influenced_by` | 影響を受けた（本人の言明か研究の裏付けがある場合のみ） | any → any |
| `responds_to` | 応答・反論として作られた | work → work / concept |
| `depicts` | 描いている主題 | work → concept / place |
| `member_of` | 所属した団体 | artist → event / movement |
| `exhibited_at` | 出品した | work → event |
| `part_of` | 上位に含まれる | place → place, movement → movement |
| `precedes` | 直前にある（時間軸の連結） | movement → movement |
| `documented_in` | 一次文献に記述がある | any → source |

逆向きの関係は書かない。`tools/build_graph.py` が両方向に展開する。

## 空間軸の役割語

`created_in`（制作地）／`held_at`（現所蔵）／`active_in`（活動地）／`born_in`／`died_in`／`sited_in`（場所の入れ子）。
`place` には必ず座標を入れる。座標があると「1885年に半径500kmで何が起きていたか」を後から引ける。

## 本文の型

frontmatter の下は、型ごとに見出しを固定する。

**work**: `## 事実` → `## 作者自身の言葉` → `## どう成立しているか` → `## 位置づけ`（時間・空間・関係の中での座標）
→ `## 自分の作品にどう使うか`

**artist**: `## 履歴` → `## 手つき`（何をどうやる人か） → `## 誰から誰へ` → `## 主要作`

**movement**: `## 定義と範囲` → `## 中心と広がり`（空間） → `## 前後`（時間） → `## 担い手` → `## 何が新しかったか`

**concept**: `## 定義の変遷`（誰がいつどう定義したか） → `## 実装例`（それを実際に使っている作品） → `## 使える手`

## 書くときの規律

- **出典URLを本文に置く。** 手元の知識だけで書いた行は書かない。
- **一次情報を優先する。** 所蔵館の API・本人の手紙・カタログ。二次情報を使うときは二次と書く。
- **実物を見ていない作品は「実物未見」と明記する。** 図版と museum text から言えることだけ書く。
- **確定できないことは `未確認` の見出しで残す。** 空欄で隠さない。転記の揺れ、年代の異説も残す。
- **`status` を正しく置く。** `stub`＝枠だけ／`draft`＝書いたが出典が薄い／`verified`＝一次情報で裏が取れた。
- **俯瞰を書いたら、根拠になる個別エンティティを1つ以上張る。** 張れないなら、まだ俯瞰を書く段階にない。

## 検証

```bash
python3 tools/build_graph.py          # frontmatter を検証し data/graph.json を出力
python3 tools/build_graph.py --check   # 出力せず検証だけ（CI 用）
```

検出するもの: 必須項目の欠落／ID とパスの不一致／存在しない ID への参照（dangling）／
未知の関係 type ／`sources` が空。
