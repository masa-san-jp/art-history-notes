---
id: movement/kilwa-swahili-architecture
uri: urn:ahn:movement/kilwa-swahili-architecture
type: movement
kind: period-style
label_ja: キルワ・スワヒリ建築
label_en: Kilwa Swahili Architecture
authority:
  wikidata: Q3107156
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "11XX"
  end: "1500~"
  display: "大モスクの北側祈祷室（最初期の建設段階）は11世紀または12世紀の建設とされる。
    キルワは独立した都市国家として12〜15世紀に栄え、13〜16世紀を最盛期とする資料もある"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Kilwa Swahili architecture"
  note: "地名『キルワ』を冠した後代の美術史記述による様式区分。当事者（スルターン・職人）
    自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Great_Mosque_of_Kilwa", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Great_Mosque_of_Kilwa", certainty: scholarly}
  - {field: kind, source: "https://www.worldhistory.org/Kilwa/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/kilwa-kisiwani}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://www.britishmuseum.org/collection/object/C_1935-1101-1"}
sources:
  - url: "https://www.wikidata.org/wiki/Q3107156"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Great_Mosque_of_Kilwa"
    kind: reference
    note: "『Great Mosque of Kilwa』の項。北側祈祷室が最初期の建設段階として11〜12世紀に
      建てられ、13世紀に側柱・梁が追加され、14世紀初頭にスルターン、アル＝ハサン・イブン・
      スライマーンが大ドームを持つ南側拡張部を加えたと記す"
  - url: "https://www.worldhistory.org/Kilwa/"
    kind: reference
    note: "『Kilwa』の項。独立した都市国家として12〜15世紀に栄え、珊瑚石・石灰モルタルを用いる
      スワヒリ建築様式の壮麗な建造物を持ったと記す"
  - url: "https://www.britishmuseum.org/collection/object/C_1935-1101-1"
    kind: institutional
    note: "大英博物館収蔵、キルワのスルターンに関するアラビア語銘文を持つ銅合金貨（登録番号
      1935,1101.1）"
status: draft
updated: 2026-09-16
---

# キルワ・スワヒリ建築 / Kilwa Swahili Architecture

## 定義と範囲

英語版Wikipedia「[Great Mosque of Kilwa](https://en.wikipedia.org/wiki/Great_Mosque_of_Kilwa)」
はこう記す（二次情報）。大モスクの北側祈祷室（最初期の建設段階）は11世紀または12世紀の建設と
され、13世紀に側柱・梁が追加され、14世紀初頭にスルターン、アル＝ハサン・イブン・スライマーンが
大ドームを持つ南側拡張部を加えた。[キルワ・キシワニ](../places/kilwa-kisiwani.md)は
独立した都市国家として12〜15世紀に栄え、珊瑚石・石灰モルタルを用いる精緻な彫刻と意匠を特徴と
する「スワヒリ建築」様式の壮麗な宮殿・モスク・石造建築を持った。フシュニ・クブワ宮殿では、
14世紀にヴォールト構造が初めて用いられ、大モスクの拡張部にも応用された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、キルワ・スルターン国という政体の存続期間を
通じて、複数世代のスルターン・職人がモスク・宮殿を建立し続けた点を、
[アラウィー朝帝都建築](alaouite-imperial-architecture.md)・[マムルーク美術](mamluk-art.md)
と同型の構造と見た。

## ロンドンでの収蔵

大英博物館は、キルワのスルターンに関するアラビア語の脚韻を踏む銘文を持つ銅合金貨（登録番号
1935,1101.1）を所蔵する。これに基づき`relations`へ`diffused_to place/london`を張り、
africa-sub起源からeurope-westへの接続を記録した。

## 未着手

- スルターン、アル＝ハサン・イブン・スライマーンを person エンティティとして立てるかどうか
- 大モスク、フシュニ・クブワ宮殿を work エンティティとして立てるかどうか
- 起点年（大モスク北側祈祷室の11世紀説・12世紀説）の食い違いの一次資料での解消
