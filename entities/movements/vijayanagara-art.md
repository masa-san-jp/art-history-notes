---
id: movement/vijayanagara-art
uri: urn:ahn:movement/vijayanagara-art
type: movement
kind: period-style
label_ja: ヴィジャヤナガル美術
label_en: Vijayanagara Art
authority:
  wikidata: Q3533669
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1336"
  end: "1565"
  display: "ヴィジャヤナガル王国はハリハラ1世とその弟ブッカ・ラーヤ1世により1336年に建国された。
    1565年、ターリコータの戦いでの敗北を機に王国は衰退し、都ハンピは破壊された。最盛期は
    クリシュナ・デーヴァ・ラーヤ王の治世（1509-1530年）"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Vijayanagara art"
  note: "王国名『ヴィジャヤナガル（勝利の都）』を冠した後代の美術史記述による括り。当事者
    （石工・彫刻家）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://smarthistory.org/art-and-architecture-of-vijayanagara-empire/", certainty: scholarly}
  - {field: originated_in, source: "https://smarthistory.org/art-and-architecture-of-vijayanagara-empire/", certainty: scholarly}
  - {field: kind, source: "https://smarthistory.org/art-and-architecture-of-vijayanagara-empire/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/hampi}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search?q=South+Indian,+Vijayanagara&sortBy=Relevance"}
sources:
  - url: "https://www.wikidata.org/wiki/Q3533669"
    kind: authority
  - url: "https://smarthistory.org/art-and-architecture-of-vijayanagara-empire/"
    kind: scholarly
    note: "『Art and architecture of the Vijayanagara empire』の項。ハンピの建造物群を1336-1565年
      の帝国の権勢を示すものとし、シヴァ派・ヴィシュヌ派・ジャイナ教それぞれの信仰を反映した彫刻、
      柱廊のある『結婚の間（カリヤーナ・マンダパ）』を特徴とすると記す。様式は先行するチョーラ・
      パーンディヤ朝の伝統の継続と記す"
  - url: "https://www.metmuseum.org/art/collection/search?q=South+Indian,+Vijayanagara&sortBy=Relevance"
    kind: institutional
    note: "メトロポリタン美術館の収蔵検索結果。『South Indian, Vijayanagara』で451件の作品を
      確認した（武具・彫刻等を含む、2026-09-16時点）"
status: draft
updated: 2026-09-16
---

# ヴィジャヤナガル美術 / Vijayanagara Art

## 定義と範囲

Smarthistoryの記事「[Art and architecture of the Vijayanagara empire](https://smarthistory.org/art-and-architecture-of-vijayanagara-empire/)」
（学術資料）はこう記す（二次情報、原文引用）。

> The group of monuments at Hampi bear witness to the power and geopolitical significance of the
> Vijayanagara Empire between the 14th and 16th Centuries in southern India.

[ハンピ](../places/hampi.md)を都に1336年、ハリハラ1世と弟ブッカ・ラーヤ1世により建国された。
様式はシヴァ派・ヴィシュヌ派・ジャイナ教それぞれの信仰を反映した彫刻表現を持ち、先行する
チョーラ・パーンディヤ朝の伝統を継承しつつ発展したとされる。柱廊を持つ「結婚の間（カリヤーナ・
マンダパ）」——花崗岩の柱に跳ねるヤーリ（神獣）に乗る騎手を彫った意匠——が代表的な建築要素と
される。1509-1530年、クリシュナ・デーヴァ・ラーヤ王の治世に最盛期を迎えた。1565年の
ターリコータの戦いでの敗北を機に王国は衰退した。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ヴィジャヤナガル王国の存続期間（1336-1565年）を
通じて、複数世代の石工・彫刻家が寺院建築・彫刻を制作し続けた点を、[クメール美術](khmer-art.md)・
[チョーラ朝ブロンズ](chola-bronzes.md)と同型の構造と見た。既存の
[チョーラ朝ブロンズ](chola-bronzes.md)（880-1279年）とは時代が連続しており、様式的にも
継承関係にあるとされる。

## ニューヨークでの収蔵

メトロポリタン美術館の収蔵検索で「South Indian, Vijayanagara」を対象に451件がヒットした
（武具・彫刻等を含む）。これに基づき`relations`へ`diffused_to place/new-york-city`を張り、
asia-south起源からamericas-northへの接続を記録した。

## 未着手

- ハリハラ1世、ブッカ・ラーヤ1世、クリシュナ・デーヴァ・ラーヤ王を person エンティティとして
  立てるかどうか
- 代表的な建造物（ヴィルーパークシャ寺院、ヴィッタラ寺院など）を work エンティティとして
  立てるかどうか
- チョーラ朝ブロンズからの様式継承を`relations`の`influenced_by`で明示するかどうか（今回は
  本文の記述にとどめた）
