---
id: movement/tosa-school
uri: urn:ahn:movement/tosa-school
type: movement
kind: lineage-school
label_ja: 土佐派
label_en: Tosa school
authority:
  wikidata: Q2915215
  aat: "300018660"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "14XX"
  end: null
  display: 15世紀（室町期）に成立。Wikidata の inception は +1500-00-00 / precision 7 で、Wikidata 自身は「15. century」と描画する（＝1401–1500）ため EDTF は 14XX
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: 土佐派
  note: 家名（土佐氏）がそのまま呼称になっており、狩野派と同様に命名という行為が存在しない型
claims:
  - {field: time, source: "https://www.fujibi.or.jp/collection/artwork-artist/a130/", certainty: scholarly}
  - {field: originated_in, source: "https://www.fujibi.or.jp/collection/artwork-artist/a130/", certainty: scholarly}
  - {field: kind, source: "https://www.fujibi.or.jp/collection/artwork-artist/a130/", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
relations:
  - {type: derives_from, target: movement/yamato-e, certainty: scholarly, source: "https://www.fujibi.or.jp/collection/artwork-artist/a130/"}
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/45258"}
sources:
  - url: "https://www.wikidata.org/wiki/Q2915215"
    kind: authority
  - url: "https://www.getty.edu/research/tools/vocabularies/aat/"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Tosa_school"
    kind: reference
  - url: "https://www.fujibi.or.jp/collection/artwork-artist/a130/"
    kind: institutional
  - url: "https://www.fujibi.or.jp/collection/artwork-artist/a960/"
    kind: institutional
  - url: "https://www.tobunken.go.jp/materials/ekatudo/808641.html"
    kind: institutional
  - url: "https://www.kyohaku.go.jp/old/eng/theme/floor2_4/past/edo_20160614.html"
    kind: institutional
  - url: "https://www.kyohaku.go.jp/old/jp/theme/floor2_4/f2_4_koremade/kinse_20160614.html"
    kind: institutional
  - url: "https://www.metmuseum.org/art/collection/search/45258"
    kind: institutional
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/DT1607.jpg
    source_page: https://www.metmuseum.org/art/collection/search/45258
    rights_source: https://www.metmuseum.org/art/collection/search/45258
    license: cc0
    note: "土佐光信《四季竹図》（Bamboo in the Four Seasons）、15世紀末〜16世紀初頭。メトロポリタン美術館蔵（isPublicDomain: true）"
status: verified
updated: 2026-08-25
---

# 土佐派 / Tosa school

## 定義と範囲

室町時代前期に成立した日本画の流派。大和絵（中国画の影響を受けた狩野派などに対し、日本古来の
主題・技法に基づく絵画様式）を専門とし、宮廷の絵所預（えどころあずかり）として朝廷に仕えた
絵師の系譜。「輪郭を単純な線で囲んだ平坦な不透明色の領域」を特徴とし、日本の文学・歴史に取材した
物語画を多く手がけたとされる（二次情報: Wikipedia 英語版）。17世紀以降は狩野派との作風の
境界が曖昧になったとも記されている（同）。

典拠: Wikidata [Q2915215](https://www.wikidata.org/wiki/Q2915215)／Getty AAT `300018660`

## 大和絵との系譜

東京富士美術館は、土佐派を「伝統的な大和絵様式を継承した画派」と説明している。京都国立博物館も、
土佐派が大和絵（日本様式の絵画）を専門としたことを確認している。ここで確認できるのは、土佐派が
大和絵を単に同時代に併存した様式として参照したということではなく、伝統的な様式を継承する画派として
位置づけられていることである。したがって、受け取り側である土佐派から大和絵へ `derives_from` を張る。

ただし、この継承は大和絵を固定的に保存したという意味ではない。東京文化財研究所は、土佐光起が
伝統的な大和絵に宋元画の画法と粉本を取り入れて、新しい作品を制作したと説明している
（[東京文化財研究所「Reading Books on the Art of Painting by the Early Modern Tosa School」](https://www.tobunken.go.jp/materials/ekatudo/808641.html)）。
ここで確認できるのは、土佐派内部の近世的な更新であり、宋代の宮廷画院を指す本KBの
`movement/song-academy-painting` 全体から土佐派への直接的な影響を意味しない。そのため、宋元画の導入は
本文の経路として記録するにとどめ、別のmovementエッジは追加しない。

Wikidata は創始者（`founded by`, P112）として土佐行広 [Q3532591](https://www.wikidata.org/wiki/Q3532591)
を挙げているが、その項目説明でも「創始とも伝わる（〜と伝わる）」という伝承のトーンで書かれている。
**未確認**: 創始者を土佐行広と確定してよいかは一次資料に当たっていない（土佐光信を創始者とする説も
一般に流布しており、どちらが通説として優勢かも未整理）。

## kind の判定 — なぜ `lineage-school` か

狩野派と同じ判断軸で見ると、土佐派も家系・工房による継承体であり、`self-declared`（当事者の宣言に
よる運動）でも `retrospective`（後代の外部による括り）でもない。

判定の根拠は、土佐派が朝廷の絵所預という**制度上の地位を伴う世襲の職能集団**だったこと。
なお外部データの分類は一貫していない——狩野派 (Q252801) には `art movement` に加えて `family`
（Q8436）が付くのに、土佐派 (Q2915215) の `P31` は `school of painting`（Q1887220）のみ。
同じ血縁による画派でも付き方が違うので、分類は典拠に従わず実体で判定した。

## 時間

- Wikidata の inception (`P571`) は `+1500-00-00` だが **precision が 7（世紀精度）** であることを
  claims で確認した。年単位の1500年ではない。Wikidata 自身にこの値を描画させると
  **「15. century」**（＝1401–1500）と出る（`action=wbformatvalue` で確認・2026-08-08）。
  したがって EDTF は `14XX`。室町時代前期という記述とも一致する。
- 終期（`P576`=dissolved）は Wikidata に値が無い。**未確認**: 土佐派がいつ途絶えた／解体したと
  見なせるかは一次資料に当たっていない。江戸期に土佐光起が朝廷への出仕を回復したという逸話も
  一般に流布しているが、これも出典を確認できていないため本文には書かない。

## 空間

発生地を京都とした。土佐派は宮廷（朝廷）の絵所預として京都で活動した画派であるという理解に基づくが、
**これは通説であり、一次資料・典拠IDでの座標的な裏（Wikidata に都市レベルの情報は無い）は取れていない**。
Wikidata が持つのは country（日本, `P17`=Q17）までで、狩野派の項目と同じ制約。

桃山期には堺へ拠点を移していたが、江戸時代初期に再び京都へ移り、承応3年（1654）に土佐光起が
宮廷絵所預へ復帰したと東京富士美術館は説明している。京都国立博物館も、光起が17世紀半ばに同職へ
返り咲き、以後江戸時代を通じて土佐派がその職を維持したと説明する。これは「江戸へ活動地が移った」
ことではなく、江戸期に京都の宮廷画壇へ復帰したという再興として記録する。

### ニューヨークでの収蔵

土佐派の国外受容を示す具体例として、メトロポリタン美術館は《四季竹図》を、土佐光信に
「伝」とする作品として収蔵している。記録は作者を「Attributed to Tosa Mitsunobu」、制作地を日本、
年代を15世紀末〜16世紀初頭とする（[メトロポリタン美術館「Bamboo in the Four Seasons」](https://www.metmuseum.org/art/collection/search/45258)）。
ここで確認できるのは、**土佐派に帰属される作例がニューヨークの美術館コレクションに入っていること**
であり、ニューヨークの別の美術運動への影響ではない。そのため `diffused_to place/new-york-city` は
作品の収蔵地点を記録するにとどめる。

## 未着手

- 創始者候補（土佐行広／土佐光信）の person エンティティと、どちらが通説かの一次資料確認
- 土佐光起の person エンティティ化と、江戸期の京都復帰を示す `event` 化
- 作品（証拠）の work エンティティ
- 狩野派との関係（同時代の並行関係は時間×空間から生成されるため、エッジは張らない。ただし
  Wikipedia の記述にある「17世紀以降は狩野派と作風の境界が曖昧になった」という接触については
  `influenced_by` / `reacts_against` のどちらで書けるか、一次資料を見てから判断する）
- 住吉派（土佐派から分派したと一般に言われる）との関係
