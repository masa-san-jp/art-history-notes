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

### 時代文脈はentityではない

時代文脈は9番目のエンティティ型にしない。`contexts/`に、時期・文化圏・アート領域を限定した分析
スナップショットとして置く。保存する正本は根拠付きの`signal`で、固定12軸のベクトル、信頼度、類似度は
`tools/build_context_vectors.py`が作る生成物である。情報がない軸を中立値0で補わない。

context比較は研究候補の生成にだけ使い、`influenced_by`などの関係や史実・因果関係へ自動変換しない。
詳細は[context-vectors.md](context-vectors.md)と[context-investigation-task.md](context-investigation-task.md)。

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
  start: "14XX"                # EDTF。Wikidata の precision 7 ＝世紀の主張
  end: "1868~"
  display: 15世紀（室町後期）〜明治維新   # 原表記（元号・王朝名）
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
  - url: https://example.org/catalogue
    kind: scholarly         # primary / scholarly / institutional / authority / reference
    note: 研究書・展覧会カタログなど、資料の位置づけ
status: draft                  # stub | draft | verified
updated: 2026-08-08
---
```

### `sources` — 構造化出典

正準形式は `url`、`kind`、任意の `note` を持つobject配列である。`kind` は次の5値に限定する。

| kind | 判断基準 |
|---|---|
| `primary` | 同時代の宣言、書簡、作品そのもの、当時の記録。資料種別がURLだけで明白でないときは `note` を必須にする |
| `scholarly` | 研究書、査読論文、研究者による展覧会カタログ・論考 |
| `institutional` | 美術館・大学・公的機関の解説やコレクションページ |
| `authority` | Wikidata、Getty、NDLなどの典拠レコード |
| `reference` | 上記に分類できない概説、百科事典、検索入口 |

旧形式のURL文字列は受理しない。URLのscheme/host、kind、同一entity内の重複URLを検証し、
`claims[].source` と解釈系 `relations[].source` が `sources[].url` に存在することを検証する。
`context` の `signals[].source` も同じ規則で扱う。全型の移行残数は次でJSONまたはMarkdownに再現できる。

```bash
uv run --locked python tools/audit_source_migration.py
uv run --locked python tools/audit_source_migration.py --format markdown
uv run --locked python tools/audit_source_migration.py --check-type movement
uv run --locked python tools/audit_source_migration.py --check-type context
uv run --locked python tools/audit_source_migration.py --check-type person
uv run --locked python tools/audit_source_migration.py --check-type work
```

全8 entity型が構造化形式へ移行済みで、各型の `--check-type` をCIのゲートにしている。

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

**3つ目の項目 `rejected_by`（任意）**: **当事者がその括りを拒んだ**場合に、誰が拒んだかを配列で残す。
「引き受けなかった」（`self_identified: false`）と「**積極的に拒んだ**」は別の事実である。

```yaml
naming:
  self_identified: false
  rejected_by: ["ロスコ（『私は抽象画家ではない』）", "李康昭", "崔秉昭"]
