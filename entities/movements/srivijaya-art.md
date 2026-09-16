---
id: movement/srivijaya-art
uri: urn:ahn:movement/srivijaya-art
type: movement
kind: period-style
label_ja: シュリーヴィジャヤ美術
label_en: Srivijaya Art
authority:
  wikidata: Q13021441
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "0650"
  end: "1025~"
  display: "西暦650年頃から1025年頃までの海上交易帝国シュリーヴィジャヤの存続期間を範囲とした。
    帝国自体はその後も13世紀まで存続したとする資料もあるが、勢力の実質的な最盛期を650-1025年と
    する記述に従った"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Srivijaya art"
  note: "王国名『シュリーヴィジャヤ』を冠した後代の美術史記述による様式区分。当事者（王・
    職人）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://countryreports.org/articles/the-srivijaya-empire-maritime-sovereign-of-southeast-asia", certainty: scholarly}
  - {field: originated_in, source: "https://countryreports.org/articles/the-srivijaya-empire-maritime-sovereign-of-southeast-asia", certainty: scholarly}
  - {field: kind, source: "https://www.hdasianart.com/blogs/news/indonesian-buddhist-sculpture-majapahit-srivijaya-legacy", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/palembang}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/39120"}
sources:
  - url: "https://www.wikidata.org/wiki/Q13021441"
    kind: authority
  - url: "https://countryreports.org/articles/the-srivijaya-empire-maritime-sovereign-of-southeast-asia"
    kind: reference
    note: "『The Srivijaya Empire』の記事。スマトラ島を拠点とする仏教海上交易帝国とし、
      西暦650-1275年頃にマラッカ海峡と交易路を支配したと記す。都パレンバンが世界有数の
      仏教学の中心地だったと記す"
  - url: "https://www.hdasianart.com/blogs/news/indonesian-buddhist-sculpture-majapahit-srivijaya-legacy"
    kind: reference
    note: "『Indonesian Buddhist Sculpture』の記事。シュリーヴィジャヤ美術の主要な遺産が
      ブロンズ彫刻とし、観音・ターラー・弥勒などの大乗仏教の尊格を表すと記す。南インドの
      パッラヴァ朝・初期チョーラ朝の様式と東南アジア独自の要素の融合と記す"
  - url: "https://www.metmuseum.org/art/collection/search/39120"
    kind: institutional
    note: "メトロポリタン美術館収蔵《立像の神格（ヴィシュヌ？）》（インドネシア、スマトラ、
      シュリーヴィジャヤ期）"
status: draft
updated: 2026-09-16
---

# シュリーヴィジャヤ美術 / Srivijaya Art

## 定義と範囲

「The Srivijaya Empire」の記事はこう記す（二次情報）。シュリーヴィジャヤは、スマトラ島を
拠点とする仏教海上交易帝国で、東南アジア各地の仏教の広がりに影響を与えた。西暦650-1275年頃、
マラッカ海峡とインド・中国間の海上交易路を支配した。都[パレンバン](../places/palembang.md)は
中国・チベットから学僧・巡礼者を集める、世界有数の仏教学の中心地となった。

現存するシュリーヴィジャヤ美術の主要な遺産はブロンズ彫刻で、観音（慈悲の菩薩）、ターラー
（解脱の女性菩薩）、弥勒（未来仏）など大乗仏教の尊格を表す。優れた作例は、南インドのパッラヴァ
朝・初期チョーラ朝の様式的伝統と、東南アジア独自の要素を融合させた鋳造技術・美的感性を示す。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、シュリーヴィジャヤという海上交易帝国の存続
期間を通じて、複数世代の鋳物師が仏教尊格のブロンズ像を制作し続けた点を、
[チョーラ朝ブロンズ](chola-bronzes.md)・[クメール美術](khmer-art.md)と同型の構造と見た。
南インドのパッラヴァ・初期チョーラ様式からの影響も本文に記した。

## ニューヨークでの収蔵

メトロポリタン美術館は、シュリーヴィジャヤ期のブロンズ像《立像の神格（ヴィシュヌ？）》
（インドネシア、スマトラ）を所蔵する。これに基づき`relations`へ`diffused_to place/new-york-city`
を張り、asia-southeast起源からamericas-northへの接続を記録した。

## 未着手

- 代表的な出土像（チャイヤーの観音像など）を work エンティティとして立てるかどうか
- パッラヴァ・初期チョーラ様式からの影響を`relations`の`influenced_by`で明示するかどうか
  （今回は本文の記述にとどめた）
- 帝国の終期（1025年頃 vs 13世紀まで存続とする資料）の食い違いの一次資料での整理
