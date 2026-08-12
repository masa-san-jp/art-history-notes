# 全体設計（ドラフト） — 10年書き足しても崩れない形にするために

作成: 2026-08-08 ／ 対象: このリポジトリの第一版実装（README.md / docs/schema.md / tools/build_graph.py / entities 8件）
性格: 設計文書。実装は後工程。**現行案を追認せず、疑う点は疑って書いた。**

> **重要（同日追記）**: オーナーから最初のミッションが確定した——「芸術史上の『xx主義』『xx派』の
> ような movement を、西洋に限らず世界規模で、時間的・空間的に体系化すること」。
> 論点1〜10 の設計は引き続き有効だが、**主役は movement 型**であり、被覆・成長・完了条件は
> movement を基準に測る。ミッションを受けた中心設計は本文書末尾の
> **「追補: movement の世界規模体系化（論点A〜E）」** にある。矛盾があれば追補側を優先する。

本文中の「確認済」は 2026-08-08 に実際に curl / 取得で確かめたもの。「未確認」は確かめていないもの。
確認の生ログ的な要点は §7 と末尾の未確認リストにまとめた。

---

## 0. 設計の前提と、全体を貫く3つの判断

1. **markdown + git が正本、生成物はすべて再生成可能**という第一版の骨格は正しい。10年スパンで
   最も壊れないのはプレーンテキストであり、この判断は変えない。
2. ただし第一版には**「書き手が一人の AI エージェントである」ことを活かしきれていない箇所**がある。
   人手レビューが無い以上、規律は文章（schema.md の「〜すること」）ではなく**検証器が落とす形**に
   しないと10年で必ず風化する。第一版の validator は形式チェックのみで、規律の大半（出典の質・
   確度の区別・俯瞰の鮮度）が機械化されていない。ここが最大の改修点。
3. **標準（EDTF / Linked Art / Getty / IIIF）には「輸入」でなく「整列」で付き合う。**
   標準のデータモデルを丸ごと採ると markdown で書けなくなり、無視すると10年後に外部データと
   突き合わせられなくなる。採るのは (a) ID（Wikidata/Getty、既に採用済・正しい）、
   (b) 日付表記（EDTF Level 1 のサブセット、§2）、(c) 将来の export 先としての Linked Art への
   対応表（docs に1枚、§1）。それ以上は採らない。

---

## 1. オントロジー — エンティティ型

### 結論

6型 → **8型**にする。`artist` を `person` に広げ、`org`（組織）と `source`（一次資料そのもの）を
新設する。`period`（時代区分）はエンティティにしない（設定ファイルで持つ、§5）。
様式（style）・技法・素材は型を増やさず `concept` の `subtype` で区別する。
CIDOC-CRM の完全なイベント中心モデルは**採らない**。

| 型 | 置き場 | 第一版からの変化 |
|---|---|---|
| `person` | `entities/people/` | `artist` を改名・拡張。批評家・理論家（Chevreul, Blanc, Beaubourg, Roger Fry）・画商・蒐集家も入る |
| `work` | `entities/works/` | 据え置き。連作は work どうしの `part_of` で表す（§1.3） |
| `org` | `entities/orgs/` | **新設**。美術館・アカデミー・団体（Société des Artistes Indépendants）・画商 |
| `place` | `entities/places/` | 純粋に地理的な場所に限定（シカゴ美術館は org へ移す） |
| `movement` | `entities/movements/` | 据え置き。「当人たちの運動／研究上の括り」の別は本文で明示（既にやれている） |
| `concept` | `entities/concepts/` | `subtype: style / technique / material / subject / genre` を任意で付ける |
| `event` | `entities/events/` | 据え置き。展覧会・サロン・設立・断絶 |
| `source` | `entities/sources/` | **新設**。書簡・書籍・カタログ・API レコードなど、一次資料そのものを1ファイルにできる |

### 理由

- **artist は狭すぎる。** 現行 KB は既に Chevreul（化学者）・Blanc（批評家）・Beaubourg（批評家）を
  本文で扱っているのに、彼らを置く型がない。影響関係のグラフは「作家→作家」だけでは張れない。
  型名を `person` にし、役割は本文と関係（`taught_by` 等）で表す。改名コストは今なら2ファイル。
  **ID は変えない原則があるからこそ、8件しかない今日が最後の改名機会。**
- **場所と組織の混同は既に破綻の芽が出ている。** 第一版はシカゴ美術館を `place` に入れたが、
  美術館は「移転しうる・合併しうる・収蔵方針を持つ」組織であり、座標を持つ建物とは寿命が違う。
  Société des Artistes Indépendants を coverage.md は `event` に入れる予定だが、団体は事件ではない
  （設立が event、団体は org）。10年続けるなら組織（アカデミー・画商・美術館）は伝播経路の主要な
  結節点になる（例: 画商 Durand-Ruel なしに印象派の米国流通は語れない）。
- **source を型にする決定打は、既に起きた実害。** スーラの1890年書簡は Rewald 版と Sotheby's 版で
  転記が違う（work/a-sunday… に記録済）。いま転記の異同は work の本文に埋まっており、
  同じ書簡を concept/harmony からも参照していて、異同情報が分散し始めている。
  「一次資料1点＝1ファイル」にすれば、転記の異同・原物の所在（Houghton Library）・アクセス手段が
  1箇所に集まり、他エンティティは `source/...` を参照するだけになる。
  さらに現行の `documented_in` は `concept/harmony → artist/georges-seurat` という**型的に不正な使われ方**
  をしている（対象が資料でなく人）。source 型を作り、validator で `documented_in` の対象を source に
  限定すれば、この種の崩れが機械で止まる。
- **period をエンティティにしない理由**: 時代区分は地域ごとに恣意的で（「江戸時代」と「バロック」は
  同じ種類の区分ではない）、区分自体が研究上の構築物。エンティティにすると「区分の正しさ」を
  維持する責任を負う。俯瞰の行としてしか使わないので、§5 の `config/periodization.yaml`（ビュー設定）
  に置き、恣意性を設定ファイルの diff として可視化する方が誠実で軽い。
  区分について散文を書きたくなったら、それは overview（俯瞰）の仕事。
- **style / technique / material に型を割らない理由**: Getty AAT がこの3つを全部カバーしており
  （点描 pointillism は既に AAT 300021505 系で参照済）、KB 側では「AAT ID を持つ concept」で足りる。
  型を増やすと validator・ディレクトリ・関係語彙の組合せが型数の積で増える。subtype 1フィールドで
  検索上の区別は付く。
- **CIDOC-CRM のイベント中心モデル（制作・取得・移動をすべて独立イベントとして具象化する）を
  採らない理由**: CIDOC-CRM は現在も活発に改版中で（versions ページで確認: 7.3.2 (2026-03) 等は
  draft、公式は 7.1 系）、本家準拠は美術館規模の体制向け。単独の書き手が全作品の来歴をイベント分解
  したら、1作品あたりのファイル数が5〜10倍になり書く速度が死ぬ。**イベントは「それ自体が情報を持つ
  とき」だけ entity にする**（第8回印象派展は event にする価値がある。「1926年にAICへ収蔵」は work の
  frontmatter の1行でよい）。ただし将来の相互運用のため、`docs/linked-art-mapping.md` に
  「この KB の型 → Linked Art のクラス」の対応表を1枚だけ持つ（person→Person, work→HumanMadeObject,
  org→Group, place→Place, concept→Type, event→Activity, source→LinguisticObject 相当、の粒度）。
  Linked Art はモデル 1.0 が公開済みで event 中心の構造を持つことをサイトで確認済（linked.art/model/）。
  対応表は export を実装しない限りただの1ページで、コストはほぼゼロ。

### 具体的な形

