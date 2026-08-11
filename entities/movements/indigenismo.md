---
id: movement/indigenismo
uri: urn:ahn:movement/indigenismo
type: movement
label_ja: インディヘニスモ
label_en: Indigenismo
authority:
  wikidata: Q5602008
  aat: "300107847"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1919"
  end: null
  display: "1919年（リマ、カサ・ブランデス画廊でのサボガル展「Impresiones del Ccoscco」＝絵画のインディヘニスモの形式的な始まりとされる）〜終期は出典間で一致せず未確定（本文参照）"
kind: retrospective
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "Indigenismo"
  note: "名称の来歴に二段階のねじれがある。①学術資料（Lorenzo 2015）は『インディヘニスモという呼称は、対立した思想潮流イスパニスモ側からの蔑称に由来するにもかかわらず、その名を保持した（conserva ese nombre a pesar de provenir de dichos peyorativos de sus opositores）』と明記する——命名者は特定の個人ではなく反対派（イスパニスモ陣営）一般とされ、named_by は特定できないため null にした。②当事者側の引き受けは、少なくとも二重に確認できる。画家カミロ・ブラス自身が1920年代の心境として『自分の土地と自分の民を描いていた、運動が生まれる前から知らずしてインディヘニスタだった（Pintaba mi tierra y mi pueblo, y sin saberlo era indigenista antes de que el movimiento hubiera surgido）』と後年語ったと伝わる（Zevallos 1991に引用、Villanueva Ccahuana 2021が孫引き、二次情報の孫引き）。サボガル自身も1943年8月21日、リマのレストラン『ラ・カバーニャ』で開かれた歓送会での答辞で『しかし、そうだ、我々は言葉の正しい意味におけるインディヘニスタである、さらに文化的インディヘニスタでもある（somos indigenistas en el justo significado de la palabra, y más aún, indigenistas culturales）』と述べたと複数の二次資料が伝える——ただしこの発言の一次資料（ICAA/MFAH Documents Project item 1140821『Homenaje a José Sabogal』が該当すると推定されるが、Cloudflareの遮断により本KBは本文を直接読めていない）は本KBが直接確認できていない。③一方でカミロ・ブラス自身は1969年、この運動を『誤って「インディヘニスタ」と呼ばれた（mal llamado 'indigenista'）』と後年批判しており、当事者内でも呼称の適否について緊張がある（Villanueva Ccahuana 2021）。以上から、名は外部（反対派）起源だが当事者が後から（1943年時点で明示的に）引き受けたと判断し、self_identified: true・kind: retrospective とした（新印象派の型と同じ構造）"
founding_control: external
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Jos%C3%A9_Sabogal", certainty: scholarly}
  - {field: originated_in, source: "https://www.museoreinasofia.es/en/activities/indigenisms", certainty: scholarly}
  - {field: kind, source: "http://sedici.unlp.edu.ar/handle/10915/151286", certainty: scholarly}
space:
  - {role: originated_in, target: place/lima}
  - {role: created_in, target: place/cusco}
relations:
  - {type: created_by, target: person/jose-sabogal}
  - {type: influenced_by, target: movement/post-impressionism, certainty: scholarly, source: "http://sedici.unlp.edu.ar/handle/10915/151286"}
sources:
  - https://www.wikidata.org/wiki/Q5602008
  - https://www.getty.edu/vow/AATFullDisplay?find=&place=&nation=&logic=&note=&role=&subjectid=300107847
  - https://en.wikipedia.org/wiki/Jos%C3%A9_Sabogal
  - https://en.wikipedia.org/wiki/Indigenismo
  - https://www.wikidata.org/wiki/Q2093376
  - https://www.wikidata.org/wiki/Q5202236
  - https://www.wikidata.org/wiki/Q2868
  - http://sedici.unlp.edu.ar/handle/10915/151286
  - http://sedici.unlp.edu.ar/bitstream/handle/10915/151286/Documento_completo.pdf-PDFA.pdf?sequence=1
  - https://revistas.javeriana.edu.co/index.php/cma/article/view/villanueva
  - https://www.museoreinasofia.es/actividad/indigenismo-1-redes-vanguardia-amauta-america-latina-1926-1930/
  - https://www.museoreinasofia.es/en/activities/indigenisms
  - https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/sabogal-jose-1888-1956
  - https://repositorio.pucp.edu.pe/items/d84354b6-20b8-4ce4-8553-a1a2d27dd1bc
  - https://icaa.mfah.org/s/en/item/1140821
