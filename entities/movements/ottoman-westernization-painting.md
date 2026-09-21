---
id: movement/ottoman-westernization-painting
uri: urn:ahn:movement/ottoman-westernization-painting
type: movement
kind: period-style
label_ja: オスマン西欧化絵画
label_en: Ottoman Westernization Painting
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "この様式・時代区分全体を指すWikidata項目は検索で特定できなかった。中心人物
    オスマン・ハムディ・ベイの項目、制度サナーイ・イ・ネフィーセ美術学校の後身ミマール・スィナン
    大学の沿革ページは別途sourcesに記載した"
time:
  start: "1793"
  end: "1914"
  display: "西洋式の絵画授業は1793年、技術目的でムヒエンディスハーネ（陸軍工兵学校）に設けられた
    のが最初とされる。1882年（学校設立は1882年1月1日、開校は1883年3月2日）、オスマン・ハムディ・
    ベイを初代校長にサナーイ・イ・ネフィーセ美術学校が設立され、本格的な西欧式美術教育が始まった。
    1914年、女子校イナス・サナーイ・イ・ネフィーセ美術学校が設立された"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Sanâyi-i Nefîse"
  note: "『オスマン西欧化絵画』は後代の美術史記述による時代区分の呼称。制度名『サナーイ・イ・
    ネフィーセ（美術）』自体は当事者由来だが、様式全体を指す運動名として当事者が用いた記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Turkish_painting", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Turkish_painting", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Turkish_painting", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/istanbul}
relations:
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Keeper_of_the_Mausoleum_(1903)"}
sources:
  - url: "https://en.wikipedia.org/wiki/Turkish_painting"
    kind: reference
    note: "『Turkish painting』の項。西洋的な意味でのトルコ絵画は19世紀半ばから本格的に発達し、
      最初の絵画授業は1793年に陸軍工兵学校で技術目的として設けられたと記す。19世紀の担い手は
      多くがオスマン軍学校出身だったと記す"
  - url: "https://en.wikipedia.org/wiki/Osman_Hamdi_Bey"
    kind: reference
    note: "オスマン・ハムディ・ベイ（1842-1910年）の項。イスタンブール考古学博物館とサナーイ・
      イ・ネフィーセ美術学校（現ミマール・スィナン大学）の創設者であり、ジャン＝レオン・ジェローム
      らに師事したと記す"
  - url: "https://en.wikipedia.org/wiki/Keeper_of_the_Mausoleum_(1903)"
    kind: reference
    note: "オスマン・ハムディ・ベイ作《霊廟の番人》（1903年）が現在パリのオルセー美術館に
      所蔵されると記す"
status: draft
updated: 2026-09-16
---

# オスマン西欧化絵画 / Ottoman Westernization Painting

## 定義と範囲

英語版Wikipedia「[Turkish painting](https://en.wikipedia.org/wiki/Turkish_painting)」は
こう記す（二次情報、原文引用）。

> Turkish painting, in the Western sense, developed actively starting from the mid-19th century.

最初の西洋式絵画授業は1793年、ムヒエンディスハーネ（陸軍工兵学校）に技術目的で設けられたのが
最初とされ、19世紀の担い手の多くはオスマン軍学校出身だった（同項、いわゆる「兵士画家
（asker ressamlar）」）。1882年（開校1883年3月2日）、画家・考古学者[オスマン・ハムディ・ベイ](https://en.wikipedia.org/wiki/Osman_Hamdi_Bey)
（1842-1910年）を初代校長に、絵画・彫刻・建築・版画の4学科を持つサナーイ・イ・ネフィーセ美術学校
（現ミマール・スィナン大学）が設立され、本格的な西欧式美術教育が始まった。ハムディ・ベイ自身は
ジャン＝レオン・ジェロームらフランスのオリエンタリスト画家に師事した。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、オスマン帝国の西欧化改革（タンジマート以降）と
いう時代の枠を通じて、陸軍工兵学校からサナーイ・イ・ネフィーセ美術学校まで複数世代の担い手が
西洋式絵画を学び続けた点を重視した。

## パリでの収蔵

オスマン・ハムディ・ベイの代表作《霊廟の番人》（1903年）は現在、パリのオルセー美術館に所蔵される。
これに基づき`relations`へ`diffused_to place/paris`を張り、mena起源からeurope-westへの接続を
記録した。

## 未着手

- オスマン・ハムディ・ベイを person エンティティとして立てるかどうか
- 《霊廟の番人》を work エンティティとして立てるかどうか
- サナーイ・イ・ネフィーセ美術学校を org エンティティとして立てるかどうか
- 1793年の陸軍工兵学校での絵画授業と、1882年の美術学校設立との間の展開の一次資料での確認
- **未接続の候補**: 英語版Wikipedia「Osman Hamdi Bey」（2026-09-21確認）は、彼がパリで
  ジャン＝レオン・ジェロームとギュスターヴ・ブーランジェに師事し、『フランス・
  オリエンタリスム派』の代表的画家2人から学んだと明記する。ただし『オリエンタリスム』
  （Orientalism）という西洋の運動を指すmovementエンティティが本KBに未整備のため、
  `relations`には反映しなかった。将来Orientalismをmovementとして立てた際に
  `influenced_by`で接続する候補
