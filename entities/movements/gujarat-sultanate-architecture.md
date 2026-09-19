---
id: movement/gujarat-sultanate-architecture
uri: urn:ahn:movement/gujarat-sultanate-architecture
type: movement
kind: period-style
label_ja: グジャラート・スルターン朝建築
label_en: Gujarat Sultanate Architecture
authority:
  wikidata: Q507796
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1407"
  end: "1573"
  display: "グジャラートのムザッファル朝は1407年頃、デリー・スルターン朝の衰退期に成立した。
    1411年、建国者の孫アフマド・シャーがサバルマティー川沿いに新都アフマダーバードを建設した。
    王朝は1573年、ムガル帝国のアクバルによる征服まで独立を保った"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Gujarat Sultanate architecture"
  note: "王朝名『グジャラート・スルターン朝』を冠した後代の美術史記述による様式区分。当事者
    （石工・建築家）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Gujarat_Sultanate", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Gujarat_Sultanate", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Indo-Islamic_architecture", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/ahmedabad}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q507796"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Gujarat_Sultanate"
    kind: reference
    note: "『Gujarat Sultanate』の項。1407年頃の成立、1411年のアフマダーバード建設、
      1573年のムガル帝国による征服までの独立期間を記す"
  - url: "https://en.wikipedia.org/wiki/Indo-Islamic_architecture"
    kind: reference
    note: "『Indo-Islamic architecture』の項。グジャラートの様式が、精緻なミフラーブ・
      ミナレット、ジャーリー（透かし彫りの石格子）、チャットリー（丸屋根の四阿）など、後の
      ムガル建築の要素の多くを先取りしていたと記す"
status: draft
updated: 2026-09-16
---

# グジャラート・スルターン朝建築 / Gujarat Sultanate Architecture

## 定義と範囲

英語版Wikipedia「[Gujarat Sultanate](https://en.wikipedia.org/wiki/Gujarat_Sultanate)」は
こう記す（二次情報、原文引用）。

> Gujarat's Muzaffarid Sultanate emerged around 1407 CE amid Delhi Sultanate's declining power.

建国者の孫アフマド・シャーが1411年、サバルマティー川沿いに新都[アフマダーバード](../places/ahmedabad.md)
を建設した。スルターン朝はアフマダーバードのジャーミー・マスジド、チャンパーネールのジャーマ・
マスジド、シディ・サイイド・モスク、サルケージ・ロザなど多数のモスク・墓廟・城塞を建立した。

『Indo-Islamic architecture』の項はこう記す（二次情報）。

> Indo-Islamic architecture style of Gujarat presages many of the architectural elements later
> found in Mughal architecture, including ornate mihrabs and minarets, jali (perforated screens
> carved in stone), and chattris (pavilions topped with cupolas).

装飾には、それ以前にヒンドゥー寺院（マールー・グルジャラ様式など）で培われた地元の石工の
技術が反映されているとされる。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、グジャラート・スルターン朝という政体の
存続期間（1407-1573年）を通じて、複数世代の石工・建築家がモスク・墓廟を建立し続けた点を、
[ヴィジャヤナガル美術](vijayanagara-art.md)・[マムルーク美術](mamluk-art.md)と同型の
構造と見た。

## 未着手

- アフマド・シャーを person エンティティとして立てるかどうか
- 代表的な建造物（ジャーミー・マスジド、サルケージ・ロザなど）を work エンティティとして
  立てるかどうか
- 文化圏間接続（4経路）: ヴィクトリア＆アルバート博物館がグジャラート産の工芸品（1600年頃の
  螺鈿キャビネット、水差しなど）を所蔵する記録は見つかったが、いずれもスルターン朝独立期
  （〜1573年）ではなくムガル支配下（1573年以降）に制作された可能性が高く、本項の範囲
  （スルターン朝期建築）との対応を確認できなかったため、`relations`への追加は見送った
