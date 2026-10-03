# #398 レビュー修正と実 intake 記録

2026-10-03 実行。知識のGit保存先をcode checkoutと分離する規約に従い、candidate / record /
payload / receipt は以下の明示したローカルowner storeへ保存した。共有KBには昇格したentityと
`derived_from`、この参照記録だけを置く。外部サイトの原文snapshotをGitに複製していない。

## 保存先と固定commit

- owner store: `/private/tmp/art-history-398-method-review.Ffjwhv/owner-store`
- store binding: owner=`art-history-notes`, creator=`masa-san-jp`, collection=`issue-398-methods`
- 実行code commit: `ce3494f7b035522b284f0b49224cb2ceb838bdf2`
- 最終knowledge commit: `d9b6e6695323402afa23e335752c685d313f9f0e`
- 詳細なargv、candidate hash、prepare結果、receipt: `/private/tmp/art-history-398-method-review.Ffjwhv/run-report.json`
- 保存ref: `objects.git` の `refs/heads/knowledge`。remoteなし。後続レビューのためstoreを保持する。

| target | 判定 reason（v2） | record / payload key | intake commit |
|---|---|---|---|
| concept/iterated-boundary-generation | existing-exact-label | b41f706523069d2af934c9f240d5a601f37f0435b741bcf032cab265d55189dd | 2bef2345ab4006a44b519930191f5f6c03f6580e |
| concept/frottage | candidate-declared-method | 9af078a71459c236e69340511f96a6bc9e0f37472dbfcbbbf79bda9f56b89222 | d9b6e6695323402afa23e335752c685d313f9f0e |

recordは `records/<key>.json`、payloadは `contexts/research-memory/payloads/<key>.json`。
両recordの `applicability.method_classification` に reason / rule_version=`method-concepts/v2` /
entity_type=`concept` / is_method=`true` が残る。origin_instance_id=`agent-398-review`、revision=1。
record_idはそれぞれ `iterated-boundary-generation`、`frottage`。

入力candidateはstoreの親ディレクトリの `<slug>-candidate.json`、未充填の生成結果は
`<slug>-template.json`、receiptは `<slug>-receipt.json` に残した。
source-mapと原文snapshotも同ディレクトリにあり、読取hash検証にだけ使用した。
Git保存treeは2 record、2 payload、2 binding、2 operation、2 canonical entityのみ（原文なし）。

## 通した経路

指定Pythonで、1テーマずつ以下の形式の実CLIを実行した（完全なargvはrun-report参照）。

```text
tools/theme_research.py --theme "Iterated Boundary Generation"
  --emit-candidate-template --entity-kind method --method-origin-domain computation
  --method-fixes ... --method-varies ... --method-requires ...
  --creator masa-san-jp --collection issue-398-methods --project-id issue-398
  --origin-instance-id agent-398-review --run-id review-398-iterated-boundary-generation
  --query-log .agent-local/398-queries.jsonl
```

Frottageも同じ経路でorigin_domain=artとして実行。既存exact hitがある反復境界生成は
既存IDを維持し、フロッタージュは `concept/frottage` を新規生成する。
実際に取得した出典から方法欄・statement・source_reads・entityを埋め、payload hashを再計算し、
公開可能な自作の要約として権利を宣言してaccepted候補にした。
`research_knowledge_intake.py prepare` は両方 `VALID`（exit 0）、`commit` は両方
`COMMITTED`（exit 0）。新しいowner entityのfrontmatterを共有KBへ昇格し、本文の出典説明と
`derived_from`を追加した。判定も保存もモデル・daemon・GitHub writeを起動していない。

## 出典と修正判断

- [Sohl-Dicksteinの実験記録](https://sohl-dickstein.github.io/2024/02/12/fractal.html):
  curlで原文取得とbyte範囲のhash確認。2024年は出典の年であり起源年ではない。
  computer-artの使用を裏付けないのでその関係を削除。方法自体は未接続で保持する。
- [ティッセン＝ボルネミッサ美術館のエルンスト解説](https://www.museothyssen.org/en/collection/artists/ernst-max):
  curlで原文取得、紙・凹凸面・鉛筆の記述を確認しhash検証してintake。
  シュルレアリスム期の半自動技法という記述に基づき、運動からの使用関係に出典を付ける。
- [Whitneyの書き起こし](https://whitney.org/media/46248): 工房参加は1936年で、
  poured paintingsは約10年後。1940年代後半のポロックの実践として `1946~` とし、
  手法全体の発明年とはしない。先行作品の「1936〜37」という年記はこのconceptから除いた。
- [MOCAの所蔵作品解説](https://www.moca.org/artworks/number-1): 床の未張りキャンバスへ
  缶から注ぎ棒から飛散させる手順、水平の支持体、抽象表現主義での位置を取得・確認。
  重力や偶然性の制御はこの資料で確認できず、方法欄と本文から削除した。
- [MoMAのマッソン作品解説](https://www.moma.org/collection/works/38201): シュルレアリストの
  自動記述・描画・絵画を取得・確認し、既存automatismとの関係に出典を付けた。
  KBにマッソンの作品entityがないため、作品や個別作品へのエッジは捏造しない。

新規の様式conceptは暗黙に免除しない。方法未記入を許すのは固定legacy 9 IDだけ。
方法判定の運用は一つの版付きconfigを共有し、CLI宣言は1テーマに限定する。

## 測定

`audit.py --methods` の修正前HEADは concept=11、method=3、到達本数=3
（うちcomputer-artの1本は根拠なし）。根拠なしを除いたintake前は11 / 3 / 2。
フロッタージュ昇格後は12 / 4 / 3。元の9 conceptと181 movementは保持し、
反復境界生成は計算由来・出典付きの方法として未接続のまま数える。
合成統合テストはcleanな一時Git fixtureで実storeを使い、候補生成→intake→conceptと
空欄・型違い・判定語彙外の拒否を検証する。実データの確認を合成fixtureで代替しない。