```yaml
# entities/sources/seurat-letter-beaubourg-1890.md
---
id: source/seurat-letter-beaubourg-1890
type: source
subtype: letter          # letter | book | article | catalog | api-record | archive | interview
label_ja: スーラのモーリス・ボーブール宛書簡（1890-08-28）
label_en: Seurat, letter to Maurice Beaubourg, 28 Aug 1890
creator: person/georges-seurat
time: {start: "1890-08-28", end: null}
relations:
  - {type: held_by, target: org/houghton-library, certainty: documented,
     source: "https://hollisarchives.lib.harvard.edu/repositories/9/archival_objects/34640"}
sources:
  - https://fr.wikiquote.org/wiki/Georges_Seurat
  - https://www.sothebys.com/en/auctions/ecatalogue/2009/impressionist-modern-art-pf9006/lot.8.html
status: draft
updated: 2026-08-08
---
# 本文には転記の異同（Rewald 版 / Sotheby's 版）を並記し、どちらが手稿に忠実か「未確認」と書く
```

### 現行案からの変更点

1. `artist` → `person`（ディレクトリ `artists/` → `people/`、ID prefix 変更。対象2ファイル＋参照）。
2. `org` 新設。`place/art-institute-of-chicago` → `org/art-institute-of-chicago` に移し、
   `place/chicago` を新規作成して `located_in` で結ぶ。
3. `source` 新設。スーラ書簡・Rewald『Seurat』・Sotheby's カタログを source 化し、
   `documented_in` の対象を source に限定（validator 強制）。
4. `concept` に任意フィールド `subtype` 追加（閉じた語彙、validator 検査）。
5. period 型は作らない（§5 の設定ファイルへ）。

---

## 2. 時間の表現

### 結論

`time.start` / `time.end` の**値を整数からEDTF (Extended Date/Time Format) Level 1 サブセットの
文字列に変える**。validator が EDTF サブセットをパースし、ソート・範囲検索用の数値
（`sort_start` / `sort_end`）を graph.json に導出する。和暦・元号など原表記は `time.display` に残す。
「様式としての継続」は movement の `end: ".."`（継続中・開かれた終端）で表し、制作年（work 側）とは
混ぜない。

### 理由

- 現行の「年の整数 or null」は、美術史で最頻出の年代をすべて表せない:
  c.1500（約）、1620s（年代まで）、「1884?」（不確実）、生年不詳・没年既知。
  第一版はこれらを `note` の自由文に逃がしており、**検索・比較の軸として死んでいる**
  （「1880年代の作品を全部出す」が機械でできない）。
- EDTF は米国議会図書館の仕様（2019-02-04 版、ISO 8601-2 対応）で、まさにこの問題のための標準。
  仕様ページを取得して確認済（loc.gov/standards/datetime/）:
  - Level 0: `1985` / `1985-04` / `1985-04-12`、区間 `1964/2008`
  - Level 1: 不確実 `1984?`、およそ `1984~`、両方 `1984%`、桁未指定 `201X` `20XX`、
    季節 `2001-21`、区間の未知端は null・開いた端は `..`、5桁以上の年 `Y170000002`
  - Level 2 の存在（適合レベルとして定義）は確認したが、詳細機能は今回取得しきれていない → 採らない
- **採るのは Level 1 のうち次だけ**: 年/年月/年月日、`?` `~` `%`、`X`（桁未指定）、null（未知）、
  `..`（開いた端）。季節・5桁年・Level 2（集合表記など）は美術史ノートに不要（YAGNI）。
  サブセットに限定するのはパーサを自前の正規表現30行で書き切るため（Python 標準+PyYAML 制約に収まる）。
- **和暦・イスラム暦などの非西暦**: 正規化した西暦（EDTF）を `start/end` に、原表記を `display` に。
  「天保3年」をそのまま検索軸にすると地域ごとに軸が分裂する。原表記を捨てないのは、
  改元・閏月由来の変換誤りを後から検証できるようにするため。ユリウス暦/グレゴリオ暦の別が
  効く精度（日単位・1582年以前）で書くことはこの KB では稀なので、必要になった項目でだけ
  `calendar: julian` を note でなく display に添える運用とし、フィールド化しない（YAGNI）。
- **「様式としての継続」と「制作年」の違い**: movement の time は「運動として活動した期間」と
  スキーマで定義を固定する。新印象派の「分割主義として20世紀へ続く」は `end: "1900~"` や `end: ".."`
  で表し、続いた実態は後続 movement への `precedes` と、個々の work の制作年が担う。
  「movement の期間」で作品を検索させない（作品は自分の制作年で引く）。

### 具体的な形

```yaml
time:
  start: "1884"        # EDTF L1 サブセット文字列。null = 不明
  end: "1886"
  display: null        # 原表記（"天保3年" 等）。西暦表記なら null のまま
  note: 額縁の彩色は1888–89年に追加

# 例
# 生年不詳・没年1503頃: {start: null, end: "1503~"}
# 1620年代:            {start: "162X", end: "162X"}
# 継続中の運動:         {start: "1884", end: ".."}
```

graph.json への導出（validator が計算）:

```json
"time": {"start": "162X", "end": "162X", "sort_start": 1620, "sort_end": 1629}
```

型ごとの start/end の意味は schema.md に固定する:
person=生没 ／ work=制作期間 ／ movement・org=活動期間 ／ event=開催期間 ／
source=成立日 ／ place・concept=原則 null（歴史を持たせたいときは本文と関係で）。

### 現行案からの変更点

- `time.start/end` の型を int → string（EDTF）に変更。既存8件は `1884` → `"1884"` の機械的変換。
- validator に EDTF サブセットパーサを追加し、不正表記をエラーにする。`sort_start/sort_end` を導出。
- `time.display` を任意フィールドとして追加。

---

## 3. 空間の表現

### 結論

place は「座標＋TGN ID＋歴史的名称のリスト」を持つ地理エンティティに限定する。組織は org へ（§1）。
「地域」（西欧・東アジア等の括り）はエンティティにせず `config/regions.yaml`（ビュー設定）で
place → 地域バケットの対応を持つ。交易路・伝播経路は今は作らない（必要になったら
`place` の `kind: route` として追加する、と決めておくだけ）。政体（国家）の変遷はモデル化しない。

### 理由

- **座標だけでは足りないが、足りない分の大半は TGN が既に持っている。** Getty TGN は歴史的名称を
  含む地名典拠で、第一版が既に ID を採用している。KB 側で世界地名辞典を再発明せず、
  「TGN ID ＋ この KB の記述で実際に使う名前だけ」を持つ。
  東京/江戸のような改名は、**同一の場所エンティティ1つ**に `names`（期間付き名称リスト、期間は EDTF）
  で持つ。場所を分裂させると relations が2重になる。コンスタンティノープル/イスタンブールも同じ。
  「どの時代の文脈でどの名で呼ぶか」は本文の仕事で、frontmatter は同一性の維持だけを担う。
- **「地域」をエンティティにしない理由は period と同じ（§1）**: 括りは恣意的で、coverage の行として
  しか使わない。`regions.yaml` に置けば、括りの変更（例:「南アジア・西アジア」を分割する）が
  設定ファイル1つの diff になり、全エンティティを触らずに済む。**割当のない place は coverage 上
  「未割当」列に出す**ことで、括りの恣意性と漏れを隠さない。
- **政体の変遷（プロイセン→ドイツ等）をモデル化しない理由**: 美術史ノートで政体が効く場面
  （国家発注・検閲・亡命）は event と本文で書ける。政体の時空間モデルは学術プロジェクト
  1個分の重さがあり、単独運用では確実に破綻する。
- **線的な空間（交易路・伝播）**: 伝播は実際には「人が動く・物が動く・版画が動く」であり、
  KB では person/work の移動（relations と event）として自然に記録される。ジャポニスムを書く段に
  なって初めて「経路そのもの」のページが要るか判断すればよい。今決めるのは
  「そのとき type を増やさず place の kind で吸収する」という置き場だけ。

### 具体的な形

