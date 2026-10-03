---
id: concept/frottage
uri: urn:ahn:concept/frottage
type: concept
label_ja: フロッタージュ
label_en: Frottage
authority:
  none_reason: "この経路では外部典拠IDを未確認"
time:
  start: null
  end: null
  display: "起源年は未確認。エルンストのシュルレアリスム期の実践を記録"
method:
  fixes:
    - "凹凸のある面に紙を重ね、鉛筆で擦ってその面のテクスチャを写す手順"
  varies:
    - "紙の下に置く面のテクスチャと、紙に写される模様"
  requires:
    - "凹凸のある面、紙、鉛筆、および紙を擦る操作"
  origin_domain: art
space: []
relations: []
sources:
  - url: "https://www.museothyssen.org/en/collection/artists/ernst-max"
    kind: institutional
    note: "エルンストの半自動技法と、凹凸面に紙を重ね鉛筆で擦るフロッタージュの手順"
derived_from:
  - {origin_instance_id: agent-398-review, owner_repository: art-history-notes, record_id: frottage, revision: 1}
status: draft
updated: 2026-10-03
---

# フロッタージュ / Frottage

## 定義の変遷

ティッセン＝ボルネミッサ美術館のエルンスト解説は、シュルレアリスムのグループと
交流した時期の半自動技法としてフロッタージュを紹介する。凹凸のある面の上に紙を置き、
鉛筆で擦る操作が確認できる。ここではその手順を方法として構造化し、様式名とは区別する。
取得した資料だけでは方法全体の起源年を確定できないため、time.start は null とした。

## 実装例

紙・凹凸面・鉛筆と擦る操作を成立条件とする。紙を重ねて擦る手順を固定し、
下に置く面のテクスチャと転写される模様を可変要素とするのは、この記述の操作的な整理である。
筆圧や方向の規則、特定作品の制作工程までは出典にないため記録しない。

## 関係と来歴

`movement/surrealism` の出典付き `uses_method` の逆関係から辿れる。
`theme_research.py` の方法宣言から owner intake を通した draft を共有KBへ昇格した。
元の candidate・record・receipt の保存先は [#398 実行記録](../../docs/method-concepts-398-review.md) を参照。
