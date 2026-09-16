---
id: movement/pala-art
uri: urn:ahn:movement/pala-art
type: movement
kind: period-style
label_ja: パーラ美術
label_en: Pala Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "『パーラ美術』全体を指すWikidata項目は検索で特定できなかった。中心地
    ナーランダーの項目（Q216243）は別途sourcesに記載した"
time:
  start: "07XX"
  end: "12XX"
  display: "パーラ朝の統治期間（8〜12世紀）を範囲とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Pala art"
  note: "王朝名『パーラ』を冠した後代の美術史記述による様式区分。当事者（王・職人）自身が
    この名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://mapacademy.io/article/pala-bronze-sculptures/", certainty: scholarly}
  - {field: originated_in, source: "https://mapacademy.io/article/pala-bronze-sculptures/", certainty: scholarly}
  - {field: kind, source: "https://mapacademy.io/article/pala-bronze-sculptures/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/nalanda}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/38934"}
sources:
  - url: "https://www.wikidata.org/wiki/Q216243"
    kind: authority
    note: "ナーランダー・マハーヴィハーラの項目"
  - url: "https://mapacademy.io/article/pala-bronze-sculptures/"
    kind: scholarly
    note: "『Pala Bronze Sculptures』の項。ビハール・西ベンガル（現バングラデシュ含む）で
      8〜12世紀に栄えた様式とし、蝋型鋳造による八金属合金のブロンズ像（仏・観音・ターラー等）が
      個人礼拝用に小型・可搬に作られたと記す"
  - url: "https://www.metmuseum.org/art/collection/search/38934"
    kind: institutional
    note: "メトロポリタン美術館収蔵《ターラー》（インド、ビハール州、パーラ期、12世紀、
      銀象嵌ブロンズ）"
status: draft
updated: 2026-09-16
---

# パーラ美術 / Pala Art

## 定義と範囲

MAP Academyの記事「[Pala Bronze Sculptures](https://mapacademy.io/article/pala-bronze-sculptures/)」
（学術資料）はこう記す（二次情報）。パーラ美術は、現在のビハール州・西ベンガル州（現
バングラデシュを含む）で8世紀から12世紀まで栄えた様式で、王朝名パーラに由来する。ブロンズ
彫刻と貝葉写本の彩色画を主な媒体とし、仏陀や諸尊を表す。蝋型鋳造による八金属合金の小型
ブロンズ像は、個人の礼拝のため持ち運べるよう作られたとされる。

[ナーランダー](../places/nalanda.md)をはじめ、ヴィクラマシーラー、オダンタプリーなどの
僧院大学が、チベット・中国・東南アジアから学僧を集める仏教学の一大中心地となった。パーラ朝の
庇護下で、グプタ朝の彫刻の伝統が新たな高みに達し、「パーラ派彫刻」と呼ばれるようになった。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、パーラ朝という政体の存続期間を通じて、
複数世代の鋳物師・写本画家が仏教尊格の像・彩色画を制作し続けた点を、
[シュリーヴィジャヤ美術](srivijaya-art.md)・[チョーラ朝ブロンズ](chola-bronzes.md)と
同型の構造と見た。

## ニューヨークでの収蔵

メトロポリタン美術館は、パーラ期のブロンズ像を複数所蔵する。12世紀の《ターラー》（銀象嵌）、
10〜11世紀の《宝冠仏》（銀・ラピスラズリ・水晶象嵌）などを含む。これに基づき`relations`へ
`diffused_to place/new-york-city`を張り、asia-south起源からamericas-northへの接続を
記録した。

## 未着手

- 代表的な仏像・写本を work エンティティとして立てるかどうか
- パーラ朝歴代の王を person エンティティとして立てるかどうか
- シュリーヴィジャヤ美術との様式的関係（`influenced_by`）を明示するかどうか（今回は
  シュリーヴィジャヤ側の本文にのみ記述）
