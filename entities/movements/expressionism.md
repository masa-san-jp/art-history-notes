---
id: movement/expressionism
uri: urn:ahn:movement/expressionism
type: movement
kind: retrospective
label_ja: 表現主義
label_en: Expressionism
authority:
  wikidata: Q80113
  aat: "300021502"
  ndl: "00576716"
  jpsearch: null
  none_reason: null
time:
  start: "190X"
  end: "193X"
  display: "1900年代〜1930年代。ドイツの初期集団を中心に、国際的な展開と後続形態を含む"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Expressionism"
  note: "内面、感情、精神状態を外界の自然主義的再現より強く前面化する実践を、絵画・版画・彫刻・建築・映画などにまたがって後世にまとめた名称。ドイツ表現主義だけに限定しない"
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q80113", certainty: scholarly}
  - {field: originated_in, source: "https://www.moma.org/collection/terms/expressionism", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q80113", certainty: scholarly}
space:
  - {role: originated_in, target: place/dresden}
relations:
  - {type: influenced_by, target: movement/symbolism, certainty: scholarly, source: "https://www.moma.org/documents/moma_catalogue_1702_300298262.pdf"}
sources:
  - url: "https://www.wikidata.org/wiki/Q80113"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021502"
    kind: authority
  - url: "https://www.moma.org/collection/terms/expressionism"
    kind: institutional
  - url: "https://www.moma.org/documents/moma_catalogue_1702_300298262.pdf"
    kind: scholarly
status: draft
updated: 2026-08-12
---

# 表現主義 / Expressionism

1900年代から1930年代にかけてドイツを主要な初期拠点とし、内面の緊張、感情、精神状態を歪んだ形態、
強い色彩、荒い筆触、版画的な輪郭で表現した近代芸術の運動。絵画だけでなく、版画、彫刻、建築、演劇、
映画、文学にも展開し、第一次世界大戦前後の複数の集団と媒体を横断する。

## kind の判定

`retrospective` とした。Die Brücke や Der Blaue Reiter など自律した集団は存在したが、Expressionism
全体はそれらと後続の国際的実践をまとめる広い歴史分類であり、一つの自称組織ではない。

## 空間と時間

Die Brücke が1905年に結成されたドレスデンを初期形成地の代表ノードとする。ベルリン、ミュンヘン、ウィーン、
パリなどへの移動と受容は別の `active_in`／`diffused_to` 関係として追加する。

## 象徴主義からの形成的な接続

ニューヨーク近代美術館の象徴主義展カタログは、象徴主義・アール・ヌーヴォー・ユーゲントシュティールが
20世紀の表現主義を含む運動の基盤を提供し、象徴主義による色彩の表現的な探究が表現主義への道を開いたと
整理している。ここでの `influenced_by` は、ドイツ表現主義の形成期における色彩・内面表現・象徴的主題の
継承を示すもので、後続の国際的な表現主義すべてを単一の系譜に還元するものではない。

## 未着手

- Die Brücke、Der Blaue Reiter、カンディンスキー、キルヒナー、ノルデの分解
- 表現主義建築・映画・文学と、ナチ期の弾圧・亡命による移動
