---
id: movement/kano-school
uri: urn:ahn:movement/kano-school
type: movement
kind: lineage-school
label_ja: 狩野派
label_en: Kanō school
authority:
  wikidata: Q252801
  aat: "300018653"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1500~"
  end: "1868~"
  display: 15世紀末〜明治維新（Wikidata の inception は1500年、解体は明治期とされる）
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: 狩野派
  note: 家名がそのまま呼称になっており、命名という行為が存在しない型。西洋の -ism のように誰かが名付けた運動ではない
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q252801", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q252801", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
  - {role: active_in, target: place/kyoto}
relations: []
sources:
  - https://www.wikidata.org/wiki/Q252801
  - https://www.getty.edu/research/tools/vocabularies/aat/
status: draft
updated: 2026-08-08
---

# 狩野派 / Kanō school

**この KB で最初に置いた非西洋の movement。** 西洋の「-ism」と同じ型に入れてよいのかという問いが、
この1件に集まっている。

## 定義と範囲

室町後期から明治維新まで約400年続いた日本絵画の画派。狩野正信に始まり、血縁と養子縁組、
工房の徒弟制度によって継承された。

典拠: Wikidata [Q252801](https://www.wikidata.org/wiki/Q252801)／Getty AAT `300018653`

## kind の判定 — なぜ `lineage-school` か

`self-declared`（当事者が名乗った運動）でも `retrospective`（後付けの括り）でもない。
**血縁と工房の継承体**であり、制度としての実体を持つ。Wikidata は Q252801 に
`art movement`（Q968159）と並んで **`family`（Q8436）** を付けており、この二重性がそのまま
「運動ではなく家系」という性質を示している。

つまり「movement」という型名はこの対象に対して**近似**である。それでも型を分けないのは、
分ければ琳派（私淑の系譜で工房組織ではない）のような中間例のたびに置き場が動き、ID が変わるから。
型は1つに保ち、`kind` で性質を区別する（[issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1) の決定）。

## 時間

- Wikidata の inception は **1500年**。ただし精度は不明（世紀レベルの丸めの可能性がある）ので
  EDTF では `1500~`（およそ）として持つ。
- 終期は明治期の解体。`1868~` として持つ。**未確認**: 「いつ終わったか」は解体の定義次第で、
  一次資料に当たっていない。

## 空間

発生地・活動地を京都とした。**これは通説（狩野正信の活動地）であり、一次資料・典拠IDでの裏は取れていない。**
Wikidata が持つのは country（日本）までで、都市の情報がない。江戸期には江戸へ移り、
奥絵師として幕府に仕えた系統が生まれる——**この移動（`diffused_to` / `patronized_by`）は未着手**。

## 未着手

- 担い手（狩野正信・元信・永徳・探幽）の person エンティティ
- 作品（証拠）の work エンティティ
- 幕府との関係（`patronized_by`）と、江戸への移動
- 琳派・土佐派との関係（同時代の並行は時間×空間から生成されるので、エッジは張らない）
