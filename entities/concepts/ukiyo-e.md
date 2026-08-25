---
id: concept/ukiyo-e
uri: urn:ahn:concept/ukiyo-e
type: concept
label_ja: 浮世絵
label_en: Ukiyo-e
authority:
  wikidata: Q185905
  aat: "300106769"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "16XX"
  end: "19XX"
  display: "Wikidataのinceptionは+1700-00-00T00:00:00Z / precision 7で、Wikidata自身の描画は「17. century」（1601〜1700年）。実証的な起点は1670年代、菱川師宣が一枚絵として独立させた段階とするのが定説。Getty AAT（300106769）は江戸時代（1600〜1868年）に紐づけて記述するが、ja.wikipediaは明治40年（1907年）の新聞記事が「衰微」を報じつつなお存続していたこと、大正期まで絵草紙屋が存在したことを記しており、実際の生産・流通は幕末以降も続いた。終期は資料によって幅があり確定できない"
space:
  - {role: active_in, target: place/tokyo}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q185905"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300106769"
    kind: authority
  - url: "https://ja.wikipedia.org/wiki/浮世絵"
    kind: reference
  - url: "https://en.wikipedia.org/wiki/Ukiyo-e"
    kind: reference
  - url: "https://www.wikidata.org/wiki/Q2297646"
    kind: authority
  - url: "https://www.wikidata.org/wiki/Q3066195"
    kind: authority
  - url: "https://www.wikidata.org/wiki/Q1335478"
    kind: authority
  - url: "https://www.artic.edu/artworks/19016"
    kind: institutional
  - url: "https://www.artic.edu/artworks/22935"
    kind: institutional
  - url: "https://www.artic.edu/artworks/24645"
    kind: institutional
images:
  - url: https://www.artic.edu/iiif/2/23ad9eea-241f-3af9-df38-875ba8825591/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/19016
    rights_source: https://www.artic.edu/artworks/19016
    license: cc0
    note: "菱川師宣「Flower-Viewing Party with Crest-Bearing Curtain」（連作「上野花見の体（Ueno hanami no tei）」より）、c.1681-84年、墨摺絵（sumizuri-e）。シカゴ美術館蔵（is_public_domain: true）。浮世絵最初期、単色摺りの段階"
  - url: https://www.artic.edu/iiif/2/dadabea0-c07e-b5b7-f39e-f877d31bb1b4/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/22935
    rights_source: https://www.artic.edu/artworks/22935
    license: cc0
    note: "鈴木春信「Beauty Under an Umbrella in the Snow」（雪の中で傘をさす美人、日本語の慣用タイトルは未確認）、c.1770年、多色摺りの錦絵（nishiki-e）。シカゴ美術館蔵（is_public_domain: true）。1765年前後に確立した多色摺り技法の段階"
  - url: https://www.artic.edu/iiif/2/b3974542-b9b4-7568-fc4b-966738f61d78/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/24645
    rights_source: https://www.artic.edu/artworks/24645
    license: cc0
    note: "葛飾北斎《神奈川沖浪裏》「冨嶽三十六景」より、1830-33年頃。シカゴ美術館蔵（is_public_domain: true）。19世紀、名所絵（風景画）へ主題が拡大した段階"
status: draft
updated: 2026-08-09
---

# 浮世絵 / Ukiyo-e

