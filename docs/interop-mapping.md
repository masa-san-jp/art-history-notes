# 外部データとの対応表

この KB を「繋がるデータ」にするために、自分の項目が外の標準のどれに当たるかを先に決めておく。
**書き出し（JSON-LD）の実装は movement 100件の節目に置く。** 今はこの対応表だけを持つ——
先に書き出しを作ると、まだ形が動くうちに二重管理になるため。

## 前提として確認したこと（2026-08-08）

- [Linked Art](https://linked.art/model/) はモデル 1.0 が公開されており、**CIDOC-CRM 7.1.3 +
  Getty Vocabularies + JSON-LD 1.1** の組み合わせ。美術館データの事実上の標準
- CIDOC-CRM は 7.3.x が draft で、公式版は 7.1 系（**版表記の対応は未確認**）
- Getty Vocabularies のライセンスは **ODC-By 1.0**

## 対応表

| このKBの項目 | 外部の対応 | 備考 |
|---|---|---|
| `uri` | JSON-LD `@id` | `urn:ahn:...`。公開時に HTTPS へ移しても URN は不変にする |
| `type: person` | `crm:E21_Person` | Linked Art の People |
| `type: org` | `crm:E74_Group` | 美術館・工房・幕府 |
| `type: work` | `crm:E22_Human-Made_Object` | Linked Art の Objects |
| `type: place` | `crm:E53_Place` | `coordinates` は `crm:P168_place_is_defined_by` |
| `type: event` | `crm:E5_Event` | 展覧会は `crm:E7_Activity` 寄り（**要検討**） |
| `type: source` | `crm:E31_Document` | 一次資料そのもの |
| `type: concept` | `crm:E55_Type` + AAT | 技法・様式・主題 |
| `type: movement` | **直接の等価クラスが無い** | Linked Art は様式・運動を AAT の Type で分類する形。`crm:E4_Period` + AAT 分類が最も近い（**この写しは近似**） |
| `kind` | 対応する外部語彙が無い | このKB固有。**AAT に写さない**（`self-declared` / `retrospective` の区別は AAT の関心事ではない） |
| `naming` | `crm:E41_Appellation` + 命名行為 | 命名者・命名年は `crm:E13_Attribute_Assignment` で表せるが重い。**要検討** |
| `time.start/end` | `crm:E52_Time-Span` | EDTF 値をそのまま持たせるか、`begin_of_the_begin` に展開するか（**要検討**） |
| `space` の役割語 | 役割ごとに別プロパティ | `created_in`→ 制作イベントの場所、`held_at`→ 現在の所在。**イベント中心に組み替えが要る** |
| `relations` の解釈系 | `crm:E13_Attribute_Assignment` | 確度と出典を持つ主張は、CRM では「誰がいつそう言ったか」の形にする |
| `certainty` | 対応語彙が無い | このKB固有。書き出し時は注記として落とす |
| `authority.*` | `owl:sameAs` / `skos:exactMatch` | Wikidata QID・Getty ID を同一性の主張として出す |

## 分かっている摩擦

1. **movement に等価クラスが無い。** Linked Art / CRM は様式や運動を「オブジェクトの分類」として
   扱い、独立したノードにしない設計。このKBは movement をノードにしているので、書き出しでは
   `E4_Period` + AAT 分類への近似になる。**近似であることを書き出しに明記する。**
2. **このKBは主張中心、CRM はイベント中心。** `certainty` 付きの関係を CRM に忠実に写すと
   `E13_Attribute_Assignment` の入れ子になり、読めるものにならない。**全体を写すのではなく、
   同一性（`sameAs`）と基本属性（時間・場所・型）に限って出す**方針を採る。
3. **`kind` と `certainty` は外に出ない。** このKB固有の区別なので、書き出しでは注記に落ちる。
   逆に言えば、この2つがこのKBの独自価値。

## 実装するときの形（100件の節目）

- `tools/export_jsonld.py` → `data/linked-art.json`（同一性と基本属性に限った JSON-LD）
- 近似・欠落を機械が数えて `data/export-report.md` に出す（何が写らなかったかを隠さない）
