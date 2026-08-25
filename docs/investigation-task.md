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

**Wikidata の日付は precision を見る（重要）。** `P571`（inception）の値は年に見えても、
`precision` が世紀や10年代を指していることがある。**値だけ読むと1世紀ずれる。**

| precision | 意味 | EDTF | 例 |
|---|---|---|---|
| 11 | 日 | `1884-05-20` | |
| 10 | 月 | `1884-05` | |
| 9 | 年 | `1884` | |
| 8 | 10年代 | `188X` | +1880 / 8 → 1880年代 |
| 7 | **世紀** | その世紀の `XX` 表記 | **+1500-00-00 / 7 は Wikidata 自身が「15. century」と描画する（＝1401–1500）ので `14XX`** |

precision 7 の解釈に迷ったら、Wikidata 自身に描画させて確かめる:

```bash
python3 - <<'EOF'
import json, urllib.parse, urllib.request
dv = {"value":{"time":"+1500-00-00T00:00:00Z","timezone":0,"before":0,"after":0,
      "precision":7,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"},"type":"time"}
q = urllib.parse.urlencode({"action":"wbformatvalue","format":"json","datatype":"time",
     "generate":"text/plain","datavalue":json.dumps(dv)})
req = urllib.request.Request("https://www.wikidata.org/w/api.php?"+q,
     headers={"User-Agent":"art-history-notes/0.1"})
print(json.load(urllib.request.urlopen(req, timeout=25))["result"])
EOF
```

**日本の対象**なら Japan Search と Web NDL Authorities も当たる（→ <https://jpsearch.go.jp/> /
<https://id.ndl.go.jp/>）。ただし **2026-08-08 時点で両方とも正しい呼び方が未確認**で、
SPARQL パーサエラーや権限エラーになる。**取れたら足す、取れなければ深追いしない。**
`wikidata` か `aat` のどちらかが取れていれば `none_reason` は不要。

**1つも見つからないとき**: `authority.none_reason` に「何を検索して見つからなかったか」を書く。
それでよい。空にしたまま進めると検証で落ちる。

### 4. frontmatter を埋める

| 項目 | 埋め方 |
|---|---|
| `kind` | 下の判定表で1つ選ぶ。**迷ったら本文にその迷いを書いてから選ぶ** |
| `naming.self_identified` | 当事者がその名で名乗ったか。`true` / `false` |
| `naming.named_by` / `named_when` | 後付けの命名なら命名者と年。不明なら `null` にして `note` に経緯 |
| `time.start` / `end` | EDTF。`1884` / `0000`（紀元前1年）/ `-0899`（紀元前900年）/ `146X`（1460年代）/ `1500~`（およそ）/ `..`（継続中）/ `null`（不明） |
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

**kind は Wikidata の `P31` に引っ張られずに、実体で決める。** 外部データの分類は不均質で、
同じ性質のものに違うクラスが付いている（狩野派には `family` があるのに土佐派には無い、など・実測）。
`P31` は判断材料の1つで、根拠にはならない。**継承の形・制度としての実体・自称の有無**を見て決め、
その判断理由を本文の `## kind の判定` に書く。

#### 関係語彙（この中から選ぶ）

構造的（出典なしで書ける）: `created_by` `belongs_to` `member_of` `part_of` `depicts`
`exhibited_at` `precedes` `taught_by` `documented_in`

解釈を含む（`certainty` と `source` が必須）: `influenced_by` `responds_to` `derives_from`
`reacts_against` `grouped_as` `diffused_to` `patronized_by`

`certainty` は `attested`（当事者の言明）/ `scholarly`（研究の通説）/ `hypothesis`（自分の仮説）。

- **後付けの括りへの所属は `part_of` ではなく `grouped_as`**（例: 新印象派 → ポスト印象派）
- **同時代の並行関係は書かない。** 時間と空間から機械が出す

### 4.5 パブリックドメインの画像を1〜3点付ける

その括りを**目で見られるようにする**。代表的な作品の画像を `images` に入れる（任意項目だが、
所蔵館のオープンアクセスで見つかるなら入れる）。

```bash
# 例: Art Institute of Chicago（データは CC0）
curl -s "https://api.artic.edu/api/v1/artworks/search?q=<作品名>&fields=id,title,image_id,is_public_domain" | python3 -m json.tool | head -40
# image_id が取れたら画像URLは https://www.artic.edu/iiif/2/<image_id>/full/843,/0/default.jpg
```

