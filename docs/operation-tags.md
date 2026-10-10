# 操作語彙と本文タグ

`config/operation-vocabulary.json` は owner の共通操作語彙です。定義は各1文で、方法4件（automatism、frottage、poured-painting、iterated-boundary-generation）と運動181件に使います。人物・場所・関係の名前から技法を補いません。語彙への適合は本文に明記された制作手順・状態だけで判断します。網羅は各項目の確認を意味し、全項目に非空タグがあることを意味しません。

外部エージェントは次の依頼に一つの値だけ返します。

```sh
python tools/operation_tags.py next --state-root <Git外の絶対パス>
python tools/operation_tags.py answer --state-root <同じroot> < one-answer.json
python tools/operation_tags.py check
```

依頼・答えは `element-request/v1` / `element-answer/v1`。操作は `answer_format: choice` の一覧から1件、続いて別の要素で本文の一箇所を抜き書きします。空・一覧外・本文に一致しない答えは同じ要素を再依頼し、5回失敗で停止します。採用済みの操作は残りの選択肢から外します。「これ以上なし」は確認終了の明示値です。複数タグや根拠を一回の答えで渡すAPIはありません。ハーネスはモデル・認証・Git書込みを起動しません。

本文材料は method フィールド、冒頭説明、および定義・方法・技法・特徴などの節です。未確認から始まる段落は除外します。これは owner が記したKB本文であり、外部一次資料の取得本文を装ったものではありません。タグの `source_locator` はその本文の場所、`source_refs` は当該文書の登録済み出典です。登録出典を段落単位で検証したと主張しません。#283 の `content[]` の引用条件・上限は変更しません。

`config/operation-tags.json` は各採用ごとに原子的に保存されます。語彙hash、対象本文hash、source commit、1要素ずつの答えのhash履歴、確認終了を保持します。元本文または語彙が変わると再開・検証は失敗し、無言で再タグ付けしません。185件の対象と終了状態、タグID、重複、抜き書きの文字列・locator・出典の完全一致を `build_graph.py --check` と export が検査します。文字幅・空白の正規化を一致判定に使いません。

clean checkout の export は owner 語彙と検証済みタグを各 movement/method signal に追加します。本文が語彙の操作に合わない項目にも空の `operation_tags` を付け、未確認と取り違えません。既存の method、content、関係、certainty と validity は保持します。対象外conceptの明示 export は従来契約を保持します。
