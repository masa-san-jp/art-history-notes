---
id: movement/gothic-art
uri: urn:ahn:movement/gothic-art
type: movement
kind: period-style
label_ja: ゴシック美術
label_en: Gothic art
authority:
  wikidata: Q46825
  aat: "300020775"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "11XX"
  end: "15XX"
  display: "12世紀前半（北フランスで1140年頃に顕著化）〜15世紀頃。地域により終期は異なる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Gothic art"
  note: "後世の美術史が中世ヨーロッパの建築・彫刻・絵画・工芸を横断して括った時代様式。名称は当事者の自己宣言ではなく、地域差と媒体差を含む広域的な整理として扱う"
claims:
  - {field: time, source: "https://www.metmuseum.org/fr/essays/gothic-art", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/fr/essays/gothic-art", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q46825", certainty: scholarly}
space:
  - {role: originated_in, target: place/paris}
relations:
  - {type: influenced_by, target: movement/byzantine-art, certainty: scholarly, source: "https://www.metmuseum.org/pt/met-publications/the-year-1200-a-background-survey"}
sources:
  - url: "https://www.wikidata.org/wiki/Q46825"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300020775"
    kind: authority
  - url: "https://www.metmuseum.org/fr/essays/gothic-art"
    kind: institutional
  - url: "https://www.metmuseum.org/pt/met-publications/the-year-1200-a-background-survey"
    kind: institutional
status: draft
updated: 2026-08-12
---

# ゴシック美術 / Gothic art

12世紀前半の北フランスで顕著になり、その後ヨーロッパ各地へ広がった中世の時代様式。尖頭アーチや
トレーサリーなどの建築語彙は、彫刻、ステンドグラス、写本、金工、象牙細工などにも展開した。
メトロポリタン美術館は、サン＝ドニの西正面で1140年頃に革新的な彫刻プログラムが現れ、ゴシックの語彙が
ヨーロッパ全体に浸透したと説明する。

## kind の判定

`period-style` とした。ゴシックは特定の自称集団ではなく、約4世紀にわたる地域的・媒体横断的な様式の
まとまりである。

## 空間と時間

起源地は北フランスを代表する都市ノードとして `place/paris` に置く。始点は1140年頃の顕著化を含むよう
`11XX`、終点は地域差を残して15世紀頃を示す `15XX` とした。

## ビザンティン美術からの形成期の受容

メトロポリタン美術館は、ハイ・ゴシックへつながる1180〜1220年頃のフランス美術を、フランス、
フランドル、モーゼル、ビザンティンの要素が混ざったものと説明している（[The Year 1200: A Background Survey](https://www.metmuseum.org/pt/met-publications/the-year-1200-a-background-survey)）。
ここで動いたものは、ビザンティンの作品・造形モデルがフランスの形成期の美術へ取り込まれたという範囲の
受容である。`influenced_by movement/byzantine-art` はゴシック美術全体がビザンティン様式を継承したという
意味ではなく、ハイ・ゴシックへ至る過渡期に限定して記録する。

## 未着手

- サン＝ドニ、シャルトル、ランスなどの個別建築・工房の分解
- イタリア、イングランド、ドイツ、イベリアでの地域別終期と受容経路
