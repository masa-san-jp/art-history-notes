---
id: movement/early-ottoman-architecture
uri: urn:ahn:movement/early-ottoman-architecture
type: movement
kind: period-style
label_ja: 初期オスマン建築
label_en: Early Ottoman Architecture
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "この様式区分全体を指すWikidata項目は検索で特定できなかった。代表建築
    緑のモスクの項目（Q1549086）は別途sourcesに記載した"
time:
  start: "1419"
  end: "1453~"
  display: "代表例の緑のモスクは1419-1424年、スルターン、メフメト1世の発注で建立された。
    終期は1453年、オスマン帝国によるコンスタンティノープル征服・遷都を目安とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Early Ottoman architecture"
  note: "『初期オスマン建築』は後代の建築史記述による時代区分の呼称。当事者（建築家・
    スルターン）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Green_Mosque,_Bursa", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Green_Mosque,_Bursa", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Green_Mosque,_Bursa", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/bursa}
relations:
  - {type: influenced_by, target: movement/byzantine-art, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Ottoman_architecture"}
sources:
  - url: "https://www.wikidata.org/wiki/Q1549086"
    kind: authority
    note: "緑のモスク（ブルサ）の項目"
  - url: "https://en.wikipedia.org/wiki/Green_Mosque,_Bursa"
    kind: reference
    note: "『Green Mosque, Bursa』の項。スルターン、メフメト1世の発注で1419-1424年に建立
      され、建築家ハジュ・イヴァズ・パシャ（1428年没）を記す。初期オスマン建築様式の
      頂点と見なされると記す"
  - url: "https://en.wikipedia.org/wiki/Ottoman_architecture"
    kind: reference
    note: "『Ottoman architecture』の項。初期オスマン朝が位置した辺境（ビザンツ帝国との
      境界地帯）が、ビザンツ建築や他の古代遺構からの影響を促し、この時期の周辺の
      テュルク系諸侯国の下でも建築的な実験の例があったと記す"
status: draft
updated: 2026-09-21
---

# 初期オスマン建築 / Early Ottoman Architecture

## 定義と範囲

英語版Wikipedia「[Green Mosque, Bursa](https://en.wikipedia.org/wiki/Green_Mosque,_Bursa)」
はこう記す（二次情報）。緑のモスクは、スルターン、メフメト1世の発注により1419年から1424年に
かけて建立された。建築家はハジュ・イヴァズ・パシャ（1428年没）で、モスク・霊廟（緑の廟）・
マドラサ・公共食堂・浴場からなる複合施設を設計した。内部の緑・青のタイル装飾から「緑の
モスク」と呼ばれる。同記事は、この建物が初期オスマン建築様式の美的・技術的な頂点と見なされる
と記す。緑の廟は、メフメト1世の死（1421年）を受け、息子のスルターン、ムラト2世により
建立された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、オスマン帝国が[ブルサ](../places/bursa.md)を
都とした時代（1326年-1453年頃）を通じて、複数の建築家がモスク・霊廟複合施設を建立し続けた点を
重視した。1453年のコンスタンティノープル征服・遷都を機に建築の中心地が移ったとされるため、
これを終期の目安とした。

## ビザンツ建築からの影響

英語版Wikipedia「[Ottoman architecture](https://en.wikipedia.org/wiki/Ottoman_architecture)」
（参考資料）はこう記す（二次情報）。初期オスマン朝が位置した辺境（ビザンツ帝国との境界
地帯）は、ビザンツ建築や他の古代遺構からの影響を受けやすい立地であり、この時期には周辺の
テュルク系諸侯国の下でも建築的な実験の例があった。これに基づき`relations`へ
`influenced_by movement/byzantine-art`を張った。

## 未着手

- スルターン、メフメト1世・ムラト2世、建築家ハジュ・イヴァズ・パシャを person エンティティ
  として立てるかどうか
- 緑のモスク、緑の廟を work エンティティとして立てるかどうか
- ~~文化圏間接続（4経路）: 検索した範囲では、海外美術館収蔵などmena外への文書化された接続は
  見つけられなかった（建築中心の様式であるため、可動作品の海外収蔵自体が想定しにくい）~~
  → 2026-09-21解消。`influenced_by movement/byzantine-art`（europe-east/europe-west起源）を
  張ったことでmovement-relation経路が成立し、`config/cross-region-reviews.yaml`の
  当該エントリは削除した