```yaml
# entities/places/tokyo.md
---
id: place/tokyo
type: place
label_ja: 東京
label_en: Tokyo
authority: {wikidata: Q1490, tgn: "7011862"}
coordinates: [35.6764, 139.65]
coord_precision: city        # exact | city | region — 曖昧さを座標の顔で隠さない
names:
  - {value: 江戸, from: null, to: "1868"}
  - {value: 東京, from: "1868", to: null}
relations:
  - {type: part_of, target: place/japan}
...
```

空間役割語（space）は現行を概ね維持し、次だけ変える:
`sited_in` を廃止（place の入れ子は relations の `part_of` に一本化）、
`located_in`（org → place）を追加、`held_at` の対象を org に変更（所蔵は組織が持つ。
建物と組織を分けた §1 の帰結）。

### 現行案からの変更点

- place から組織を追い出す（§1 と同じ変更の空間側）。
- `names`（期間付き名称）と `coord_precision` を place に追加。
- `config/regions.yaml` を新設し、coverage 生成（§5）がこれを読む。
- `sited_in` 廃止・`located_in` 追加・`held_at` の対象型を org に。

---

## 4. 関連性 — 関係語彙と確度

### 結論

閉じた関係語彙は**正しい方針であり維持する**。そのうえで、解釈を含む関係
（`influenced_by` / `responds_to` / `belongs_to`）に **`certainty`（確度）と `source`（根拠）を
必須化**する。確度は4値の閉じた語彙: `stated`（本人の言明）／ `documented`（一次資料に記録がある）／
`scholarly`（研究の通説）／ `hypothesis`（自分の仮説）。`hypothesis` の関係は graph.json 上で
フラグされ、俯瞰の生成（§5）から既定で除外される。本文側では仮説は `## 仮説` 見出しの下にだけ書く。

### 理由

- 閉じた語彙を疑ってみたが、開いた語彙（自由記述の関係名）は10年の単独運用で確実に
  `influenced_by` / `influence_from` / `inspired_by` の揺れを生む。語彙追加は「schema.md と validator を
  同じコミットで変更する」という手続きにすれば、閉じたまま成長できる。**語彙の閉性は欠点ではなく、
  この KB の検索可能性の土台。**
- 確度の区別は第一版最大の欠落。schema.md は `influenced_by` に「本人の言明か研究の裏付けがある
  場合のみ」と注記しているが、**注記は機械で検査できない**。スーラ本人が Blanc を反復している
  （stated に近い）ことと、「東アジアの調和は西欧と別概念のはず」（hypothesis）が、いまは同じ強さの
  エッジになりうる。作品制作の判断材料に使う KB では、仮説が通説に化けるのが一番危険な劣化。
- 事実的関係（`created_by` / `taught_by` / `exhibited_at` / `part_of` / `member_of` / `depicts` /
  `precedes` / `held_by`）は certainty 省略可（既定 `documented`）。全関係に必須化すると記述コストが
  跳ねて書かなくなる。**解釈系の3つに限って必須**が、規律と速度の均衡点。

### 具体的な形

```yaml
relations:
  - {type: created_by, target: person/georges-seurat}      # 事実系: 省略時 documented
  - type: influenced_by
    target: person/charles-blanc
    certainty: stated          # 本人が書簡で Blanc の定式を反復している
    source: source/seurat-letter-beaubourg-1890
    note: analogie des contraires の定式
  - type: responds_to
    target: concept/wa-harmony
    certainty: hypothesis      # 自分の仮説。俯瞰生成から除外される
    source: null               # hypothesis のみ source 省略可（検証したら昇格）
```

validator の検査: 解釈系3種は certainty 必須／`certainty != hypothesis` なら source 必須
（URL または `source/...` ID）／未知の certainty 値はエラー。

語彙の追加（最小限）: `held_by`（work → org。所蔵。space の `held_at` から関係へ移す。
所蔵は「空間」ではなく組織との関係なので）／`located_in`（org → place、space 役割）。
`collaborated_with` 等はまだ入れない（必要例が3件出てから）。

### 現行案からの変更点

- relations の各要素に `certainty` / `source` / `note`（いずれも構造化）を追加。解釈系は必須。
- `documented_in` の対象を source 型に限定。
- `held_at`（space）→ `held_by`（relation, work→org）へ移動。
- 本文の規約に「仮説は `## 仮説` 見出しの下にだけ」を追加し、validator が
  frontmatter の hypothesis エッジと本文見出しの存在を突き合わせる（警告レベル）。

---

## 5. 俯瞰と細部の接続

### 結論

俯瞰を「手書きの散文 ＋ 機械生成ブロック ＋ 依存宣言」の3層にする。
(a) coverage の数表は**手で書かない**——`tools/build_views.py` が graph.json と
`config/periodization.yaml` / `config/regions.yaml` から生成し、md 内のマーカー間を書き換える。
(b) 俯瞰ページは frontmatter に `depends_on:`（根拠エンティティの ID リスト）と `as_of:`（執筆時点）を
持ち、依存先の `updated` が `as_of` より新しくなったら validator が **STALE** を報告する。

### 理由

- 第一版の coverage.md は数字を手書きしており、**初日から既に自己矛盾の芽がある**
  （「数字は実ファイル数」と言いながら手動転記。8件目を足した瞬間に古びる）。
  俯瞰が古びる問題は「気をつける」では防げない。数えられるものは全部生成に落とす。
- 手書き散文（「19世紀西欧の1点にしか光が当たっていない」という判断や、埋める順番の意図）は
  生成できないし、生成すべきでない。これが俯瞰の価値そのもの。だから**境界をマーカーで明示**する:
  マーカー内＝機械の領分・手で触らない、マーカー外＝人（エージェント）の領分・機械は触らない。
- `depends_on` / `as_of` は「俯瞰は個別の集約として検証可能に保つ」の機械化。README の規律
  「俯瞰を書いたら根拠になる個別エンティティを1つ以上張る」は、いまリンクの有無すら検査されていない。
  依存宣言があれば (1) 根拠ゼロの俯瞰はエラー、(2) 細部の更新が俯瞰の再読を自動でトリガー、の両方が
  機械で回る。STALE は「即修正せよ」ではなく「再読して as_of を進めるか、書き直すか判断せよ」の合図。

### 具体的な形

```markdown
---
id: overview/coverage
depends_on: [person/georges-seurat, work/a-sunday-on-la-grande-jatte, ...]
as_of: 2026-08-08
---
（手書き: このKBの現在地についての判断）

<!-- BEGIN GENERATED: coverage-matrix -->
| 期 \ 地域 | 西欧 | 東アジア | … | 未割当 |
…（build_views.py が書き換える）
<!-- END GENERATED -->

（手書き: 埋める順番と、その理由）
```

```yaml
# config/periodization.yaml — 恣意性をここに閉じ込め、diff で追えるようにする
periods:
  - {id: c19, label: 19世紀, start: "1800", end: "1899"}
  - {id: c20a, label: 20世紀前半, start: "1900", end: "1949"}
# config/regions.yaml
regions:
  west-europe: {label: 西欧, places: [place/paris, place/london, ...]}
```

### 現行案からの変更点

- coverage.md をマーカー方式に変換、数表を生成に移管（`tools/build_views.py` 新設）。
- 俯瞰ページに frontmatter（`depends_on` / `as_of`）を必須化、validator に STALE 検査を追加。
- overview の ID 空間（`overview/<slug>`）を導入（entities とは別扱い。関係の対象にはしない）。

---

## 6. スケール — 100 / 1,000 / 10,000 件で何が壊れるか

### 結論

いま入れる備えは3つだけ: **(a) 参照はすべて ID 経由**（本文の相対リンクは validator が ID 解決で
検査し、将来のディレクトリ再編を機械的リライト可能にしておく）、**(b) slug 衝突規則の明文化**、
**(c) 生成 index**。ディレクトリのシャーディング・SQLite・全文検索基盤は入れない（YAGNI）。

### 何がいつ壊れるかの見立てと手当て

