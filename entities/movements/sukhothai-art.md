---
id: movement/sukhothai-art
uri: urn:ahn:movement/sukhothai-art
type: movement
kind: period-style
label_ja: スコータイ美術
label_en: Sukhothai Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "『スコータイ美術』全体を指すWikidata項目は検索で特定できなかった。王国自体・
    代表的な寺院ワット・マハータートの項目は別途sourcesに記載した"
time:
  start: "1200"
  end: "1350~"
  display: "スコータイ王国の存続期間（伝統的な建国年は1238年、Smarthistoryは代表様式
    『歩行仏（Walking Buddha）』を1200-1350年のスコータイ王国の古典様式とする）。歩行仏
    という様式的発明自体は14世紀とされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Sukhothai style"
  note: "地名『スコータイ』を冠した後代の美術史記述による様式区分。当事者がこの名で自らの
    様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://smarthistory.org/sukhothai-walking-buddha/", certainty: scholarly}
  - {field: originated_in, source: "https://smarthistory.org/sukhothai-walking-buddha/", certainty: scholarly}
  - {field: kind, source: "https://smarthistory.org/sukhothai-walking-buddha/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/sukhothai}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/39102"}
sources:
  - url: "https://www.wikidata.org/wiki/Q986737"
    kind: authority
    note: "スコータイ市（旧王都）の項目"
  - url: "https://smarthistory.org/sukhothai-walking-buddha/"
    kind: scholarly
    note: "『Sukhothai Walking Buddha』の項。歩行仏をスコータイ王国（1200-1350年）の
      古典様式の代表像とし、インドに先行例を持たないタイ独自の発明と記す。スリランカの
      上座部仏教美術が最も直接の影響源とする"
  - url: "https://www.metmuseum.org/art/collection/search/39102"
    kind: institutional
    note: "メトロポリタン美術館収蔵《歩行仏》（タイ）"
status: draft
updated: 2026-09-16
---

# スコータイ美術 / Sukhothai Art

## 定義と範囲

Smarthistoryの記事「[Sukhothai Walking Buddha](https://smarthistory.org/sukhothai-walking-buddha/)」
（学術資料）はこう記す（二次情報、原文引用）。

> The creation of a walking Buddha image is a distinctive feature of Thai art in the thirteenth
> century.

歩行仏（cankrama）は、インドに先行する図像を持たない、タイ独自の考案とされ、仏陀を地上を
歩む存在として描く点が特徴とされる。様式面では、滑らかで長い四肢、卵型の顔、流れるような
衣文の表現が特徴とされる。同記事は、スリランカ（セイロン）の上座部仏教美術が最も直接の
影響源だったと記す。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、[スコータイ](../places/sukhothai.md)を都と
する王国の存続期間（1200-1350年頃を中心とする古典期）を通じて、複数世代の鋳造職人が仏像を
制作し続けた点を、[クメール美術](khmer-art.md)・[チョーラ朝ブロンズ](chola-bronzes.md)と
同型の構造と見た。

## ニューヨークでの収蔵

メトロポリタン美術館は《歩行仏》（タイ）を所蔵する。これに基づき`relations`へ
`diffused_to place/new-york-city`を張り、asia-southeast起源からamericas-northへの接続を
記録した。

## 未着手

- 個別の仏像（歩行仏など）を work エンティティとして立てるかどうか
- スコータイ王国の建国年（伝統的に1238年）の一次資料での確認
- スリランカ上座部仏教美術との影響関係を`relations`の`influenced_by`で明示するかどうか
  （対応するスリランカのmovementエンティティが本KBに未整備のため今回は本文の記述にとどめた）
