---
id: movement/brancovenesc-art
uri: urn:ahn:movement/brancovenesc-art
type: movement
kind: retrospective
label_ja: ブルンコヴェネスク様式
label_en: Brâncovenesc Art
authority:
  wikidata: Q460596
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1688"
  end: "1714"
  display: "ワラキア公コンスタンティン・ブルンコヴェアヌの治世（1688-1714年）に発達した"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "stil brâncovenesc"
  note: "『ブルンコヴェネスク』は公コンスタンティン・ブルンコヴェアヌの名に由来する呼称だが、
    様式全体を指す名として当事者（建築家・職人）自身が用いた記録は無い。ブルンコヴェアヌ自身は
    建設事業の発注者ではあるが、様式そのものの命名者だという記録には当たっておらず、後代の
    美術史記述による呼称である可能性が高い。person/movement双方ともこのKBに未登録のため
    named_byはnullとした"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/bucharest}
relations:
  - {type: influenced_by, target: movement/byzantine-art, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art"}
  - {type: influenced_by, target: movement/renaissance, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art"}
sources:
  - url: "https://www.wikidata.org/wiki/Q460596"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art"
    kind: reference
    note: "『Brâncovenesc art』の項。ワラキア公コンスタンティン・ブルンコヴェアヌ（在位1688-1714年）
      の治世に発達した様式とし、ビザンティン・オスマン・盛期ルネサンスの融合と記す。代表例として
      UNESCO世界遺産のホレズ修道院、モゴショアイア宮殿、クレツレスク教会（1722年完成）を挙げる"
status: draft
updated: 2026-09-21
---

# ブルンコヴェネスク様式 / Brâncovenesc Art

## 定義と範囲

英語版Wikipedia「[Brâncovenesc art](https://en.wikipedia.org/wiki/Br%C3%A2ncovenesc_art)」は
こう記す（二次情報、原文引用）。

> Brâncovenesc art or Brâncovenesc style ... is an artistic style that evolved during the
> administration of Prince Constantin Brâncoveanu in the late 17th and early 18th centuries.

「ワラキア・ルネサンス」「ルーマニア・ルネサンス」とも呼ばれ、[ビザンティン](byzantine-art.md)・
オスマン・盛期[ルネサンス](renaissance.md)の融合とされる（同項）。建築が中心だが絵画・彫刻にも
表れた。代表例が、ブルンコヴェアヌ自身が墓所として意図したホレズ修道院（UNESCO世界遺産）、
ブカレスト近郊のモゴショアイア宮殿、1722年完成のクレツレスク教会など。これに基づき
`relations`へ`influenced_by`を`movement/byzantine-art`・`movement/renaissance`の双方に張った。
オスマン建築については、この時代・地域に対応する具体的なmovementを本KBで特定できなかった
（[初期オスマン建築](early-ottoman-architecture.md)は14〜15世紀ブルサが対象で、時代が異なる）
ため、影響として明記されているものの`relations`には反映しなかった。

## kind の判定

`retrospective`とした。単一の統治者（ブルンコヴェアヌ公）の治世という明確な期間・発注主体に
紐づく点は他の期間様式（ノヴゴロド派・モスクワ派など）と同型だが、様式の名称自体を公や当事者の
建築家・職人が名乗った記録は見出せず、後代の美術史記述による括りと判断した。

## 時間・空間

`originated_in`はブカレスト（[place/bucharest](../places/bucharest.md)）、ワラキア公国の
宮廷所在地。`time`はブルンコヴェアヌの治世（1688-1714年）とした。

## 未着手

- コンスタンティン・ブルンコヴェアヌを person エンティティとして立てるかどうか
- ホレズ修道院・モゴショアイア宮殿を work エンティティとして立てるかどうか
- 様式名称の最初の使用者・使用年の確認
- ~~文化圏間接続（4経路）: 検索した範囲では、海外美術館収蔵などeurope-east外への文書化された
  接続は見つけられなかった（建築中心の様式であるため、可動作品の海外収蔵自体が想定しにくい）~~
  → 2026-09-21解消。`influenced_by`を`movement/byzantine-art`・`movement/renaissance`
  （いずれもeurope-west/europe-east起源）に張ったことでmovement-relation経路が成立し、
  `config/cross-region-reviews.yaml`の当該エントリは削除した
