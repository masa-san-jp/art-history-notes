---
id: movement/utagawa-school
uri: urn:ahn:movement/utagawa-school
type: movement
kind: lineage-school
label_ja: 歌川派
label_en: Utagawa school
authority:
  wikidata: Q2297646
  aat: "300018662"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "178X"
  end: null
  display: "18世紀後半（1780年代、歌川豊春による創始）〜終期は未確認。Wikidataのinceptionは+1900-00-00 / precision 7で、Wikidata自身の描画は「19. century」（1801〜1900年）の主張だが、豊春（1735-1814）の現存作（Art Institute of Chicago蔵『Perspective Picture of a Kabuki Theater』c.1776年）や初代豊国の現存最初期作（同館蔵、c.1787年）と整合しない"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: 歌川
  note: "「歌川」は血縁ではなく、一門の長が技量を認めた弟子に授与した家名・画号で、弟子自身がその名を落款に署名して名乗った（自称の実質を持つ）。一方、これを「歌川派」という一括りの呼称でいつ・誰が最初に呼んだか（当時の自称か後代の呼称か）は英語圏・日本語圏の資料に明記が見当たらず未確認。self_identifiedはあくまで「歌川」という名自体の引き受けを指す"
claims:
  - {field: time, source: "https://www.artic.edu/artworks/15804", certainty: scholarly}
  - {field: originated_in, source: "https://www.wikidata.org/wiki/Q1490", certainty: hypothesis}
  - {field: kind, source: "https://kunisada-and-kabuki.fitzmuseum.cam.ac.uk/themes/kunisadas-names", certainty: scholarly}
space:
  - {role: originated_in, target: place/tokyo}
  - {role: active_in, target: place/tokyo}
relations:
  - {type: part_of, target: concept/ukiyo-e}
images:
  - url: https://www.artic.edu/iiif/2/22e03cc0-d3cb-26e5-c024-167f8e22c55f/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/15804
    license: cc0
    note: "歌川豊春《Perspective Picture of a Kabuki Theater（浮絵 歌舞伎芝居之図）》c.1776年。シカゴ美術館蔵（is_public_domain: true）。西洋の透視図法を取り入れた「浮絵」で、歌川派創始者・豊春の初期作にあたる"
  - url: https://www.artic.edu/iiif/2/d338babb-13b0-77ab-b86d-56065ec9ff88/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/24248
    license: cc0
    note: "初代歌川豊国《Yamatoya: Iwai Hanshiro IV as Okaru, from the series Portraits of Actors on Stage（役者舞台之姿絵）》1795年。シカゴ美術館蔵（is_public_domain: true）。「豊国」の名を最初に名乗った代の役者絵で、この名跡がのちに国貞（三代豊国）へ襲名される"
  - url: https://www.artic.edu/iiif/2/6792ccb2-bd96-b6a3-f144-242fd2d1530a/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/11229
    license: cc0
    note: "歌川国芳《Snake (Mi): Nitan Shiro, from the series Heroes for the Twelve Animals of the Zodiac（勇武見立十二支）》c.1840年。シカゴ美術館蔵（is_public_domain: true）。国貞と並ぶ豊国門下の大勢力で、武者絵を得意とした系統の作例"
sources:
  - url: "https://www.wikidata.org/wiki/Q2297646"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300018662"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Utagawa_school"
    kind: reference
  - url: "https://ja.wikipedia.org/wiki/歌川派"
    kind: reference
  - url: "https://kunisada-and-kabuki.fitzmuseum.cam.ac.uk/themes/kunisadas-names"
    kind: institutional
  - url: "https://toshidama.wordpress.com/2018/07/06/the-utagawa-lineage-in-japanese-prints/"
    kind: reference
  - url: "https://www.artic.edu/artworks/15804"
    kind: institutional
  - url: "https://www.artic.edu/artworks/24248"
    kind: institutional
  - url: "https://www.artic.edu/artworks/11229"
    kind: institutional
  - url: "https://www.wikidata.org/wiki/Q1490"
    kind: authority
status: draft
updated: 2026-08-09
---

# 歌川派 / Utagawa school

## 定義と範囲

18世紀後半に歌川豊春が興し、幕末から明治にかけて浮世絵の中で最大の勢力となった一門。
Getty AAT [300018662](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300018662)
は「School or style associated with a group of artists surrounding Utagawa Toyoharu, including
Hiroshige. The Utagawa School was influential and was the most popular print house in 19th
century Japan.」と記す（英語、二次情報）。歌川国貞（三代豊国）・歌川国芳という二大系統を筆頭に、
歌川広重も豊春門下の豊広の弟子として一門に連なる。英語版Wikipediaは「より半数以上の現存する浮世絵
版画がこの派に帰属する」（"more than half of all surviving ukiyo-e prints"）と記す（二次情報）。

