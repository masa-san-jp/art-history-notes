# 時代文脈を1件調査する手順

順序を変えない。

1. **scope固定** — 時期、13文化圏、`domain: art`、topicsを先に限定する。
2. **source収集** — 一次資料または研究資料を最低3件開く。現在contextは確認日を本文に明記する。
3. **signal化** — 1 sourceから同じdimensionへ複数signalを作らない。主張、方向、顕著性、担い手、確度を記録する。
4. **反対証拠** — 内部差、別方向の主張、一般化できない範囲を探し、`note`と本文へ残す。
5. **検証** — `python3 tools/build_context_vectors.py --check`を通す。
6. **比較** — 生成後に`compare_context.py`で候補を見る。

宣言文だけを根拠に`audiences`や社会全体の立場を付けない。一般化できない範囲をsignalの`note`に必ず書く。
類似結果をrelationsへ自動追加しない。候補は通常の調査で出典を確認してからKBへ反映する。