status: draft
updated: 2026-08-10
---

# インディヘニスモ / Indigenismo

## 定義と範囲

**本エントリの範囲**: 「インディヘニスモ（indigenismo）」という語は、ラテンアメリカ全域にまたがる
社会・政治思想／文学／美術を横断する広い「潮流（corriente）」を指す（Wikidata
[Q5602008](https://www.wikidata.org/wiki/Q5602008)「trend in social and political thought, visual
arts, and literature in Latin American countries」、Getty AAT
[300107847](https://www.getty.edu/vow/AATFullDisplay?find=&place=&nation=&logic=&note=&role=&subjectid=300107847)
のスコープノートも同様に「ラテンアメリカにおける20世紀前半の運動」として社会・政治的側面を中心に
記述する）。本KBの型は`movement`＝「集合的な芸術実践の括り」であり、政治思想そのものは範囲外である
（`docs/schema.md`）。したがって本エントリは、この広い潮流のうち**絵画（美術）の担い手の集合として
特定できる部分**——ペルー・リマの国立美術学校（Escuela Nacional Superior Autónoma de Bellas Artes、
以下ENBA、Wikidata [Q5202236](https://www.wikidata.org/wiki/Q5202236)、1918年設立）を拠点に
ホセ・サボガル（[person/jose-sabogal](../persons/jose-sabogal.md)）が主導した絵画運動——に範囲を
絞って記述する。

**地理的範囲**: ペルー中心か否かは出典で確認した。学術書（Lorenzo, C. H. 2015.「Indigenismo:
vanguardia peruana」. In: Rueda, M. de los Ángeles [comp.], *Revoluciones, apropiaciones y críticas
a la modernidad*. La Plata: EDULP, pp. 112-121）はこの絵画潮流を明確に「ペルーの前衛（vanguardia
peruana）」として扱い、クスコ（1909年の大学改革を機に自文化再評価が始まった地）とリマ（ENBA設立
1918年、サボガル展1919年）をペルー国内の二つの結節点として記述する。同時に、隣国エクアドルにも
エドゥアルド・キングマン、オスワルド・グアヤサミン、カミロ・エガス、ディオヘネス・パレデスらによる
並行した絵画のインディヘニスタ潮流が1930年代から存在したことが複数の二次資料で確認できる。
メキシコにおける「インディヘニスモ」は、本KBでは政治・民族学的な潮流として別に扱われ（Wikidata
[Q21010090](https://www.wikidata.org/wiki/Q21010090)「Indigenismo in Mexico」）、美術面では
[メキシコ壁画運動](mexican-muralism.md)が既に別の`movement`として立っている。この2つは同時代に
接触があった（後述）が、担い手の集合が異なる別々の運動であり、本KBでは統合しない。**未確認**:
エクアドルの絵画インディヘニスモを独立の`movement`として立てるかどうかは、今回は範囲外として
見送った（詳細は「未着手」）。したがって本エントリの`space.originated_in`は**ペルー（リマ）**に
限定し、地理的にはペルーを中心とした運動として扱う。

## kind の判定

### ①官職・工房・師弟の継続

**部分的にある。** ENBAは1918年に設立された国立の美術学校で、狩野派の奥絵師のような世襲の官職では
ないが、サボガルは1920年に教員として着任し、1932年（学術資料によっては1933年）から1942年
（学術資料によっては1943年）まで校長を務めた。この教育上の地位を通じて、フリア・コデシード、
テレサ・カルバリョ、エンリケ・カミノ・ブレント、カミロ・ブラス（本名ホセ・アルフォンソ・
サンチェス・ウルテアガ）、アリシア・ブスタマンテらの画家を直接育て、彼らが「サボガルの教えを
受け入れ」インディヘニスモの画家群として認識されるに至った（Villanueva Ccahuana, P. S. 2021.
「Cuestionamiento al indigenismo plástico peruano: el caso de Camilo Blas en la década de 1920」.
*Cuadernos de Música, Artes Visuales y Artes Escénicas* 16(2): 250-263、学術論文・二次情報）。
これは血縁ではなく師弟の継承体であり、`docs/schema.md`のlineage-school定義（「血縁・工房・師弟の
継承体。制度としての実体を持つ」）の一部に文字どおり当てはまる。ただし、ENBA自体はサボガル以前
から存在し彼の解任（1942/43年）後も存続する一般的な国立美術学校であり、「インディヘニスモという
派」と「ENBAという制度」は一致しない——制度の継続は担い手側の継承体というより、後述する
`founding_control`の論点（国の美術教育機関を誰が主導したか）に近い。

### ②血縁の継続

**無い。** サボガルと彼が育てた画家たちの間に血縁関係の記録は無い。

### ③様式的同一性

**ある。** 出典間でおおむね一致する特徴として、アンデスの先住民の風貌・伝統衣装を主題とし、太い
筆致（trazos gruesos）、厚塗り（empastes）、単純化され調和的な色彩、静的で量感のある人物表現が
挙げられる（前掲Lorenzo 2015、および「Definición del Indigenismo Pictórico Peruano」の複数の
二次資料）。サボガルはスペイン滞在時にイグナシオ・スロアーガ、バレンティン・スビアウレ、
エルメネヒルド・アングラダ・カマラサといった地方主義・後期印象派の画家から作風の影響を受けており
（前掲Lorenzo 2015）、この様式的な語彙を教員としてENBAの弟子たちに直接伝えた。ただし学術的な批判
（前掲Villanueva Ccahuana 2021）は、この「様式的同一性」が実際には内部で一様ではなかったことを
示す——カミロ・ブラスの1920年代の作品《Fiesta andina, La cashua》（1924年）は、当時の「インカ的
理想化された過去の先住民」という支配的な図像から離れ、同時代の「アメスティサヘ（混血化）」した
先住民を描いており、この違いは当時「インディヘニスタ」という一枚のレッテルの下に均されて
不可視化されたと論じられる。

このため本項では、サボガルの形成期とENBAを通じた継承に限って `influenced_by movement/post-impressionism`
を記録する。これはペルーのインディヘニスモ全体の画家が後期印象派を共有した、あるいはアンデスの
主題が欧州様式へ置き換えられたという主張ではない。関係の対象は、スペインでの具体的な画家との接触と、
そこから弟子へ移った様式語彙である。

### 判定 — `retrospective`

`naming`欄で詳述したとおり、「インディヘニスモ」という名称そのものは対立する思想潮流イスパニスモ
側からの蔑称に由来し、当事者側がその名を後から（サボガル自身の場合は少なくとも1943年の答辞という
形で明示的に）引き受けた、という構造が学術資料（前掲Lorenzo 2015）で確認できる。これは
`docs/schema.md`が新印象派を例に説明する型——「外部が付けた名を当事者が後から引き受けた場合は
self_identified: true かつ kind: retrospective」——と同じ構造である。①②③の実体（師弟の継承・
様式の共有）は確かに存在するが、それらを束ねる**名前**の成立過程が外部起源である以上、`kind`は
その名前の成り立ちを基準に`retrospective`と判定した。

## founding_control の判定 — 誰が「先住民」を語ったか

`founding_control`（設立・所有・意思決定への対象文化の外部者の構造的関与）を`external`と判定した。

この運動が主題として掲げた「対象文化」は、アンデスの先住民（ケチュア語を話す農民層）である。
一方、この運動の主導者・担い手・決定機関はいずれも非先住民のクリオージョ／メスティーソの都市
知識人層で占められていた。

- **サボガル自身がスペイン系であり先住民ではない**（[英語版Wikipedia「José Sabogal」](https://en.wikipedia.org/wiki/Jos%C3%A9_Sabogal)、
  出典はCongdon & Hallmark『Artists from Latin American Cultures』2002、二次情報）
- サボガルが育てた中心的な画家群（コデシード、カルバリョ、カミノ・ブレント、ブラス、ブスタマンテ）
  について、いずれかが先住民出自であったとする記録は本KBが当たった出典の範囲では見つからなかった
- 運動を主導したもう一人の知的指導者、クスコ大学の指導者ルイス・エドゥアルド・バルカルセルも
  非先住民の知識人エリートであり、1914年のクスコ歴史研究所開設演説で「ケチュア語の純粋性の保存」
  を掲げるなど、先住民文化を**外側から**理想化・体系化する立場を取った（前掲Villanueva Ccahuana
  2021が引用するDe la Cadena 2004の分析、学術論文・二次情報経由）
- 学術論文（前掲Villanueva Ccahuana 2021）は、この時代のリマの知的言説を「クリオージョの二分法的
  言説（discurso dicotómico criollo）」と呼び、芸術上の主張が「インディオかクリオージョか」という
  一つの型に押し込められ、先住民自身の声がこの言説の構築過程に構造的に参加していなかったことを
  論じる

**留保**: この判定には二つの限界がある。第一に、`founding_control`が想定する典型（Papunya Tula／
Pita Maha、`docs/schema.md`）は「自国民／外国人」という国籍の外部性を測る軸だが、この運動では
サボガルもバルカルセルも同じペルー国民であり、「外部性」は国籍ではなく**民族・階級の外部性**
（都市クリオージョ／メスティーソのエリート vs. アンデス先住民農民層）として現れる。この意味の
ずれを踏まえたうえで`external`と判定した。第二に、Villanueva Ccahuana(2021)自身が「インディオか
クリオージョか」という二分法そのものを批判的に検討しており（カミロ・ブラスの作品を「メスティーソ
化した現代の先住民」を描いたものとして再評価する論旨）、当時の人種・文化的アイデンティティは
この二分法が示すほど単純ではなかった可能性がある。

## 時間

`time.start`は`1919`とした。1918年末にクスコから戻ったサボガルが同地で描いた油彩約40点を、1919年
リマのカサ・ブランデス画廊で「Impresiones del Ccoscco」として発表した展覧会が、絵画のインディヘニ
スモの形式的な始まりとして複数の出典で一致して扱われる（[英語版Wikipedia「José Sabogal」](https://en.wikipedia.org/wiki/Jos%C3%A9_Sabogal)、
Jane Turner編『The Dictionary of Art』1996年v.24、509頁からの引用経由、前掲Lorenzo 2015、いずれも
二次情報）。マドリードのレイナ・ソフィア国立芸術センター（国立美術館）が2019年に開催した企画
「Indigenismos. Arte y diferencia en América Latina」も、1919年を歴史的前衛運動の指標年として
明示的に位置づけている（[museoreinasofia.es](https://www.museoreinasofia.es/en/activities/indigenisms)、
機関情報）。

`time.end`は確定できず`null`のままにした。出典間で運動の終わりの捉え方が大きく割れている。

- 前掲Lorenzo(2015)は「インディヘニスタとイスパニスタの論争は1940年代に終わる（La polémica entre
  Indigenistas e Hispanistas termina en los años '40）」とする
- サボガルのENBA校長辞任は1942年（前掲Lorenzo 2015）または1943年（英語版Wikipedia、Jane Turner
  1996年経由）と出典間で年が割れ、複数の二次資料はこの解任を「イスパニスタ的な公式美術からの
  排除」と結びつけて記述する
- 一方、Getty AATのスコープノートはこの潮流を「ラサロ・カルデナス大統領期（1934-1940、メキシコ）
  に影響力を強めた」と記述し、より広い政治潮流としては1940年代以降も続いたことを示唆する

**未確認**: 単一の終了年。絵画運動としての実質的な終わりを数える基準（サボガルの公職離脱か、
様式的影響力の減衰か、より広い社会思想としてのインディヘニスモの終わりか）で出典の前提自体が
異なっており、当たった出典の範囲では一致点を見出せなかった。

## 空間

`originated_in`はリマ（[place/lima](../places/lima.md)）とした。根拠は、絵画のインディヘニスモの
形式的な始まりとされる1919年の展覧会がリマのカサ・ブランデス画廊で開催されたこと、および運動の
制度的な拠点（ENBA、および1926年創刊のホセ・カルロス・マリアテギの雑誌『アマウタ』——サボガルは
その芸術ディレクターを務め、創刊号の表紙図案を手がけた）がいずれもリマにあったことによる
（[museoreinasofia.es](https://www.museoreinasofia.es/actividad/indigenismo-1-redes-vanguardia-amauta-america-latina-1926-1930/)、
機関情報）。

`created_in`にクスコ（[place/cusco](../places/cusco.md)、本KBに既存の`movement/cusco-school`の
発生地として置かれたstub）を加えた。サボガルが1919年展のもとになる約40点の油彩を実際に制作した
のはクスコ滞在中（1918年末〜）であり、前掲Lorenzo(2015)は「クスコこそが自文化再評価が最初に現れた
場所（Es en Cuzco donde aparecen las primeras revalorizaciones de las tradiciones autóctonas）」
だとし、1909年のクスコ大学改革をその背景として挙げる。**この運動を「複数起源」（`docs/schema.md`の
件数集計上の特別扱い）として扱うかどうかは判断が割れる**が、本KBでは「制作の場」（クスコ）と
「運動として公に立ち上がった場・その後の制度的拠点」（リマ）を役割で分け、`originated_in`は
後者一つに絞った（メキシコ壁画運動がSEP庁舎の所在地メキシコシティ一つに`originated_in`を絞った
先例に合わせた）。

## メキシコ壁画運動との関係 — 出典は「並行」を支持し「影響」を支持しない

[メキシコ壁画運動](mexican-muralism.md)との接触は史実として存在する。サボガルは1922年にメキシコを
訪れ、ディエゴ・リベラ、ホセ・クレメンテ・オロスコ、ダビッド・アルファロ・シケイロスと接触した
（[英語版Wikipedia「José Sabogal」](https://en.wikipedia.org/wiki/Jos%C3%A9_Sabogal)、Jane Turner
1996年経由、二次情報）。また1926年創刊の雑誌『アマウタ』には、サボガルとリベラの両者が寄稿者として
名を連ねている（[museoreinasofia.es](https://www.museoreinasofia.es/actividad/indigenismo-1-redes-vanguardia-amauta-america-latina-1926-1930/)、
機関情報）。

**しかし本KBが当たった学術資料は、この接触を「影響」として一方向に結ぶ主張に慎重、あるいは
明確に否定的である。** リマの美術館MALIを典拠に前掲Lorenzo(2015)は「サボガルの企図は、社会主義
リアリズムやメキシコ壁画運動の政治化から大きく隔たった美学に特徴づけられる（el proyecto de
Sabogal está marcado por una estética muy alejada del Realismo socialista o de la politización del
Movimiento Muralista Mejicano）」と明記する。別の学術論文（Malca, L. C. 2008.「La nación del
Indigenismo sabogalino」. *Summa Humanitatis*〈PUCP〉）も、ペルーの絵画インディヘニスモとメキシコ
壁画運動を「比較対象」として並置し、ペルー側をメキシコに従属させる読み方を明示的に退けている
（両者は類似した衝動を異なる歴史的条件のもとで独立に生んだ、という趣旨）。

以上から、`relations`に`influenced_by`（メキシコ壁画運動→インディヘニスモ）を張ることは見送った。
**同時代に接触があったという理由だけでは張らない**という方針（`movement/antropofagia`の未来派の
扱いに合わせた）に加え、ここでは学術資料自体が「影響」の主張に否定的であるため、関係を明示的に
張らないことにも根拠がある。1922年の接触という史実と、その解釈をめぐる学術的な対立は、この節に
事実として残す。

## 未着手

- サボガル自身の1943年の答辞（「somos indigenistas...」）の一次資料。ICAA/MFAH Documents Project
  の該当項目（<https://icaa.mfah.org/s/en/item/1140821>、タイトルから該当転記と推定）はCloudflare
  による遮断で本KBは本文を直接読めていない。現状は複数の二次資料の一致のみに依拠している
- カミロ・ブラスの1969年の発言（「José Sabogal, guía y maestro」、Gamma誌）の一次資料。運動の名称
  への当事者内の批判（「mal llamado 'indigenista'」）の直接確認
- エクアドルの絵画インディヘニスモ（エドゥアルド・キングマン、オスワルド・グアヤサミン、カミロ・
  エガス、ディオヘネス・パレデス）を独立の`movement`として立てるかどうか。ペルーの運動と接続する
  `diffused_to`で繋ぐか、無関係な別の運動として扱うかの判断は今回は範囲外とした
- ホセ・カルロス・マリアテギ（雑誌『アマウタ』編集主幹、思想的指導者）の`person`化。`docs/schema.md`
  の作成基準（kind/time/originated_inの根拠になる／2movementを繋ぐ／作品を分解して読んだ）のどれに
  も単独では当たらないため、本文に名前を書くのみに留めた
- ルイス・エドゥアルド・バルカルセル（クスコの知的指導者）の`person`化。同上の理由で見送った
- パブリックドメインの図版。Art Institute of Chicago（CC0）・Metropolitan Museum（Open Access）・
  Cleveland Museum（CC0）のオープンAPIをサボガル／カミロ・ブラスで検索したが、権利が明確な該当
  作品を確認できなかった（Metropolitan Museumにカミロ・ブラスの版画1点がヒットしたが
  `isPublicDomain: false`で画像も無い）。`images`は空のままにした
- 単一の終了年の確定。統計的・様式的にどの基準で「終わり」を数えるかという出典間の前提の違いを
  解消する一次資料には当たっていない
- サボガル校長就任・退任の正確な年（1932/1933年、1942/1943年で出典が割れる）の一次資料での確定
