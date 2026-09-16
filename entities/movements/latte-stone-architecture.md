---
id: movement/latte-stone-architecture
uri: urn:ahn:movement/latte-stone-architecture
type: movement
kind: retrospective
label_ja: ラッテ・ストーン建築
label_en: Latte Stone Architecture
authority:
  wikidata: Q4211672
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "09XX"
  end: "17XX"
  display: "英語版Wikipedia『Latte stone』は、紀元900年頃に使用が始まり、1521年の
    フェルディナンド・マゼラン来航後も続いたが、スペインによる植民地化を経て1700年頃
    までに完全に廃れたと記す"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "latte stone"
  note: "『ラッテ』（latte）自体はチャモロ語由来とされる語だが、これを建築movementとして
    括るのは後代の考古学・建築史記述による。当事者自身がこの語を運動名として綱領的に
    用いた記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Latte_stone", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Latte_stone", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q4211672", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/guam}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q4211672"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Latte_stone"
    kind: reference
    note: "『Latte stone』の項。半球形の笠石を頂く柱状の石造構造物で、初期のチャモロ人が
      建物の土台として用い始めたのは紀元900年頃とし、1521年のマゼラン来航後も一般的に
      使われ続けたが、スペインによる植民地化を経て1700年頃までに完全に廃れたと記す。
      現在ではグアム・北マリアナ諸島の米国硬貨、道路標識などにチャモロ人アイデンティティ
      の象徴として用いられると記す"
status: draft
updated: 2026-09-16
---

# ラッテ・ストーン建築 / Latte Stone Architecture

## 定義と範囲

英語版Wikipedia「[Latte stone](https://en.wikipedia.org/wiki/Latte_stone)」（参考資料）は
こう記す（二次情報）。ラッテ・ストーンは、半球形の笠石（タサ）を頂く柱状の石材（ハリギ）
からなる構造物で、初期のチャモロ人が[グアム](../places/guam.md)を含むマリアナ諸島各地で
建物の土台として用いた。使用開始は紀元900年頃とされ、1521年のフェルディナンド・
マゼラン来航後もしばらく続いたが、スペインによる植民地化を経て1700年頃までに完全に
廃れた。現代では、グアム・北マリアナ諸島の米国硬貨や道路標識などに、チャモロ人
アイデンティティの象徴として用いられている。

## kind の判定

`retrospective`とした。『ラッテ』自体はチャモロ語由来とされる語だが、これを800年近くに
わたる建築慣行の集合として一つのmovementに括るのは、後代の考古学・建築史記述による
整理である。単一の血縁・工房ではなく、複数世代のチャモロの共同体がマリアナ諸島各地で
同じ建築技法を共有し続けた点を、[モアイ](moai.md)・[ラーイ・ストーン](rai-stones.md)と
同型の構造と見た。

## 空間的接続の判定

検索した範囲では、ラッテ・ストーンそのもの、あるいは関連するチャモロの工芸品が
マリアナ諸島外の博物館へ収蔵された記録を見つけられなかった（石造構造物という性質上、
可搬性の高い作例が乏しいことも一因と考えられる）。よって`relations`に`diffused_to`は
張らず、`config/cross-region-reviews.yaml`に「文化圏をまたぐ接続の記録なし」として
記録した。

## 未着手

- 個々のラッテ・ストーン遺跡（例：タロフォフォ、リティディアン岬）を place エンティティ
  として立てるかどうか
- チャモロの織物・カヌー・土器など、他の物質文化についての海外収蔵記録の調査
- 紀元900年という起点年代の考古学論文（放射性炭素年代測定）での確認
