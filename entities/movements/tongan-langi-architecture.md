---
id: movement/tongan-langi-architecture
uri: urn:ahn:movement/tongan-langi-architecture
type: movement
kind: period-style
label_ja: トンガのラーンギ王墓建築
label_en: Tongan Langi Royal Tomb Architecture
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "movement単位のWikidata項目は検索で特定できなかった。ラーンギ（王墓）建築
    様式そのものを指す独立した項目は見当たらない"
time:
  start: "15XX"
  end: "17XX"
  display: "ラーンギ（トゥイ・トンガ王家の石造階段状墓所）自体は、13世紀半ばに遡る最古の
    埋葬例が確認されるが、様式が最も洗練された『最も壮大』とされる例——トゥイ・
    ウルアキマタ1世（テレア）による『パエパエ・オ・テレア』——は16世紀の建立とされる。
    この最盛期を起点とした。トゥイ・トンガ王権が実質的な統治権を失ったのは17世紀とされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "langi"
  note: "『ラーンギ』はトンガ語で王家の墓所を指す当事者由来の語だが、これを建築movementと
    して束ねるのは後代の考古学・建築史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Monuments_of_Tonga", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Monuments_of_Tonga", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Monuments_of_Tonga", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/mua}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q2359181"
    kind: authority
    note: "originated_inの対象地（ムア）のWikidata項目"
  - url: "https://en.wikipedia.org/wiki/Monuments_of_Tonga"
    kind: reference
    note: "『Monuments of Tonga』の項。ラパハ（ムア近郊）に22〜28基のラーンギ（王墓）が
      あり、階段状ピラミッド状の土盛りを丁寧に配置した擁壁で支えると記す。最古の埋葬は
      トゥイ・トゥイタトゥイの娘ファタフェヒとされ13世紀半ばに遡ると記す。『最も壮大』
      とされるパエパエ・オ・テレアは、幅8フィートの珊瑚岩板を隙間なく組み合わせたもので、
      16世紀にトゥイ・ウルアキマタ1世（テレア）により建立されたが、王がサモアで没した
      ため空のまま残されたと記す"
  - url: "https://en.wikipedia.org/wiki/Tu%CA%BBi_Tonga_Empire"
    kind: reference
    note: "『Tuʻi Tonga Empire』の項。ムアの王墓写真に『16世紀、ウルアキマタ1世建立』の
      注記があると記す"
status: draft
updated: 2026-09-16
---

# トンガのラーンギ王墓建築 / Tongan Langi Royal Tomb Architecture

## 定義と範囲

英語版Wikipedia「[Monuments of Tonga](https://en.wikipedia.org/wiki/Monuments_of_Tonga)」
（参考資料）はこう記す（二次情報）。[ムア](../places/mua.md)近郊のラパハには22〜28基の
ラーンギ（トゥイ・トンガ王家の石造階段状墓所）があり、階段状ピラミッド状の土盛りを
丁寧に配置した擁壁で支える。最古の埋葬例はトゥイ・トゥイタトゥイの娘ファタフェヒとされ、
13世紀半ばに遡る。様式が最も洗練された「最も壮大」とされる例は、幅8フィートの珊瑚岩板を
隙間なく組み合わせたパエパエ・オ・テレアで、16世紀にトゥイ・ウルアキマタ1世（テレア）に
より建立されたが、王がサモアで没したため空のまま残された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、トゥイ・トンガ王朝という政体の存続期間を
通じて、複数世代の石工が階段状石造墓所という同じ建築様式を発展させ続けた点を、
[ナンマドール建築](nan-madol-architecture.md)・[ラッテ・ストーン建築](latte-stone-architecture.md)
と同型の構造と見た。

## 時間の判定

ラーンギ自体の起源は13世紀半ばに遡るが、本項では様式的に最も洗練され「最も壮大」と
明示的に評されるパエパエ・オ・テレア（16世紀）を起点として採用した。より古い13世紀の
埋葬例が存在することは`time.display`に残した。

## 空間的接続の判定

検索した範囲では、ラーンギ建築様式や関連する副葬品がトンガ域外の博物館等へ拡散した
文書化された記録を見つけられなかった（石造の墓所建築という性質上、可搬性の高い作例が
乏しいことも一因と考えられる）。よって`relations`に`diffused_to`は張らず、
`config/cross-region-reviews.yaml`に「文化圏をまたぐ接続の記録なし」として記録した。

## 未着手

- トゥイ・トゥイタトゥイ、トゥイ・ウルアキマタ1世（テレア）を person エンティティとして
  立てるかどうか
- パエパエ・オ・テレア、ハアモンガ・ア・マウイ（三石塔）を work/place エンティティと
  して個別に立てるかどうか
- 13世紀半ばの最古の埋葬例（ファタフェヒ）の一次資料での確認
