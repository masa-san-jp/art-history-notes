---
id: movement/rinpa
uri: urn:ahn:movement/rinpa
type: movement
kind: retrospective
label_ja: 琳派
label_en: Rimpa school
authority:
  wikidata: Q3179819
  aat: "300106734"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1600~"
  end: "18XX"
  display: 17世紀初頭〜19世紀（Wikidata の inception は1600年。終期は未確認）
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: 琳派
  note: 尾形光琳の一字から作られた呼称で、当事者が名乗った名ではない。光琳派・宗達光琳派とも呼ばれる（Wikidata Q3179819 の日本語記述）。Getty AAT の見出し語は Sōtatsu-Kōrin School（300106734）。「琳派」という語がいつ誰によって定着したかは未確認
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q3179819", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q3179819", certainty: hypothesis}
space:
  - {role: originated_in, target: place/kyoto}
relations: []
sources:
  - https://www.wikidata.org/wiki/Q3179819
  - https://www.getty.edu/research/tools/vocabularies/aat/
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/DT231.jpg
    source_page: https://www.metmuseum.org/art/collection/search/39664
    license: cc0
    note: "尾形光琳《八橋図》（Irises at Yatsuhashi）、江戸時代18世紀。メトロポリタン美術館蔵（isPublicDomain: true）"
  - url: https://www.artic.edu/iiif/2/13c3192f-2844-7eb9-4db5-3cd7ce4eb66a/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/35620
    license: cc0
    note: "俵屋宗達《牡丹・木蓮・蒲公英図》（Peonies, Magnolia, and Dandelions）。シカゴ美術館蔵（is_public_domain: true）"
status: draft
updated: 2026-08-08
---

# 琳派 / Rimpa school

## 定義と範囲

本阿弥光悦と俵屋宗達に始まり、尾形光琳が発展させ、酒井抱一らが江戸に定着させた系統
（[Wikidata Q3179819](https://www.wikidata.org/wiki/Q3179819) の日本語記述。**二次情報**）。

典拠: Wikidata `Q3179819`（instance of は `school of painting` のみ）／Getty AAT `300106734`

## kind の判定 — なぜ `lineage-school` ではなく `retrospective` か

狩野派と並べると同じ「派」に見えるが、成り立ちが違う。

| | 狩野派 | 琳派 |
|---|---|---|
| 継承の形 | 血縁・養子・工房の徒弟制 | **私淑**（世代を跨いで慕い、様式を受け継ぐ） |
| 制度としての実体 | ある（奥絵師として幕府に仕える組織） | 無い |
| 世代の連続 | 途切れない | **宗達と光琳の間に約100年の隔たり** |
| Wikidata の分類 | `family` + `art movement` + `school of painting` | `school of painting` のみ |

継承が制度ではなく私淑である以上、**当事者たちが1つの集団として存在したわけではない**。
「琳派」という括りは後から外側で作られたものなので `retrospective` とした。
呼称そのものも尾形光琳の一字から作られた後代の語で、当事者が名乗った名ではない。

**Getty AAT の見出し語が「Sōtatsu-Kōrin School」であること自体が、命名の歴史的バイアスの実例。**
誰を中心に置くかで名前が変わる（宗達光琳派／光琳派／琳派）。だから `naming.original_label` に原語を
保存し、見出し語には従属しない。

**未確認**: 「琳派」という語の定着時期と命名者。近代の美術史記述の中で成立したと考えられるが、
一次資料に当たっていない。当たった時点で `naming.named_by` と `named_when` を埋め、
`kind` の判定根拠もそこに差し替える。

## 時間

Wikidata の inception は1600年。精度は不明なので EDTF では `1600~`。
終期は `18XX` としたが、**これは幅を示しているだけで根拠が弱い**——江戸琳派（酒井抱一）以降、
近代の日本画へどう繋がるかを読んでいない。

## 空間

発生地を京都とした（本阿弥光悦・俵屋宗達の活動地）。**一次資料は未確認。**
江戸への移動（酒井抱一による江戸琳派）が確認できれば `diffused_to` を張る。**未着手。**

## 未着手

- 担い手（本阿弥光悦・俵屋宗達・尾形光琳・酒井抱一）の person エンティティ
- 作品（証拠）——光琳《紅白梅図屏風》は「調和」の観点でも読む価値がある
- 江戸への伝播（`diffused_to`）と、近代日本画への接続
- 狩野派との対比は、この2件が揃った時点で overviews 側に書ける（並行関係はエッジにしない）
