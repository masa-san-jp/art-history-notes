# 他の人格（アイコたち）向けの入口

このKBの**使い手はアイコたち**（aiko-pr / hisyo / aiko-dev / maid / artisan / tao-aiko）。
2026-08-08 マサ指示「外って誰のこと？ 俺はアイコたちだと思ってるよ」。だから外部の美術館システムより
先に、この入口を整える。

書き手は aiko-art。**読むだけなら私に聞かなくていい。** 下の3つのコマンドで足りる。

## 1. まず被覆マップを見る（何が入っているか）

```bash
cd ~/dev/art-history-notes && cat overviews/coverage.md
```

movement × 文化圏 × 世紀の表。**空欄は「まだ無い」**という意味なので、無いものを探して時間を使わない。

## 2. 語で探す（IDを知らなくていい）

```bash
python3 tools/bundle.py --search 調和      # 触れているものの一覧
python3 tools/bundle.py --search 浮世絵    # 該当なしなら「まだ無い」と返る
```

複数当たれば一覧、1件だけなら束をそのまま出す。**該当なしは「まだ無い」**という答えなので、
そこで探すのをやめてよい（無いものを探して時間を使わないため）。

## 3. 知りたいものを1文書で取り出す

```bash
python3 tools/bundle.py movement/kano-school          # 1件＋周辺（担い手・場所・出典）
python3 tools/bundle.py --region asia-east-japan      # 文化圏でまとめて
python3 tools/bundle.py --century 19                  # 世紀でまとめて
python3 tools/bundle.py movement/rinpa -o /tmp/x.md   # ファイルへ
```

出力は markdown 1本。**出典URLが末尾に集約される**ので、そのまま引用の根拠に使える。

## 4. 機械で引くなら graph.json

```bash
python3 -c "import json;g=json.load(open('data/graph.json'));print(len(g['entities']),len(g['edges']))"
```

`entities` は id → frontmatter、`edges` は `{from, type, to, certainty}`。逆向きは展開済み
（`derived: true` が付く）。

## 引用するときの約束（aiko-pr は特に）

このKBの記述は3段階に分かれている。**外に出す文章で扱いを変えてください。**

| 印 | 意味 | 外に出すとき |
|---|---|---|
| `status: verified` | 一次情報で裏が取れている | 出典URLを添えて書ける |
| `status: draft` | 書いたが出典が薄い | 「〜とされる」の形にする。断定しない |
| `status: stub` | 枠だけ | **引用しない** |
| 本文の `**未確認**:` の行 | 私が確かめられなかったこと | **事実として書かない。** 触れるなら「未確認」と明示する |
| `certainty: hypothesis` | 私の仮説 | 私の見立てとして書く。通説と混ぜない |

**「未確認」を落として断定文にするのが、いちばんやってはいけない加工です。** そこは私が確かめていない
という記録で、消すと出典のない断定になります。

いま `verified` は1件だけです（スーラ《グランド・ジャット島の日曜日の午後》）。他は draft か stub。
記事や投稿で断定が要るときは、先に私に言ってください——その1件を verified に上げる作業を優先します。

## 私に聞いた方が早いこと

- **「この主題で使える素材はある？」** — 被覆マップに無い領域でも、隣接から辿れることがある
- **「この記述を断定で書きたい」** — 一次資料に当たって status を上げる作業になる。日数が要る
- **入れてほしい movement のリクエスト** — 被覆の穴埋めと並べて順番を決める

連絡は SendMessage（cross-session）で aiko-art へ。急ぎでなければ、リクエストは
「いつまでに要るか」を添えてください。制作の締切と並べて順番を決めます。

## やってほしくないこと

- `entities/` を直接書き換える（スキーマ検証があるので壊れます。追加・修正は私に言ってください）
- `data/` と `overviews/coverage.md` の生成ブロックを編集する（次の生成で消えます）
- 未確認の記述を断定に変えて外に出す（上の表のとおり）
