---
id: movement/khmer-art
uri: urn:ahn:movement/khmer-art
type: movement
kind: period-style
label_ja: クメール美術
label_en: Khmer Art
authority:
  wikidata: Q4203993
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "0802"
  end: "1431"
  display: "クメール王朝の存続期間（802-1431年）を範囲とした。代表例のアンコール・ワットは
    12世紀の建立。1431年はアユタヤ王朝によるアンコール陥落の年"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Khmer art"
  note: "『クメール美術』は民族名『クメール』を冠した後代の美術史記述による括り。本項は
    Wikidata Q4203993（Cambodian art／カンボジア美術全体を指す項目）を典拠として借用しつつ、
    範囲をクメール王朝期（802-1431年）に限定した——現代までのカンボジア美術全体は範囲外とした"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Khmer_art", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Khmer_art", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Khmer_art", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/angkor}
relations:
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "https://cambodianess.com/article/the-musee-guimet-and-the-khmer-treasures-of-paris"}
sources:
  - url: "https://www.wikidata.org/wiki/Q4203993"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Khmer_art"
    kind: reference
    note: "『Cambodian art』（英語版記事名はKhmer_art）の項。最も広く認知される時代がクメール
      王朝期（802-1431年）とし、アンコール・ワット（12世紀）を代表例に、規模・豊かさ・
      石彫の精緻さを特徴とすると記す"
  - url: "https://cambodianess.com/article/the-musee-guimet-and-the-khmer-treasures-of-paris"
    kind: reference
    note: "パリのギメ美術館のクメール・コレクションが、1888年のエミール・ギメによる収集と
      旧トロカデロ・インドシナ博物館（ルイ・ドラポルトが着手）のコレクションを1927-31年に
      統合して成立し、カンボジア国外では最大・最も網羅的なクメール美術コレクションと
      なったと記す"
status: draft
updated: 2026-09-16
---

# クメール美術 / Khmer Art

## 定義と範囲

英語版Wikipedia「[Khmer art](https://en.wikipedia.org/wiki/Khmer_art)」（記事名はCambodian art）
はこう記す（二次情報、原文引用）。

> The most widely recognized period of Cambodian art is that of the Khmer Empire (802–1431),
> especially in the area around Angkor and the 12th-century temple-complex of Angkor Wat.

同項はクメール美術の影響が東南アジア全域に及んだと記す。本項では、カンボジア美術の全時代を
扱うのではなく、クメール王朝期（802-1431年、[アンコール](../places/angkor.md)を中心地とする）
に範囲を限定した。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、クメール王朝という政体の存続期間を通じて、
複数世代の石工・彫刻家が寺院建築・彫刻を制作し続けた点を、[モスクワ派](moscow-school-icon-painting.md)・
[サンテロ](santero.md)と同型の構造と見た。

## パリでの収蔵

パリのギメ美術館のクメール・コレクションは、1888年のエミール・ギメによる収集と、旧トロカデロ・
インドシナ博物館（ルイ・ドラポルトが着手）のコレクションを1927-31年に統合して成立した。
Cambodianess誌の記事はこう記す（二次情報）。

> The Khmer art collection at Guimet ... is the largest in the West.

これに基づき`relations`へ`diffused_to place/paris`を張り、asia-southeast起源からeurope-west
への接続を記録した。

## 未着手

- アンコール・ワット、アンコール・トム（バイヨン）を work エンティティとして立てるかどうか
- クメール王朝の歴代王を person エンティティとして立てるかどうか
- 1431年のアユタヤ王朝によるアンコール陥落の一次資料での確認
- 802-1431年より後（ポスト・アンコール期）のカンボジア美術は本項の範囲外とし、別movementとして
  立てるべきかどうか