**パブリックドメイン相当だけ**（`license: public-domain` / `cc0` / `pdm`）。検証が語彙を強制する。
`source_page`（所蔵館の作品ページ）を必ず添える——ライセンスの根拠がそこにある。
**権利が不明なものは入れない。** 「古いから大丈夫」で入れない。**画像ファイルは repo に置かない**（リンクだけ）。

出どころの候補: Art Institute of Chicago（CC0）／Metropolitan Museum（Open Access）／
Cleveland Museum（CC0）／Rijksmuseum／National Gallery of Art／Wikimedia Commons（ファイル単位で確認）。

### 5. 本文を書く

見出しは固定（`docs/schema.md` の「本文の型」）。movement は:

`## 定義と範囲` → `## kind の判定` → `## 時間` → `## 空間` → `## 未着手`

- **出典URLを本文に置く。** 手元の知識だけで書いた行は書かない
- 確定できないことは **`**未確認**:` で始める行**にして残す。空欄で隠さない
- 二次情報は「二次情報」と書く
- **本文は主題のことだけを書く。KB の内部事情を混ぜない。** 書かないもの——
  「このKBで最初の1件」「stub として置いた」「型を分けない方針だから」「◯◯を試すために入れた」など、
  この KB の設計・運用・進捗の話。読む人が要るのは対象の事実で、こちらの事情ではない。
  `status` は frontmatter が持つので本文で言わない。
  **判断の根拠は主題の事実として書く**（例: ✗「型を1つに保つ方針なので lineage-school」→
  ○「朝廷の絵所預という世襲の職があったので lineage-school」）

### 6. 検証を通す

```bash
python3 tools/build_graph.py --check     # 落ちたらメッセージのとおりに直す
python3 tools/build_graph.py            # 通ったらグラフと被覆マップを更新
```

落ちる主な理由: TODO が残っている／典拠ゼロで `none_reason` が空／`kind` 未設定／
EDTF の形式違反／解釈系の関係に `certainty` か `source` が無い／参照先のエンティティが存在しない。

**YAML で必ず踏む罠**: `note:` や `display:` の説明文に **半角コロン＋スペース**（`: `）が入ると、
YAML がそこを新しい項目の区切りだと解釈して落ちる。長い説明を書くときは値全体を
`"` で囲む（例: `note: "命名は董其昌『画禅室随筆』に由来: 二次情報"` → 引用符で囲めば通る）。
全角コロン（`：`）に替えるのでもよい。

**`git checkout` / `git restore` / `git stash` を使わない。** 生成物を元に戻したくなっても使わない——
他のエージェントや私（aiko-art）の**未コミットの編集を消す**（2026-08-09 に俯瞰の未コミット分が
これで消えた）。生成物がおかしくなったら、**そのまま報告して止まる**。戻すのは私がやる。

**自分のファイル以外の理由で落ちたとき**（他の調査が同時に走っていて、その未完成ファイルが
検証に引っかかる場合）は、**他のファイルを動かさない・直さない**。自分のファイルだけを完成させ、
「他の未完成ファイルのために全体の検証が通らない」と報告して終わる。私（aiko-art）が順序をつける。

**参照先が無い**と言われたら、その参照先を先に作る（`new_entity.py` で `place` や `person` を stub で置く）。
ただし**孤児 stub を量産しない**——今回の1件に必要なものだけ。

`person` / `work` を作ってよいのは次の3つのどれかに当たるときだけ（`docs/schema.md` の
「person / work / event をいつ作るか」が正本）:

1. その movement の `kind` / `time` / `originated_in` の根拠になる
2. 2つ以上の movement を繋ぐ（師弟・分派・伝播）
3. 作品として実際に分解して読んだ

**どれにも当たらない担い手は、movement の本文に名前を書いて終わりにする。** 担い手を全員ファイルに
するのは名簿づくりで、この KB の仕事ではない。

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

`overviews/coverage.md` を見る。3つの材料が並んでいる。

1. **被覆マップ** — 空いている文化圏×世紀
2. **体系の食い違い・偏り**（`tools/audit.py` の出力）— 仮説が未検証のまま／kind が地域の言い換えに
   なっている疑い／継承の先が stub で辿れない、など。**ここは「体系が次に要求していること」なので、
   ただの空欄より優先度が高い**
3. **探されたが無かった語** — 他の人格が探して空振りした記録

迷ったら 2 → 3 → 1 の順で選ぶ。
