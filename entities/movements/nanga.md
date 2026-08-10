---
id: movement/nanga
uri: urn:ahn:movement/nanga
type: movement
kind: retrospective
label_ja: 南画
label_en: Nanga
authority:
  wikidata: Q2928221
  aat: "300018580"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "17XX"
  end: "1887~"
  display: "江戸中期（18世紀前半）に興り、明治20年（1887）の東京美術学校開設で「旧派」として制度上排除されるまで。個々の担い手（富岡鉄斎、1924年没）の活動はそれ以降も続いた"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: 南画
  note: "『南画』という呼称そのものの定着は幕末から明治にかけて（日本語版Wikipedia「南画」、二次情報）。より古い語『文人画』（中国の文人画に由来し、専門画工に対する在野の文人の余技としての絵画を指す語）が先にあり、『南画』はそのうち中国・南宗画の系統を継ぐものを指す語として後から定着した。当事者（池大雅・与謝蕪村ら18世紀の担い手）が自ら『南画』または『文人画』という語で群れを名乗った一次的記述は見つかっていない。英語版Wikipediaは担い手たちが自らを『literati（文人）』とみなしていたと記すが、これは学者・知識人としての自己認識であり、絵画の一括りとしての群れの名称そのものではない——この区別のため self_identified は false とした"
claims: []
space:
  - {role: originated_in, target: place/kyoto}
  - {role: active_in, target: place/tokyo}
