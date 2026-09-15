---
id: movement/ndop
uri: urn:ahn:movement/ndop
type: movement
kind: period-style
label_ja: ンドプ
label_en: Ndop
authority:
  wikidata: Q17144276
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "178X"
  end: "19XX"
  display: "英語版Wikipediaは伝統の始まりを『18世紀後半』とする。ただし個々のンドプ像は、より
    早い時代（例えば1650年頃・1710年頃・1740年頃在位の王）を遡って表すものもあり、像の制作年代と
    表される王の在位年代は区別される。19世紀まで王の即位儀礼に伴い制作が続いたとされる"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "ndop"
  note: "『ンドプ』はクバ王国の言語で当事者が用いる語であり、後代の外部研究者による命名ではない"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Ndop_(Kuba)", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Ndop_(Kuba)", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Ndop_(Kuba)", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/mushenge}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Ndop_(Kuba)"}
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Ndop_(Kuba)"}
sources:
  - url: "https://www.wikidata.org/wiki/Q17144276"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Ndop_(Kuba)"
    kind: reference
    note: "『Ndop (Kuba)』の項。18世紀後半に伝統が始まったとし、王（nyim）が即位儀礼を終えた後に
      制作を発注したと記す。ハンガリー人探検家エミール・トルデーが1907年に大英博物館の資金による
      探検で収集した4体、ベルギーの大臣ジュール・レンキンが1909年に収集した1体（現ブルックリン
      美術館）を記す。ミシェ・ミシャーング・マムブル王（1710年頃在位）のンドプ（1760-1780年制作、
      ブルックリン美術館）を代表例とする"
  - url: "https://www.brooklynmuseum.org/objects/4791"
    kind: institutional
    note: "ブルックリン美術館の作品ページ。所蔵するンドプ像が表す可能性のある王（在位c.1650・
      c.1710・c.1740年）を記す"
status: draft
updated: 2026-09-16
---

# ンドプ / Ndop

## 定義と範囲

英語版Wikipedia「[Ndop (Kuba)](https://en.wikipedia.org/wiki/Ndop_(Kuba))」はこう記す
（二次情報、原文引用）。

> Figurative sculptures representing different kings (nyim) of the Kuba kingdom.

ンドプは特定の王の顔立ちを写実的に再現したものではなく、理想化された特徴と王の霊性を体現する
彫像とされる。クバ王国（現コンゴ民主共和国、[ムシェンゲ](../places/mushenge.md)を旧都とする）の
王（ニイム）が、即位儀礼を終えた後に制作を発注したと記す。

## kind の判定

`period-style` とした。単一の彫刻家系の血縁継承ではなく、クバ王国という政体の存続期間を通じて、
代々の王が即位のたびに個別に発注し、無名の彫刻家たちが制作を担い続けた点を、
[ノヴゴロド派](novgorod-school-icon-painting.md)や[サンテロ](santero.md)と同型の構造と見た。

## 時間

伝統そのものの始まりは18世紀後半とされる。ただし個々の像が表す王の在位年代（例えば
ミシェ・ミシャーング・マムブル王は1710年頃在位）は、像自体の制作年代（同王のンドプは
1760-1780年制作、ブルックリン美術館蔵）より早いことが多く、両者は区別される。

## ロンドン・ニューヨークでの収蔵

ハンガリー人探検家エミール・トルデーが1907年、大英博物館の資金による探検でンドプ4体を収集し、
現在大英博物館が所蔵する。ベルギーの大臣ジュール・レンキンが1909年に収集した1体は、現在
ブルックリン美術館（ニューヨーク）が所蔵する。これに基づき`relations`へ`diffused_to`を
`place/london`・`place/new-york-city`の双方に張り、africa-sub起源からeurope-west・
americas-northへの接続を記録した。

## 未着手

- ミシェ・ミシャーング・マムブル王ら個々の王、彫刻家（無名）を person エンティティとして
  立てるかどうか
- 個々のンドプ像を work エンティティとして立てるかどうか
- ベルギー王立中央アフリカ博物館所蔵の2体の一次資料での確認
