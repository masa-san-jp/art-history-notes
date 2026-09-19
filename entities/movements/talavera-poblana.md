---
id: movement/talavera-poblana
uri: urn:ahn:movement/talavera-poblana
type: movement
kind: period-style
label_ja: タラベラ・ポブラーナ
label_en: Talavera Poblana
authority:
  wikidata: Q7678980
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1653"
  end: "1750~"
  display: "1550〜70年代、スペイン・タラベラ・デ・ラ・レイナ出身の職人がプエブラへスズ釉技法を
    伝え、現地の意匠と融合したとされる（起源）。ギルドとしての制度化は1652年にプエブラの陶工が
    副王へ規約制定を求め、1653年に最初の規約（Ordenanzas）が発布されたことで確立した。1650〜
    1750年が『黄金時代』とされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Talavera poblana"
  note: "スペインの陶器産地タラベラ・デ・ラ・レイナの名を冠した呼称で、プエブラの陶工が当事者と
      してこの名を制度名（ギルド規約上の呼称）として用いた記録がある一方、様式全体としての
      『タラベラ・ポブラーナ』という括りが後代の美術史・工芸史記述でどこまで確立したかは
      本調査では厳密に区別できていない"
claims:
  - {field: time, source: "https://smarthistory.org/talavera-poblana/", certainty: scholarly}
  - {field: originated_in, source: "https://smarthistory.org/talavera-poblana/", certainty: scholarly}
  - {field: kind, source: "https://smarthistory.org/talavera-poblana/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/puebla}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/essays/talavera-de-puebla"}
sources:
  - url: "https://www.wikidata.org/wiki/Q7678980"
    kind: authority
  - url: "https://smarthistory.org/talavera-poblana/"
    kind: scholarly
    note: "『Talavera poblana』の項。1550-70年代のスペイン職人伝来、1652-53年のギルド規約制定、
      1650-1750年の黄金時代を記す"
  - url: "https://www.metmuseum.org/essays/talavera-de-puebla"
    kind: institutional
    note: "メトロポリタン美術館Heilbrunn Timelineの『Talavera de Puebla』essay。17世紀初頭以降
      プエブラがメキシコの陶器生産の中心地となり、マニラ・ガレオン船で運ばれた中国磁器の影響を
      受けた青白の意匠が特徴と記す。同館所蔵の『Master Potter A』作の水盤（c.1650年）を挙げる"
status: draft
updated: 2026-09-16
---

# タラベラ・ポブラーナ / Talavera Poblana

## 定義と範囲

Smarthistoryの記事「[Talavera poblana](https://smarthistory.org/talavera-poblana/)」（学術資料）
によれば、1550〜70年代、スペインのタラベラ・デ・ラ・レイナ出身の陶工がプエブラへ渡り、ろくろと
スズ釉技法を伝え、現地の意匠と融合したことでタラベラ・ポブラーナが生まれたとされる。1580年までに
プエブラはメキシコにおけるタラベラ生産の中心地となった。

メトロポリタン美術館Heilbrunn Timelineの essay「[Talavera de Puebla](https://www.metmuseum.org/essays/talavera-de-puebla)」
（機関資料）は、プエブラの特徴的な青白の意匠が、マニラ・ガレオン船によって運ばれた中国磁器の
影響を受けたと記す。

## kind の判定

`period-style` とした。単一の血縁・工房ではなく、プエブラの陶工ギルドという制度・時代の枠を
通じて、複数世代の陶工が制作し続けた点を、[サンテロ](santero.md)・[ンドプ](ndop.md)と同型の
構造と見た。1652年、プエブラの陶工らはディエゴ・サルバドール・カレートを通じて副王に規約制定を
求め、1653年に最初の規約（Ordenanzas）が発布された。ギルドは製品を黄色い日用陶器（loza amarilla）・
並級品（loza común）・上級品（loza fina）・後の高級品（loza refina）に分類した（Smarthistory、
学術資料）。1650〜1750年が「黄金時代」とされ、プエブラは新大陸で最も重要な陶器生産地となった。

## ニューヨークでの収蔵

メトロポリタン美術館は『Master Potter A』作の水盤（c.1650年、直径52.7cm）を所蔵する。これに基づき
`relations`へ`diffused_to place/new-york-city`を張り、americas-latin起源からamericas-northへの
接続を記録した。

## 未着手

- ディエゴ・サルバドール・カレートを person エンティティとして立てるかどうか
- 1653年の最初の規約（Ordenanzas）の一次資料での確認
- 中国磁器からの様式的影響を`relations`の`influenced_by`で明示するかどうか（対応する
  中国磁器のmovementエンティティが本KBに未整備のため今回は本文の記述にとどめた）
