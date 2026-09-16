---
id: movement/akan-goldweights
uri: urn:ahn:movement/akan-goldweights
type: movement
kind: retrospective
label_ja: アカン金分銅
label_en: Akan Goldweights
authority:
  wikidata: Q4291228
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "14XX"
  end: "19XX"
  display: "幾何学文様の分銅は現存最古のもので1400年代に遡るとされ、北アフリカのイスラーム
    社会由来の意匠を交易路経由で取り入れたと記される。17世紀から19世紀末にかけては、人物・
    動物・植物・器物を象る具象的な分銅も作られるようになった。大英博物館は16〜20世紀に収集
    された分銅コレクションを所蔵する"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "mrammuo / abrammuo"
  note: "『ムラムオ（mrammuo）／アブラムオ（abrammuo）』はアカンの言葉で当事者が用いる語
    である。ただしこれを一つの美術movementとして束ねたのは後代の人類学・美術史記述である"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Akan_goldweights", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Bono_Manso", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Akan_goldweights", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/bono-manso}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "http://www.britishmuseum.org/research/online_research_catalogues/agw/african_gold-weights/origins_and_history.aspx"}
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/312390"}
sources:
  - url: "https://www.wikidata.org/wiki/Q4291228"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Akan_goldweights"
    kind: reference
    note: "『Akan goldweights』の項。現存最古の幾何学文様の分銅が1400年代に遡り、北アフリカ
      のイスラーム社会由来の意匠を交易路経由で取り入れたと記す。蝋型鋳造による真鍮製で、
      17世紀以降は具象的な意匠も作られたと記す"
  - url: "https://en.wikipedia.org/wiki/Bono_Manso"
    kind: reference
    note: "『Bono Manso』の項。アカン人の金鉱山とジェンネ・トンブクトゥなどサヘル地域の
      市場を結ぶトランス・サハラ交易の要衝だったと記す"
  - url: "http://www.britishmuseum.org/research/online_research_catalogues/agw/african_gold-weights/origins_and_history.aspx"
    kind: institutional
    note: "大英博物館のオンライン研究カタログ。16〜20世紀に収集された分銅約2000点の
      コレクションを所蔵すると記す"
  - url: "https://www.metmuseum.org/art/collection/search/312390"
    kind: institutional
    note: "メトロポリタン美術館収蔵《鳥の爪の分銅》（アサンテ、アカン作）"
status: draft
updated: 2026-09-16
---

# アカン金分銅 / Akan Goldweights

## 定義と範囲

英語版Wikipedia「[Akan goldweights](https://en.wikipedia.org/wiki/Akan_goldweights)」は
こう記す（二次情報）。アカン金分銅（現地語でムラムオ／アブラムオ）は、西アフリカのアカン人が
金の粉・塊を計量するために用いた真鍮製の分銅。蝋型鋳造で作られ、幾何学文様と具象的な意匠の
2種がある。現存最古の幾何学文様の分銅は1400年代に遡り、[ボノ・マンソ](../places/bono-manso.md)
を要衝とするトランス・サハラ交易を通じて、北アフリカのイスラーム社会由来の意匠を取り入れた
とされる。17世紀から19世紀末にかけては、人物・動物・植物・器物を象る具象的な分銅も作られる
ようになった。

## kind の判定

`retrospective`とした。『ムラムオ』自体は当事者由来の語だが（`self_identified: true`）、
これを一つの美術movementとして束ねたのは後代の人類学・美術史記述である。単一の血縁・工房
ではなく、複数世代・複数のアカン人集団（ボノ、後のアサンテなど）が同じ計量・鋳造の慣習を
400年以上にわたり共有し続けた点を重視した。

## ロンドン・ニューヨークでの収蔵

大英博物館は、16〜20世紀に収集された分銅約2000点のコレクションを所蔵する。メトロポリタン
美術館も、アサンテ（アカン）の《鳥の爪の分銅》をはじめ複数の分銅を所蔵する。これに基づき
`relations`へ`diffused_to`を`place/london`・`place/new-york-city`の双方に張り、africa-sub
起源からeurope-west・americas-northへの接続を記録した。

## 未着手

- 個々の分銅を work エンティティとして立てるかどうか
- ボノ王国からアサンテ王国への担い手の移行の一次資料での確認
- 幾何学文様への北アフリカ・イスラーム由来の意匠の影響を`relations`の`influenced_by`で
  明示するかどうか（対応するmovementエンティティが本KBに未整備のため今回は本文の記述に
  とどめた）
