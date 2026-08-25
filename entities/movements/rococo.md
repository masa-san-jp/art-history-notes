---
id: movement/rococo
uri: urn:ahn:movement/rococo
type: movement
kind: period-style
label_ja: ロココ
label_en: Rococo
authority:
  wikidata: Q122960
  aat: "300021466"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "173X"
  end: "178X"
  display: "1730年代〜1780年代"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Rococo"
  note: "18世紀の芸術運動・様式。絵画、彫刻、建築、室内装飾、工芸を横断するが、地域ごとの宮廷・都市文化と媒体差を残すため後世の様式分類として扱う"
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q122960", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q122960", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/de/essays/american-rococo", certainty: scholarly}
space:
  - {role: originated_in, target: place/paris}
relations:
  - {type: influenced_by, target: movement/baroque, certainty: scholarly, source: "https://resources.metmuseum.org/resources/metpublications/pdf/Vienna_Circa_1780_An_Imperial_Silver_Service_Rediscovered.pdf"}
sources:
  - url: "https://www.wikidata.org/wiki/Q122960"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021466"
    kind: authority
  - url: "https://www.metmuseum.org/de/essays/american-rococo"
    kind: institutional
  - url: "https://resources.metmuseum.org/resources/metpublications/pdf/Vienna_Circa_1780_An_Imperial_Silver_Service_Rediscovered.pdf"
    kind: scholarly
status: draft
updated: 2026-08-12
---

# ロココ / Rococo

1730年代から1780年代にかけて広がった18世紀の芸術運動・様式。曲線、非対称性、軽快な装飾性、親密な
室内空間への適応を特徴とし、絵画・彫刻・建築・室内装飾・工芸にまたがる。フランス語圏の宮廷・都市文化を
主要な起点の一つとして、ヨーロッパ各地と大西洋世界へ展開した。

## kind の判定

`period-style` とした。Rococo は特定の宣言集団が自称した運動ではなく、18世紀の複数媒体・地域にまたがる
様式を後世に整理した名称である。

## 空間と時間

フランス語圏で成立した装飾語彙の主要結節点として `place/paris` を置く。Wikidata の1730年代〜1780年代を
そのままEDTFで表現した。

## バロックからロココへ

メトロポリタン美術館の出版物は、ウィーンのロココをバロックの「様式上の後継」と位置づけ、マリア・
テレジア期の宮廷文化について、ハイ・バロックから優雅で軽快なロココへ移行したと説明する。ここでの
`influenced_by` は、ロココ全体をバロックの単純な置換とみなすものではなく、18世紀の宮廷・装飾文化に
おける継承と変形を記録するものである。

## 未着手

- ワトー、ブーシェ、フラゴナールの人物・作品と制度的 patronage
- ドイツ語圏、イタリア、イベリア、大西洋世界での地域差