| 規模 | 壊れるもの | 手当て（いつ入れるか） |
|---|---|---|
| 〜100 | 何も壊れない | 今: 上記 (a)(b)(c) の規約だけ |
| 〜1,000 | 人間的ブラウジング（ファイル一覧が読めない）／俯瞰の手動把握 | 100件時点: `data/index/`（型別・時代別・地域別の生成 md インデックス）。ビルドは全件走査のままで問題ない（1,000件×frontmatter parse は1秒未満のオーダー） |
| 〜10,000 | (1) 1ディレクトリ数千ファイルで GitHub UI・エディタが鈍る (2) graph.json が10MB級になり「全部読む」使い方が苦しい (3) grep 検索の速度より**結果のノイズ**が問題化 | 1,000件を超えてから: works/ の年代別サブディレクトリ化（ID は不変・パスだけ変える。(a) の備えで機械リライト可能）／graph.json の型別分割出力。**それでも DB サーバは入れない** |

- **slug 衝突規則（今決める）**: person は `<姓>-<名>`、衝突したら生年を後置（`utagawa-toyokuni-1769`）。
  work は題名スラッグ、衝突したら作者姓を後置（`self-portrait-van-gogh-1889` 型）。
  無題作品は `untitled-<作者>-<年>`。validator が ID 重複を既に検査している（維持）。
- **ビルドの計算量**: 現行 build_graph.py は全件走査 O(n) で、10,000件でも数秒。インクリメンタル
  ビルドは複雑さに見合わない（YAGNI）。graph.json の git 差分が肥大する問題は、1,000件時点で
  「graph.json を gitignore し CI 生成物にする」判断に切り替える（今は少数なのでコミットして良い。
  切替は1コミット）。
- **レビュー（品質面のスケール）**: 件数が増えるほど「どこが腐っているか」が見えなくなる。
  §8 の health レポート（status 分布・STALE 一覧・リンク切れ・孤児 stub）を生成し、
  これを見る習慣だけが1万件でのレビュー可能性を保つ。

### 現行案からの変更点

- schema.md に slug 衝突規則を追記。
- validator に「本文内の相対リンクが実在エンティティに解決できるか」の検査を追加
  （現在は frontmatter の relations だけ検査していて、本文リンクは野放し）。
- `data/index/` 生成を 100件時点のタスクとして予約（今は作らない）。

---

## 7. 投入経路（ingestion） — 使える一次データ源

### 結論

「fetch は補助・記述は手」を原則にする。API から候補 frontmatter を**印字する**薄いツール
（`tools/fetch/`）は作ってよいが、エンティティの自動生成・自動コミットはしない（§9 の孤児 stub
問題と、規律「手元の知識だけで書いた行は書かない」の裏返し——**読んでいないデータを書かない**）。
取得した生 JSON は `data/cache/<source>/` に保存し、出典 URL とともに再現可能にする。

### 確認結果（2026-08-08、すべて実際に叩いた／取得した）

| ソース | 確認方法と結果 | キー | ライセンス（確認できた範囲） |
|---|---|---|---|
| **Art Institute of Chicago API** (api.artic.edu) | 27992 を取得、応答確認済 | 不要 | 応答内 license_text で確認: データ CC0、`description` フィールドのみ CC-BY。IIIF Image API 2 のURLも応答内に明示 |
| **Met Museum API** (collectionapi.metmuseum.org) | object 436535 取得済。`isPublicDomain` フラグと画像URL直載 | 不要 | metmuseum.github.io に "Creative Commons Zero" の記載を確認。**画像はパブリックドメイン作品のみ**（isPublicDomain で判定） |
| **Cleveland Museum of Art Open Access** (openaccess-api.clevelandart.org) | 検索応答確認済。`share_license_status: "CC0"` がレコード単位で付く | 不要 | レコード単位で CC0 判定可能 |
| **Wikidata** (Special:EntityData / SPARQL) | Q34013 の JSON 取得済 | 不要 | データは CC0（プロジェクト方針として周知。本日ライセンスページ自体は未再取得→取込時に1回確認して記録する） |
| **Getty Vocabularies** (vocab.getty.edu — AAT/ULAN/TGN, SPARQL/LOD) | **本日2回とも "Service temporarily degraded"**。エンドポイントは応答するが実データ未取得 | 不要 | getty.edu の vocabularies ページで **ODC-By 1.0** を確認済（帰属表示が必要） |
| **国立国会図書館 NDL サーチ SRU** (ndlsearch.ndl.go.jp/api/sru) | 検索応答（XML, numberOfRecords）確認済 | 不要 | メタデータ利用条件は未確認（取込前に規約を読む） |
| **Gallica / BnF SRU** (gallica.bnf.fr/SRU) | 検索応答確認済（Chevreul で 7,796 件） | 不要 | Gallica の IIIF は**今回試した ark で 403/500**（ark 不正の可能性）。再配布条件・IIIF の正しい叩き方は未確認 |
| **Smithsonian Open Access** (api.si.edu) | API 実在をエラー応答で確認（`API_KEY_MISSING`, api.data.gov キー要） | 要（無料） | 未確認（キー取得後に確認） |
| **Europeana** (api.europeana.eu) | API 実在をエラー応答で確認（`invalid_apikey`） | 要（無料） | 未確認。メタデータは CC0 とされるが本日原典未確認 |
| **Rijksmuseum** | data.rijksmuseum.nl はHTTP 200（ポータル実在）。旧 API はキー無しで空応答 | 要 | 未確認 |
| **ColBase**（国立文化財機構） (colbase.nich.go.jp) | サイト HTTP 200。JS アプリで、機械可読 API の有無は**未確認** | — | 未確認 |
| **e国宝** (emuseum.nich.go.jp) | サイト HTTP 200 のみ | — | 未確認（API の有無も未確認） |
| **IIIF** | Presentation API 3.0 仕様ページ取得済。AIC が Image API 2 を提供していることは AIC の API 応答内で確認済 | — | IIIF は配信規格でありライセンスは提供館ごと |

### 運用の形

- **優先順**: (1) AIC / Met / Cleveland（キー不要・CC0・レコード単位で来歴と画像まで引ける）、
  (2) Wikidata（同一性のハブ）、(3) Getty（典拠。復旧確認後）、(4) NDL・Gallica（一次文献の書誌）、
  (5) キー要のもの（Europeana / Smithsonian / Rijksmuseum）は必要になった時点でキー取得。
- **画像は repo にコミットしない**（§10）。IIIF / 画像 URL とライセンス表記を frontmatter に持つ。
  ローカル作業用のダウンロードは `data/cache/`（gitignore）へ。
- `tools/fetch/aic.py <artwork_id>` → 生 JSON をキャッシュ保存し、frontmatter 候補と出典行を
  標準出力に印字。書くかどうか・何を書くかはエージェントが本文を読んで決める。

### 現行案からの変更点

- `tools/fetch/`・`data/cache/`（gitignore）の新設。
- schema.md に「API 由来の値には API URL を、目視転記には accessed 日付を」の出典規約を追記。

---

## 8. 品質と鮮度

### 結論

status 3値（stub/draft/verified）は妥当、維持する。足すのは (a) `verified` 遷移時の
`verified_date` 記録、(b) **リンク切れ検査**（`tools/linkcheck.py`、HTTP HEAD で sources を舐めて
`data/health.md` に報告。手動 or 月1）、(c) 転記異同の置き場としての source 型（§1 で解決済）、
(d) 引用の**アクセス日**（`accessed`）。再検証は「期限で腐る」方式にしない——verified は失効しないが、
リンク切れ・依存先変更（§5 STALE）・異説の追加が再検証のトリガーとして health レポートに並ぶ。

### 理由

- status を5値等に増やす案も考えたが、単独運用では状態遷移の運用コストが増えるだけ。3値は正しい。
  ただし現行は「いつ verified にしたか」が `updated`（最終編集日）と区別できず、
  「verified のまま2年触っていない」が検出できない。`verified_date` 1フィールドで足りる。
