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
  - url: "https://www.wikidata.org/wiki/Q406"
    kind: authority
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

**この場所の基準 `region` は1つだが、担った movement の時代によって属する文化圏が変わる。**
`config/regions.yaml` は `europe-east` を「中東欧・ロシア・ビザンツ圏」、`mena` を「中東・北アフリカ」と
定義しており、ビザンティン美術は前者、オスマン朝細密画は後者に当たる。基準値 `mena` は
オスマン朝細密画側に合わせたものだが、`config/place-region-history.yaml` の期間辞書を
集計側がmovementの開始時期に適用するため、ビザンティン美術は `europe-east` へ移る。
オスマン朝細密画の `145X` は1453年の境界に重なるため、現状は両地域を保持する。
`docs/schema.md` は「土地1つにエンティティ1つ。座標と文化圏は土地の性質」としており、
別エンティティに分ける解決は取らない。区間が曖昧に重なる場合は複数地域として保持する。

**未確認**: 都市としての時間軸（`time`）は空のまま。必要になった時点で埋める。
