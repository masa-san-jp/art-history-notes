---
id: movement/santero
uri: urn:ahn:movement/santero
type: movement
kind: period-style
label_ja: サンテロ
label_en: Santero (New Mexican santos tradition)
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "『santero』のWikidata項目（Q35293314）は本文中でメキシコの地名を指すとの
    注記があり、ニューメキシコの聖人像制作の伝統そのものを指す項目ではないため採用しなかった。
    代表的な担い手『ラグーナ・サンテロ』個人の項目（Q30213495）はsourcesに別途記載した"
time:
  start: "178X"
  end: ".."
  display: "18世紀最後の四半期（1780年代）に始まったとされる。代表的な匿名画家『ラグーナ・
    サンテロ』の活動期は1795〜1810年（資料により1796〜1808年）。1821年のサンタフェ・
    トレイル開通で安価な量産版画が流入し、伝統的なサンテロは廃業に追い込まれたとされるが、
    20世紀に民芸復興運動の中で再興され、現在も継続する（ニコラス・エレーラら現代のサンテロ）"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "santero"
  note: "『サンテロ（聖人を作る者）』はスペイン語で担い手自身が用いる職業名であり、当事者由来の
    語である。ただし個々の匿名の担い手を『ラグーナ・サンテロ』のように様式・作例のまとまりで
    後代の研究者が名指した例が多く、個人名の特定できない担い手が多数を占める"
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q30213495", certainty: scholarly}
  - {field: originated_in, source: "https://blog.nmhistorymuseum.org/2011/09/exploring-the-global-roots-of-santeros/", certainty: scholarly}
  - {field: kind, source: "https://blog.nmhistorymuseum.org/2011/09/exploring-the-global-roots-of-santeros/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/santa-fe}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q30213495"
    kind: authority
    note: "代表的な匿名画家『ラグーナ・サンテロ』の項。活動期を1795-1810年とし、ラグーナ・
      プエブロの祭壇画に由来する後代の呼称であると記す"
  - url: "https://blog.nmhistorymuseum.org/2011/09/exploring-the-global-roots-of-santeros/"
    kind: institutional
    note: "ニューメキシコ歴史博物館の公式ブログ。18世紀最後の四半期以降、約10名のサンテロが
      教会向けに聖人像を制作したこと、ラグーナ・サンテロがラグーナ・アコマ両プエブロの祭壇画を
      手がけたことを記す"
  - url: "https://en.wikipedia.org/wiki/Santos_(art)"
    kind: reference
    note: "『Santos』の項。レタブロ（板絵）とブルト（彫像）の技法区分を記す"
status: draft
updated: 2026-09-16
---

# サンテロ / Santero

## 定義と範囲

サンテロ（santero、「聖人を作る者」）は、スペイン領・メキシコ領時代のニューメキシコで、カトリックの
聖人像（サントス）を制作した担い手を指す。作例はレタブロ（板絵）とブルト（彩色木彫像）の2形式に
分かれる。ニューメキシコ歴史博物館の公式ブログはこう記す（機関資料、二次情報）。

> Early pieces from New Mexico date from the late 1700s. About ten santeros provided carved and
> painted images for various churches beginning in the last quarter of the 18th century.

代表的な担い手が、匿名のまま「ラグーナ・サンテロ」と呼ばれる画家で、[Wikidata Q30213495](https://www.wikidata.org/wiki/Q30213495)
は活動期を1795〜1810年とする。ラグーナ・プエブロとアコマ・プエブロの祭壇画がこの初期サンテロの
最も重要な現存例とされる。

## kind の判定

`period-style` とした。単一の血縁・工房による継承ではなく、スペイン領・メキシコ領ニューメキシコ
という政体・時代の枠を通じて、複数の匿名・有名の担い手（ラグーナ・サンテロ、ペドロ・アントニオ・
フレスキース〈1749-1831年、ニューメキシコ生まれの最初のサンテロとされる〉ら）が教会の発注に
応じて制作し続けた点を、[ノヴゴロド派](novgorod-school-icon-painting.md)・
[モスクワ派](moscow-school-icon-painting.md)・[ミナス・バロック](barroco-mineiro.md)・
[タルノヴォ画派](tarnovo-artistic-school.md)と同型の構造と見た。

## 時間

`start`は18世紀最後の四半期（1780年代）とした。1821年、サンタフェ・トレイルの開通により
安価な量産版画がニューメキシコへ流入し、伝統的なサンテロの仕事は失われたとされる。ただし
20世紀の民芸復興運動でこの伝統は再興され、ニコラス・エレーラら現代のサンテロが活動を続けている
ため、`end`は継続中（`..`）とした。

## 空間

`originated_in`はサンタフェ（[place/santa-fe](../places/santa-fe.md)）。スペイン領・メキシコ領
ニューメキシコの行政中心地。

## 未着手

- ラグーナ・サンテロ、ペドロ・アントニオ・フレスキースらを person エンティティとして立てるか
  どうか
- ラグーナ・アコマ両プエブロの祭壇画を work エンティティとして立てるかどうか
- 文化圏間接続（4経路）: 検索した範囲では、収蔵先はいずれも米国内の博物館（Museum of
  International Folk Art、Palace of the Governorsなど）で、域外への文書化された接続は
  見つけられなかった
