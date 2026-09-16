---
id: movement/champa-art
uri: urn:ahn:movement/champa-art
type: movement
kind: period-style
label_ja: チャンパ美術
label_en: Art of Champa
authority:
  wikidata: Q2864642
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "0500"
  end: "1700~"
  display: "起点年には資料間で幅がある。英語版Wikipedia『Art of Champa』は西暦500〜1700年頃と
    し、ギメ美術館の展覧会タイトルは『5〜15世紀』とする。政体としてのチャンパ王国自体の建国は
    西暦192年とされ、美術的な様式の確立とは区別した"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Art of Champa"
  note: "民族・王国名『チャンパ』を冠した後代の美術史記述による括り。当事者（王・職人）自身が
    この名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Art_of_Champa", certainty: scholarly}
  - {field: originated_in, source: "https://whc.unesco.org/en/list/949/", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Art_of_Champa", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/my-son}
relations:
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "https://www.guimet.fr/fr/la-sculpture-du-champa-tresors-dart-du-vietnam-ve-xve-siecles"}
sources:
  - url: "https://www.wikidata.org/wiki/Q2864642"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Art_of_Champa"
    kind: reference
    note: "『Art of Champa』の項。西暦500〜1700年頃の千年間にわたり栄えた文明とし、砂岩彫刻
      （丸彫り・浮彫）と煉瓦造建築を主な遺産とすると記す。ミーソンをバドレーシュヴァラ寺院の
      所在地、北部チャンパの主要な宗教施設と記す"
  - url: "https://whc.unesco.org/en/list/949/"
    kind: institutional
    note: "UNESCO世界遺産センターのミーソン聖域登録ページ（1999年登録）。4〜13世紀にわたり
      インド・ヒンドゥー教に精神的起源を持つ独自の文化がベトナム沿岸部に発達したと記す"
  - url: "https://www.guimet.fr/fr/la-sculpture-du-champa-tresors-dart-du-vietnam-ve-xve-siecles"
    kind: institutional
    note: "パリ・ギメ美術館の展覧会『La sculpture du Champa – Trésors d'art du Vietnam
      Ve-XVe siècles（チャンパの彫刻——ベトナム美術の至宝、5〜15世紀）』のページ。同館が
      世界有数のチャム美術コレクションを持つと記す"
status: draft
updated: 2026-09-16
---

# チャンパ美術 / Art of Champa

## 定義と範囲

英語版Wikipedia「[Art of Champa](https://en.wikipedia.org/wiki/Art_of_Champa)」はこう記す
（二次情報、原文引用）。

> Champa was a Southeast Asian civilization that flourished ... for roughly a one thousand-year
> period between 500 and 1700 AD.

主な遺産は砂岩の彫刻（丸彫り・浮彫）と煉瓦造建築で、一部にブロンズ像・金属工芸品も残る。
北部チャンパの主要な宗教施設が[ミーソン](../places/my-son.md)で、シヴァ神を祀る
バドレーシュヴァラ寺院を中心に、時代ごとに異なる様式を示す複数の建造物群からなる。1999年、
UNESCO世界遺産に登録された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、チャンパという政体・文化圏の存続期間を通じて、
複数世代の王・職人が寺院建築・彫刻を制作し続けた点を、[クメール美術](khmer-art.md)・
[バガン美術](bagan-art.md)と同型の構造と見た。

## パリでの収蔵

パリのギメ美術館は「世界有数のチャム美術コレクション」を持つとされ、展覧会「La sculpture
du Champa – Trésors d'art du Vietnam Ve-XVe siècles」（チャンパの彫刻——ベトナム美術の至宝、
5〜15世紀）を開催した。これに基づき`relations`へ`diffused_to place/paris`を張り、
asia-southeast起源からeurope-westへの接続を記録した。ダナン・チャム彫刻博物館（1910年代、
アンリ・パルマンティエにより創設）が世界最大のチャンパ美術コレクションを持つとされ、その一部が
ギメ美術館・メトロポリタン美術館へ貸し出された記録もある。

## 未着手

- 個々のミーソン建造物・彫刻を work エンティティとして立てるかどうか
- 起点年（政体としての建国192年、美術様式としての確立500年頃）の食い違いの一次資料での整理
- ダナン・チャム彫刻博物館からの貸し出しを通じたニューヨークへの接続を`diffused_to`で
  追加すべきかどうか