relations:
  - {type: influenced_by, target: person/dong-qichang, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Nanga_(art)"}
sources:
  - https://ja.wikipedia.org/wiki/南画
  - https://ja.wikipedia.org/wiki/文人画
  - https://en.wikipedia.org/wiki/Nanga_(art)
  - https://www.wikidata.org/wiki/Q2928221
  - https://www.metmuseum.org/art/collection/search/671023
  - https://www.artic.edu/artworks/185222
images:
  - url: https://www.artic.edu/iiif/2/637a65fa-a6f2-8a9f-a6f4-98fcffe2ec92/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/185222
    license: public-domain
    note: "池大雅《地蔵尊への集団参詣（Group Pilgrimage to the Jizo Nun）》1755-65年頃、シカゴ美術館蔵（is_public_domain: true）"
  - url: https://images.metmuseum.org/CRDImages/as/original/DP704972.jpg
    source_page: https://www.metmuseum.org/art/collection/search/671023
    license: cc0
    note: "与謝蕪村《山野跋渉図屏風（Travels through Mountains and Fields）》1765年頃、メトロポリタン美術館蔵（isPublicDomain: true）"
status: draft
updated: 2026-08-10
---

# 南画 / Nanga

## 定義と範囲

江戸中期以降、専門の絵師集団（狩野派・土佐派など）とは別に、文人（士大夫の余技として画を描く在野の
知識人）を自任する者たちが描いた絵画。中国の南宗画（文人画）を模範としつつ、北宗画や大和絵など他の
要素も取り込んで日本独自の様式に展開した（日本語版Wikipedia「南画」、二次情報）。

典拠: Wikidata [Q2928221](https://www.wikidata.org/wiki/Q2928221)（`description(ja)`:
「江戸中期以降の画派、画様」）／Getty AAT `300018580`。

初期の担い手として祇園南海（1676-1751）・柳沢淇園（1704-1758）・彭城百川が挙げられ、池大雅
（1723-1776）・与謝蕪村（1716-1784）の世代で様式が確立したとされる（日本語版Wikipedia「南画」、
二次情報）。

## kind の判定 — なぜ `retrospective` か

狩野派（幕府の奥絵師という官職の世襲）・土佐派（朝廷の絵所預）のような、集団全体を覆う血縁や官職は
南画に無い。担い手は各地に散った在野の文人で、専門画工の工房制度の外に位置する——この点は
`entities/movements/wu-school.md`（中国・呉派）の在野の文人という立場と同じ構造である。

師弟関係は存在するが部分的で、集団全体を束ねる一本の鎖ではない。たとえば与謝蕪村の門人であった
松村呉春は、のちに円山応挙の様式へ転じて独自の四条派を興している
（[movement/maruyama-shijo-school](maruyama-shijo-school.md)）——師弟の線が集団の同一性を保証しない
好例である。世代を超えて手本を慕う「私淑」的な継承（`movement/rinpa` に見られる型）も、南画では
直接的な師弟関係と併存していたと考えられるが、一次資料での裏付けはこれから。

集団を実質的に束ねているのは、**中国の文人画・南宗画を模範とする様式・理念の共有**である。清代の
画譜（『芥子園画伝』など）や渡来した黄檗僧・商人を通じて中国の様式が伝わり（日本語版Wikipedia
「南画」、二次情報）、担い手たちはそれを模範として自らの絵画観・技法を組み立てた。この構図は
浙派・呉派の kind 判定（様式的同一性が実質的な束ねの軸）と同じ形をとる。

呼称そのものについても、「南画」という語の定着は幕末から明治にかけてで（同記事）、池大雅・与謝蕪村
らが活動した18世紀半ばよりも後代である。これは印象派・ポスト印象派型の「後代に外部が名付けた」
パターンに近い。ただし新印象派のように「後から当事者が名乗りを引き受けた」という一次的記述は
見つかっていない——むしろ明治20年（1887）の東京美術学校開設では「旧派」として排除の対象になって
おり（同記事）、後継の担い手が積極的に「南画」を名乗りとして引き受けたのか、外部から一貫して
そう呼ばれ続けただけなのかは未確認のままである。

以上、（1）制度・血縁による集団全体の束ねが無い、（2）師弟関係は部分的で集団の同一性を保証しない、
（3）様式・理念の共有が実質的な括りの軸、（4）呼称自体が担い手の活動期より後代に定着——という
組み合わせから `retrospective` と判定した。

**違和感**: 「文人」という自己認識（学者・知識人としての立場）は当事者自身が持っていたとされる
（英語版Wikipedia）。集団としての名乗りではなく個人の思想的立場としての自己認識であり、
`self-declared`（宣言文・機関誌を伴う運動）とは性質が違うと判断したが、この境界線は狩野派の
「家名がそのまま呼称になっており命名という行為が存在しない」型とも異なる、南画に固有の迷いとして
記録しておく。

## 時間

Wikidata Q2928221 には `P571`（inception）・`P576`（dissolved）の claim が無い——時間軸は個々の
担い手の生没年から組み立てた。祇園南海（1676-1751）を最初期の担い手としつつ、日本語版Wikipediaが
「江戸中期以降」と記すことから、`start` は世紀精度の `17XX`（18世紀）とした。**未確認**: 南海の
文人画としての制作活動が具体的に何年から始まったかの一次資料には当たっていない。

`end` は明治20年（1887）の東京美術学校開設——南画が「旧派」として制度上排除された年——を目安に
`1887~`（およそ）とした。ただし富岡鉄斎（1837-1924）は「最後の南画家」ともされ、個人としての活動は
それ以降も続いた（英語版Wikipedia「Nanga (art)」）。**未確認**: 「集団としての活動終期」と
「最後の個人の没年」のどちらを `end` に取るべきかは、記事間で記述が一致しておらず一次資料の
裏も取れていない——琳派の宗達・光琳のような「私淑」型の継承がどこまで南画にも当てはまるかが
未整理なため、`1887~` は仮の値として置いた。

## 空間

日本語版Wikipediaは京都を中心とした上方（京阪以西）と、後発の江戸の二大中心地があったと記す
（二次情報）。これに沿って `originated_in` を京都（[place/kyoto](../places/kyoto.md)）、
`active_in` を江戸（現在の東京、[place/tokyo](../places/tokyo.md)）とした。

**未確認**: 「上方」は京都・大坂を含む広域の呼称で、単一都市への発生地の特定は一次資料での裏が
取れていない。祇園南海自身は紀州藩（現在の和歌山県）に仕えた儒者で、江戸で学び紀州で活動しており、
単純な「京都発祥」に収まらない広がりを持つ——この地理的な複数性は本文で明記するにとどめ、
`space` には主要な2地点のみを置いた。

## 未着手

- `movement/literati-painting`（中国側の文人画・南宗画）への `influenced_by` — 対象のエンティティが
  このKBにまだ無いため（他の調査が並行して作成中）、`person/dong-qichang` への関係で代替した。
  対象movementが揃ったら、より直接の movement 間の関係として張り直せる可能性がある
- 桑山玉洲（クワヤマ・ギョクシュウ、1746-1799）——英語版Wikipediaによれば董其昌の理論・文人理念を
  日本の文人画家に適用するよう説いた理論家で、「日本の董其昌」とも評される。`docs/schema.md` の
  person 作成基準への当てはまりを検討する余地があるが、一次資料未確認のため今回は本文言及のみに
  留めた
- 池大雅・与謝蕪村の person エンティティ化——images の根拠として名前と生没年をリンクで示したが、
  作品を分解して読む・movement 間を繋ぐ、のいずれの基準にも今回は届いていない
- 松村呉春を介した円山四条派との関係（師弟→分岐）——`relations` の語彙（`precedes` か
  `derives_from` か）の選定を含めて一次資料で詰めていない
- 「南画」という呼称の命名者・命名年（`naming.named_when`）
- 発生地の複数性（京都／大坂／江戸）を `space` にどう反映するか