## kind の判定 — なぜ `lineage-school` か、そして「名跡の襲名」はどこに置くか

### 継承の実体は血縁ではなく、工房・一門としての制度

歌川派は狩野派のような血縁の家系ではない。ja.wikipediaは「弟子入りした後に技量が認められれば、
歌川一門に正式に認められ、長が歌川姓と名乗りを与え」たと記す（[ja.wikipedia「歌川派」](https://ja.wikipedia.org/wiki/歌川派)、
二次情報）。英語圏の記述もこれを裏づける。Toshidamaのブログ記事（浮世絵専門の二次情報）は
「They were obviously not related by blood or marriage and the names they used are honorary
and titular… one master or teacher conferring his title on a favoured pupil and so on.」と
明記する（[toshidama.wordpress.com](https://toshidama.wordpress.com/2018/07/06/the-utagawa-lineage-in-japanese-prints/)、
二次情報）。つまり「歌川」という姓・名乗りは血縁ではなく、**師が弟子の技量を認めて授与する称号**
であり、その意味で `lineage-school`（血縁・工房の継承体）の「工房」側の実体に当たる。狩野派の
「家」に対して、歌川派は「名（な）」で結ばれた集団である。

### 画号の襲名——継承の線の語彙のどれに当たるか

この調査でいちばん重要な論点として、「豊国」という画号（名跡）の継承を具体的に追う。

Fitzwilliam美術館の学術キャプション（[kunisada-and-kabuki.fitzmuseum.cam.ac.uk](https://kunisada-and-kabuki.fitzmuseum.cam.ac.uk/themes/kunisadas-names)、
英語、二次情報だが美術館の研究記述）は次のように記す。

1. 国貞の最初の名「Kunisada（国貞）」は、1807年、師である初代豊国（1769-1825）から
   「bestowed on him at the start of his career」（キャリアの初めに授与された）。
   → **継承の線の語彙（血縁／師の指名／両方／制度上の職／庇護の枠）で言えば明確に「師の指名」**。
   師が存命のまま、弟子個人に新しい名を与える単純な形。
2. 1825年に初代豊国が没すると、名跡「豊国」は空位になった。これを継いだのは
   **豊国の娘婿（son-in-law）である豊重**で、1825年から1835年（豊重の没年）まで「豊国」を
   名乗った。娘婿という続柄は血縁そのものではないが、婚姻による擬似的な血縁の線であり、
   継承の線の語彙のうち「血縁」に最も近いが厳密には血縁ではない。
3. 豊重の死から9年後の1844年、**国貞が「Kunisada changing to Toyokuni II」と署名して
   「豊国」の襲名を宣言した**。Fitzwilliamの記述によれば、これは
   「he rejected the use of the name by Tokokuni's son-in-law Toyoshige」——**国貞が豊重の代を
   正統と認めず、自分を（豊重を数えずに）「豊国二代目」と自称した**行為である
   （現在の通説では豊重＝二代目豊国、国貞＝三代目豊国と数える。この食い違い自体が
   Fitzwilliamの記述に明記されている）。

この3段階を継承の線の語彙（血縁／師の指名／両方／制度上の職／庇護の枠）に当てはめると、
1は「師の指名」にきれいに収まるが、2〜3は当てはまらない。2は血縁ではなく婚姻による継承、3に至っては
**名跡の前の保持者が存命でも指名した記録でもなく、空位になってから約19年後に、有力な元弟子が
自らの判断で名跡を名乗り直した**——師による指名でも血縁でも、既存の五語彙のどれでもない。

**これは日本の伝統芸能・工芸に広く見られる「名跡（みょうせき）の相続」という別の継承形式に近い。**
歌舞伎役者の名や落語家の名、茶道の家元の名のように、名前そのものが個人から独立した
「地位・ブランド」として存在し、誰が継ぐかが単一の権威者の生前の指名だけでは決まらず、
血縁・婚姻・弟子筋・当人の実力と市場での認知が絡み合って（時には空位期間を挟んで、時には
当事者同士の主張が食い違ったまま）事後的に確定していく。歌川派の「豊国」の継承はこの型に
当てはまり、**このKBの現行の継承の線の語彙（血縁／師の指名／両方／制度上の職／庇護の枠）の
どれか1つには収まらない。新しい種類（例えば「名跡の相続」）が要ると考える**。ただし、これは調査対象の
事実についての判断であり、スキーマの語彙を実際に増やすかどうかはこの調査の範囲外の決定なので、
ここでは事実として記録するにとどめる。

### `kind` 自体は `lineage-school`

上記のとおり継承の線は複合的だが、歌川派全体としては**一門という制度としての実体**を持ち、
師弟間で名と技量が受け渡されていく点で狩野派・土佐派と同じ構造にある。当事者が唱えた宣言文を
持つ運動（`self-declared`）でも、外部が後から括った様式（`retrospective`）でもなく、
王朝に紐づく様式（`period-style`）でもない。よって `kind: lineage-school` とした。

## 時間

- Wikidata Q2297646 の `P571`（inception）は **+1900-00-00 / precision 7**。Wikidata自身の
  描画は「19. century」（1801〜1900年）で、これは初代豊国が没した1825年よりも後の期間まで
  含む主張になり、史実と整合しない。**未確認**: この値が何を根拠にしているかは辿れていない。
- 一方、Art Institute of Chicagoの所蔵作品データでは、創始者・豊春の現存作
  [《Perspective Picture of a Kabuki Theater》](https://www.artic.edu/artworks/15804)が
  c.1776年、初代豊国の現存最初期作が[c.1787年](https://www.artic.edu/artworks/23350)と
  記録されており、いずれも18世紀後半に活動していたことを示す。二次情報のブログ記事も
  「Toyokuni I was active in the 1780's」とする（[toshidama.wordpress.com](https://toshidama.wordpress.com/2018/07/06/the-utagawa-lineage-in-japanese-prints/)）。
  これらを踏まえ `178X`（1780年代）とした。**未確認**: 一門としての創始を明確に画す一次資料
  （宣言・門人帳の類）には到達していない。豊春自身の作画開始（1770年代）と、教育者として
  弟子を取り一門を成した時期は同一ではない可能性がある。
- 終期は**未確認**のため `null` とした。「豊国」の名跡が国貞（三代豊国）以降も継承されたか、
  一門としての実質的な解体がいつかは一次資料に到達していない。

## 空間

`space` は既存の `place/tokyo`（旧称・江戸を `former_names` に持つ）を参照した。歌川豊春・豊国・
国貞・国芳のいずれも江戸で活動しており、[concept/ukiyo-e](../concepts/ukiyo-e.md)の空間記述
（江戸が中心）と一致する。**未確認**: 発生地を「江戸」と断定できる一次資料までは到達しておらず、
`claims` の `originated_in` は `certainty: hypothesis` とした。

## 西欧へ渡った先

この一門の版画を受け取った側として、2つのフランスの括りが `influenced_by` を張っている。どちらも
関係は受け取った側に書いてある。

| 受け取った側 | 何が渡ったか | 書いてある場所 |
|---|---|---|
| [ポスト印象派](post-impressionism.md) | ファン・ゴッホがパリで購入した版画。うち広重の2図を1887年に油彩で模写した | [同項](post-impressionism.md#日本の版画がパリへ運ばれた経路) |
| [印象派](impressionism.md) | モネのジヴェルニーの家に残る浮世絵243点のうち、広重が48点で最多 | [同項](impressionism.md#日本の版画との接続--壁に掛かっていた48枚) |

どちらの経路も広重（歌川豊広の弟子）を通っている。**この一門の側にこの往来の記録は無い**——
渡った先の美術館とコレクションの記録から辿れるだけで、送り出した側の帳面（版元の輸出記録など）は
本KBでは押さえていない。

## 未着手

- 豊春・初代豊国・国貞（三代豊国）・国芳・広重の `person` エンティティ化。特に国貞と豊重の
  「豊国」襲名をめぐる対立は、2つの movement（あるいは同一 movement 内の分岐）を繋ぐ事実として
  `person` を作る条件（`docs/schema.md` の条件2）に当たる可能性があるが、本稿では未着手
- 「歌川派」という一括りの呼称が当時の自称か後代の呼称かの一次資料での確認
- `naming` の語彙に「名跡の相続」に類する第5の種類が要るかどうかの検討（本稿の `## kind の判定`
  に事実として記録したのみで、スキーマ自体は変更していない）
- 国芳門下からの分岐（武者絵の系統）や、広重の風景画への展開を `diffused_to` として張る作業
- 「豊国」の名跡が三代（国貞）以降どこまで継承されたか（四代・五代豊国）の裏取り
- Web NDL Authorities・Japan Search: `docs/investigation-task.md` が既知の課題として挙げる
  問題（SPARQLパーサエラー等）のため未着手
