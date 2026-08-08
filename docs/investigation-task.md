# 1件の調査のやり方（この手順だけで1件が終わる）

**この手順書は Sonnet が単独で1件を完了できる粒度で書いてある。** 設計の判断は済んでいるので、
調査する側は判断しない。迷ったら「未確認」と書いて次へ進む。**空欄を推測で埋めない。**

対象は原則 **movement 1件**（「〜主義」「〜派」「〜様式」「流派」）。1件＝1タスク。

---

## 手順

### 1. 重複を確かめる

```bash
ls entities/movements/ | grep -i <slug の一部>
grep -ril "<日本語名>" entities/
```

既にあれば、新規作成ではなく**そのファイルを埋める**タスクに変える。

### 2. 雛形を作る

```bash
python3 tools/new_entity.py movement <slug> --ja "<日本語名>" --en "<英語名>"
```

`slug` は英語名のケバブケース（例 `kano-school`、`bengal-school`）。**一度決めた slug は変えない**
（ID になる）。

### 3. 典拠IDを取る（最初にこれをやる）

**Wikidata**（同一性のハブとして使う。時間・空間の典拠には使わない）:

```bash
curl -s -H "User-Agent: art-history-notes/0.1" \
  "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=<名前>&language=ja&format=json&limit=5" \
  | python3 -c "import json,sys;[print(d['id'],d.get('label'),'|',d.get('description')) for d in json.load(sys.stdin)['search']]"
```

QID が取れたら claims を見る（`P1014`=Getty AAT／`P571`=開始／`P576`=解散／`P31`=何であるか）:

```bash
curl -s -H "User-Agent: art-history-notes/0.1" \
  "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=<QID>&props=claims|labels|descriptions&languages=ja|en&format=json" \
  | python3 -m json.tool | head -60
```

**Getty AAT**（様式・流派の典拠。非西洋も入っている）: `P1014` にあればそれを使う。無ければ
<https://www.getty.edu/vow/AATServlet> で名前を検索して ID を拾う。

**日本の対象**なら Japan Search（SPARQL 動作確認済）と Web NDL Authorities も当たる。
→ <https://jpsearch.go.jp/> / <https://id.ndl.go.jp/>

**1つも見つからないとき**: `authority.none_reason` に「何を検索して見つからなかったか」を書く。
それでよい。空にしたまま進めると検証で落ちる。

### 4. frontmatter を埋める

| 項目 | 埋め方 |
|---|---|
| `kind` | 下の判定表で1つ選ぶ。**迷ったら本文にその迷いを書いてから選ぶ** |
| `naming.self_identified` | 当事者がその名で名乗ったか。`true` / `false` |
| `naming.named_by` / `named_when` | 後付けの命名なら命名者と年。不明なら `null` にして `note` に経緯 |
| `time.start` / `end` | EDTF。`1884` / `146X`（1460年代）/ `1500~`（およそ）/ `..`（継続中）/ `null`（不明） |
| `time.display` | 原表記（元号・王朝名）をそのまま |
| `space` | `originated_in`（発生地・被覆集計のキー）。特定できないなら**書かない**（「発生地未確認」として表に出る） |
| `relations` | 下の関係語彙から。解釈を含むものは `certainty` と `source` が必須 |
| `claims` | `verified` を名乗るときだけ。`time` / `originated_in` / `kind` の3つに出典を付ける |
| `status` | `stub`（枠だけ）/ `draft`（書いたが出典が薄い）/ `verified`（一次情報で裏が取れた） |

#### kind の判定表

| kind | 判定の目安 | 例 |
|---|---|---|
| `self-declared` | 当事者が名乗った。宣言文・機関誌・自称の証拠がある | 未来派、シュルレアリスム |
| `retrospective` | 後代に外部（批評家・史家・市場）が付けた括り | 印象派、ポスト印象派、マニエリスム |
| `lineage-school` | 血縁・工房・師弟の継承体。制度としての実体を持つ | 狩野派、土佐派、シエナ派 |
| `period-style` | 王朝・時代に紐づく様式。担い手は交代する | ムガル絵画、国際ゴシック |

**「movement」という型名が対象に合わない感覚は正しい。** 狩野派は運動ではない。それでも型は1つに
保つ（理由は `docs/schema.md`）。合わない感覚は本文に書く——それが記録として要る。

#### 関係語彙（この中から選ぶ）

構造的（出典なしで書ける）: `created_by` `belongs_to` `member_of` `part_of` `depicts`
`exhibited_at` `precedes` `taught_by` `documented_in`

解釈を含む（`certainty` と `source` が必須）: `influenced_by` `responds_to` `derives_from`
`reacts_against` `grouped_as` `diffused_to` `patronized_by`

`certainty` は `attested`（当事者の言明）/ `scholarly`（研究の通説）/ `hypothesis`（自分の仮説）。

- **後付けの括りへの所属は `part_of` ではなく `grouped_as`**（例: 新印象派 → ポスト印象派）
- **同時代の並行関係は書かない。** 時間と空間から機械が出す

### 5. 本文を書く

見出しは固定（`docs/schema.md` の「本文の型」）。movement は:

`## 定義と範囲` → `## kind の判定` → `## 時間` → `## 空間` → `## 未着手`

- **出典URLを本文に置く。** 手元の知識だけで書いた行は書かない
- 確定できないことは **`**未確認**:` で始める行**にして残す。空欄で隠さない
- 二次情報は「二次情報」と書く

### 6. 検証を通す

```bash
python3 tools/build_graph.py --check     # 落ちたらメッセージのとおりに直す
python3 tools/build_graph.py            # 通ったらグラフと被覆マップを更新
```

落ちる主な理由: TODO が残っている／典拠ゼロで `none_reason` が空／`kind` 未設定／
EDTF の形式違反／解釈系の関係に `certainty` か `source` が無い／参照先のエンティティが存在しない。

**参照先が無い**と言われたら、その参照先を先に作る（`new_entity.py` で `place` や `person` を stub で置く）。
ただし**孤児 stub を量産しない**——今回の1件に必要なものだけ。

### 7. 取り出して読み返す

```bash
python3 tools/bundle.py movement/<slug>
```

1文書として読んで、周辺との繋がりが見えるか確かめる。関係が1本も無ければ、
それは体系に載っていない（受け入れ条件の「孤立10%未満」に効く）。

### 8. commit する

```bash
git add entities/ overviews/coverage.md data/ && git commit -m "<なぜこの1件を置いたか>"
```

コミットメッセージは「何をしたか」ではなく **なぜこれを置いたか**を書く。

---

## やらないこと

- 空欄を推測で埋める（`null` と「未確認」が正しい答え）
- 設計を変える（型を増やす・関係語彙を足す・閾値を動かす）。必要だと思ったら
  [issue #1](https://github.com/masa-san-jp/art-history-notes/issues/1) にコメントして止まる
- 1タスクで複数の movement を仕上げる（1件ずつ。周辺の stub は例外）
- 画像や全文を repo に置く（リンクと典拠IDで参照する）
- `data/graph.json`・`overviews/coverage.md` の生成ブロックを手で編集する

## 次に何を調べるか

`overviews/coverage.md` の被覆マップを見て、空いている文化圏×世紀から選ぶ。
埋める順番は同ファイルの「埋める順番」に書いてある。
