# 時代文脈スナップショット

`contexts/` は、限定した時期・文化圏・アート領域について、誰がどの立場を示したかを根拠付きの
`signal` として保存する場所です。時代全体を一枚岩の実体として記述しません。

正本は各Markdownのfrontmatterにある根拠付きsignalです。`data/context-vectors.json` と
`data/context-similarity.json` は常に再生成できる生成物であり、直接編集しません。空欄の軸は中立値0ではなく
「観測なし」です。

```bash
python3 tools/build_context_vectors.py --check
python3 tools/build_context_vectors.py
python3 tools/compare_context.py context/ai-art-japan-2026-h2 --kind historical --top 10
```

比較結果は調査候補を選ぶためのものです。歴史的同一性、影響、因果関係の証拠として扱いません。
