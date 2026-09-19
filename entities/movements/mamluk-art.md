---
id: movement/mamluk-art
uri: urn:ahn:movement/mamluk-art
type: movement
kind: period-style
label_ja: マムルーク美術
label_en: Mamluk Art
authority:
  wikidata: Q2864675
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1250"
  end: "1517"
  display: "マムルーク朝の成立年は資料により1250年（アイユーブ朝スルターン、アッ＝サーリフの
    死とシャジャル・アッ＝ドゥッルの即位）または1260年（モンゴル軍撃退・アッバース朝カリフ制の
    カイロ再興）とされる。終期は1517年、オスマン帝国による征服。現存最古の年紀入り彩飾クルアーン
    とされる『バイバルスのクルアーン』は1304-1306年制作"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Mamluk art"
  note: "『マムルーク』はアラビア語で『所有された者（奴隷軍人）』を意味する語で、王朝の担い手を
    指す語ではあるが、美術の様式を自称する語として当事者が用いた記録は無い。『マムルーク美術』は
    王朝名を冠した後代の美術史上の括りである"
claims:
  - {field: time, source: "https://www.missedhistory.com/article/mamluk-qurans", certainty: scholarly}
  - {field: originated_in, source: "https://www.missedhistory.com/article/mamluk-qurans", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q2864675", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/cairo}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://hyperallergic.com/british-library-digitizes-one-of-the-worlds-oldest-quran-manuscripts/"}
sources:
  - url: "https://www.wikidata.org/wiki/Q2864675"
    kind: authority
  - url: "https://www.missedhistory.com/article/mamluk-qurans"
    kind: reference
    note: "『Cairo's Golden Words: The Art of Mamluk Qurans』の記事。マムルーク朝（1250-1517年）
      のカイロで制作された彩飾クルアーンを扱い、現存最古の年紀入り例『バイバルスのクルアーン』
      （1304-1306年制作、7巻）を記す"
  - url: "https://hyperallergic.com/british-library-digitizes-one-of-the-worlds-oldest-quran-manuscripts/"
    kind: reference
    note: "スルターン・バイバルス2世治下で制作された『バイバルスのクルアーン』が現在ロンドンの
      大英図書館に所蔵されると記す"
status: draft
updated: 2026-09-16
---

# マムルーク美術 / Mamluk Art

## 定義と範囲

マムルーク朝（1250-1517年）は、カイロを首都にエジプト・シリアを支配したスルターン朝で、
モンゴル軍を撃退しアッバース朝カリフ制をカイロに再興したことで「イスラームの守護者」と
みなされた（WebSearch経由、二次情報）。マムルークのスルターン・アミールたちは、自らが建立した
宗教・教育施設に豪華なクルアーンを寄進する慣習を持ち、書家・彩飾師・製紙職人・製本職人が
分業する大規模な制作事業として彩飾クルアーンが作られた（同）。

現存最古の年紀入り彩飾クルアーンとされる『バイバルスのクルアーン』（1304-1306年制作、7巻）は、
スルターン・バイバルス2世の治下で作られ、金地に幾何学文様・唐草文様を用いる様式が確立していた
（Missed History記事、二次情報）。

## kind の判定

`period-style` とした。単一の血縁・工房ではなく、マムルーク朝という政体の存続期間を通じて、
複数のスルターン・アミールの発注に応じて、複数世代の書家・彩飾師が制作し続けた点を、
[ノヴゴロド派](novgorod-school-icon-painting.md)・[サンテロ](santero.md)・
[ンドプ](ndop.md)と同型の構造と見た。

## ロンドンでの収蔵

『バイバルスのクルアーン』は現在、ロンドンの大英図書館に所蔵される。これに基づき`relations`へ
`diffused_to place/london`を張り、mena起源からeurope-westへの接続を記録した。

## 未着手

- バイバルス2世、書家（無名）を person エンティティとして立てるかどうか
- 『バイバルスのクルアーン』を work エンティティとして立てるかどうか
- チェスター・ビーティ・ライブラリー（ダブリン）所蔵の複数のマムルーク・クルアーン写本の
  一次資料での確認
