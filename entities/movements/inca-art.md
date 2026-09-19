---
id: movement/inca-art
uri: urn:ahn:movement/inca-art
type: movement
kind: period-style
label_ja: インカ美術
label_en: Inca Art
authority:
  wikidata: Q28573
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1425~"
  end: "1532"
  display: "インカ帝国の存続期間（c.1425-1532年）を範囲とした。皇帝パチャクティの治世
    （15世紀）に太陽信仰と帝国が拡大したとされ、1532年のスペインによる征服開始を終期とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Inca art"
  note: "『インカ』は帝国の統治者を指す当事者由来の語（ケチュア語でIncaは皇帝の称号）だが、
    美術movementとしての『インカ美術』という括りは後代の美術史記述による"
claims:
  - {field: time, source: "https://www.worldhistory.org/Inca_Art/", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/essays/ancient-andean-metalworking", certainty: scholarly}
  - {field: kind, source: "https://www.worldhistory.org/Inca_Art/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/cusco}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/751901"}
sources:
  - url: "https://www.wikidata.org/wiki/Q28573"
    kind: authority
  - url: "https://www.worldhistory.org/Inca_Art/"
    kind: reference
    note: "『Inca Art』の項。インカ文明の美術（c.1425-1532年）を、精緻な金属細工・陶器・
      とりわけ織物（インカ自身が最も権威ある芸術形式と見なした）に見出せると記す。皇帝
      パチャクティの治世に帝国が拡大したと記す"
  - url: "https://www.metmuseum.org/essays/ancient-andean-metalworking"
    kind: institutional
    note: "メトロポリタン美術館essay『Ancient Andean Metalworking』。インカが帝国各地から
      金属職人を都クスコに集め、金・銀・銅・青銅の器物を作らせたと記す"
  - url: "https://www.metmuseum.org/art/collection/search/751901"
    kind: institutional
    note: "メトロポリタン美術館収蔵《チュニカ》（インカ）。同館はインカ関連の織物908点を
      所蔵する（2026-09-16時点の検索結果）"
status: draft
updated: 2026-09-16
---

# インカ美術 / Inca Art

## 定義と範囲

World History Encyclopediaの記事「[Inca Art](https://www.worldhistory.org/Inca_Art/)」
（学術資料）はこう記す（二次情報）。インカ文明の美術（c.1425-1532年）は、古代アメリカ大陸で
作られた最も優れた作品群の一つとされる。皇帝パチャクティ・クシ・ユパンキの治世に、インカは
現エクアドル・ペルー・ボリビア西部と中南部・アルゼンチン北西部・チリ北部と中北部・コロンビア
南部に及ぶ領域まで版図を拡大した。インカ美術は、精緻な金属細工・陶器、とりわけ織物（インカ
自身が最も権威ある芸術形式と見なした）に最もよく表れる。金属細工は、1470年頃に征服・吸収した
チムー文化の冶金伝統に強く影響を受け、蝶・ジャガー・リャマなどの動物文様を刻んだ金・銀の
装飾品が皇帝・エリート層のために作られた。石造建築では、ナイフの刃も入らないほど精密に石を
組み合わせる無目地の乾式石積み技法（クスコを中心とする）が用いられた。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、インカ帝国（タワンティンスウユ）という
政体の存続期間を通じて、帝国各地から集められた複数世代の織工・金属職人・石工が制作し続けた
点を、[チョーラ朝ブロンズ](chola-bronzes.md)・[クメール美術](khmer-art.md)と同型の構造と
見た。

## ニューヨークでの収蔵

メトロポリタン美術館は、インカ関連の織物908点（チュニカ、投票用チェッカーボード柄チュニカ、
星と鳥のタペストリーパネルなど）を含む豊富なコレクションを持つ。これに基づき`relations`へ
`diffused_to place/new-york-city`を張り、americas-latin起源からamericas-northへの接続を
記録した。

## 未着手

- 皇帝パチャクティを person エンティティとして立てるかどうか
- 代表的な織物・金属工芸品を work エンティティとして立てるかどうか
- チムー文化からの影響を`relations`の`influenced_by`で明示するかどうか（対応する
  movementエンティティが本KBに未整備のため今回は本文の記述にとどめた）
