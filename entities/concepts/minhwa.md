---
id: concept/minhwa
uri: urn:ahn:concept/minhwa
type: concept
label_ja: 民画
label_en: Minhwa
authority:
  wikidata: Q204791
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "17XX"
  end: "19XX"
  display: "朝鮮後期（18世紀）に量産の中心を迎え、19世紀に最盛（京城の市場での活発な流通が確認される）。生産がいつまで続いたかは出典によって幅があり、Met所蔵品には20世紀初頭の作例もある"
space:
  - {role: active_in, target: place/hanseong}
relations: []
sources:
  - https://www.wikidata.org/wiki/Q204791
  - https://encykorea.aks.ac.kr/Article/E0020370
  - https://ko.wikipedia.org/wiki/%EB%AF%BC%ED%99%94
  - https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_r300510&code=kc_age_30
  - https://contents.history.go.kr/mobile/tt/view.do?levelId=tt_b57
  - https://encykorea.aks.ac.kr/Article/E0064832
  - https://www.tongilnews.com/news/articleView.html?idxno=102045
  - https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11077260
  - https://www.metmuseum.org/art/collection/search/929075
  - https://www.metmuseum.org/art/collection/search/853891
  - https://www.metmuseum.org/art/collection/search/853896
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/DP-44213-002.jpg
    source_page: https://www.metmuseum.org/art/collection/search/929075
    license: cc0
    note: "《葡萄とリス》掛軸、朝鮮・17〜18世紀、絹本墨画、作者不明（Metropolitan Museum of Art, Open Access）。花鳥翎毛系の画題で、リスと葡萄の多産・多子の吉祥図像"
  - url: https://images.metmuseum.org/CRDImages/as/original/LC-2024_89_2_at-002.jpg
    source_page: https://www.metmuseum.org/art/collection/search/853891
    license: cc0
    note: "《山神とトラ》、朝鮮・19世紀後半、作者不明（Metropolitan Museum of Art, Open Access）。巫俗・道教系の画題である山神図"
  - url: https://images.metmuseum.org/CRDImages/as/original/DP-40204-001.jpg
    source_page: https://www.metmuseum.org/art/collection/search/853896
    license: cc0
    note: "《冊架と文房具》二曲屏風、朝鮮・19世紀、作者不明（Metropolitan Museum of Art, Open Access）。冊架図（チェッコリ）——儒教的な学問尊重の象徴として飾られた"
status: draft
updated: 2026-08-09
---

# 民画 / Minhwa

