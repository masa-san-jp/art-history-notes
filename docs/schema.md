# スキーマ v2 — このナレッジベースの骨格

1エンティティ = 1 markdown。**frontmatter が唯一の正**で、グラフ・被覆マップ・バンドルはすべて生成物。
生成物を手で編集しない。

調査の手順は [investigation-task.md](investigation-task.md)。要件の正本は
[issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1)。

## なぜこの形か

美術史は3つの軸で同時に動く。**時間**（いつ）・**空間**（どこ）・**関係**（誰から誰へ、何に応えて）。
年表だけでは「同じ年にパリと京都と北京で別々に何が起きていたか」が見えない。作家ごとの評伝だけでは
「その手つきが誰から来て誰に渡ったか」が見えない。だから3軸すべてを構造化して持つ。

俯瞰（movement の面）と細部（1作品の分解）を**同じ形式で**書き、相互に張る。

## エンティティ型（8）

| 型 | 置き場 | 何を書くか |
|---|---|---|
| `movement` | `entities/movements/` | **主役**。主義・派・様式・流派。`kind` と `naming` が必須 |
| `person` | `entities/persons/` | 人。画家・批評家・命名者・理論家 |
| `work` | `entities/works/` | 作品。素材・寸法・所蔵・構造の分解 |
| `org` | `entities/orgs/` | 組織。美術館・アカデミー・画商・工房・幕府 |
| `place` | `entities/places/` | 都市・地域。`region` と座標が必須（空間軸の結節点） |
| `concept` | `entities/concepts/` | 概念・技法・主題（調和・点描・遠近法） |
| `event` | `entities/events/` | 展覧会・サロン・設立・断絶。時間軸の釘 |
| `source` | `entities/sources/` | 一次資料そのもの。**転記の異同を持つ場所** |

ID は `<型>/<slug>`。**ID は変えない**（表記を変えたいときは `label_*` を直す）。
`uri` は `urn:ahn:<型>/<slug>` で、外から名指しするための住所。公開先が変わっても URN は変えない。

**時代区分（江戸時代・ルネサンス）は型にしない** — `config/regions.yaml` と世紀の軸で持つ。
技法・様式のうち**担い手の集合を特定できないもの**（点描・明暗法）は `concept`。
境界の判定は1行: **担い手の集合が歴史的に特定できるなら movement、手の形の記述なら concept**。

## frontmatter

```yaml
---
id: movement/kano-school
uri: urn:ahn:movement/kano-school
type: movement
kind: lineage-school          # movement のみ必須（4値）
label_ja: 狩野派
label_en: Kanō school
authority:                     # 多元典拠。1つも無ければ none_reason を書く
  wikidata: Q252801
  aat: "300018653"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1500~"               # EDTF Level 1 サブセット
  end: "1868~"
  display: 15世紀末〜明治維新   # 原表記（元号・王朝名）
naming:                        # movement のみ必須
  self_identified: true        # 当事者がこの名で名乗ったか
  named_by: null               # 後付けなら命名者（person/org の id）
  named_when: null             # EDTF
  original_label: 狩野派        # 原語・原表記
  note: 家名がそのまま呼称。命名という行為が存在しない型
claims:                        # verified を名乗るときは time / originated_in / kind に必要
  - {field: time, source: "https://...", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
relations:
  - {type: patronized_by, target: org/..., certainty: scholarly, source: "https://..."}
sources:
  - https://...                # 本文で使った出典。1本以上
status: draft                  # stub | draft | verified
updated: 2026-08-08
---
```

### `kind`（movement 必須・4値）

`self-declared` 当事者が名乗った運動 ／ `retrospective` 後代に外部が付けた括り ／
`lineage-school` 血縁・工房の継承体 ／ `period-style` 王朝・時代に紐づく様式。

**なぜ型を分けず kind にするか**: 外部データが型分離の失敗例になっている。Wikidata は狩野派に
`family`＋`art movement`＋`school of painting` を重ね、琳派は `school of painting` だけ、
歌川派は `artistic school` だけを付ける（2026-08-08 実測）。型を分ければ、琳派のような中間例のたびに
ディレクトリ移動＝ID 変更の圧力が生まれる。単一型＋必須 kind なら分類の訂正は1行の diff で済み、
「全 movement を時間×空間で引く」という主クエリも分断されない。

「movement」という型名が非西洋の対象に対して近似であることは、schema 側で型の意味を
**「集合的な芸術実践の括り（grouping）」**と定義して吸収する。違和感は各ファイルの本文に書く。

