---
id: concept/poured-painting
uri: urn:ahn:concept/poured-painting
type: concept
label_ja: ポーリング絵画
label_en: Poured Painting
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "この方法名に対応する外部典拠IDは未調査"
time:
  start: "1946~"
  end: null
  display: "1940年代後半のポロックの poured paintings の記録。1936年の実験工房参加の約10年後（Whitney）。手法全体の発明年は未確認"
method:
  fixes:
    - "支持体を水平に置き、絵具を筆で塗る代わりに流れとして配置する"
  varies:
    - "缶から注ぐ位置と棒の先から飛散させる位置、画面内の身体的な操作"
    - "画面上で形成される線・滴・層の密度"
  requires:
    - "流動する絵具と、それを受け止める水平な支持体"
    - "缶から注ぐ、または棒の先から飛散させる操作"
  origin_domain: art
space: []
relations: []
sources:
  - url: "https://www.moca.org/artworks/number-1"
    kind: institutional
    note: "Number 1, 1949 を床の未張りキャンバスへ缶から注ぎ、棒の先から飛散させたと記録。水平な支持体の根拠"
  - url: "https://whitney.org/media/46248"
    kind: institutional
    note: "Whitney Museum の音声ガイド。ポロックの poured paintings と、先行する airbrush / automotive lacquer の制作を記録"
status: draft
updated: 2026-10-03
---

# ポーリング絵画 / Poured Painting

## 定義の変遷

ポーリング絵画は、絵具を画面へ流し、滴らせ、または注ぐことで、筆先の輪郭だけではなく
液体の移動そのものを画面の構造にする方法である。Whitney Museum の解説は、ジャクソン・
ポロックが1936年に実験工房へ参加したことと、エアブラシ・自動車用ラッカーによる
先行実験を紹介し、その約10年後の poured paintings と区別している。
ここでは1940年代後半の制作記録として扱い、1936年をこの方法の開始年にはしない。

## 実装例

MOCA の《Number 1, 1949》解説は、床の未張りキャンバスに缶から絵具を注ぎ、
棒の先から飛散させ、画面内で身体を動かしながら制作したと記録する。
method はこの確認できる実装を構造化したもの。重力の制御や偶然性の扱いは
取得した資料で確認できないため主張しない。

## 使える手

- 床の水平な支持体に、缶や棒から絵具を配置する。
- 注ぐ・飛散させる位置と身体の操作を動かす。
- 完成後の見た目だけでなく、流れがどの順序で重なったかを記録する。

この項目は、既存の `movement/abstract-expressionism` から `uses_method` で辿れる。
ポロック本人の entity は現時点の KB に無いため、本人への個別関係は作っていない。
