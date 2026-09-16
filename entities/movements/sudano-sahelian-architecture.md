---
id: movement/sudano-sahelian-architecture
uri: urn:ahn:movement/sudano-sahelian-architecture
type: movement
kind: retrospective
label_ja: スーダノ・サヘル建築
label_en: Sudano-Sahelian Architecture
authority:
  wikidata: Q489021
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1327"
  end: null
  display: "トンブクトゥのジンガレイベル・モスク（大モスク）が1327年、マンサ・ムーサの
    メッカ巡礼（1324年）の資金で建立された。この年を代表例の起点とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Sudano-Sahelian architecture"
  note: "『スーダノ・サヘル』という地理区分名を冠した後代の建築史記述による様式区分。当事者
    （建築家・職人）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Sudano-Sahelian_architecture", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Sudano-Sahelian_architecture", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Sudano-Sahelian_architecture", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/timbuktu}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q489021"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Sudano-Sahelian_architecture"
    kind: reference
    note: "『Sudano-Sahelian architecture』の項。西アフリカのサヘル・スーダン草原地帯の
      諸民族に共通する土着の建築様式群とし、日干しレンガとアドベ漆喰、壁面から突き出た
      大きな木材梁を特徴とすると記す"
  - url: "https://sahistory.org.za/article/summary-kingdom-mali-and-city-timbuktu-14th-century"
    kind: reference
    note: "マンサ・ムーサ（在位1312-1337年）の治世下、1324年のメッカ巡礼後、ムスリムの
      建築家・学者・書物を持ち帰り、1327年、巡礼の資金でジンガレイベル・モスクを建立した
      と記す"
status: draft
updated: 2026-09-16
---

# スーダノ・サヘル建築 / Sudano-Sahelian Architecture

## 定義と範囲

英語版Wikipedia「[Sudano-Sahelian architecture](https://en.wikipedia.org/wiki/Sudano-Sahelian_architecture)」
はこう記す（二次情報）。西アフリカのサヘル・スーダン草原地帯の諸民族に共通する土着の建築様式群で、
日干しレンガとアドベ漆喰を用い、壁面から突き出た大きな木材梁を特徴とする。

代表例が、マンサ・ムーサ（在位1312-1337年）が1324年のメッカ巡礼後、ムスリムの建築家・学者・
書物を持ち帰り、1327年に巡礼の資金で建立した[トンブクトゥ](../places/timbuktu.md)の
ジンガレイベル・モスク（大モスク）である。サンコレ・モスク、シディ・ヤヒヤ・モスクとともに
UNESCO世界遺産に登録されている。サンコレ大学をはじめとする学問機関には、神学・天文学・
医学・法学・詩学に関する数万点の写本（トンブクトゥ写本）が伝わる。

## kind の判定

`retrospective`とした。「スーダノ・サヘル」という地理区分名は後代の建築史記述による括りで
あり、当事者（建築家・職人）自身がこの様式を一つの運動として名乗った記録は無い。単一の
血縁・工房ではなく、サヘル地域の広い範囲・長い期間にわたり、複数の民族・世代の建築家が
共通する土着の技法（日干しレンガ、突き出た木材梁）を用い続けた点を重視した。

## 未着手

- マンサ・ムーサを person エンティティとして立てるかどうか
- ジンガレイベル・モスク、サンコレ・モスクを work エンティティとして立てるかどうか
- 文化圏間接続（4経路）: トンブクトゥ写本の一部はライブラリー・オブ・コングレス・大英図書館が
  デジタル化に関わっているが、原本はマリ国内の家族図書館に残り続けており、物理的な資料の
  域外への移動ではないため接続には数えなかった。検索した範囲では、海外美術館・図書館への
  文書化された物理的移転は確認できない