江戸時代の17世紀後半に成立した、木版画を中心媒体とする日本の絵画ジャンル。美人画・役者絵・名所絵・
相撲絵など、同時代の風俗・娯楽を主題とする。Wikidata [Q185905](https://www.wikidata.org/wiki/Q185905)
は`P31`（instance of）に「art genre」（Q1792379）と「art movement」（Q968159）を併記し、`P279`
（subclass of）は「Japanese art」（Q603399）とする。Getty AAT `300106769`は"Record Type: concept"
として登録され、階層はStyles and Periods facet配下の「Japanese printmaking styles」（日本の版画様式）
に位置づけられる（[getty.edu/vow/AATFullDisplay](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300106769)、
英語、二次情報）。

## 浮世絵は movement か concept か——担い手の集合を特定できるか

**担い手の集合は単一の系譜として特定できない。結論として `concept` とした。** 理由は3つある。

### 1. 浮世絵の内部に、それぞれ独立した継承を持つ複数の「派」が並立する

鳥居派・懐月堂派・勝川派・喜多川派・歌川派など、浮世絵を制作した集団は単一の系譜ではなく、それぞれ
独自の師弟継承を持つ派に分かれていた（分業と併せて後述「実装例」）。歌川派・鳥居派・勝川派はいずれも
Wikidataで独立したQIDを持つ（歌川派 [Q2297646](https://www.wikidata.org/wiki/Q2297646)、鳥居派
[Q3066195](https://www.wikidata.org/wiki/Q3066195)、勝川派 [Q1335478](https://www.wikidata.org/wiki/Q1335478)）。
歌川派の英語記述は「one of the main schools of ukiyo-e」（浮世絵の主要な派の1つ）とする。つまり
「浮世絵」という語自体が、複数のmovement候補（各派）を束ねる上位区分として機能している。狩野派
（[movement/kano-school](kano-school.md)ではなく本KBの
[entities/movements/kano-school.md](../movements/kano-school.md)）のような単一の血縁・工房ではなく、
独立した継承体の集合であり、担い手を1本の系譜として特定できない。

### 2. Getty AATが自ら「concept」と分類し、「複数の派による様式の分化」を明記する

Getty AAT 300106769は"Record Type: concept"（レコード種別そのものがconcept）であり、Note欄は
「Distinctive genre in painting and other media...built up a broad popular market among the
middle classes...Distinctive styles and specialties in subject matter were developed by
different schools throughout the period」（絵画などのメディアにおける独自のジャンル…中間層に
広い大衆市場を築いた…この期間を通じて、複数の派によってそれぞれ異なる様式・専門分野が発展した）
と記す（前掲URL、英語、二次情報）。狩野派に付いた"family"のような血縁集団を示す分類は、浮世絵には無い。

### 3. 制作体制も単一の作者ではなく分業であり、様式的同一性の軸は「手つき（生産様式）」にある

浮世絵を束ねているのは「同じ絵師の系譜」ではなく、版元・絵師・彫師・摺師による分業という**生産の型**
と、遊里・芝居・美人・名所という**主題の型**である（詳細は「実装例」）。これは
[movement/indochina-lacquer-painting](../movements/indochina-lacquer-painting.md)で③様式的同一性を
「素材と技法」で測った型に近く、担い手ではなく手つきで束ねる`concept`の性質に合致する。

以上から、`docs/schema.md`の判定基準「担い手の集合が歴史的に特定できるなら movement、手の形の記述なら
concept」に照らして`concept`とした。`concept`には`kind`は無い。歌川派・鳥居派・勝川派など個々の派は、
それぞれ独立した師弟継承を持つため、将来は個別の`movement`として立てられる候補だが、本稿では作成して
いない（1タスク1件の原則、かつ孤児stubを増やさない原則のため）。

## 定義の変遷

### 語源と初出

「浮世」は、平安時代初期の「憂し」に由来する仏教的な「憂き世」（この世は苦しく辛い、という無常観）が
語源。平安末期に「浮き世」の表記が現れ、中世末〜近世初頭にかけて「享楽的に生きるべき世」という逆の
意味に転じたとされる（[ja.wikipedia「浮世絵」](https://ja.wikipedia.org/wiki/浮世絵)、二次情報、
原典未確認）。

「浮世絵」という語自体の初出は、1681年（延宝9年）刊の俳書『それそれ草』に見える「浮世絵や　下に
生いたる　思ひ草」という句とされる（同、二次情報、原典未確認）。1826年（文政9年）の『柳亭記』には
「浮世絵は今様絵なり」との説明があり、この時点で既に一般に通用する語として扱われている（同、二次情報）。

### 自称ではなく、当初は並存していた複数の呼称の1つ

浮世絵の始祖とされる菱川師宣（1618?-1694）は、自らの落款に「日本絵師」「大和絵師」と記しており、
「浮世絵師」を名乗った記録ではない（同、二次情報）。1681年の時点で「浮世絵」という語は俳諧の中に
既に登場していたが、これは当事者（絵師・版元）が自派の呼称として掲げた宣言的な名ではなく、同時代の
口語・文芸の中で対象（当世の風俗を描いた絵）を指すために自然発生的に定着していった語と見られる。
この点は、命名者・命名時期が特定できる後代の学術用語（[movement/rinpa](../movements/rinpa.md)
——尾形光琳の名から後代に作られた呼称）とは性質が異なる。**浮世絵は「後付けの学術用語」ではなく、
対象が制作されていた同時代（少なくとも1681年時点）から並行して存在した呼称**である一方、
**個々の絵師が自派の名乗りとして掲げた語でもない**——movementの`naming.self_identified`のような
二値には収まらない位置にあり、これも`concept`として立てた判断を補強する。

**未確認**: 菱川師宣自身、または当時の版元が「浮世絵」の語を自らの仕事を指す語として使った一次資料
（広告文・奥付など）には到達していない。

## 実装例

### 分業体制——絵師1人による制作ではない

浮世絵の木版画は、単一の作者ではなく**版元・絵師・彫師・摺師の分業**で成り立つ。ja.wikipediaは
「商業資本たる版元の企画の下での、絵師（作画）、彫師（原版彫）、摺師（印刷）の分業体制が確立」と
明記し、各工程を次のように記す（[ja.wikipedia「浮世絵」](https://ja.wikipedia.org/wiki/浮世絵)、
二次情報）。

- **版元**: 企画を立案し、絵師に作画を依頼する（資金の出し手でもある）
- **絵師**: 墨線のみの版下絵を描く
- **彫師**: 版下を版木に裏返して貼り、主版を彫る。色指定された校合摺りをもとに色版も彫る
- **摺師**: 版木に墨・顔料を摺り込み、初摺りを摺る（馬楝を用いる）

英語圏の記述も同じ分業を確認する。"Artists rarely carved their own woodblocks for printing;
rather, production was divided between the artist, who designed the prints; the carver, who
cut the woodblocks; the printer, who inked and pressed the woodblocks onto handmade paper;
and the publisher, who financed, promoted, and distributed the works."（[英語版Wikipedia
「Ukiyo-e」](https://en.wikipedia.org/wiki/Ukiyo-e)、二次情報）。**絵師の名前だけが今日まで
伝わっているが、実際の制作は4者の分業だった。**

### 幕府の出版統制——庇護ではなく規制

寛政2年（1790年）、版行される浮世絵に検閲済みを示す「改印」を要することを定めた制度が始まり、明治
5年（1872年）まで続いた（[ja.wikipedia「浮世絵」](https://ja.wikipedia.org/wiki/浮世絵)、二次情報）。
英語版Wikipediaも"A law went into effect in 1790 requiring prints to bear a censor's seal of
approval to be sold. Censorship increased in strictness over the following decades...From 1799
even preliminary drafts required approval."と記す（二次情報）。

寛政の改革（1787-1793年頃）では、市井の美人の実名を絵に記すことを禁じる触れが出された。天保の改革
（1841-1843年）では、色摺りを7、8回までに制限し、1枚の値段を16文以下に規制した（『藤岡屋日記』の
引用として「16文の値段では売れば売るほど赤字になった」との記述がある、同、二次情報）。具体的な処罰
の例として、喜多川歌麿は『絵本太閤記』（豊臣秀吉を描いた作品）の出版により1804年に手鎖50日の刑を
受け、歌川国芳の「源頼光公館土蜘作妖怪図」は天保の改革下の贅沢禁止を揶揄しているとの噂が立ち、版木が
削られた（同、二次情報）。英語版Wikipediaも、1801年に歌川派の複数の絵師（豊国を含む）の作品が発禁に
なった例、1804年に歌麿が投獄された例を挙げる（二次情報）。

**これは庇護ではなく規制である。** 本KBの関係語彙（`created_by` `belongs_to` `member_of` `part_of`
`depicts` `exhibited_at` `precedes` `taught_by` `documented_in` `influenced_by` `responds_to`
`derives_from` `reacts_against` `grouped_as` `diffused_to` `patronized_by`）の中に、検閲・出版統制
そのものを指す語は無い。`patronized_by`は資金・地位を与える庇護の関係を指し、統制は逆に表現を
制約する力であるため、これを`patronized_by`として書くのは意味を反転させることになる。該当する
関係語彙が無いため、`relations`にはエッジを張らず、本文の記述としてのみ残した。

### 様式と主題の変化——時間の中でどう振る舞うか

浮世絵を束ねる③様式的同一性は「単一の視覚的な様式」ではなく、**木版画という媒体・分業という生産
様式・遊里や芝居など当世風俗という主題**の組み合わせであり、この組み合わせ自体が時期によって変化する。

- **17世紀後半**: 墨一色の「墨摺絵」。菱川師宣が一枚絵として独立させた（[英語版Wikipedia](https://en.wikipedia.org/wiki/Ukiyo-e)
  は"The earliest ukiyo-e works emerged in the 1670s, with Hishikawa Moronobu's paintings and
  monochromatic prints of beautiful women"と記す。師宣は1672年から作品に署名した最初の絵本作者とも
  される）
- **1765年前後**: 鈴木春信らにより多色摺りの「錦絵」が確立し、彩色が版木の重ね摺りで可能になった
  （本稿`images`の《雪の中で傘をさす美人》c.1770年がこの技法にあたる）
- **19世紀前半**: 主題が美人画・役者絵中心から、葛飾北斎・歌川広重らによる名所絵（風景画）へ拡大した
  （本稿`images`の北斎《神奈川沖浪裏》1830-33年頃）

歌川派・鳥居派・勝川派・喜多川派などの内部の「派」は、それぞれこの共通の生産様式・主題の型の上で、
役者絵に特化する（鳥居派）、大首絵を開発する（勝川派）など独自の専門化を遂げた（[英語版Wikipedia](https://en.wikipedia.org/wiki/Ukiyo-e)、
二次情報）。

## 空間

浮世絵の中心は**江戸**（現在の東京）である。菱川師宣以降の主要な絵師・版元の大半は江戸で活動し、
歌川派・鳥居派・勝川派・喜多川派もいずれも江戸を拠点とした。上方（京都・大坂）にも独自の浮世絵
（上方浮世絵、主に役者絵）が存在したことが知られているが、本稿では一次資料に当たれておらず
**未確認**のまま残す。

このKBにはまだ`place/tokyo`も`place/edo`も存在しない。江戸→東京という改称・改編を伴う土地をどう
`place`として置くか（同一の場所として1つのIDにするか、時代で分けるか）は未決の論点のため、本稿では
新しい`place`を作らず`space`を空のままにした。

## 使える手

- **企画・原案・仕上げを分離する生産モデル**（版元＝企画、絵師＝線画、彫師＝再現、摺師＝仕上げ）は、
  量産を前提にした制作の設計として転用できる。絵師の役割を「最終画面の全工程を担う」から「線画という
  中間成果物を渡す」役割に絞り込むことで、他の工程の専門性を最大化できる
- **主題を型として反復運用する**（役者絵・美人画・名所絵という決まった画題のバリエーションとして
  量産する）手つきは、[concept/minhwa](minhwa.md)の「主題の語彙を固定された記号の集合として運用する」
  型と同種で、量産・反復を前提にした制作設計に応用できる
- **規制の中での様式的な工夫**（天保の改革下での色数・値段の制限にもかかわらず、歌川国芳のように
  諷刺を隠して制作を続けた例）は、制約条件下でも表現を継続する手として参照できる

## 未着手

- 歌川派・鳥居派・勝川派・喜多川派・懐月堂派などを個別の`movement`（`kind: lineage-school`が有力）
  として立てる作業。本稿はこれらを束ねる上位の`concept`として立てたのみで、各派の系譜・時間・空間は
  未着手
- 上方（京都・大坂）の浮世絵の一次資料への到達
- 菱川師宣・鈴木春信・葛飾北斎らのperson化（現状は本文に名前を書くのみ）
- Web NDL Authorities: `id.ndl.go.jp`の検索APIに「浮世絵」でクエリしたところ、
  `docs/investigation-task.md`が既知の課題として挙げるSPARQLパーサエラー
  （"Could not properly handle "浮世絵" in ARC2_SPARQLPlusParser"）が発生し、確認できなかった
- Japan Search: 未着手
- Getty AATの`vocab.getty.edu`のJSON APIは「Service temporarily degraded」で確認できず、
  `getty.edu/vow/AATFullDisplay`のHTML経由で内容を確認した（本文中に引用）
- 浮世絵の終期の確定。Getty AATは江戸時代（1600〜1868年）に紐づけるが、ja.wikipediaは明治40年
  （1907年）の新聞記事や大正期までの絵草紙屋の存在を記しており、実際の生産・流通は幕末以降も続いた
  可能性が高い。どこまでを「浮世絵」の範囲とし、どこから「新版画」など後継のジャンルとして区別する
  かは一次資料での裏取りが必要
- **place をどう置くか（`place/edo` / `place/tokyo`の扱い）は aiko-art の判断待ち**
- 「浮世絵」という語を当事者（絵師・版元）自身がいつから自称として用いたかの一次資料（現状は菱川
  師宣が「日本絵師」「大和絵師」と署名したという二次情報の記述からの推論のみ）
