---
id: movement/golden-horde-art
uri: urn:ahn:movement/golden-horde-art
type: movement
kind: period-style
label_ja: ジョチ・ウルス美術
label_en: Golden Horde Art
authority:
  wikidata: Q79965
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1240~"
  end: "1502"
  display: "都サライはバトゥ・ハン（在位1227-1255年）により1240〜1250年頃に建設されたとされる。
    終期はジョチ・ウルスの解体・クリミア・ハン国等への分裂が実質化した時期（1502年、
    大帳国の滅亡）とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Golden Horde art"
  note: "『ジョチ・ウルス（Golden Horde）』という呼称自体、当事者由来かロシア語資料
    『Золотая Орда』に遡る後代の呼称かは資料により見解が分かれる。様式・美術上の括りとしては
    後代の考古学・美術史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Sarai", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Sarai", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Golden_Horde", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/sarai}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q79965"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Sarai"
    kind: reference
    note: "『Sarai』の項。バトゥ・ハンの孫（原文ママ、系譜の詳細は資料により異なる）が13世紀半ばに
      ヴォルガ川下流に建設した都とし、モンゴル・ペルシア・イスラームの様式が融合した建築を
      特徴とすると記す"
  - url: "https://en.wikipedia.org/wiki/Golden_Horde"
    kind: reference
    note: "『Golden Horde』の項。中国・イラン・中央アジアとの広範な交易・文化的つながりが
      建築装飾の伝統に反映されたと記す"
status: draft
updated: 2026-09-16
---

# ジョチ・ウルス美術 / Golden Horde Art

## 定義と範囲

サライ（[place/sarai](../places/sarai.md)）は、チンギス・ハンの孫バトゥ・ハン（在位1227-1255年）
により、ヴォルガ川下流、現ロシア・アストラハン州近辺に13世紀半ばに建設された、ジョチ・ウルス
（金帳汗国、キプチャク・ハン国）の都である。壮麗なモスク・宮殿・公共建築を持ち、モザイク・彫刻
など豊かな装飾を伴ったとされ、モンゴル・ペルシア・イスラームの様式が融合した独自の建築様式を
持つと記される（WebSearch経由、複数の二次情報）。シルクロードの交易拠点として、陶製の水道管・
浮橋・冶金や陶器の工房を備えた高度なインフラを持ち、金属・ガラス・骨・陶器の日用品・装飾品が
出土している。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ジョチ・ウルスという政体の存続期間を通じて、
複数世代の職人が中国・イラン・中央アジアとの広範な交易・文化的つながりを反映した工芸・建築を
作り続けた点を、[モスクワ派](moscow-school-icon-painting.md)・[タルノヴォ画派](tarnovo-artistic-school.md)
と同型の構造と見た。

## 時間・空間

`originated_in`はサライ。`time`はバトゥ・ハンによる建設（1240〜1250年頃）から、ジョチ・ウルスの
実質的な解体期（1502年）までとした。

## 未着手

- バトゥ・ハンを person エンティティとして立てるかどうか
- サライの発掘出土品を work エンティティとして立てるかどうか
- 文化圏間接続（4経路）: 検索した範囲では、大英博物館・メトロポリタン美術館などでの明確な
  収蔵記録を確認できず、エルミタージュ美術館・国立歴史博物館（いずれもロシア国内、
  europe-east）の収蔵は確認できたが域外への接続としては数えられない。起源region外への
  文書化された接続は現時点で確認できない