朝鮮王朝後期、主に無名の担い手によって量産された、生活の中の装飾・吉祥祈願を目的とする実用的な絵画の総称。
Wikidata [Q204791](https://www.wikidata.org/wiki/Q204791) は "Korean folk art" と記述し、`P31`
（instance of）は「絵画ジャンル」（Q16743958）、`P279`（subclass of）は「韓国画」（Q1187814）。
`P1014`（Getty AAT）は無い。Getty AAT の検索サービス（<https://vocab.getty.edu/sparql.json>）は
2026-08-09 時点で "Service temporarily degraded" を返し確認できなかった——Wikidata の QID が
取れているため `none_reason` は空欄のままとした。

## 空間

民画は特定の都市だけで制作されたものではないが、韓国史資料は18世紀末以降、漢陽の鍾路・廣通橋周辺に
画店が現れ、民間の需要と売買の構造とともに広く流通したと説明する（[우리역사넷「民画」](https://contents.history.go.kr/mobile/tt/view.do?levelId=tt_b57)）。
このため、朝鮮王朝期の漢城（現在のソウル中心部）を主要な活動・流通地として `active_in` に記録する。
これは民画の制作地・受容地が漢城に限られるという意味ではない。

## movement か concept か——担い手の集合を特定できるか

**担い手の集合は特定できない。結論として `concept` とした。** 理由は3つある。

### 1. 担い手が単一の職能・身分に属さない

한국민족문화대백과사전（encykorea）「민화」は、民画の作者層を「도화서 화원과 화원의 제자에서부터
화원이 되지는 못하고 그림에 재주가 있어 사람들의 요구에 따라 그림을 그렸던 화공 그리고 일반
백성들에 이르기까지 다양」（図画署の画員とその弟子から、画員にはなれなかったが絵の才があり人々の
求めに応じて描いた画工、さらに一般庶民に至るまで多様）と記す。加えて「귀족・문인・승려・무당
중에서 재주 있는 사람」（貴族・文人・僧侶・巫堂のうち才のある者）や「시골 장터와 동네를 돌아다니며
낙화・혁필화 등을 그리던 유랑 화가」（田舎の市や村を回って落画・革筆画などを描いた流浪画家）も
含むとする（<https://encykorea.aks.ac.kr/Article/E0020370>、二次情報）。これは
[org/dohwaseo](../orgs/dohwaseo.md) の画員（制度上の職）・その弟子・在野の画工・貴族文人・宗教者・
流浪画家という、身分も職能も互いに重ならない集団の寄せ集めであり、単一の系譜や職業集団として
境界を引けない。

### 2. 担い手のほとんどが個人として特定できない（無名）

encykorea は民画を担った層について「대개 신분이나 사회적 지위가 낮은 사람들이었다」（大半は身分や
社会的地位の低い者たちだった）と記し、우리역사넷「민화」も「주로 조선시대 무명 화가들이…그린
그림」（主に朝鮮時代の無名画家たちが…描いた絵）とする
（<https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_r300510&code=kc_age_30>、二次情報）。
実例として、Metropolitan Museum of Art が所蔵する民画作例3点（本稿の`images`）はいずれも
作者欄が "Unidentified artist"（作者不明）である
（[929075](https://www.metmuseum.org/art/collection/search/929075)、
[853891](https://www.metmuseum.org/art/collection/search/853891)、
[853896](https://www.metmuseum.org/art/collection/search/853896)）。狩野派や真景山水画
（[movement/jingyeong-sansuhwa](jingyeong-sansuhwa.md)、こちらも後代の命名だが鄭敾・沈師正・
金弘道という個々の名は辿れる）と違い、民画は個々の担い手をほとんど名指しできない——
「誰が」ではなく「何のために・どう描かれたか」という手の形の記述に留まる。

### 3. 名づけ自体が「集団」ではなく「用途・様式」を指すものだった

3節（下記「命名」）で見る通り、1959年に柳宗悦が「民画」と名付けた対象は、特定の作者集団ではなく
「民衆の中から生まれ、民衆のために描かれ、民衆によって買われる絵」という**用途と流通の形**である。
1968年の趙子庸（조자용）による再定義も「身分の区別なく全ての朝鮮民族が描いた絵」という、
むしろ担い手を限定しない方向の定義だった（後述）。担い手を絞り込むのではなく、
「誰でも良い・実用のために作られた絵全般」という残余カテゴリーとして機能している点が、
血縁・師弟・制度上の職・自称の綱領のいずれかで境界を引く `movement` とは根本的に異なる。

以上から、`docs/schema.md` の判定基準「担い手の集合が歴史的に特定できるなら movement、
手の形の記述なら concept」に照らして `concept` とした。`concept` には `kind` は無い。

### 図画署との関係——重なりはあるが、境界にはならない

encykorea は広義の民画について「직업 화가인 도화서(圖畫署)의 화원(畫員)이나 화가로서의 재질과
소양을 갖춘 화공(畫工)이 그린 그림도 포함」（職業画家である図画署の画員や、画家としての資質と
素養を備えた画工が描いた絵も含む）とし、「도화서 화원의 절대수가 모자라 이런 화공들의 도움을
받았던」（図画署画員の絶対数が不足していたため、こうした画工の助けを受けた）と記す
（<https://encykorea.aks.ac.kr/Article/E0020370>、二次情報）。すなわち[org/dohwaseo](../orgs/dohwaseo.md)
の画員が余技・副業として民画を手掛けた記録はある。ただし民画の担い手全体からすれば図画署系統は
一部に過ぎず（上記1節）、[movement/jingyeong-sansuhwa](jingyeong-sansuhwa.md) が同種の重なりに
ついて行ったのと同じ判断で、`relations` にエッジは張らず本文の記述に留めた。

## 定義の変遷——命名は当事者ではなく後代の外部者

| 誰 | いつ | 呼称・定義 |
|---|---|---|
| 李圭景『五洲衍文長箋散稿』 | 19世紀（李圭景 1788-1865） | 「俗畵」。「여염집의 병풍・족자나 벽에 붙인다」（庶民の家の屏風・掛軸や壁に貼る）と用途を記す（우리역사넷「민화」経由の二次情報、原典未確認） |
| 柳宗悦（야나기 무네요시） | 1959年、雑誌『民藝』 | 「民画」という語を初めて提案。冊架図（책거리）の民画を見て書いた文章とされる。「민중 속에서 태어나고 민중을 위하여 그려지고 민중에 의해서 구입되는 그림」（民衆の中に生まれ、民衆のために描かれ、民衆によって買われる絵）と定義（<https://www.tongilnews.com/news/articleView.html?idxno=102045>、二次情報。同記事はほかに「민속 회화의 준말」＝民俗絵画の略、という柳の説明も引く） |
| 趙子庸（조자용）／エミレ博物館 | 1968年、エミレ博物館開館 | 定義を拡張。「서민・평민・상민・민중 등 사회 계층이나 신분의 구별 없이 도화서 화원은 물론 모든 한국 민족들이 그린 그림」（庶民・平民・常民・民衆など社会階層や身分の区別なく、図画署の画員はもちろん全ての韓国民族が描いた絵）と再定義した（DBpia論文「19세기 말-20세기 초 민화의 수집・보존 활동과 민화 명칭의 쟁점 검토」<https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11077260> 経由、encykorea「민화」も同旨、いずれも二次情報） |
| 現在の学界 | — | 「民衆の絵」なのか「宮中の彩色画まで含む豪華な絵」なのかで見解が一致しない（同DBpia論文）。同論文の結論は、名称自体は既に定着し代替不能であるとして「民画」の呼称を維持する提案 |

**当事者による自称ではない。** 朝鮮時代当時の呼称は「俗畵」（李圭景）であり、これは「格の低い絵」
という蔑称に近い記述的な呼び方であって、担い手が自らを名乗った流派名・綱領名ではない。「民画」という
語自体は20世紀の日本人評論家（柳宗悦）が外部から与えた名であり、後にエミレ博物館の趙子庸が
韓国側で定義を再編集して定着させた。命名者と当事者が完全に別であるという点で、
[movement/jingyeong-sansuhwa](jingyeong-sansuhwa.md)（真景山水画、命名者個人までは特定できないが
少なくとも同時代・同文化圏内の後代学界による命名）よりもさらに外部性が強い。

**未確認**: 柳宗悦の1959年の文章の正確なタイトル・掲載号（「不可思議한 朝鮮民畵」という題で言及する
記事はあるが、当たった出典はいずれも二次情報で、『民藝』誌そのものの書誌情報には当たっていない）。
李圭景『五洲衍文長箋散稿』の該当箇所の原文。

## 実装例——用途と画題

encykorea「민화」による主題分類は次の9種——화조영모도（花鳥翎毛図）・어해도（魚蟹図）・
작호도（鵲虎図）・십장생도（十長生図）・산수도（山水図）・풍속도（風俗図）・문자도（文字図）・
책가도（冊架図）・무속도（巫俗図）（<https://encykorea.aks.ac.kr/Article/E0020370>）。
共通するのは「감상적 회화성」（鑑賞のための絵画性）よりも「실용적 상징성」（実用的な象徴性）に
重きを置くという手つきで、屏風・掛軸・壁に貼って住まいを飾り、吉祥（長寿・多産・立身・厄除け）を
祈る道具として機能した点である（ko.wikipedia「민화」）。

`images` に挙げた3点はこの分類のうち3つを具体的に示す。

- [Grapevine and Squirrel](https://www.metmuseum.org/art/collection/search/929075)（花鳥翎毛系。
  葡萄とリス＝多産・多子の吉祥図像。朝鮮・17〜18世紀・作者不明）
- [Mountain god with tiger](https://www.metmuseum.org/art/collection/search/853891)（巫俗系。
  山神図——朝鮮固有の山岳信仰とトラ信仰が結びついた図像。朝鮮・19世紀後半・作者不明）
- [Books and Scholarly Accoutrements](https://www.metmuseum.org/art/collection/search/853896)
  （冊架図＝책거리。書斎の文房具・書物を並べて描き、儒教的な学問尊重を象徴する。朝鮮・19世紀・
  屏風・作者不明）

3点とも Metropolitan Museum of Art の Open Access（CC0）で、作者欄はすべて "Unidentified artist"
——上記「担い手が特定できない」という判定を実例として裏づける。

## 使える手

- **主題の語彙は固定された記号の集合として運用されていた。** トラ＝魔除け、カササギ＝吉報、
  牡丹＝富貴、鴛鴦＝夫婦和合、といった約束事の組み合わせで意味を伝える（画題ごとに象徴が対応する
  という構造そのものが、encykorea の9分類に現れている）。作る対象を選ぶとき「何を象徴させるか」を
  先に決め、図像の組み合わせで語らせる手として応用できる。
- **実用（誰の家の何のために飾るか）を先に決めてから様式を選ぶ**、という順序が民画の作られ方に
  近い。鑑賞のための一点物ではなく、用途（結婚祝い・書斎の装飾・厄除け）に対応する画題を当てはめる
  発想は、量産・反復を前提にした制作設計として参照できる。
- **匿名の量産と様式の一貫性は両立する。** 個々の作者が特定できなくても、画題・図像の語彙・
  用途という3つの軸さえ共有していれば、外から見て一つのまとまりとして認識される
  （これが本稿を `concept` として立てた理由そのものでもある）。

## 未着手

- 柳宗悦「不可思議한 朝鮮民畵」（1959、雑誌『民藝』）の書誌情報の一次確認
- 李圭景『五洲衍文長箋散稿』の「俗畵」該当箇所の原文
- 趙子庸のエミレ博物館が用いた画目（화목）20種の一次資料（一部記事が「趙子庸が20種に分類した」と
  触れるのみで、20種の内訳リストそのものには当たっていない）
- Getty AAT・NDL・Japan Search の典拠ID（AAT はサービス degraded で確認不能、NDL・Japan Search は
  `docs/investigation-task.md` が既知の未確認事項として挙げる範囲）
- 民画の生産がいつまで続いたか（20世紀初頭の作例はあるが、朝鮮王朝終焉・日本統治期における
  継続・断絶の一次資料には当たっていない。現代の「民画復興」は生活工芸ではなく現代美術の文脈に
  移っており、本稿の対象からは外した）
- 「俗畵」という当代の呼称が、今日の「民画」と完全に同一の対象を指していたか（DBpia論文が触れる
  「광통교 일대의 속화」という別の文脈があり、風俗画（풍속화）との境界も含めて未整理）
