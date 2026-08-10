---
id: place/istanbul
uri: urn:ahn:place/istanbul
type: place
label_ja: イスタンブール
label_en: Istanbul
authority:
  wikidata: Q406
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: null
  end: null
  display: null
region: mena
former_names:
  - {name: コンスタンティノープル, until: "1930"}
coordinates: [41.01, 28.960277777778]
space: []
relations: []
sources:
  - https://www.wikidata.org/wiki/Q406
status: stub
updated: 2026-08-09
---

# イスタンブール

オスマン朝細密画（[movement/ottoman-miniature](../movements/ottoman-miniature.md)）の発生地として
置いた stub。1453年のメフメト2世によるコンスタンティノープル征服後、オスマン朝の首都となり、
宮廷工房ナッカーシュハーネが置かれた。座標はWikidata [Q406](https://www.wikidata.org/wiki/Q406)
の値（北緯41.01 東経28.960278）。

330年から1453年までは東ローマ帝国の首都コンスタンティノープルで、[ビザンティン美術](../movements/byzantine-art.md)の
発生地でもある。`former_names` の `until` は**改称の年**を取って1930年とした——1453年は政体が
替わった年で、名前が公式にイスタンブールへ一本化されたのはトルコ共和国下の1930年である。
2つの年は数えているものが違う（政体の断絶と、名前の改称）。

**この場所は `region` を1つしか持てないが、担った movement によって属する文化圏が変わる。**
`config/regions.yaml` は `europe-east` を「中東欧・ロシア・ビザンツ圏」、`mena` を「中東・北アフリカ」と
定義しており、ビザンティン美術は前者、オスマン朝細密画は後者に当たる。現在の値 `mena` は
オスマン朝細密画に合わせたもので、**ビザンティン美術はこの土地を経由すると `mena` として集計される**。
`docs/schema.md` は「土地1つにエンティティ1つ。座標と文化圏は土地の性質」としており、
別エンティティに分ける解決は取らない。集計の側で扱いを決める必要があるため、
[issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1) の論点として上げてある。

**未確認**: 都市としての時間軸（`time`）は空のまま。必要になった時点で埋める。
