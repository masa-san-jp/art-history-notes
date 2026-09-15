---
id: movement/suzani
uri: urn:ahn:movement/suzani
type: movement
kind: retrospective
label_ja: スザニ
label_en: Suzani
authority:
  wikidata: Q1432446
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "178X"
  end: ".."
  display: "刺繍の技法自体はより古い時代に遡るとされ、15世紀にはカスティーリャの使節ルイ・
    ゴンサレス・デ・クラビホがティムール朝の宮廷でこれに先行する刺繍を記録している。ただし
    現存する作例は繊細さゆえに極めて少なく、確認できる最古のものは18世紀末〜19世紀初頭。
    今日も刺繍として継続する（アメリカでも収集・展示の対象になっている）"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "سوزن (suzan)"
  note: "『スザニ』はペルシア語で『針』を意味する語に由来し、当事者（中央アジアの女性刺繍職人）が
    自らの制作物を指して用いる語である"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Suzani_(textile)", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Suzani_(textile)", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Suzani_(textile)", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/bukhara}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/698681"}
sources:
  - url: "https://www.wikidata.org/wiki/Q1432446"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Suzani_(textile)"
    kind: reference
    note: "『Suzani (textile)』の項。タジキスタン・ウズベキスタン・アフガニスタンなど中央アジアで
      作られる刺繍textileとし、現存最古の作例が18世紀末〜19世紀初頭に限られると記す。ブハラ・
      サマルカンド・タシケントなど複数の地域様式があると記す"
  - url: "https://www.metmuseum.org/art/collection/search/698681"
    kind: institutional
    note: "メトロポリタン美術館収蔵のスザニ。同館は花嫁の持参品としての位置づけ、専門の下絵師
      （kalamkesh）が図案を描き、花嫁の女性親族が刺繍する分業制作の過程を記す。同館のブハラ・
      ウズベキスタン産スザニのコレクションは16〜20世紀に及ぶと記す"
status: draft
updated: 2026-09-16
---

# スザニ / Suzani

## 定義と範囲

英語版Wikipedia「[Suzani (textile)](https://en.wikipedia.org/wiki/Suzani_(textile))」は
こう記す（二次情報、原文引用）。

> Suzani is a type of embroidered and decorative tribal textile made in Tajikistan, Uzbekistan,
> Afghanistan and other Central Asian countries.

『スザニ』はペルシア語で「針」を意味する語に由来する。花嫁の持参品として重要な役割を持ち、
専門の下絵師（kalamkesh）が綿布数枚に図案を描き、花嫁の女性親族がそれぞれ刺繍した後に縫い合わせる
という分業で作られた（メトロポリタン美術館、機関資料）。

刺繍の伝統自体は古く、15世紀にカスティーリャの使節ルイ・ゴンサレス・デ・クラビホがティムール朝の
宮廷でこれに先行する刺繍を記録しているが、現存する作例は繊細さゆえに極めて少なく、確認できる
最古のものは18世紀末〜19世紀初頭に限られる（同項）。ブハラ（[place/bukhara](../places/bukhara.md)）・
ホジェンド・ヌラタ・サマルカンド・シャフリサブス・タシケントなど地域ごとに様式が異なるとされる。

## kind の判定

`retrospective`とした。「スザニ」という語自体は当事者由来（`self_identified: true`）だが、
これを一つの美術movementとして束ねたのは後代の美術史・工芸史記述である。地域ごとに様式は
異なるが単一の系譜・工房ではなく、複数の地域・複数世代の女性刺繍職人による分業的な制作様式を
束ねた括りである。

## ニューヨークでの収蔵

メトロポリタン美術館は16〜20世紀にわたるブハラ・ウズベキスタン産スザニのコレクションを持つ。
これに基づき`relations`へ`diffused_to place/new-york-city`を張り、asia-central起源から
americas-northへの接続を記録した。

## 未着手

- 地域ごとの様式差（ブハラ・サマルカンド・タシケントなど）を個別のmovementとして分けるべきか
  どうか
- ルーヴル美術館・大英博物館所蔵作例の一次資料での確認
- 15世紀のクラビホの記録と18世紀末以降の現存作例との間の空白期間の一次資料での確認
