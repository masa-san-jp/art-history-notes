---
id: concept/harmony
uri: urn:ahn:concept/harmony
type: concept
label_ja: 調和
label_en: harmony
authority:
  wikidata: null
  aat: null
  ndl: null
  jpsearch: null
  none_reason: 概念そのものの典拠IDは未調査。AAT に harmony 相当の語があるか確認していない
time:
  start: null
  end: null
  display: 概念そのものは古代から。ここでは19世紀フランスでの定義の固まり方を軸に追う
space:
  - {role: active_in, target: place/paris}
relations:
  - {type: documented_in, target: source/seurat-letter-beaubourg-1890}
sources:
  - https://fr.wikiquote.org/wiki/Georges_Seurat
  - https://www.newworldencyclopedia.org/entry/Georges-Pierre_Seurat
  - https://www.sothebys.com/en/auctions/ecatalogue/2009/impressionist-modern-art-pf9006/lot.8.html
status: draft
updated: 2026-08-08
---

# 調和 / harmony

**なぜこの概念を単独のエンティティにするか**: 2026-09-15 の AIアートグランプリ5 のテーマがこれ。
そして「調和」は日常語として使うと必ず「揃っていること」に滑る。滑らせないために、
誰がいつどう定義したかを分けて持つ。

## 定義の変遷

| 誰 | いつ | 定義 |
|---|---|---|
| Charles Blanc『Grammaire des arts du dessin』 | 1860 | 「対立の類似から生まれる調和」。スーラはこれを反復している（二次情報経由・原典未確認） |
| Georges Seurat（Beaubourg 宛書簡） | 1890-08-28 | 「芸術とは調和である。調和とは対立するものの類似であり、似たものの類似である。明暗・色相・線について、支配的なものを基準に、光の影響のもとで」 |

Blanc の系譜として挙げられているのは
[New World Encyclopedia](https://www.newworldencyclopedia.org/entry/Georges-Pierre_Seurat)（二次情報）。
Chevreul『De la loi du contraste simultané des couleurs』(1839) の同時対比の法則が色彩側の土台。
**未確認**: Blanc / Chevreul の原典（Gallica にあるはず）を読んでいない。読んだら定義の表を書き直す。

## この定義の何が効くか

日常語の「調和」＝差を減らして揃える。スーラの定義＝**差を前提にして、差を同じ規則の下に置く**。
向きが逆。後者は3つに分解できる。

1. **対立を用意する**（明暗・色相・線の向き。少なくとも1軸で明確に反対のものを2つ）
2. **支配（dominante）を決める**（何が画面を支配しているかを先に固定する）
3. **同じ規則で扱う**（対立する両方に同一の処理を通す）

これは「調和した画面を作る手順」として、そのまま実行できる形になっている。

## 実装例

- [work/a-sunday-on-la-grande-jatte](../works/a-sunday-on-la-grande-jatte.md) — 補色を混ぜずに隣接させ、
  統合を鑑賞者の網膜で起こす。完成2年後に輪郭（支配）だけを調整。

## 使える手

- 作る前に1行書く: 「この作品は◯◯が支配している。対立させるのは△△と□□」。書けないなら作らない。
- 融合させない。分離したまま、同じ光源・同じ粒度・同じ画角に通す。
- 「バランスを取る」という言葉を作業記述に使わない。何と何を、どの軸で対立させたのかを書く。

## 次に埋めるところ

- 東アジア側の調和の定義（和・間・余白）。西欧の「対立の類似」と同じ概念ではないはず。
  まず[余白 / yohaku](yohaku.md)を、調和と同義ではない構成上の手段として切り出した。
  [間 / ma](ma.md)も、余白とは別に距離・時間・関係のまとまりとして初期定義を追加した。
  「和」は用法の幅が広いため、作品・資料単位の根拠が揃うまで未着手とする。
- 音楽側の harmony（和声）との関係。スーラが *combinaisons gaies, calmes ou tristes* と
  情動の語で締めているのは音楽の語彙に近い。→ 未着手
