---
id: movement/hawaiian-featherwork
uri: urn:ahn:movement/hawaiian-featherwork
type: movement
kind: retrospective
label_ja: ハワイの羽根細工
label_en: Hawaiian Featherwork
authority:
  wikidata: Q8083959
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: null
  end: ".."
  display: "起源は特定できない（古代からの伝統とされるが、開始点を示す一次資料には本調査では
    到達していない）。具体的に日付を追える最初期の例は、1779年のキャプテン・クック来訪時に
    首長カラニオプウが贈った羽根マント（ʻahuʻula）・兜（mahiole）で、カラーカウア王
    （在位1874-1891年）の時代まで王族の正装として製作が続いた。2025年時点でも復興の
    取り組みが報じられており、伝統は途絶えていない"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "nā hulu aliʻi"
  note: "『ハワイの羽根細工』は外部・分析的な括りの英語名。『nā hulu aliʻi（王族の羽根）』は
    ハワイ語の呼称で、製作物の総称ではあるが、担い手がこれを集団的な運動の自称として用いた記録は
    見出せなかった。個々の技法・製品（ʻahuʻula＝マント、mahiole＝兜、kāhili＝羽根の杖）は
    それぞれ別の語を持つ"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/%CA%BBAhu_%CA%BBula", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/%CA%BBAhu_%CA%BBula", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q8083959", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/hawaii-island}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://en.wikipedia.org/wiki/%CA%BBAhu_%CA%BBula"}
sources:
  - url: "https://www.wikidata.org/wiki/Q8083959"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/%CA%BBAhu_%CA%BBula"
    kind: reference
    note: "『ʻAhu ʻula』の項。ハワイの首長階級（aliʻi）の正装であるマントの定義・製法・鳥の種類
      （ʻiʻiwi、mamo、ʻōʻō）を記す。1779年のキャプテン・クック来訪から19世紀のカラーカウア王の
      時代までの使用例と、大英博物館・ドレスデン民族学博物館・ピーボディ・エセックス博物館・
      スミソニアン協会など160点以上が世界各地の博物館に現存すると記す"
status: draft
updated: 2026-09-15
---

# ハワイの羽根細工 / Hawaiian Featherwork

## 定義と範囲

英語版Wikipedia「[ʻAhu ʻula](https://en.wikipedia.org/wiki/%CA%BBAhu_%CA%BBula)」はこう記す
（二次情報、原文引用）。

> ʻAhu ʻula ... were symbols of the highest rank among the chiefly aliʻi class of ancient Hawaii.

マント（ʻahuʻula）は、ネットル科の植物オロナ（olonā）の繊維で編んだ網地に、固有種の鳥の羽根を
数十万枚単位で編み込んで作られた。赤い羽根は主にイイヴィ（ʻiʻiwi）から採り、黄色い羽根は絶滅危惧種の
マモ（mamo）・オオオ（ʻōʻō）から採ったが、後者は生け捕りにして羽根を採取した後に放すという持続的な
方法が取られたと記す（同項）。マント（ʻahuʻula）に加え、兜（mahiole）、羽根の杖（kāhili）も
王族の権威の象徴として製作された。

## kind の判定

`retrospective` とした。「ハワイの羽根細工」という括りは外部・分析的なカテゴリで、当事者は
個々の製品（ʻahuʻula、mahiole、kāhiliなど）をそれぞれ別の語で呼んでいた。[北西海岸先住民の
彫刻](northwest-coast-carving.md)・[樹皮画](bark-painting.md)と同じ構造の外部性を持つ。

## 時間・空間

`start`は特定できないため`null`とした。`originated_in`は[ハワイ島](../places/hawaii-island.md)
（首長カラニオプウの統治地）とした。具体的に日付を追える最初期の例は、1779年のキャプテン・クック
来訪時にカラニオプウが贈ったマント・兜で、これらは237年後の2016年にニュージーランドの
テ・パパ博物館からハワイのビショップ博物館へ長期貸与という形で返還された（WebSearch経由、
二次情報）。同じオセアニア域内の移動であるため、この経緯は4経路監査の接続には数えていない。

## ロンドンでの収蔵

Wikipediaは、大英博物館・ドレスデン民族学博物館・ピーボディ・エセックス博物館・スミソニアン協会
など、160点以上のʻahuʻulaが世界各地の博物館に現存すると記す。これに基づき`relations`へ
`diffused_to place/london`（大英博物館）を張り、オセアニア起源からeurope-westへの接続を
記録した。

## 未着手

- カラニオプウを person エンティティとして立てるかどうか
- 大英博物館所蔵のマント個別のwork化
- Getty AATに対応する項目IDの確認
- 2025年に報じられた復興の取り組みの一次資料への到達
