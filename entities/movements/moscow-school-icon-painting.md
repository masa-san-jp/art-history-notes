---
id: movement/moscow-school-icon-painting
uri: urn:ahn:movement/moscow-school-icon-painting
type: movement
kind: period-style
label_ja: モスクワ派
label_en: Moscow school of icon painting
authority:
  wikidata: Q122978289
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "14XX"
  end: "15XX"
  display: "14〜16世紀（Московская школа）。フェオファン・グレク、アンドレイ・ルブリョフ、ダニイル・
    チョールヌィによる14世紀末〜15世紀初頭の隆盛（1405年のモスクワ・クレムリン全告知大聖堂の
    仕事が最初期の記録）を経て、15世紀末〜16世紀初頭のディオニシーの世代まで続いたとされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Московская школа"
  note: "ノヴゴロド派（movement/novgorod-school-icon-painting）と同じく、中世の画家・発注者自身が
    この名で自らを呼んだ記録は無い。地域別に『派（школа）』を区別する用法自体が後代（19〜20世紀）の
    美術史記述に由来する点も同様と見て、named_by・named_whenは未特定のままとした"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Moscow_School", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Moscow_School", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Moscow_School", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/moscow}
relations:
  - {type: influenced_by, target: movement/byzantine-art, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Moscow_School"}
sources:
  - url: "https://www.wikidata.org/wiki/Q122978289"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Moscow_School"
    kind: reference
    note: "『Moscow school』の項。14〜16世紀のロシアの建築・絵画の学派とし、フェオファン・グレク、
      アンドレイ・ルブリョフ、ダニイル・チョールヌィによる隆盛と、ビザンティン・南スラヴ美術との
      総合を基盤とすると記す"
  - url: "https://en.wikipedia.org/wiki/Andrei_Rublev"
    kind: reference
    note: "アンドレイ・ルブリョフの項。1405年、フェオファン・グレク、プロホル・ゴロデツキーとともに
      モスクワ・クレムリンの全告知大聖堂のイコン・壁画を手がけた最初の記録を記す"
  - url: "https://en.wikipedia.org/wiki/Dionisius"
    kind: reference
    note: "ディオニシー（Dionisius, c.1440–1503/1508）の項。15〜16世紀の境目における『モスクワ派の
      最重要な担い手の一人』とし、ルブリョフの伝統を継いだと記す"
status: draft
updated: 2026-09-15
---

# モスクワ派 / Moscow school of icon painting

## 定義と範囲

英語版Wikipedia「[Moscow School](https://en.wikipedia.org/wiki/Moscow_School)」はこう記す
（二次情報、原文引用）。

> The Moscow school ... is the name applied to a Russian architectural and painting school in the
> 14th to 16th centuries.

絵画（イコン・壁画）に限れば、隆盛期は次のように記述される。

> The flourishing of the Moscow school in the late 14th and early 15th centuries is associated with
> Theophanes the Greek, Andrei Rublev and Daniel Chorny.

様式の基盤について、同項はこう記す。

> The basis of the Moscow school of painting was the synthesis of local traditions with Byzantine
> and South Slavic art.

もっとも早期に具体的な記録があるのは1405年、モスクワ・クレムリンの全告知大聖堂（Cathedral of the
Annunciation）の仕事で、[アンドレイ・ルブリョフの項](https://en.wikipedia.org/wiki/Andrei_Rublev)は
フェオファン・グレク、プロホル・ゴロデツキーとともにこれを手がけた最初の記録とする（二次情報）。
ルブリョフの伝統は15世紀末〜16世紀初頭、[ディオニシー](https://en.wikipedia.org/wiki/Dionisius)へ
引き継がれた。

## kind の判定

`period-style` とした。[ノヴゴロド派](novgorod-school-icon-painting.md)と同じ構造で、単一の
血縁・工房・官職による継承ではなく、モスクワ大公国という政体の隆盛期を通じて、フェオファン・グレク
（移住画家）→ルブリョフ・チョールヌィ→ディオニシーと担い手が交代しながら、ビザンティン・南スラヴ
美術との総合という共通の基盤が保たれた点を重視した。**ただしノヴゴロド派と異なり**、フェオファン
からルブリョフへ、ルブリョフからディオニシーへという師弟・様式継承の線が資料上より明確に語られる
点は、`lineage-school`的な性格も併せ持つ。**未確認**: この師弟関係が血縁的な工房継承（狩野派型）に
匹敵するほど制度化されていたのか、それとも個別の評判に基づく緩やかな継承だったのかは、今回は
一次資料まで遡れていない。

## 時間・空間

`originated_in` はモスクワ（[place/moscow](../places/moscow.md)）。`start`・`end`は
Wikipedia英語版の「14th to 16th centuries」という記述に合わせ、ノヴゴロド派と同じ粒度で
`14XX`〜`15XX`とした。

## ビザンティン美術との関係

Wikipediaの記述する「ビザンティン・南スラヴ美術との総合」を根拠に、`relations`へ
`influenced_by movement/byzantine-art`を張った。**訂正**: 当初、ビザンティン美術の発生地
（[place/istanbul](../places/istanbul.md)、現在の文化圏バケットは`mena`）が`europe-east`の
モスクワと異なる文化圏として4経路監査の接続に使えると見込んだが、`config/place-region-history.yaml`
はイスタンブールを「330〜1453年（東ローマ帝国の首都だった期間）は`europe-east`」と時代限定で
上書きしており、ビザンティン美術（およびモスクワ派の活動期）はいずれもこの期間内にあるため、
`regions_of`の判定上は両者とも`europe-east`となり、文化圏を跨ぐ接続としては機能しない。
この関係は様式的影響の記録として残すが、4経路監査の接続には数えない。

## ノヴゴロド派との関係

[ノヴゴロド派](novgorod-school-icon-painting.md)の項目は「16世紀にモスクワ派へ主導権が移った」と
記し、モスクワ派をこのKBにまだ存在しない movement として未着手に挙げていた。本項目の追加により、
ノヴゴロド派側に`precedes`（構造的関係、出典不要）を張り、両派の時代的な前後関係を機械可読にした。

## 未着手

- フェオファン・グレク、アンドレイ・ルブリョフ、ダニイル・チョールヌィ、ディオニシーを person
  エンティティとして立てるかどうか（今回は本文中の記述にとどめた）
- Tretyakov Gallery等の機関資料への直接アクセスと、代表作（《至聖三者》など）の個別作品化
- フェオファン→ルブリョフ→ディオニシーの師弟継承が制度化されていたのかの一次資料での確認
- 文化圏間接続（4経路）: 西側美術館（Metなど）へのイコンの収蔵記録など、`europe-east`外への
  文書化された接続を探す。今回は見つけられず、`config/cross-region-reviews.yaml`に
  no-documented-cross-region-relationとして記録した
