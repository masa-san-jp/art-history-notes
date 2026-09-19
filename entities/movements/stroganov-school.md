---
id: movement/stroganov-school
uri: urn:ahn:movement/stroganov-school
type: movement
kind: period-style
label_ja: ストロガノフ派
label_en: Stroganov School
authority:
  wikidata: Q1968335
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "159X"
  end: "16XX"
  display: "16世紀末にモスクワで現れ、17世紀を通じて富豪ストロガノフ家の庇護のもとで最盛期を
    迎えたとされる。ロシア美術の西欧化が進んだ17世紀末が終期の目安となる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Строгановская школа"
  note: "『ストロガノフ派』という呼称は、イコン裏面にストロガノフ家への言及が頻出することに
    由来する後代の慣用名。英語版Wikipediaは、プロコピー・チーリンら名の挙がる画家の多くは実際には
    ストロガノフ家お抱えではなく、モスクワを拠点にツァーリの発注をこなした画家だったと明記する
    ——名称と実態にずれがあることを示す"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Stroganov_School", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Stroganov_School", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Stroganov_School", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/moscow}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q1968335"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Stroganov_School"
    kind: reference
    note: "『Stroganov school』の項。16世紀末〜17世紀、富豪ストロガノフ家の庇護のもとで栄えた
      ロシア最後の主要なイコン画派とし、小型で緻密な技法・金箔の多用を特徴とすると記す。プロコピー・
      チーリンらの多くは実際にはモスクワ拠点でツァーリの発注をこなした画家だったと明記する"
status: draft
updated: 2026-09-16
---

# ストロガノフ派 / Stroganov School

## 定義と範囲

英語版Wikipedia「[Stroganov school](https://en.wikipedia.org/wiki/Stroganov_School)」はこう記す
（二次情報、原文引用）。

> The Stroganov school is a conventional name for the last major Russian icon-painting school,
> which thrived under the patronage of the rich Stroganov family of merchants in the late 16th
> and 17th centuries.

小型で緻密な技法、豊かな装飾と色彩、金箔・銀箔の多用を特徴とする。代表的な画家がプロコピー・
チーリン（?-1627年頃）だが、同項はこう補足する（原文引用）。

> Most of these icon painters, however, did not belong to the Stroganov school. They were icon
> painters from Moscow and executed commissions by the tsar.

つまり「ストロガノフ派」という名称は、イコン裏面の銘文にストロガノフ家への言及が頻出することに
由来する後代の慣用であり、画家たち自身がモスクワを拠点にツァーリの発注をこなしていた実態とは
ずれがある。

## kind の判定

`period-style` とした。単一の血縁・工房ではなく、ストロガノフ家の富裕な庇護と、モスクワの
ツァーリ工房の技量が交差する16世紀末〜17世紀という時代の枠を通じて、複数の画家が様式を
共有し続けた点を、[モスクワ派](moscow-school-icon-painting.md)の後継として位置づけた。

## 時間・空間

`originated_in`はモスクワ（[place/moscow](../places/moscow.md)）。ストロガノフ家自体の
本拠地はソリヴィチェゴツクだが、名前の由来となった画家たちの実際の活動拠点はモスクワだった
という英語版Wikipediaの指摘に従った。**未確認**: ソリヴィチェゴツク自体での制作活動の実態。

## 未着手

- プロコピー・チーリン、イストマ・サーヴィンらを person エンティティとして立てるかどうか
- ソリヴィチェゴツクをplace化し、庇護者ストロガノフ家の拠点として区別すべきかどうか
- 文化圏間接続（4経路）: 検索した範囲では、海外美術館収蔵などeurope-east外への文書化された
  接続は見つけられなかった
