---
id: concept/iterated-boundary-generation
uri: urn:ahn:concept/iterated-boundary-generation
type: concept
label_ja: 反復境界生成
label_en: Iterated Boundary Generation
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "この構成方法に対応する外部典拠IDは未調査"
time:
  start: null
  end: null
  display: "起源年は未確認。2024年の出典で確認できる実験例を記録する（方法の発明年ではない）"
method:
  fixes:
    - "同じ更新関数を反復して適用すること"
    - "収束・発散など、反復の振る舞いを分ける境界を観測すること"
  varies:
    - "学習率などのハイパーパラメータ、初期値、データ、ネットワーク設計"
    - "反復後の出力が有界に留まるか発散するかという結果"
  requires:
    - "出力を次の入力へ戻せるパラメータ化された関数"
    - "反復結果を収束・発散などの状態へ分類する観測規則"
  origin_domain: computation
space: []
relations: []
sources:
  - url: "https://sohl-dickstein.github.io/2024/02/12/fractal.html"
    kind: primary
    note: "反復関数、ハイパーパラメータ、収束・発散の境界がフラクタル構造を生む実験記述（2024-02-12）"
derived_from:
  - {origin_instance_id: agent-398-review, owner_repository: art-history-notes, record_id: iterated-boundary-generation, revision: 1}
status: draft
updated: 2026-10-03
---

# 反復境界生成 / Iterated Boundary Generation

## 定義の変遷

ここでいう反復境界生成は、出力を同じ関数へ戻す反復を固定し、反復が有界に留まるか
発散するかなどの振る舞いの境界を観測する方法である。Jascha Sohl-Dickstein は、
フラクタルとニューラルネットワーク訓練が「関数を自分の出力へ繰り返し適用する」点で
似ており、訓練が成功する領域と失敗する領域の境界にフラクタル構造が現れると記述している。
この項目では、特定のアルゴリズム名ではなく、反復・条件変化・境界観測の組み合わせを方法として採る。

## 実装例

ニューラルネットワークの勾配降下では、学習率などのハイパーパラメータを変えながら
パラメータ更新を反復し、訓練が収束する領域と発散する領域を比較する。同じ考え方は、
マンデルブロ集合やニュートン・フラクタルのように、反復の境界を可視化する計算にも現れる。

## 使える手

1. 何を反復して次の入力へ戻すかを固定する。
2. 反復の結果を、少なくとも二つの振る舞い（たとえば有界／発散）に分ける。
3. 入力条件やハイパーパラメータを少しずつ動かし、結果が切り替わる境界を記録する。

出典は計算手順そのものを美術史上の技法と呼んでいるわけではない。そのため、ここでは
美術外で生まれた方法を同じ concept 経路へ記録したものとして扱い、芸術作品への適用や
歴史的影響は主張しない。

方法宣言から owner intake を実行した記録と、その共有KBへの昇格元は
[#398 実行記録](../../docs/method-concepts-398-review.md) に示す。
