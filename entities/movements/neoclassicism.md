---
id: movement/neoclassicism
uri: urn:ahn:movement/neoclassicism
type: movement
kind: retrospective
label_ja: 新古典主義
label_en: Neoclassicism
authority:
  wikidata: Q14378
  aat: "300021474"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "17XX"
  end: "18XX"
  display: "18世紀半ば〜19世紀前半。地域・媒体により持続期間は異なる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Neoclassicism"
  note: "古代ギリシア・ローマへの関心、考古学、美術アカデミー、啓蒙主義を結びつけて後世に整理された広域的な様式。単一の自称運動や一つの都市のみに還元しない"
claims:
  - {field: time, source: "https://www.metmuseum.org/fr/essays/neoclassicism", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/fr/essays/neoclassicism", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q14378", certainty: scholarly}
space:
  - {role: originated_in, target: place/rome}
relations:
  - {type: influenced_by, target: movement/renaissance, certainty: scholarly, source: "https://www.metmuseum.org/fr/essays/neoclassicism"}
sources:
  - https://www.wikidata.org/wiki/Q14378
  - https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021474
  - https://www.metmuseum.org/fr/essays/neoclassicism
status: draft
updated: 2026-08-12
---

# 新古典主義 / Neoclassicism

18世紀半ばから19世紀前半にかけて、古代ギリシア・ローマの建築・彫刻・文学を参照しながら、啓蒙主義、
考古学、美術アカデミー、公共的な徳の表象を結びつけた広域的な様式。ローマは古代遺跡とコレクション、
アカデミー、旅行者のネットワークを介した重要な形成地となった。

## kind の判定

`retrospective` とした。Neoclassicism は複数地域の実践を、古典回帰という共通項によって後世にまとめた
歴史的な分類である。地域の当事者が一つの集団名として自称した運動とは扱わない。

## 空間と時間

ローマを重要な形成地として `originated_in` に置くが、パリ、ロンドン、ベルリンなどでも制度と制作が展開した。
終点は19世紀の地域差を残して `18XX` とした。

## ルネサンスを介した古典回帰

メトロポリタン美術館は、ラファエロからプッサン、クロード・ロランに至るルネサンスの達成が、調和・
単純性・比例への新たな関心を媒介し、その関心が考古学の進展によって強まったと説明する。ここでの
`influenced_by` は、ルネサンスの古典理解と作品・理論の蓄積が新古典主義の古代回帰を媒介した経路を示し、
両者の様式を同一視するものではない。

## 未着手

- ポンペイ・ヘルクラネウム発掘、ローマのアカデミー、グラン・ツアーの関係化
- ダヴィッド、カノーヴァ、ピラネージらの人物・作品ノード
- ロマン主義との同時並行・反応関係の典拠化