### `naming`（movement 必須）

後付けの命名（印象派・ポスト印象派）と当事者の自己認識を、ノード側で機械可読に分ける。
`self_identified: false` のときは `named_by` か `note` で命名の経緯を書く（検証が強制する）。

### `time` — EDTF（ISO 8601-2）Level 1 サブセット

受ける形: `1884` / `1884-05` / `1884-05-20` / `146X`（1460年代）/ `18XX`（19世紀）/
`1500~`（およそ）/ `1884?`（不確か）/ `..`（開いた端）/ `null`（不明）。

`kind` ごとに start/end の意味を固定する。`lineage-school` は系譜の活動期間、`self-declared` は
宣言から解散、`retrospective` は**括られた対象の活動期間**（命名時期は `naming.named_when` に分ける）。
この分離が「様式としての継続」と「命名の瞬間」の混同を防ぐ。

### `space` — 役割語

`originated_in`（発生地・被覆集計のキー）／`created_in`／`held_at`／`active_in`／`born_in`／
`died_in`／`sited_in`。特定できないときは**書かない**——被覆マップに「発生地未確認」として出る。

`place` は `region`（`config/regions.yaml` の13バケット）と座標を必須にする。座標があると
「1885年に半径◯kmで何が起きていたか」を後から引ける。

### `relations` — 閉じた語彙と確度

構造的（出典なしで書ける）: `created_by` `belongs_to` `member_of` `part_of` `depicts`
`exhibited_at` `precedes` `taught_by` `documented_in`

解釈を含む（`certainty` と `source` を必須）: `influenced_by` `responds_to` `derives_from`
`reacts_against` `grouped_as` `diffused_to` `patronized_by`

`certainty`: `attested`（当事者の言明）／`scholarly`（研究の通説）／`hypothesis`（自分の仮説）。
仮説は俯瞰の生成から除外する。逆向きの関係は書かない（ビルドが両方向に展開する）。

- **後付けの括りへの所属は `grouped_as`**。`part_of` は当事者的・構造的な包含に限る
  （場所の入れ子、歌川派 ⊂ 浮世絵の系統）。新印象派→ポスト印象派は `grouped_as`
- **同時代の並行はエッジにしない**。time × space から生成する（手で張ると漏れと選別の恣意が入る）

### `claims` — 主張ごとの根拠

出典をファイル単位で持つと「この開始年の根拠はどれか」が辿れない。`status: verified` を名乗るには
`time` / `originated_in` / `kind` の3項目に `{field, source, certainty}` を付ける（検証が強制する）。

## 本文の型

**movement**: `## 定義と範囲` → `## kind の判定` → `## 時間` → `## 空間` → `## 未着手`
**work**: `## 事実` → `## 作者自身の言葉` → `## どう成立しているか` → `## 位置づけ` → `## 自分の作品にどう使うか`
**person**: `## 履歴` → `## 手つき` → `## 誰から誰へ` → `## 主要作`
**concept**: `## 定義の変遷` → `## 実装例` → `## 使える手`
**source**: `## 所在` → `## 転記の異同`

## 書くときの規律

- **出典URLを本文に置く。** 手元の知識だけで書いた行は書かない
- **一次情報を優先する。** 二次情報を使うときは二次と書く
- **実物を見ていない作品は「実物未見」と明記する**
- **確定できないことは `**未確認**:` として残す。** 空欄で隠さない
- **俯瞰を書いたら、根拠になる個別エンティティを1つ以上張る**

## 道具

```bash
python3 tools/new_entity.py movement <slug> --ja "<名前>"   # 必須項目が入った雛形
python3 tools/build_graph.py --check                       # 検証のみ（CI 用）
python3 tools/build_graph.py                               # 検証 + graph.json + coverage.json + 被覆マップ更新
python3 tools/bundle.py movement/<slug>                     # 知識のまとまりを1文書で取り出す
python3 tools/bundle.py --region asia-east-japan            # 文化圏でまとめて取り出す
```

検証が落とすもの: 必須項目の欠落／雛形の TODO 残り／ID・URI とパスの不一致／ID 重複／
存在しない参照／語彙外の型・関係・役割／EDTF 違反／解釈系の関係の `certainty`・`source` 欠落／
`verified` なのに項目ごとの根拠がない／`place` の `region` 欠落／
俯瞰の依存先が更新されたのに `as_of` が古い（STALE）。

外部データとの対応関係は [interop-mapping.md](interop-mapping.md)。