- リンク切れは10年で**必ず**起きる（出典URLを本文に置く規律の裏面のリスク）。対策の本命は
  「URL だけに依存しない」こと: 使った一節は**引用として本文に転記**し（既にやれている——
  スーラ書簡の全文転記はまさに正しい形）、URL は検証経路として持つ。linkcheck は
  「切れたら直ちに直す」ためでなく「どの根拠が検証不能になったかを知っている」ために回す。
  Wayback Machine への保存自動化は外部サービス依存が増えるので**やらない**（切れた時に手で探す）。
- 転記揺れ（Rewald 版 vs Sotheby's 版）は第一版が正しく「両方の存在を示す」で扱っている。
  source 型はこの扱いを構造にする: 異本・異転記は source のファイル内に並記し、
  引用する側は source ID を指す。**どの転記を引いたか**が曖昧にならない。

### 具体的な形

```yaml
sources:
  - url: https://api.artic.edu/api/v1/artworks/27992
    accessed: 2026-08-08
  - id: source/seurat-letter-beaubourg-1890     # URL でなく source エンティティ参照も可
status: verified
verified_date: 2026-08-08
updated: 2026-08-08
```

（互換: 素の URL 文字列も引き続き受け付ける。validator は dict 形式を推奨警告に留め、
既存を壊さない。）

health レポート（`data/health.md`、生成）に載るもの:
リンク切れ／STALE な俯瞰／孤児 stub（§9）／`verified` かつ sources に切れを含むもの／
status 分布の推移。

### 現行案からの変更点

- `verified_date`・`sources[].accessed` の追加（後方互換）。
- `tools/linkcheck.py` と `data/health.md` の新設。
- 再検証トリガーの定義を schema.md に明文化（期限失効ではなくイベント駆動）。

---

## 9. 成長の駆動 — 単独の書き手が10年続けるために

### 結論

3つの仕組みで駆動する。**(1) 深さ優先・近傍展開**: 1本の「深掘り」（work 1点の完全分解）を単位とし、
その深掘りが参照した相手だけを stub に起こす（**孤児 stub の禁止**——どの relations からも指されない
stub を validator が警告する。API 大量流し込みで庭を荒らさないための構造的な歯止め）。
**(2) 制作との往復記録**: work の「自分の作品にどう使うか」（既にある・良い）に加え、
自作を作った**後**に「何を使い、何が効いたか」を `practice/` に1枚書き、使った concept/work へ
逆リンクする。KB→制作の一方通行を双方向にする。
**(3) 生成される「次の一手」リスト**: `data/next.md`（生成）に、(a) 参照されている未作成 ID、
(b) 深掘り済みエンティティの未展開の近傍、(c) coverage の空白のうち締切テーマに効く行、を並べる。

### 理由

- 被覆マップは有効だが**それだけだと「面を埋める作業」に堕ちる**。第一版自身が正しく書いている
  （「埋めた数を成果にしない」）。埋める動機は常に制作か深掘りから来るべきで、coverage は
  「偏りを自覚する鏡」に限定する。次に書くものの第一候補は常に「いま深掘りしているものが
  参照した相手」——これが近傍展開で、10年後にグラフが**実際に歩いた道の形**になる。
  一様に薄い1万件より、濃い経路の絡んだ3千件の方が制作の栄養として強い。
- 「1点を深く」と「面を広げる」の均衡は、比率で決めない（守れない）。**深掘り1本につき、
  それが生んだ stub を近傍に置く**という単位で自然に面が広がる。今回のスーラ1点が
  8エンティティを生んだのが実例で、この比（深掘り1 : 周辺7）は健全。
- 制作へのフィードバック経路は現在、work 側の「使える手」で終わっている。実際に作った後の
  検証（dominante を先に決めたら本当に画面がばらけなかったか？）が KB に還流しないと、
  KB は「読んだことの倉庫」で止まり「作るための道具」にならない。practice ノートは
  グランプリ5点（2026-09-15）でそのまま5枚書ける。

### 具体的な形

```
practice/2026-09-grand-prix-5/piece-01.md
---
id: practice/2026-09-piece-01
used: [concept/harmony, work/a-sunday-on-la-grande-jatte]
---
（何を援用し、何が効き、何が嘘だったか。KB 側の記述を直すべき発見があれば直してから書き終える）
```

practice は entities の外（グラフの検証対象外・`used` の解決だけ検査）。作品そのものの管理は
このリポジトリの仕事にしない（§10）。

### 現行案からの変更点

- 孤児 stub 警告を validator に追加。
- `practice/` の新設と `used` フィールドの規約。
- `data/next.md` 生成を build_views.py に追加（100件時点でよい。当面は coverage の「埋める順番」手書きで足りる）。

---

## 10. やらないこと（作り込むと確実に破綻するもの）

1. **CIDOC-CRM 完全準拠のイベント具象化**（§1）。来歴・制作・移動の全イベント化は美術館の体制向け。
2. **RDF / JSON-LD の export 実装**。消費者が現れるまで作らない。対応表（1ページ）だけ持つ。
3. **画像の repo コミット**。容量・権利・再配布の三重リスク。URL・IIIF 参照と、gitignore された
   ローカルキャッシュまで。
4. **DB サーバ・ウェブ UI・全文検索基盤**。markdown+git+生成 index で 10,000 件まで持つ設計にした。
5. **時代区分・地域区分の「正しい」体系の追求**。区分は config のビュー設定であり、研究対象ではない。
6. **政体・国境変遷の時空間モデル**（§3）。
7. **API からの一括自動投入**（読んでいないデータを書かない。孤児 stub 禁止が構造的な歯止め）。
8. **多言語ラベルの網羅**（ja/en の2つで固定。他言語は authority ID の向こう側にある）。
9. **Wayback 保存の自動化などの外部サービス連携の常時稼働**（§8）。
10. **作品制作物そのものの管理**（practice はメモまで。制作物は既存の制作フローの側）。
11. **status の細分化・ワークフロー化**（3値で足りる。増やすと遷移の管理が仕事になる）。

---

## 移行手順（現行8エンティティを壊さない順序）

各ステップは「validator が green のまま」進められる順に並べた。1ステップ＝1コミット。

1. **schema v2 の文書化**: docs/schema.md を本設計に沿って改訂（型・EDTF・certainty・slug 規則・
   出典規約）。コードより先に正本を直す。
2. **validator 改修（受け入れ拡張）**: EDTF パーサ・certainty 検査・source 型・org 型・person 型を
   「新旧両方受け付ける」形で追加（int 年も EDTF 文字列も通る等）。既存8件は無修正で green。
3. **リネーム**: `artists/` → `people/`（ID `artist/*` → `person/*`）、
   `place/art-institute-of-chicago` → `org/art-institute-of-chicago` ＋ `place/chicago` 新設。
   relations・本文リンクを同コミットで一括置換し、`--check` で dangling ゼロを確認。
4. **source 化**: `source/seurat-letter-beaubourg-1890`（転記異同2系統を集約）、
   `source/rewald-seurat-1990`、`source/sothebys-2009-lot8` を作成。concept/harmony の不正な
   `documented_in`（→artist）を source 参照に修正。
5. **時間の EDTF 化**: 8件の time を文字列化（機械的）。validator の旧 int 受け入れを削除して締める。
6. **俯瞰の生成化**: `config/periodization.yaml` / `config/regions.yaml` 新設、
   `tools/build_views.py` 新設、coverage.md をマーカー方式へ変換、`depends_on`/`as_of` 付与。
7. **締め**: validator の後方互換モードを全部外し、schema v2 のみ受け付ける状態にして
   README を改訂。ここまでで9件目以降は v2 で書ける。

## 実装の段階