```

実例: 抽象表現主義（ロスコが「私は抽象画家ではない」と明言）／単色画（李康昭・崔秉昭が2016年に
分類を拒否）。2件出たので項目にした。

**2つの項目は別のことを聞いている。**

- `self_identified` — 当事者が**その名を引き受けたか**（後からでもよい）
- `named_by` — **最初に付けたのは誰か**

だから「外部が付けた名を当事者が後から引き受けた」場合は `self_identified: true` かつ
`kind: retrospective` になる（新印象派——批評家フェネオンが1886年に命名し、参加者シニャックが
1899年に著書の題名として引き受けた）。逆に「当事者が結成して綱領も書いたが、いま通る名は後から
付いた」場合は `kind: self-declared` で `original_label` に当事者の呼称を残す（ザリア・アート・
ソサエティ——名乗ったのは "Art Society"）。**成り立ち（kind）と呼称の来歴（naming）は独立に動く。**

### frontmatter の意味制約

`tools/build_graph.py --check` は、YAMLとして読めるだけでは通さず、次の意味制約も検証する。

- `place.coordinates` は `[latitude, longitude]` の有限な数値2要素。緯度は `-90..90`、経度は `-180..180`
- `time` は `start` と `end` を持つマップ。両方ともEDTF Level 1サブセットで、`start: ".."` は不可。
  startの最小年がendの最大年より後の区間は不可だが、世紀表記などの曖昧な区間の重なりは許す
- movement の `naming.self_identified` はbool。`false` なら `named_by` または `note` が必要。
  `original_label` は必須で、nullにする場合はnoteに未確認理由を書く。`named_when` はEDTF、
  `named_by` は存在するperson/org IDにする
- `authority` のキーは `wikidata` / `aat` / `ulan` / `tgn` / `ndl` / `jpsearch` / `none_reason` に限定する。
  ID形式はそれぞれ Wikidata QID、AAT/ULAN 9桁、TGN 7–8桁、NDL 8桁。IDが1つでもあれば
  `none_reason` はnull、IDが無ければ空でない理由が必要
- `updated` は実在する `YYYY-MM-DD`。`aliases` は空でない文字列で、既存ID・他entityのaliasと衝突させない。
  型付きalias（`movement/old-slug`）は小文字slug、旧名などの人間向け文字列aliasは許可する
- `claims` の各項目は空でない `field`、`source`、`certainty` を持ち、同じclaimを完全重複させない

この検証の異常系fixtureは `tests/test_semantic_validation.py` に置く。仕様変更時はfixtureと本文を同じ変更で更新する。

### `former_names`（任意・place）— 土地の名前が時代で変わるとき

**土地1つにエンティティ1つ。名前の変化は `former_names` に持つ。** 別エンティティに分けない。

```yaml
# entities/places/tokyo.md
label_ja: 東京
former_names:
  - {name: 江戸, until: "1868"}
```

**なぜ分けないか**: 座標と文化圏（`region`）は**土地の性質**で、名前の性質ではない。江戸と東京を別の
エンティティにすると、同じ土地が地図の上で2点になり、「1885年に半径◯kmで何が起きていたか」という
空間の問いが壊れる。`label_ja` は**現在通用する名**にし、当時の名は `former_names` に期間つきで残す。
本文では当時の名で呼んでよい（「江戸（現在の東京）」）。

同じ扱いになる例: コンスタンティノープル／イスタンブール、漢城／ソウル、ペトログラード／
サンクトペテルブルグ。

### `place-region-history` — 場所と文化圏の時代差

土地を時代ごとに別エンティティへ分割すると、座標と参照が壊れる。そのため、場所の基準 `region` は
frontmatter に残し、時代で文化圏バケットが変わる例外だけを
`config/place-region-history.yaml` の辞書に置く。区間は `[start, end)`（開始を含み、終了を含まない）で、
movement の `time.start` と重なる項目を集計に使う。

```yaml
places:
  place/istanbul:
    - {start: "0330", end: "1453", region: europe-east}
    - {start: "1453", end: "..", region: mena}
