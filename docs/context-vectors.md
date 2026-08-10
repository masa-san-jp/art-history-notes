# 時代文脈ベクトル

## 正本と生成物

時代文脈の正本は`contexts/`の根拠付きsignalである。ベクトル、信頼度、類似度は生成物で、
`config/context-dimensions.yaml`の固定12軸から決定論的に再計算する。情報がない軸は`null`とし、0で補わない。

contextは`id`、`label_ja`、`kind`、`scope`、`about`、`signals`、`sources`、`status`、`updated`を持つ。
`kind`は`historical`または`current`。`scope`はEDTFの開始・終了、13文化圏の配列、`domain: art`、
kebab-caseのtopicsを持つ。historicalは既存entityを`about`で最低1件参照し、currentは空配列でもよい。

signalはcontext内で一意な`s001`形式のID、固定軸ID、`direction`（-2〜2）、`salience`（1〜3）、
`holders`、1文の`claim`、`certainty`、`source`、一般化できない範囲を示す`note`を持つ。情報不足は
`direction: 0`ではなくsignal自体を置かない。0は中立または両方向が同程度という明示的な根拠がある場合だけ使う。

draftはsignalとsourceが最低1件必要。verifiedはsignal 12件以上、8軸以上、一意なsource 6件以上、
holders 3役割以上、hypothesis 0件を満たす。同じ軸に正負のsignalがある場合は、本文の
「反対証拠・内部差」に両側のsignal IDを書く。

## signalの重み

各signalについて`x = direction / 2`、`c = certainty weight`、`w = salience * c`とする。同じ軸の値は
`sum(w*x) / sum(w)`。信頼度は、一意な出典数、一意な担い手役割数、確度の加重平均から計算する。

```text
certainty_mean = sum(salience*c) / sum(salience)
salience = min(1, sum(salience) / 9)
polarization = sqrt(sum(w*(x-value)^2) / sum(w))
confidence = min(1, source_count/3) * min(1, holder_count/2) * certainty_mean
coverage = signalがある軸数 / 12
```

比較では双方の信頼度が0.25以上の軸だけを使う。比較可能軸が4未満なら類似度を出さない。方向の近さを80%、
分極の近さを20%として軸類似度を作り、顕著性と信頼度で重み付けする。8軸未満の比較には被覆係数を掛ける。

```text
axis_weight = min(salience_A, salience_B) * min(confidence_A, confidence_B)
direction_similarity = 1 - abs(value_A-value_B) / 2
polarization_similarity = 1 - abs(polarization_A-polarization_B)
axis_similarity = 0.8*direction_similarity + 0.2*polarization_similarity
raw_similarity = sum(axis_weight*axis_similarity) / sum(axis_weight)
similarity = raw_similarity * min(1, comparable_dimension_count/8)
```

数値は小数6桁。`data/context-vectors.json`は`schema_version`、`input_digest`、`dimension_order`、
`contexts`の順、`data/context-similarity.json`は`schema_version`、`input_digest`、`pairs`の順で書く。
contextとpairはID辞書順、dimensionは固定index順。同点もdimension indexで決める。

`input_digest`は軸設定と`contexts/`直下の全Markdownについて、リポジトリ相対パス、NUL、raw bytes、NULを
パス辞書順でSHA-256へ入力した値である。更新時刻は使わない。生成物は同じディレクトリの一時ファイルへ
完全に書いてから置換する。

完全なスキーマ、数式、検証条件、JSONキー順は[Issue #2](https://github.com/masa-san-jp/art-history-notes/issues/2)
を正とする。類似は調査候補であり、同一性・影響・因果の証拠ではない。
