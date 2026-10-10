# カードの抜き書き

段階 A v2（agentic-art-orchestration `docs/20261010-phase-a-v2-design.md` 4.1〜4.2・9.2）の「カード」の材料です。書き出し（`tools/export_signals.py`）の各 signal に `card: [{text, source_locator, source_sha256}]` を加えます。

## 抜き書きの出どころ

| 項目 | 抜き書き |
| --- | --- |
| 操作タグを持つ（111件） | タグの根拠（`config/operation-tags.json` / `operation-tag-additions.json`）を、追加の推論なしにそのまま使う |
| タグが無く本文がある（68件） | 1項目1要素の推論（K1）。`config/card-excerpts.json` に保存する |
| 本文もタグも無い（6件） | カード無し。書き出しは `card: []` と、最上位の `card_missing` に ID を出す。名前だけで埋めない |

本文とは、書き出しの `content[]`（定義・方法・技法・特徴などの節にある、出典URLを持つ段落。最大2400字）です。カード無しの6件は `movement/an-gyeon-school`、`movement/bagan-art`、`movement/gothic-art`、`movement/neoclassicism`、`movement/renaissance`、`movement/rococo` です。

## 固定の表示規則（設計書 4.1）

`text` はこの規則を通した後の文字列です。引用記号 `>`、Markdown のリンク記法（文字だけ残す）、URL、`P571` のようなID・エンティティID（`movement/…` など）を取り除き、日本語どうしの改行は詰め、ASCII どうしの改行は空白1つにします。空になった括弧は落とします。抜き書きは段落をまたがず、同じ規則を通した固定 commit のファイル本文に一字一句含まれることを検査します（`source_sha256` はその commit のファイル blob の sha256）。一致しなければ export は `CARD_SOURCE_MISMATCH` で止まり、項目を黙って捨てません。

## K1 要素（1回に1つの値）

```sh
python tools/card_excerpts.py next --state-root <Git外の絶対パス>
python tools/card_excerpts.py answer --state-root <同じroot> < one-answer.json
python tools/card_excerpts.py run --state-root <同じroot> [--limit N]   # 依頼を adapter に1件ずつ渡す
python tools/card_excerpts.py check [--commit SHA]                      # 全項目のカードと一字一句一致を確かめる
```

依頼・答えは `element-request/v1` / `element-answer/v1`（`schemas/` に親の契約を複製。出所は `schemas/element-contract-provenance.json`）。要素ID は `K1.card.<id の / を . にしたもの>.<1|2>` です（契約の `element_id` の形式が `/` を許さないため）。

1. `.1`: 本文（3000バイト以内に段落単位で切ったもの）から、作り方・考え方を最もよく表す部分を12〜120字で抜く。
2. `.2`: 別の箇所を抜く。無ければ `これ以上なし`。

確認はプログラムで行います: 本文の1段落に一字一句含まれる／12〜120字／URL・ID・リンク記法・「出典」「未確認」を含まない／2つ目は1つ目と重ならない。落ちたら理由（`previous_failure`）を付けてその要素だけを再依頼し、5回で `BLOCKED`。保存は本文の sha256、1要素ずつの答えの sha256 と確認の結果、採用した抜き書きです。本文が変わった項目だけやり直し、本文以外の状態（`--state-root`）は Git に置きません。

`tools/haiku_adapter.py` は依頼1件を標準入力で受け、`claude -p --model claude-haiku-5-5 --effort max` を道具なし・設定なし・セッションなしで1回呼び、答えの値だけを標準出力に返します。ハーネス自身はモデルを起動しません。