| 時期 | 入れるもの |
|---|---|
| **今（〜エンティティ9件目を書く前）** | 移行手順1〜7の全部。＋pre-commit / GitHub Actions で `build_graph.py --check`（既に CI 可能な形になっているので YAML 1枚） |
| **100件時点** | `data/index/`（型別・時代別の生成インデックス）／`tools/linkcheck.py` と `data/health.md` の定期実行化／`data/next.md` 生成／`tools/fetch/` を実際に使う源（AIC/Met/Cleveland/Wikidata）分だけ整備 |
| **1,000件時点** | graph.json を gitignore して CI 生成物へ切替／works/ の年代別サブディレクトリ化の要否判断（ID 不変・§6 の備えで機械リライト）／graph.json の型別分割 |
| **入れない（無期限）** | §10 の全項目 |

---

---

# 追補: movement の世界規模体系化（論点A〜E）

要件の正本は [issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1)。ここでは要件を再掲せず、
issue の「開いている論点」1〜5 に設計としての答えを出す。論点1〜10（前半）の設計は movement を主役に
読み替えて引き続き有効。読み替えの波及は E の後にまとめた。

## A. movement を主役にしたスキーマ（issue 論点1・4への回答）

### 結論

**エンティティ型は `movement` の1つに保ち、必須フィールド `kind`（閉じた語彙・validator 強制）で
性質を型区別する。** kind は4値:

| kind | 何であるか | 例 |
|---|---|---|
| `self-declared` | 当事者が名乗った運動。宣言文・機関誌・自称の証拠がある | 未来派、シュルレアリスム、白樺派 |
| `retrospective` | 後代に外部（批評家・史家・市場）が付けた括り | 印象派、ポスト印象派、マニエリスム、プリミティヴィスム |
| `lineage-school` | 血縁・工房・師弟の継承体。制度としての実体を持つ | 狩野派、土佐派、歌川派、琳派（※）、シエナ派 |
| `period-style` | 宮廷・王朝・時代に紐づく様式の括り。担い手は交代する | ムガル絵画、白鳳様式、インターナショナル・ゴシック |

「時代区分」（江戸時代・ルネサンスの「時代」側の顔）は movement にしない——§1 の判断どおり
`config/periodization.yaml`（ビュー設定）で持つ。技法・様式のうち**担い手の集合を特定できないもの**
（点描・明暗法）は `concept`（subtype: style/technique）のまま。境界規則は1行で決める:
**「担い手の集合が歴史的に特定できるなら movement、手の形の記述なら concept」**。

そのうえで、後付け命名と自己認識の区別（issue の機能要件）は kind だけに背負わせず、
**`naming` ブロックを movement の必須フィールド**にする:

```yaml
# entities/movements/post-impressionism.md（改訂形）
kind: retrospective
naming:
  self_identified: false          # 当事者がこの名で名乗ったか
  named_by: person/roger-fry      # 命名者（不明なら null + note）
  named_when: "1910"              # EDTF
  original_label: Post-Impressionism
  note: 1910年グラフトン・ギャラリーズ展の展覧会名に由来（一次資料は未確認）

# entities/movements/kano-school.md（新規の形）
kind: lineage-school
naming: {self_identified: true, named_by: null, named_when: null,
         original_label: 狩野派, note: 家名がそのまま呼称。命名行為が存在しない型}
time: {start: "146X", end: "18XX", note: 正信の活動開始から明治の解体まで。要典拠}
space:
  - {role: originated_in, target: place/kyoto}
  - {role: active_in, target: place/edo}
relations:
  - {type: patronized_by, target: org/tokugawa-shogunate, certainty: scholarly, source: ...}
```

### 理由 — なぜ型を分けず、なぜ kind を必須にするか

1. **外部データが「型を分ける」戦略の失敗例になっている（実測）。** Wikidata は狩野派に
   `family`＋`art movement`＋`school of painting` の3クラスを重ね、琳派は `school of painting` だけ、
   歌川派は `artistic school` だけ、呉派は `art movement`＋`artistic school`＋`style of painting`、
   ムガル絵画は `art style`＋`painting of an area`（2026-08-08 WDQS 実測）。同種のものがクラス間に
   散らばり、**「movement の全集合」をクラスで取ることがもはや不可能**になっている。
   型を分けるとこの分類難problemを自分が引き受けることになり、境界事例（琳派は私淑の系譜であり
   工房組織ではない——lineage-school と retrospective の中間）のたびにディレクトリ移動＝ID変更の
   圧力が生まれる。単一型＋kind なら、分類の訂正は frontmatter 1行の diff で済む。
2. **issue の要件「同一視して1つの型に潰さない」は、kind を必須＋閉語彙にすることで満たす。**
   区別が任意フィールドなら潰れるが、validator が kind 欠落を落とすなら、これは実質的な型区別で
   あり、かつ「全 movement を横断して時間×空間で引く」というミッションの主クエリを分断しない。
   ※もしマサさんが「型＝エンティティ型（ディレクトリ）の分離」を意図しているなら、ここが
   issue 編集の判断点（推奨は本案。理由は上記1）。
3. **「movement」概念の非西欧への当てはめの歪み**は、(a) 型の意味を schema.md で「集合的な芸術実践の
   括り（grouping）」と再定義し西洋近代の「運動」を規範にしないこと、(b) kind が emic/etic の違いを
   明示すること、(c) `naming.original_label` が原語・原表記を保存すること、の3点で吸収する。
   狩野派を「movement（運動）」と呼ぶ違和感は残るが、型名は ID 安定性のため変えない
   （表示名の問題は README と schema.md の定義で解く）。
4. **琳派の実例が方針の試金石**: AAT の見出し語は「Rinpa」ではなく「Sōtatsu-Kōrin School」
   （AAT 300106734、2026-08-08 VOW で確認）——**典拠側にも命名の歴史的バイアスが焼き付いている**。
   kind と naming を KB 側で持つ設計は、典拠を信頼の基盤にしつつ、典拠の分類・命名には従属しない
   ための構え。

### 時間表現（issue 論点4への回答）

**EDTF（ISO 8601-2）Level 1 サブセットを採用する**。§2 のとおり（仕様は LOC で本日確認済）。
movement はまさに不確実年代の塊（「146X」「18XX」「1884/..」）であり、整数年では最初の10件で破綻する。
kind=lineage-school の time は「系譜の活動期間」、self-declared は「宣言〜解散/消滅」、
retrospective は「括られた対象の活動期間（命名時期は naming.named_when に分離）」と、
kind ごとに start/end の意味を schema.md で固定する。**この分離が「様式としての継続」と
「命名の瞬間」の混同を構造的に防ぐ。**

## B. 世界規模の被覆の定義と測り方（issue 論点2・3への回答）

### 地域区分（論点2）: 13バケット・2層構造

大陸括り（西欧・東アジア）を廃し、**「その内部差がミッションの主題になる粒度」**で切る。
文化圏バケット13個を `config/regions.yaml` に定義（エンティティにしない。§3 の判断を維持）:

```
europe-west（西欧・南欧・北欧） / europe-east（中東欧・ロシア・ビザンツ圏） /
mena（中東・北アフリカ） / africa-sub（サブサハラ） / asia-central（中央アジア・チベット・モンゴル） /
asia-south（南アジア） / asia-southeast（東南アジア） /
asia-east-china（中国圏） / asia-east-korea（朝鮮半島） / asia-east-japan（日本） /
americas-north（北米） / americas-latin（中南米・カリブ） / oceania（オセアニア・太平洋）
```

- 東アジアを3分割するのは、まさに「派」の性質差（狩野派／浙派・呉派／朝鮮画院)がこのKBの主題だから。
  逆に西欧は仏・英・独に割らない——そこを割り始めると近代美術史の慣行（パリ中心）に引きずられ、
  バケット数が主題でなく資料量で決まる。**粒度の原則: 内部差が主題になったら割る、それまで割らない。**
  割るときは config の diff 1つ（エンティティ無傷）。
