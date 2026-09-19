---
id: movement/kongo-christian-art
uri: urn:ahn:movement/kongo-christian-art
type: movement
kind: period-style
label_ja: コンゴ・キリスト教美術
label_en: Kongo Christian Art
authority:
  wikidata: Q796583
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1509"
  end: "17XX"
  display: "ポルトガル人が1483年にコンゴ川河口に到達し、王ジョアン1世の子アフォンソ・
    ムヴェンバ・ア・ンジンガ（在位1509-1543年）の治世にキリスト教が国教として確立した。
    16〜17世紀を範囲とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Kongo Christian art"
  note: "『コンゴ・キリスト教美術』は後代の美術史記述による様式区分。当事者（王・鋳物師）
    自身がこの名で自らの様式を運動として名乗った記録は無い。authority.wikidataには様式
    そのものではなくコンゴ王国自体の項目（Q796583）を代わりに登録した——様式単独の項目は
    検索で特定できなかった"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Afonso_I_of_Kongo", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/toah/ht/08/afc.html", certainty: scholarly}
  - {field: kind, source: "https://smarthistory.org/crucifix/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/mbanza-kongo}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/318329"}
sources:
  - url: "https://www.wikidata.org/wiki/Q796583"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Afonso_I_of_Kongo"
    kind: reference
    note: "アフォンソ1世（在位1509-1543年）の項。キリスト教を伝統的な信仰と結びつけ
      『アフリカ化』したと記す"
  - url: "https://www.metmuseum.org/toah/ht/08/afc.html"
    kind: institutional
    note: "メトロポリタン美術館Heilbrunn Timelineの『Central Africa, 1400-1600 A.D.』
      chronology。ポルトガル人が1483年にコンゴ川河口に到達し、コンゴ王がキリスト教を
      急速に受容したと記す"
  - url: "https://smarthistory.org/crucifix/"
    kind: scholarly
    note: "『Crucifix (Kongo peoples)』の項。コンゴ王が権威の象徴として現地製の真鍮製
      十字架像を発注し、ヨーロッパのキリスト教図像とコンゴ独自の美意識を融合させたと記す。
      十字架は信仰の印であると同時に、伝統的なコンゴの宗教的物品と同様、護符・治療具として
      も機能したと記す"
  - url: "https://www.metmuseum.org/art/collection/search/318329"
    kind: institutional
    note: "メトロポリタン美術館収蔵《十字架像》（コンゴ人、コンゴ王国）"
status: draft
updated: 2026-09-16
---

# コンゴ・キリスト教美術 / Kongo Christian Art

## 定義と範囲

Smarthistoryの記事「[Crucifix (Kongo peoples)](https://smarthistory.org/crucifix/)」
（学術資料）はこう記す（二次情報）。ポルトガル人が1483年にコンゴ川河口に到達した後、
コンゴの支配者たちは急速にキリスト教を受容した。王[ンバンザ・コンゴ](../places/mbanza-kongo.md)
を都とするアフォンソ1世（アフォンソ・ムヴェンバ・ア・ンジンガ、在位1509-1543年）の治世に
キリスト教が国教として確立し、コンゴの王室美術家たちは新しい信仰の図像体系の中で、ヨーロッパの
図像的原型と現地の美意識を融合させた真鍮製十字架像を制作した。十字架は指導力・権威の象徴として
発注され、ヨーロッパと同様に信仰の証・祭壇や墓の装飾として用いられたが、同時に伝統的なコンゴの
宗教的物品と同様、護符・治療の道具としても機能した。アフォンソ1世はキリスト教を伝統的な信仰と
結びつけることで「アフリカ化」したとされる。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、コンゴ王国という政体・王室美術の枠組みを
通じて、複数世代の鋳物師が十字架像・関連の宗教美術を制作し続けた点を、
[アラウィー朝帝都建築](alaouite-imperial-architecture.md)・[ンドプ](ndop.md)と同型の
構造と見た。

## ニューヨークでの収蔵

メトロポリタン美術館は複数のコンゴ製十字架像を所蔵し、2015年には展覧会「Kongo: Power and
Majesty」を開催した。これに基づき`relations`へ`diffused_to place/new-york-city`を張り、
africa-sub起源からamericas-northへの接続を記録した。

## 未着手

- アフォンソ1世を person エンティティとして立てるかどうか
- 個々の十字架像を work エンティティとして立てるかどうか
- 大英博物館所蔵の関連作例の一次資料での確認
