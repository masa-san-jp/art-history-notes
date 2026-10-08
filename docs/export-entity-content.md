# 出典付き entity 本文の signal export

`tools/export_signals.py --purpose artistic-research` は movement と出典付き method concept を同じ export に含める。既存の ID、関係、certainty、validity は保持する。解釈や draft を verified に昇格させない。

`content[]` は `text`、`source_locator`、`source_refs` を持つ。`text` は entity markdown の定義・方法・手法・技法・態度・特徴・実装例の節から決定的に抜き出す。本文の段落に明記された URL が frontmatter の sources と完全一致した場合だけ採用し、直後の引用段落はその引用元を継承する。出典のない別の段落、未確認・未着手節、entity 名の見出しは採用しない。frontmatter の出典付き method.fixes / varies / requires は、その既存の owner 出典契約に従って原文の値を先に採用する。

一 entity の text 合計は最大 2400 文字。超過時は元の文字列の prefix に切り詰め、別フィールドの出典 URL と locator は保持する。推論で要約したり、引用元 URL を生成したりしない。出典を局所的に特定できない本文は省かれるため、すべての既存 entity に本文があるとは限らない。本文不足は消費側が 0 点として検知する。

`entity_labels` は日本語・英語の entity 名を渡し、消費側で名前だけの一致を採点から除外するために使う。名前の一致そのものを内容上の関係の根拠にしない。関係が空でも出典付き本文のある movement は export できる。既存の --limit は movement の ID 順を保持し、その後に method を加える。

検証:

```bash
python tools/build_graph.py --check
python tools/build_context_vectors.py --check
python -m unittest discover -s tests -p test_export_signals.py -v
python tools/verify.py
```

入力の entity・sources・method と正準グラフは変更しない。export は clean checkout の HEAD を provenance に使う。
