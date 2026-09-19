---
id: movement/pa-fortification-architecture
uri: urn:ahn:movement/pa-fortification-architecture
type: movement
kind: period-style
label_ja: パー要塞集落建築
label_en: Pā Fortified Settlement Architecture
authority:
  wikidata: Q1234236
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "13XX"
  end: ".."
  display: "英語版Wikipedia『Pā』は、クマラ（サツマイモ）の貯蔵技術の発達が、北から南へ
    広がる要塞化された丘陵集落（パー）の勃興の契機になったとし、14〜15世紀を勃興・拡大の
    時期とする。17〜18世紀にはタイアハ（棒状武器）が主要武器となる時期まで発展が続いたと
    記す。ニュージーランド戦争（1845-1872年）の戦場としても使われ続けたため、終期は
    継続中とした"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "pā"
  note: "『パー』はマオリ語で村・要塞化された集落を指す当事者由来の語である。ただし
    『建築movement』として時代を貫いて括るのは後代の考古学・建築史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/P%C4%81", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/P%C4%81", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q1234236", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/new-zealand}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q1234236"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/P%C4%81"
    kind: reference
    note: "『Pā』の項。クマラ（サツマイモ）貯蔵穴の技術発達が、北から南へ広がる要塞化された
      丘陵集落の勃興・拡大を後押ししたとし、14〜15世紀を勃興期とする。約500年前
      （15世紀頃）以前からの古い時期のパーも知られるとする一方、17〜18世紀には
      タイアハが主要武器となる時期まで発展が続いたと記す。精巧な設計のパーには
      『入念に彫刻された出入口・意匠を凝らした主柱』が特徴として見られるとする。
      ワイカト地方ンガーロト湖の泥炭から保存状態の良い彫刻木工品が多数出土し、
      近隣のテ・アワムトゥ博物館（ニュージーランド国内）に展示されていると記す"
status: draft
updated: 2026-09-17
---

# パー要塞集落建築 / Pā Fortified Settlement Architecture

## 定義と範囲

英語版Wikipedia「[Pā](https://en.wikipedia.org/wiki/P%C4%81)」（参考資料）はこう記す
（二次情報）。クマラ（サツマイモ）を貯蔵する技術の発達が、[ニュージーランド](../places/new-zealand.md)
北島から南島へ広がる要塞化された丘陵集落（パー）の勃興・拡大を後押しし、14〜15世紀を
その勃興期とする。約500年前（15世紀頃）より古い時期のパーも知られる一方、17〜18世紀には
タイアハ（棒状武器）が主要武器となる時期まで発展が続いた。精巧な設計のパーは、入念に
彫刻された出入口（ワハロア）・意匠を凝らした主柱を特徴とする。ワイカト地方ンガーロト湖の
泥炭からは保存状態の良い彫刻木工品が多数出土し、テ・アワムトゥ博物館（ニュージーランド
国内）に展示されている。

## kind の判定

`period-style`とした。『パー』自体はマオリ語で当事者が用いる語だが
（`naming.self_identified: true`）、単一の血縁・工房ではなく、複数世代・複数部族の
マオリが数世紀にわたり要塞建築・彫刻を共有し続けた点を、[コーワイワイ](kowhaiwhai.md)
と同様の構造と見た。

## 空間的接続の判定

出土した彫刻木工品はテ・アワムトゥ博物館（ニュージーランド国内）に展示されるのみで、
検索した範囲では、パーの建築様式・彫刻がニュージーランド域外の博物館等へ拡散した
文書化された記録は見つからなかった。よって`relations`に`diffused_to`は張らず、
`config/cross-region-reviews.yaml`に「文化圏をまたぐ接続の記録なし」として記録した。

## 未着手

- カイアポイ・パー等、個別のパー遺跡を place エンティティとして立てるかどうか
- ンガーロト湖出土の彫刻木工品を work エンティティとして立てるかどうか
- [コーワイワイ](kowhaiwhai.md)・[ンガーティ・タラーワイ彫刻](ngati-tarawhai-whakairo.md)
  との担い手・様式の重なりの整理
