---
id: movement/melayu-mauli-buddhist-art
uri: urn:ahn:movement/melayu-mauli-buddhist-art
type: movement
kind: period-style
label_ja: マラユ・マウリ朝仏教美術
label_en: Melayu Mauli Dynasty Buddhist Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Melayu Kingdom』（Q3112053）は王国（政体）そのものを指す項目
    であり、美術・様式単位の項目ではないため採用しなかった。movement単位のWikidata項目は
    検索で特定できなかった"
time:
  start: "1183"
  end: "1347"
  display: "マラユ王国自体は7世紀（Wikidataは671年）に遡るとされるが、マウリ朝の下で
    『黄金期』を迎えたのは1183年のグラヒ碑文以降とされる。1347年（Wikidataの
    dissolved年）を終期とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Melayu Mauli dynasty Buddhist art"
  note: "『マウリ』は王朝名として碑文に現れる当事者由来の語だが、これを美術movementとして
    括る呼称は後代の美術史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Melayu_Kingdom", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Melayu_Kingdom", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Melayu_Kingdom", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/dharmasraya}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q3112053"
    kind: reference
    note: "『Melayu Kingdom』の項。inception年として671年と1183年の両方を記録し、
      dissolved年を1347年とする。movement単位の項目ではない点はauthority.none_reasonに
      記載した"
  - url: "https://en.wikipedia.org/wiki/Melayu_Kingdom"
    kind: reference
    note: "『Melayu Kingdom』の項。1183年のグラヒ碑文（現タイ南部チャイヤーで発見）が、
      マハーラージャ・シュリマット・トライローキヤラージャ・マウリブサナ・ワルマデーワ
      による命令として、グラヒの太守（ブパティ）マハーセーナーパティ・ガラナイに対し、
      重さ1バーラ2トゥラー・価値10金タムリンの仏像を作らせたと記す。この碑文の発見地
      （マレー半島南部タイ領）は、王国の版図が現タイ領にまで及んでいたことを示すと記す。
      1180年代以降、マウリ朝の下で王国が『黄金期』を迎え、13世紀を通じて地域的な影響力を
      維持したと記す"
status: draft
updated: 2026-09-17
---

# マラユ・マウリ朝仏教美術 / Melayu Mauli Dynasty Buddhist Art

## 定義と範囲

英語版Wikipedia「[Melayu Kingdom](https://en.wikipedia.org/wiki/Melayu_Kingdom)」（参考
資料）はこう記す（二次情報）。スマトラ島の[マラユ王国](../places/dharmasraya.md)（マウリ朝）
は1183年、グラヒ碑文（現タイ南部チャイヤーで発見）に記録される仏像鋳造の勅命——マハー
ラージャ・シュリマット・トライローキヤラージャ・マウリブサナ・ワルマデーワが、マレー半島
南部（現タイ領）のグラヒ太守マハーセーナーパティ・ガラナイに対し、重さ1バーラ2トゥラー・
価値10金タムリンの仏像を作らせた——以降、「黄金期」を迎えた。この碑文の発見地は、王国の
版図・宗教的権威が現タイ領マレー半島にまで及んでいたことを示す。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、マウリ朝という政体の存続期間
（1183-1347年）を通じて、複数世代の職人が仏教彫像を発展させ続けた点を、
[ホイサラ美術](hoysala-art.md)・[カーカティーヤ美術](kakatiya-art.md)と同型の構造と見た。

## 空間的接続の判定

グラヒ碑文の発見地（現タイ領マレー半島）はマラユ王国の版図の一部であり、現タイと現
インドネシアはいずれも本KBのregionバケット上asia-southeast内であるため、域内の勅令の
発出先であって域外接続には当たらない。検索した範囲では、この時期のマラユ美術・作品が
asia-southeast外の博物館等へ拡散した文書化された記録は見つからなかった。よって
`relations`に`diffused_to`は張らず、`config/cross-region-reviews.yaml`に「文化圏を
またぐ接続の記録なし」として記録した。

## 未着手

- マハーラージャ・トライローキヤラージャを person エンティティとして立てるかどうか
- グラヒ碑文に記録される仏像そのものを work エンティティとして立てるかどうか
- 後継のアーディティヤワルマン代（14世紀、パガルユン王国への移行期）との連続性の調査
