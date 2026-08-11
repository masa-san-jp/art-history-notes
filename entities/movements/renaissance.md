---
id: movement/renaissance
uri: urn:ahn:movement/renaissance
type: movement
kind: period-style
label_ja: ルネサンス
label_en: Renaissance
authority:
  wikidata: Q1404472
  aat: "300021140"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "13XX"
  end: "16XX"
  display: "14世紀頃〜17世紀初頭。地域と分野により時期は異なる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Renaissance"
  note: "古典古代の再発見、人文主義、自然観察、個人の知的能力を結びつけた広域的な文化・芸術史上の括り。単一の自称運動ではなく、イタリアを起点に地域ごとに異なる展開をしたため時代様式として扱う"
claims:
  - {field: time, source: "https://82nd-and-fifth.metmuseum.org/toah/ht/08/eustc.html", certainty: scholarly}
  - {field: originated_in, source: "https://82nd-and-fifth.metmuseum.org/toah/ht/08/eustc.html", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q1404472", certainty: scholarly}
space:
  - {role: originated_in, target: place/florence}
relations:
  - {type: influenced_by, target: movement/byzantine-art, certainty: scholarly, source: "https://www.metmuseum.org/exhibitions/listings/2004/byzantium-faith-and-power"}
sources:
  - https://www.wikidata.org/wiki/Q1404472
  - https://www.metmuseum.org/essays/anatomy-in-the-renaissance
  - https://82nd-and-fifth.metmuseum.org/toah/ht/08/eustc.html
  - https://www.metmuseum.org/exhibitions/listings/2004/byzantium-faith-and-power
  - https://www.metmuseum.org/press-releases/dazzling-byzantine-treasures-displayed-at-metropolitan-museum-opening-march-23-2004-exhibitions
status: draft
updated: 2026-08-12
---

# ルネサンス / Renaissance

14世紀頃から17世紀初頭にかけて、古典古代の再発見、人文主義、自然観察、個人の知的能力への関心が
結びついた文化・芸術の展開。イタリアでは15世紀のフィレンツェが人文主義研究と芸術制作の結節点となり、
その語彙と制度が他地域へ伝播した。

## kind の判定

`period-style` とした。「ルネサンス」は後世の歴史叙述で広域の文化現象をまとめる名称であり、単一の
結社や宣言を指す自称ではない。絵画・彫刻・建築だけでなく、文学、科学、都市計画にもまたがる。

## 空間と時間

本KBでは初期の主要結節点としてフィレンツェを `originated_in` に置く。始点・終点は地域差を吸収するため
世紀精度に留め、北方ルネサンスやヴェネツィア、ローマの別経路は個別エンティティで分解する。

## ビザンティン美術・東方キリスト教世界との接続

メトロポリタン美術館は、ビザンティン文明の文化的・芸術的影響がラテン語圏の西方に及び、とりわけ
東方キリスト教世界がルネサンスの発展に影響したと説明している（[展覧会概要](https://www.metmuseum.org/exhibitions/listings/2004/byzantium-faith-and-power)）。
同館の関連資料は、ギリシアの修道院・文化センターにおける古典学習の復興がイタリア・ルネサンスを刺激し、
ビザンティン美術の影響がイタリアおよび北方ルネサンスに現れるとも記す（[関連資料](https://www.metmuseum.org/press-releases/dazzling-byzantine-treasures-displayed-at-metropolitan-museum-opening-march-23-2004-exhibitions)）。
ここでの `influenced_by movement/byzantine-art` は、ルネサンスの全作品がビザンティン様式を継承したという
意味ではなく、ギリシア語の学術・古典学習と東方の美術伝統がイタリアへ届いた形成経路に限定する。

## 未着手

- 初期・盛期・北方ルネサンスの分解
- フィレンツェの工房、メディチ家、個別作品の関係化
- マニエリスムおよびバロックへの移行経路の典拠化