```

movement の開始時期が複数区間にまたがる場合は、最初の1つに丸めず複数起源として扱う。開始時期が不明、
または辞書に該当項目がない場合は、place の基準 `region` に戻る。辞書のplace ID、region、EDTF、区間の重複は
`tools/build_graph.py --check` が検証する。

### overview frontmatter — 俯瞰の機械検証

手書きの `overviews/*.md` は、自由文を残したまま機械判定できる事実だけを `assertions` に置く。
`coverage.md` は生成物なので `assertions` を持たず、frontmatter の `as_of` と生成ブロックの最新日が
entityの `updated` の最大値と一致することを検証する。

```yaml
as_of: 2026-08-13
depends_on: [movement/kano-school, movement/rinpa]
assertions:
  - {subject: movement/kano-school, field: kind, equals: lineage-school}
  - {subject: movement/kano-school, relation: derives_from, target: movement/other}
  - {subject: movement/kano-school, space_role: originated_in, target: place/tokyo}
```

`assertions` の判定対象は次の3種類だけ。

- `field`: ドット区切りで辿れるscalar値との一致。配列・マップ・自由文は対象外。
- `relation`: entityの `relations` に同じ `type` と `target` が存在すること。
- `space_role`: entityの `space` に同じ `role` と `target` が存在すること。

`subject`、`target`、`tested[].by`、本文の相対entityリンクはすべて `depends_on` に含める。
存在しない参照、assertionとの不一致、依存漏れ、重複、古い `as_of` は
`uv run --locked python tools/build_graph.py --check` が止める。自由文全体の真偽は検証対象にしない。

### `coverage-reviews.yaml` — 調査済みの空セル

被覆表の空欄は未着手と調査済みの該当なしを兼ねない。後者は
`config/coverage-reviews.yaml` に文化圏・世紀単位で記録する。

```yaml
cells:
  - region: oceania
    century: "20"
    status: no-known-grouping
    note: "調査した範囲では、この文化圏・世紀に既存の movement として採れる直接の括りは確認できない"
    sources:
      - https://www.nma.gov.au/explore/collection/highlights/papunya-collection
```

`no-known-grouping` は「そのセルに movement が存在しない」という否定命題ではなく、記録した調査範囲で
このKBの movement として採れる括りが見つからなかった、という調査結果である。`build_graph.py --check`
は文化圏・世紀・URL・重複を検証し、既に movement があるセルへの記録を拒否する。生成された被覆表では
`∅` と表示され、通常の空欄（未着手）と区別される。

### `cross-region-reviews.yaml` — 4経路で接続を確認できないmovementの調査記録

`tools/audit.py` は movement 起源regionから外部regionへ到達する次の4経路だけを監査する。

1. movement→movement relation
2. movement→place の `diffused_to`
3. `space.active_in`
4. movement→event/org の `exhibited_at` から `held_at` / `sited_in` place への1 hop

接続が確認できないものを調査済みとして閉じる場合だけ、次の記録を追加する。`status` は固定値で、
URL 2件以上、重複・既接続movement・存在しないIDは監査が拒否する。

```yaml
reviews:
  - movement_id: movement/example
    status: no-documented-cross-region-relation
    checked: "2026-08-25"
    note: "調査範囲の資料では4経路による域外接続を確認できない"
    sources:
      - https://example.org/catalogue
      - https://example.org/institution
```

`data/audit.json` の `cross_region` は全movementを一度だけ、`connected` /
`reviewed-no-documented-link` / `unreviewed` の排他的3区分で返し、各接続の経路・edge列・到達regionを含む。

### `founding_control`（任意・movement）

**設立・所有・意思決定に、対象文化の外部者が構造的に含まれていたか。** `internal` / `shared` / `external`。

「外部者が関わったか」ではなく、**関わり方が構造的だったか**で測る。同じ `self-declared` でも、
外部者が触媒だった場合（Papunya Tula——教員が契機を作ったが、社名選定・法人化・会長・株主は
すべて当事者）と、組織の中核機能を外部者が設計・運営した場合（Pita Maha——審査制度と海外販売網を
ヨーロッパ人が担った）は、位置が違う。**世界規模で扱うなら、この差を潰してはいけない。**

判定に迷ったら `shared` を選び、誰が何を担ったのかを本文に書く。空欄でもよい（該当しない対象には書かない）。

**この値は「成立の時点」を指す。** 途中で決定の所在が移った場合は次の `control_changes` に書く。

### `control_changes`（任意・movement）— 決定の所在が移った時

`founding_control` は成立時点の1値しか持てない。だが決定の所在は**動く**。2件で確認した。

- [チュニス派](../entities/movements/ecole-de-tunis.md) — 1956年、独立の年に会長職がフランス人から
  チュニジア人に移った
- [バンドン派](../entities/movements/bandung-school.md) — 独立（1949年）では**変わらず**、
  1959年に西ニューギニア紛争でオランダ人が国籍選択を迫られて去り、同年 ITB がインドネシアの
  国立大学として独立したことで移った

**この2件で分かるのは、引き金は独立そのものではないということ。** 決定の所在が動くのは、
**具体の仕組みが決定者を入れ替えたとき**で、政治的独立はその仕組みの1つでしかない。
だから `trigger` を必須にする——年と値だけ書くと、何が動かしたのかが消える。

```yaml
founding_control: external        # 成立時点
control_changes:
  - {year: "1959", to: internal, trigger: "西ニューギニア紛争によるオランダ人の退去と、ITB のインドネシア国立大学としての独立"}
```

`year` は EDTF、`to` は `internal` / `shared` / `external`、`trigger` は必須（何が決定者を
入れ替えたか）。移る前の値は直前の要素、最初の要素の前は `founding_control` が指す。

### `images`（任意）— パブリックドメインの作品画像への参照

**その括りを目で見られるようにする。** 代表的な作品の画像URLを持つ。
`movement` なら代表作、`work` ならその作品、`person` なら代表作。

```yaml
images:
  - url: https://www.artic.edu/iiif/2/2d484387-.../full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/27992
    rights_source: https://www.artic.edu/artworks/27992
    license: public-domain          # public-domain / cc0 / pdm のどれか
    note: スーラ《グランド・ジャット島の日曜日の午後》
```

**規律**:
- **パブリックドメイン相当のものだけ**（`public-domain` / `cc0` / `pdm`）。検証が語彙を強制する
- **リンクだけ。画像ファイルを repo に置かない**（再配布はしない）
- `source_page` と `rights_source` は必須の http(s) URL。権利表示が作品ページにある場合は同じURLでよい
- `rights_source` は画像単体または所蔵機関の権利表示を直接確認できるページにする
- 権利が不明なものは**入れない**。「たぶん古いから大丈夫」で入れない
- 出どころの候補: Art Institute of Chicago（CC0）／Metropolitan Museum（Open Access CC0）／
  Cleveland Museum（CC0）／Rijksmuseum／National Gallery of Art／Wikimedia Commons（ファイル単位で確認）

### `time` — EDTF（ISO 8601-2）Level 1 サブセット

受ける形: `1884` / `0000`（紀元前1年）/ `-0001`（紀元前2年）/ `-0899`（紀元前900年）/ `1884-05` / `1884-05-20` /
`146X`（1460年代）/ `14XX`（15世紀）/ `-08XX`（紀元前900年代）/ `1500~`
（およそ1500年）/ `1884?`（不確か）/ `..`（開いた端）/ `null`（不明）。
年の符号は天文学的年番号で統一する。`0000` は紀元前1年、`-0001` は紀元前2年、
紀元前900年は `-0899` になる。表示用ラベルは `astronomical_year_to_label` で `1BCE` のように作り、
被覆マップの世紀列では紀元前を `10BCE` のように表示する。

**Wikidata の日付は `precision` を見てから写す。** 値が `+1500-00-00` でも precision 7 なら
「15. century」（1401–1500）の主張なので `14XX`。値だけ読むと1世紀ずれる（実際にずらした・
`docs/investigation-task.md` に確認手順あり）。

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

### `evidence` — movementと詳細の接続

movementの俯瞰を、根拠として読んだperson/workへ構造化して接続する。targetへの既存relationが必要で、
supportsは次の閉じた語彙だけを使う。

```yaml
evidence:
  - target: work/a-sunday-on-la-grande-jatte
    supports: [kind, time, visual-character]
```

`target` は存在するpersonまたはwork。`visual-character` を含むworkは本文に
`## どう成立しているか`を置き、素材・工程、構図または形態、鑑賞時の作用、実物未見の有無を記述する。
evidence自体は新しいrelationを作らず、既存relationと本文の根拠を明示するだけである。
13文化圏の代表選定は [config/detail-baseline-v1.yaml](../config/detail-baseline-v1.yaml) に固定し、
`tools/audit.py` が未接続のbaseline movementをIDで報告する。

## person / work / event をいつ作るか

**網羅しない。証拠として入れる。** 狩野派だけで絵師は数百人いる。全員を入れれば体系ではなく名簿になり、
名簿は既に美術館と Wikidata が持っている。ここが作るべきなのは「この主張はこの人・この作品で裏が取れる」
という接続の方。

`person` / `work` は、次のどれかに当たるときだけファイルを作る。

1. その movement の `kind` / `time` / `originated_in` の**根拠になる**（`claims` の source として使う）
2. **2つ以上の movement を繋ぐ**（師弟・分派・伝播・後付けの括りの対象）
3. **作品として実際に分解して読んだ**（`## どう成立しているか` を書いた）

どれにも当たらない担い手は、movement の本文に名前を書いて終わりにする。ファイルを作らない
（＝孤児 stub を量産しない）。

`event` は**時間軸の釘**として使う。設立・展覧会・断絶・改革。複数の person / movement を同じ日付に
固定したいときだけ作る。数は person / work より少なくてよい。

**深さは揃えない。** 1つの movement を深く掘り、隣は名前だけ、が正しい状態。被覆マップは movement の面で
測り、person / work は従属指標として数える（全 movement に同じ人数・点数を並べると、浅いものが並ぶだけになる）。

`work` は所蔵館 API から引けるものを優先する（Art Institute of Chicago / Metropolitan / Cleveland は
典拠IDと基本属性が機械で取れ、画像も IIIF で参照できる）。日本側は Japan Search の呼び方が未確認なので、
当面は文字の典拠のみになる。

## 名前の単位と担い手の単位がずれるとき

**名前の単位でエンティティを作る。担い手の系譜は別のエンティティにして、関係で繋ぐ。**

実例（2026-08-09）: カーングラ派の担い手はパンディト・セウの一族だが、この一族はグレール・ジャスロタ・
バソーリ・カーングラ・チャンバという独立した複数の宮廷を渡り歩いており、「カーングラ様式」の名は
一族と無関係な画家も覆っている。真景山水画でも、担い手の一部だけが図画署と重なっていた。

名前と系譜を1つのファイルに押し込むと、どちらかが歪む。**総称に見えるものは、担い手の集合が
特定できる単位まで降りる**（`movement` と `concept` の切り分けと同じ原則）。

## 未解決（構造の穴）

**エッジが期間を持てない。** `belongs_to` は「属している」を1本の線で表すだけで、「いつからいつまで」を
持てない。カミーユ・ピサロのように**一時期だけ運動に属して離れた**人を正しく書けない。
`diffused_to` だけが `{time, via}` の修飾子を持つ設計になっているが、これを他のエッジに広げるか、
所属を `event` として持つかは**未決**。ピサロを入れる時点で決める（2026-08-08 に person の設計を
詰めた際に判明）。

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
- **本文は主題のことだけを書く。** KB の設計・運用・進捗（「最初の1件」「stub として置いた」
  「型を分けない方針だから」）を本文に混ぜない。`status` は frontmatter が持つ。
  判断の根拠は主題の事実として書く

## 道具

```bash
uv run --locked python tools/new_entity.py movement <slug> --ja "<名前>"   # 必須項目が入った雛形
uv run --locked python tools/build_graph.py --check                       # 検証のみ（CI 用）
uv run --locked python tools/build_graph.py                               # 検証 + graph.json + coverage.json + 被覆マップ更新
uv run --locked python tools/bundle.py movement/<slug>                     # 知識のまとまりを1文書で取り出す
uv run --locked python tools/bundle.py --region asia-east-japan            # 文化圏でまとめて取り出す
```

検証が落とすもの: 必須項目の欠落／雛形の TODO 残り／ID・URI とパスの不一致／ID 重複／
存在しない参照／語彙外の型・関係・役割／**関係と空間が指す相手の型違反**（`created_by` が場所を指す等）／
EDTF 違反／解釈系の関係の `certainty`・`source` 欠落／`verified` なのに項目ごとの根拠がない／
`place` の `region` 欠落／**本文の相対リンクの切れ**／**alias と id の衝突**／
俯瞰の依存先が更新されたのに `as_of` が古い（STALE）。

`push` 時は GitHub Actions（`.github/workflows/validate.yml`）が同じ検証と「生成物が最新か」を走らせる。
ローカルのフックは clone ごとの設定に依存するので、そこだけには頼らない。

### 件数の数え方と起源の扱い

- **`stub` は実績に数えない。** 受け入れ条件の件数は `draft` と `verified` だけを数える
  （枠だけのファイルで100件を満たせてしまうと条件が意味を失う）。内訳は被覆マップに出る。
- **起源が複数あるものは、どのバケットにも代表させない。** `originated_in` を複数持つ movement は
  「複数起源」として別に数える（最初の1つで代表させると地域比率が歪む）。

### `aliases`（任意）

slug を変えたときに古い id で参照が切れないように、旧 id を `aliases` に残せる。
`aliases: [movement/old-slug, "旧称"]` のように、型付き旧IDと人間向けの旧名を併記できる。
型付きaliasだけは `<type>/<小文字slug>` の形式にする。検証がid・alias同士の衝突を落とし、`bundle.py` は aliasでも引ける。

外部データとの対応関係は [interop-mapping.md](interop-mapping.md)。