- movement→バケットの割当は `originated_in`（発生地、space 役割語に追加）の place から機械導出。
  発生地が特定できない movement は「発生地未確認」として被覆表に**別行で見える化**する。

### 受け入れ条件の推奨閾値（論点3、マサさん承認待ちとして提示）

| 項目 | 推奨値 | 根拠 |
|---|---|---|
| movement 件数 N | **100**（第1マイルストーン） | E の候補リストが典拠2系統つきで現実に組める規模。1件/日ペースで約4ヶ月。1000件を先に掲げると件数稼ぎ（issue のスコープ外）に堕ちる |
| 非西洋比率 | **50%以上**（西洋= europe-west, europe-east, americas-north の3バケット起源。それ以外＝非西洋） | 「同格に扱う」の機械化。E の配分案では非西洋57%になり、達成可能かつ緩すぎない。中南米を非西洋に数える定義も含めて承認事項 |
| 地域最低件数 | **全13バケットで3件以上** | 「載っているが1件だけ」は体系ではない。3件あれば地域内の関係エッジが張れる |
| 時代の偏り防止 | **1800年以前起点の movement が30%以上** | 「世界規模」が「近代のグローバル化以後」に縮退するのを防ぐ |
| 関係の連結 | **関係エッジ0の movement が10%未満** | 孤立ノードの羅列は「体系化」ではない（issue 目的の「渡った先が見える」の機械化） |

**測り方について issue 側の修正を1点提案する**: 受け入れ条件「全 movement が空間（発生地・伝播先）を
持つ」のうち**伝播先は必須にできない**（伝播しなかった／伝播が未研究の movement は正当に存在する）。
「発生地（または発生地未確認の明示）は必須、伝播先は該当する場合に記録」への修正を推奨。
また被覆マップには「調査したがこのセルに該当なし」を `config/coverage-reviews.yaml` の
`no-known-grouping` として空欄と区別して記録する（空欄＝未着手、no-known-grouping＝調査済み）。
`tools/build_graph.py` はこれを `∅` として生成表に表示し、既に movement があるセルへの記録を拒否する。

時間軸の行は**世紀（必要なら半世紀）で機械的に切る**。文化圏固有の時代区分（江戸・オスマン朝など）は
region-local な periodization としてビュー切替で見られるようにする（グローバル行に恣意的な「中世」を
置かない。「中世」は欧州ローカルの区分）。

## C. 典拠の非西欧バイアス — 実測結果と代替典拠（issue 論点5への回答）

### 実測（2026-08-08）

**Wikidata**（WDQS で実測）:
- `P31 = art movement (Q968159)`: **988件**。下位クラス込み（P31/P279*）: **1,957件**
- 隣接クラスに分散: artistic school 123件・style of painting 70件・school of painting 47件・
  art style 463件 → movement 相当の総体はクラス横断でしか取れない
- **地域分布はプロパティ欠落で測定不能に近い**: Q968159 のうち country of origin (P495) を持つのは
  **55件（5.6%）**、P17 でも 328件（33%）、開始時点（P571/P580）を持つのは 325件（33%）。
  P495 上位は日本10・米国6・仏3（n=55 なので分布として無意味）
- 結論: Wikidata は**同一性のハブ（QID）としては使えるが、movement の時間・空間・分類の典拠としては
  使えない**。この KB が自前で time/space/kind を持つ設計は実測で裏付けられた

**Getty AAT**（vocab.getty.edu の SPARQL/LOD は本日終日 "Service temporarily degraded"。
旧 VOW HTML 検索で個別確認）:
- 予想（「非西欧が薄い」）に反し、**主要な東アジア・南アジアの流派・様式は存在する**:
  Kano School **300018653**／Sōtatsu-Kōrin School（琳派）**300106734**／Tosa School **300018660**／
  Ukiyo-e **300106769**／Yamato-e **300018589**／Nihonga **300114441**／Nanga **300018580**／
  Wen ren（文人画）**300106509**／New Literati Painting **300417409**／Mughal **300018939**（+ periods/styles 下位）。
  アフリカも Styles and Periods ファセットに Nkanu（コンゴ様式）300262946 等が存在
- ただし件数の網羅測定は SPARQL 復旧待ち（**未確認**）。また見出し語に歴史的バイアスあり
  （琳派→ Sōtatsu-Kōrin School）。西アジア絵画（サファヴィー朝絵画等）は検索1ページ目に
  絨毯しか出ず**要深掘り（未確認）**
- 運用: AAT ID は付けられるなら付ける。無ければ「典拠なし」＋代替典拠、の優先順で

**代替典拠（本日実際に応答を確認できたもの）**:
- **Japan Search (jpsearch.go.jp) SPARQL エンドポイント**: 動作確認済（クエリに応答）。
  日本の文化財・作家の統合LOD。日本の流派の典拠・作品裏付けの第一候補
- **Web NDL Authorities (id.ndl.go.jp)**: 個別レコードページの取得可（HTTP 200）。国立国会図書館の
  件名典拠で「狩野派」等が件名として存在するはず——**検索APIの正しい呼び方は未確認**（今回の
  プローブはパーサエラー応答）。NDL サーチ SRU（確認済・§7）から書誌の裏取りは今日から可能
- **ColBase / e国宝**: サイト実在は確認、機械可読 API の有無は**未確認**（§7）
- 中国（故宮博物院 北京/台北）・韓国（国立中央博物館）・中東・アフリカ・中南米の機関データは
  **すべて未確認**。E の第2四半期（当該地域に着手する時点）までに各1つ確認するタスクとして積む

### 設計への反映

`authority` ブロックを「Wikidata/Getty 前提」から**多元典拠**に広げる:

```yaml
authority:
  wikidata: Q252801
  aat: "300018653"
  ndl: null            # Web NDL Authorities ID
  jpsearch: null       # Japan Search entity URI
  none_reason: null    # 典拠ゼロのときは理由を必須で書く（validator 強制）
```

## D. movement 間の関係語彙（issue 機能要件「継承・反発・並行・伝播・再分類」への回答)

### 結論

既存語彙では足りない。**4語を追加し、「同時代の並行」はエッジにしない**（時間×空間から生成する）。

| type | 意味 | 例 |
|---|---|---|
| `derives_from` | 系譜的継承（意識的に受け継いだ。単なる前後 `precedes` と区別） | 分割主義 derives_from 新印象派 |
| `reacts_against` | 反発・対抗として成立 | ダダ reacts_against アカデミスム |
| `diffused_to` | 地理的伝播（movement → place。`{time, via}` 修飾子つき） | 新印象派 diffused_to ブリュッセル {time: "1887", via: org/les-xx} |
| `grouped_as` | 後付けの括りへの再分類（movement/person → kind=retrospective の movement） | 新印象派 grouped_as ポスト印象派 |

- **並行（同時代性）をエッジにしない理由**: 「同じ頃に別の場所で起きていた」は time と space から
  機械導出できる事実であり、手で張ると必ず漏れと恣意（どの並行を「関係」と呼ぶかの選別）が入る。
  `tools/build_views.py` が「同時代マトリクス」（期間の重なる movement の組を地域横断で列挙）を
  生成物として出す。エッジは「影響・反発など**主張**があるもの」に限る。
- `grouped_as` を `part_of` から分離する理由: part_of は当事者的・構造的包含（歌川派 part_of 浮世絵の
  系統、場所の入れ子）に限定し、**外部からの遡及的な括りは grouped_as** に一本化する。現行の
  「新印象派 part_of ポスト印象派」は型的に誤り（ポスト印象派は1910年の後付け括り）で、
  grouped_as に移す。これで「後付けの命名と自己認識の区別」が naming（ノード側）と
  grouped_as（エッジ側）の両面で機械可読になる。
- これらはすべて解釈系なので **§4 の certainty + source が必須**。「誤って一括りにされた」ことの
  記述は、grouped_as エッジ＋本文（括りの妥当性への批判は `## 仮説` または通説なら本文）で持つ。
- 併せて space 役割語に `originated_in`（発生地。B の被覆集計のキー）を追加。

## E. 最初の100件の選び方と候補

### 選定基準（順に適用）

1. **バケット×世紀の空白を埋める順**（B の最低件数3件を先に満たす）
2. **典拠2系統以上**（Wikidata QID + AAT/NDL 等）が確定できるもの優先——同一性が10年壊れない
3. **一次資料への到達可能性**（宣言文・当事者文書・所蔵館 API の作品群）があるもの優先
4. kind の4値が**どの地域にも混ざる**こと（非西洋＝lineage-school だけ、西洋＝self-declared だけ、
   という対応付けに陥ると、kind が地域の言い換えに堕ちる）
5. 制作テーマ（調和）に効くもの（日本の琳派・南画、色面構成系）を深掘り枠に

### 配分と候補（100件 = 西洋43 / 非西洋57）

以下は**候補**であり、各件は起票時に典拠確認を通す（このリスト自体はまだ典拠確認前。確定リストは
起票の PR が正本になる）。件数はバケット配分の設計値。

- **asia-east-japan (12)**: やまと絵・土佐派・狩野派・琳派・浮世絵（＋歌川派）・南画・円山四条派・
  日本画（院展系）・白樺派周辺の洋画・具体・もの派・スーパーフラット
- **asia-east-china (8)**: 浙派・呉派・文人画・海上画派・嶺南画派・木版画運動（1930s）・
  新文人画・政治ポップ
- **asia-east-korea (3)**: 朝鮮画院（図画署）の系統・真景山水・単色画（Dansaekhwa）
- **asia-south (6)**: ムガル絵画・ラージプト（＋パハーリー）絵画・カンパニー派・ベンガル派・
  Progressive Artists' Group・バローダ派
- **asia-southeast (4)**: バリ絵画（＋Pita Maha）・ベトナム漆画（インドシナ美術学校系）・
  フィリピン Thirteen Moderns・タイ近代（Silpa Bhirasri 系）
- **asia-central (3)**: チベット仏画の流派（メンリ派等）・ティムール朝細密画・モンゴル・ザナバザル系統
- **mena (8)**: サファヴィー朝細密画（タブリーズ／イスファハーン派）・オスマン細密画・
  マムルーク工芸様式・コプト美術・Hurufiyya 運動・エジプト近代（Cairo modernists）・
  バグダード近代美術グループ・イラン Saqqakhaneh
- **africa-sub (6)**: ベニン王国美術・ヨルバ様式圏・エチオピア教会絵画・Négritude 系近代・
  ナイジェリア Zaria Art Society（Natural Synthesis）・南ア Polly Street / Rorke's Drift 系
- **europe-west (25)**: ゴシック（国際ゴシック含む）・シエナ派・フィレンツェ派・ヴェネツィア派・
  北方ルネサンス・マニエリスム・バロック（カラヴァッジェスキ）・ロココ・新古典主義・ロマン主義・
  ラファエル前派・写実主義・バルビゾン派・印象派・新印象派・ポスト印象派・象徴主義・
  アール・ヌーヴォー・フォーヴィスム・キュビスム・未来派・ダダ・シュルレアリスム・
  デ・ステイル・バウハウス
- **europe-east (8)**: ビザンツのイコン様式（＋ノヴゴロド派）・移動派・ロシア・アヴァンギャルド
  （構成主義／シュプレマティスム）・ポーランド形成主義・チェコ・キュビスム・社会主義リアリズム・
  モスクワ・コンセプチュアリズム・ハンガリー activism
- **americas-north (6)**: ハドソン・リバー派・アッシュカン派・ハーレム・ルネサンス・
  抽象表現主義・ポップアート・ミニマリズム
- **americas-latin (6)**: メキシコ壁画運動・ブラジル Antropofagia・マドリ（Madí）・
  ネオコンクレチスモ・キネティック（ベネズエラ）・インディヘニスモ
- **oceania (3)**: パプア（セピック）様式圏・マオリ工芸の流派・Papunya Tula（西部砂漠絵画運動）
- **バッファ (2)**: 深掘り中に必要が判明した近傍に充てる

先住民・古代の「様式圏」（ベニン・セピック等）を kind=period-style で扱うのは近似であり、
起票時に kind の妥当性を本文で明示する（「movement 概念の当てはめの歪み」を各ファイルが自覚を持つ）。

### 既存論点への波及（movement 主役への読み替え）

- **§5 被覆マップ**: 主対象を「エンティティ総数」から **movement×バケット×世紀**に変える。
  work/person の被覆は従属指標
- **§9 成長の駆動**: 深掘りの単位を「movement 1件を verified にする（naming・kind・時間・空間・
  関係・証拠 work ≥1 まで）」に置き、work の完全分解は movement の証拠づくりとして従属させる。
  孤児 stub 禁止・近傍展開・practice 往復はそのまま
- **移行手順への追加**: 手順1（schema v2）に kind・naming・originated_in・grouped_as ほか D の4語と
  authority 多元化を含める。手順4の後に「既存 movement 2件（新印象派・ポスト印象派）の v2 化」を
  挟む（part_of → grouped_as の付け替えを含む）。100件の起票は移行完了後に開始する

---

## 付記: 本日の確認で判明した事実と未確認事項（要約）

**確認済（2026-08-08）**: EDTF 仕様（LOC, 2019-02-04 版）の Level 0/1 の全機能詳細／
Linked Art モデル 1.0 の公開とイベント中心構造／CIDOC-CRM の版状況（7.3.x は draft、公式は 7.1 系）／
AIC・Met・Cleveland・Wikidata・NDL SRU・Gallica SRU の各 API が今日この環境から実際に応答すること
とキー要否／AIC のライセンス内訳（CC0＋description のみ CC-BY）／Met の CC0 表記／
Cleveland のレコード単位 CC0 フラグ／Getty Vocabularies のライセンスが ODC-By 1.0 であること／
Smithsonian・Europeana の API 実在（キー必須のエラー応答）／IIIF Presentation 3.0 仕様の存在。

**確認済（同日・追補分、WDQS/VOW 実測）**: Wikidata の art movement (Q968159) 直接インスタンス 988件・
下位クラス込み 1,957件・P495（起源国）保持は 55件（5.6%）のみ／狩野派等の非西欧流派の Wikidata
クラス付けが不均質（family / art movement / school of painting / artistic school / art style に分散）／
AAT に狩野派 300018653・琳派（見出しは Sōtatsu-Kōrin School）300106734・土佐派 300018660・
浮世絵 300106769・やまと絵 300018589・日本画 300114441・南画 300018580・文人画 300106509・
ムガル 300018939 等が実在（VOW HTML 検索）／Japan Search SPARQL (jpsearch.go.jp) の動作／
Web NDL Authorities (id.ndl.go.jp) の個別レコード取得（HTTP 200）。

**未確認**: Getty vocab.getty.edu の実データ応答（本日終日 "Service temporarily degraded"、
復旧後に AAT の非西欧被覆を SPARQL で件数測定し直す）／AAT の西アジア絵画（サファヴィー朝等）・
アフリカ様式の網羅度／EDTF Level 2 の機能詳細（不採用なので実害なし）／Gallica IIIF の正しい叩き方と
再配布条件／NDL メタデータの利用規約と Web NDL Authorities 検索 API の正しい呼び方（今回のプローブは
パーサエラー応答）／Rijksmuseum・Europeana・Smithsonian のライセンス詳細（キー取得後）／
ColBase・e国宝の機械可読 API の有無／中国（故宮 北京/台北）・韓国（国立中央博物館）・中東・アフリカ・
中南米の機関データすべて／Wikidata の CC0 宣言ページの本日時点の文言／CIDOC-CRM 公式版表記の正確な対応
（versions ページの表の読み取りに曖昧さが残る）／E の候補100件リストの各件の典拠（起票時に個別確認）。
