---
id: movement/bandung-school
uri: urn:ahn:movement/bandung-school
type: movement
kind: retrospective
label_ja: バンドン派
label_en: Bandung School
authority:
  wikidata: Q65214081
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "195X"
  end: null
  display: "1947年（オランダ植民地政庁の認可でバンドン工科大学前身に美術教員養成課程が開設）〜1950年代（アフマド・サダリらインドネシア人第一世代の様式的成立、1954年に名称論争）〜1970年代（スナルヨ・A.D.ピロウスらによる第二世代、DECENTA結成）。「バンドン派」という括りそのものの終期を示す資料は確認できていない"
control_changes:
  - {year: "1959", to: internal, trigger: "西ニューギニア紛争でオランダ人教員が国籍選択を迫られて離任し、同年ITBがインドネシアの国立大学として独立、初世代のインドネシア人卒業生が教員となってカリキュラムと人事を担った"}
founding_control: external   # 1947年の課程開設はオランダ政庁の認可に基づき、初代教員（ミュルダー・アドミラール・ペイパース・ザイレマーカー）は全員オランダ人でカリキュラムもミュルダーが自ら設計した。1949年のインドネシア独立後もオランダ人教員は在任を続け、1959年、西ニューギニア紛争でオランダ人教員が離任すると同時にITBが国立大学として独立し、初世代のインドネシア人卒業生（サダリ・スリハディ・ムフタル・アピンら）が教員となってカリキュラムと人事を担うようになった
naming:
  self_identified: false
  named_by: person/trisno-soemardjo
  named_when: "1954"
  original_label: "aliran Ries Mulder / laboratorium Eropa（Barat）"
  note: "現在通用する「Mazhab Bandung（バンドン派）」という語そのものを最初に使った個人・年は確認できていない。確認できる最初の名づけの行為は、美術批評家トリスノ・スマルジョが1954年、ラジオ番組でバンドン工科大学出身の画家たちの展覧会を批評し「aliran Ries Mulder（ミュルダーの流派）」と呼び、その作風を「laboratorium Eropa（ヨーロッパの実験室）」と評したことである（インドネシア語版Wikipediaは同じ趣旨を『laboratorium Barat（西洋の実験室）』と表現し、年を1953年とする——年について複数の二次資料が1953年説と1954年説に割れる。本KBはスジョコの公開反論の発行日〔1954年12月19日、雑誌シアサット393号〕が確認できることから1954年説を採った）。この名づけは当事者による自称ではなく、批評家による否定的な評価として外部から与えられたものであり、当事者側がバンドン工科大学出身の画家たちを『Mazhab Bandung』と自称した記録は確認できていない"
claims:
  - {field: kind, source: "https://sejarahbersama.id/2021/06/04/kritik-kritik-terhadap-pelukis-pelukis-bandung/", certainty: scholarly}
  - {field: time, source: "https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni)", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Ries_Mulder", certainty: scholarly}
space:
  - {role: originated_in, target: place/bandung}
relations:
  - {type: created_by, target: person/ries-mulder}
  - {type: influenced_by, target: movement/cubism, certainty: scholarly, source: "https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni)"}
sources:
  - https://www.wikidata.org/wiki/Q65214081
  - https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni)
  - https://en.wikipedia.org/wiki/Ries_Mulder
  - https://sejarahbersama.id/2021/06/04/kritik-kritik-terhadap-pelukis-pelukis-bandung/
  - https://historia.id/article/mula-pertentangan-dua-kubu
  - https://en.wikipedia.org/wiki/Bandung_Institute_of_Technology
  - https://www.itb.ac.id/history
  - https://en.wikipedia.org/wiki/Mochtar_Apin
status: draft
updated: 2026-08-09
---

# バンドン派 / Bandung School (Mazhab Bandung)

## 定義と範囲

インドネシアのバンドン工科大学（ITB、[org/itb](../orgs/itb.md)）の美術教育課程を出自とする
一群のインドネシア人画家と、その作風を指す名称。インドネシア語では「Mazhab Bandung」
「Aliran Bandung」「Modernisme Bandung」と表記が揺れる。Wikidata
[Q65214081](https://www.wikidata.org/wiki/Q65214081)（ラベルは"Mazhab Bandung"、インドネシア語版
Wikipediaへのサイトリンクのみを持つ）には `P31`（instance of）も `P571`（inception）も付与されて
おらず、外部典拠としては非常に痩せている。

インドネシア語版Wikipediaは「この派はフォルマリズムの美学概念と同一視される芸術の潮流であり、
バンドン工科大学の美術科の環境で、その創設者リース・ミュルダーがもたらした教育制度の結果として
1950年代に生まれた。その歴史を通じて、この派は明確な定義を持ったことがない」と記す
（[id.wikipedia.org/wiki/Mazhab_Bandung_(seni)](https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni))、
二次情報。原文: 「Mazhab ini lahir di lingkungan Seni Rupa ITB pada tahun 1950-an sebagai akibat
dari sistem pengajaran yang dibawa pendirinya, Ries Mulder... Dalam perjalanan sejarahnya, mazhab
ini belum memiliki pengertian yang tegas」）。作風は、物語性（ナラシオン）から絵画を解放しようとする
点、西洋的な合理性——作品はどのような姿であれ理性によって説明できるという立場——に立つ点に特徴が
あるとされる（同資料）。

### 発端：オランダ人教員による美術教員養成課程（1947年）

第二次世界大戦中、日本軍の抑留所でシモン・アドミラールとリース・ミュルダー
（[person/ries-mulder](../persons/ries-mulder.md)、いずれもオランダ人画家）はバンドンで美術教員を
養成する計画を語り合ったとされる（[Spanjaard, "Bandung, the Laboratory of the West?" in Modern
Indonesian Art, 1945-1990, 1990](https://en.wikipedia.org/wiki/Ries_Mulder)、二次情報）。1947年、
アドミラールはオランダ政庁の許可を得て「Kursus Guru Gambar（素描教員養成課程）」をバンドンで
開始した。この課程は「Fakultas Ilmu Pengetahuan Teknik, Universitas Indonesia（ウニヴェルシタス・
インドネシア工学系学部）」バンドン校地の一部として置かれた
（[en.wikipedia.org/wiki/Ries_Mulder](https://en.wikipedia.org/wiki/Ries_Mulder)）。1948年、
ミュルダーが「教育省」に招かれてバンドンに着任し、絵画・美術鑑賞を教えた（招いた「教育省」が
どの統治機構に属するかは資料上明記されず——**未確認**）。同僚のアドミラール（素描）、ピート・
ペイパース（工芸）、ジャック・ザイレマーカー（装飾素描）とともに教え、教授法はミュルダー自身が
開発したと記される（同資料）。

第一世代——アフマド・サダリ、ブット・ムフタル、スリハディ・スダルソノ、ムフタル・アピン、
ポポ・イスカンダルら——は1950年代にこの課程で育った。当初の作品はフォーヴィスムとキュビスムの
中間に位置するフランスの画家ジャック・ヴィヨンの様式を継承したとされる
（[id.wikipedia.org/wiki/Mazhab_Bandung_(seni)](https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni))）。
1954年、この課程の助手・学生ら11人による立体派的な作品の展覧会がジャカルタで開かれ、大きな論争を
呼んだ（下記「命名と対立」参照）。

### 第二世代（1970年代）とDECENTA

1970年代、スナルヨ、A.D.ピロウス、G.シダルタの3名の影響のもとで「第二世代」が展開したとされる。
3名はキャンパス外に「DECENTA」という実験の場（同資料は「'laboratorium' mazhab Bandung」と表現）を
設立した。第一世代との違いとして、パプアやニアス諸島の伝統的な文様などローカルな美学的資源への
回帰、伝統工芸とフォルマリズムの融合が挙げられる（同資料）。

## kind の判定 — なぜ `retrospective` か

### 名づけの主体：批評家による否定的な評価として始まった

インドネシア語版Wikipediaは「1953年、美術批評家トリスノ・スマルジョ
（[person/trisno-soemardjo](../persons/trisno-soemardjo.md)）が、このITB出身の絵画の流派を指す
独自の呼び名——『aliran Ries Mulder（ミュルダーの流派）』——を持った。彼はこの流派が国民的な
人格性（kepribadian nasional）を持たないとみなし、『laboratorium Barat（西洋の実験室）』として
非難した」と記す（同資料）。より詳細な二次資料は、この批評が1954年、ジャカルタのラジオ局RRIの
番組「Mutu Ilmu dan Seni」でなされ、バレ・ブダヤ（ジャカルタ）での展覧会を対象にしたこと、
2週間後の1954年12月19日発行の雑誌『シアサット』393号（第8年）26–27頁でスジョコが公開書簡形式の
反論を寄せたことを記す
（[sejarahbersama.id](https://sejarahbersama.id/2021/06/04/kritik-kritik-terhadap-pelukis-pelukis-bandung/)、
二次情報。年が1953年か1954年かは資料間で不一致——**未確認**、上記 `naming.note` 参照）。

この名づけは、対象文化（インドネシアの画家集団）の内部からの自称ではなく、外部の批評家が
否定的な評価として与えたものである。当事者側がこの名を積極的に引き受けた記録（新印象派における
シニャックのような、批評家由来の名を後から著書の題名として採用する行為）は確認できていない。
Wikidata上の呼称「Mazhab Bandung」自体がいつ・誰によって、批評的な「aliran Ries Mulder」から
中立的・記述的な学術用語へ転じたのかも確認できていない。

### 「東西論争」の枠組みは、より古い論争の再演として持ち込まれた

バンドン派とジョグジャカルタ派（インドネシア語版Wikipedia に単独の項目は無い——同版の全文検索で
「Mazhab Yogyakarta」に該当する記事は返らない。**未確認**）の対立は、しばしば「バンドン＝西洋美術の実験室」対
「ジョグジャカルタ＝国民的アイデンティティ」という構図で語られる。だが複数の二次資料は、この
対立の起源をインドネシア独立以前、1935年のスタン・タクディル・アリシャバナとサヌシ・パネの
文化論争（西洋文化の摂取を主張するアリシャバナと、インドネシア文化への準拠を説くパネの対立）に
遡って説明する（[historia.id/article/mula-pertentangan-dua-kubu](https://historia.id/article/mula-pertentangan-dua-kubu)、
二次情報）。独立後、この対立の構図が、ジョグジャカルタのASRI（インドネシア美術アカデミー、
伝統的・社会的価値を掲げたとされる）とバンドンのITB出身者（普遍的ヒューマニズムを掲げたが
「西洋かぶれ」とみなされたとされる）という2つの教育機関の対立として再演されたと記される
（同資料）。すなわち「バンドン対ジョグジャカルタ」という枠組み自体、1935年の文化論争を1950年代の
2つの美術教育機関に当てはめ直すという、後知恵の再構成を経て成立している。

さらに1950〜1960年代には、共産主義系の文化団体LEKRA（インドネシア人民文化協会）もバンドンの
絵画を「PERSAGI（インドネシア絵画家連合）」やスニマン・インドネシア・ムダ（SIM）、
プルキサン・ラクヤット（人民画家）の写実主義から逸脱したものとして批判したとされ、対立軸は
「東西」だけでなく「イデオロギー」の軸でも構成されていた（[id.wikipedia.org/wiki/Mazhab_Bandung_(seni)](https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni))）。1960年代の文化緊張期には、バンドン派の
画家たちは共産主義系LEKRAに対抗する「文化宣言（Manifesto Kebudayaan）」派への支持署名という形で
みずからの立場を明確にしたとも記される（同資料）——ただしこれは「Mazhab Bandung」という名称への
自己同一化ではなく、別の政治的な旗印（文化宣言）のもとでの結束である。

### `lineage-school`（師弟の継承体）との近さと、そこで止まらない理由

ミュルダーから第一世代（サダリ、スリハディ、ムフタル・アピンら）へ、さらに第一世代が教員となって
第二世代（スナルヨ、ピロウス、シダルタら）を育てるという流れは、単発の展覧会企画ではなく、
同一の教育機関（ITB美術学科）を通じた世代的な教員―学生の継承であり、`lineage-school`
（血縁・工房・師弟の継承体）の性質に近い。実際、第一世代が後に自らの手でカリキュラムと人事を
担うようになった点（`founding_control` 参照）は、狩野派のような世襲の工房に類する制度的な実体を
思わせる。

しかし`lineage-school`の典型例（狩野派・土佐派）は「家名がそのまま呼称になり、命名という行為が
そもそも存在しない」（`docs/schema.md`）。バンドン派はこれと異なり、明確な「名づけの瞬間」（1954年
前後、批評家による否定的な命名）を持ち、かつ当事者集団がその名を自称した形跡がない。この
名づけの構造——批評家が外部から括りを与え、それが後に学術的な標準用語として定着した——は
`retrospective`の典型例（印象派）にきわめて近い。教育機関を通じた継承という実体は本文に残しつつ、
`kind` は名づけの出自を優先して`retrospective`と判定した。

## 時間

`time.start`は`195X`（1950年代）とした。Wikidata Q65214081には`P571`（inception）が付与されて
おらず、依拠できるのはインドネシア語版Wikipediaの「1950年代に生まれた」という年代のみの記述
（precisionに相当する情報を年単位以上に絞り込めない）。制度としての教育課程自体は1947年に開設
されているが、`retrospective`の`time`は「括られた対象（画家たちの作風・活動）の活動期間」を
示すため（`docs/schema.md`）、教育課程の開設年（1947年）ではなく、その作風が形になった1950年代を
採った。

`time.end`は空欄とした。第一世代の活動（1950年代）に続き、第二世代（1970年代、DECENTA）の存在が
複数資料で確認できるため、少なくとも1970年代までは活動が続いたと見られるが、「バンドン派」という
括りそのものがいつ終わった（あるいは今も続いている）とする資料は確認できていない。

## 空間

`originated_in`は[place/bandung](../places/bandung.md)とした。バンドン工科大学の前身にあたる
美術教員養成課程が置かれた都市であり、参照した二次資料すべてがバンドンを発祥地として扱う。

### ヨーロッパからの受容——動いたのは教師

`influenced_by` を[キュビスム](cubism.md)（europe-west）へ1本張った。**動いたのは人であり、
しかも制度に組み込まれた人である。**

1948年にオランダから招かれた[リース・ミュルダー](../persons/ries-mulder.md)が美術教員養成課程で
教え、その第一世代——アフマド・サダリ、ブット・ムフタル、スリハディ・スダルソノ、ムフタル・アピン、
ポポ・イスカンダルら——が1950年代にこの課程で育った。インドネシア語版Wikipediaは、かれらの当初の
作品が「フォーヴィスムとキュビスムの中間に位置するフランスの画家ジャック・ヴィヨンの様式を継承した」
と記す（[id.wikipedia](https://id.wikipedia.org/wiki/Mazhab_Bandung_(seni))、二次情報）。1954年には
この課程の助手・学生ら11人による**立体派的な作品**の展覧会がジャカルタで開かれ、大きな論争を呼んだ
（同）。

受容の経路が個人の旅行や作品の流入ではなく、**植民地期に設置された美術教育課程そのもの**だった点が
この1本の性格を決めている。批評家トリスノ・スマルジョがこの一派を「laboratorium Eropa（ヨーロッパの
実験室）」と呼んで攻撃したこと（下記「命名と対立」）は、受け手の側がこの経路を制度的な従属として
認識していたことを示す。

**この1本の粗さ**: 出典が名指すのはジャック・ヴィヨン個人の様式であって、キュビスムという括りでは
ない。ヴィヨンはピュトー・グループ／セクション・ドールに連なるキュビスムの画家だが、出典自身が彼を
「フォーヴィスムとキュビスムの中間」と位置づけている。**未確認**: ミュルダー自身がキュビスムを
どのように学び、何を教材としたか。person/ries-mulder の本文でも彼の修業歴は追い切れていない。

## 未着手

- 「Mazhab Bandung」という語そのものを最初に用いた個人・文献。確認できているのは1954年前後の
  批評家トリスノ・スマルジョによる「aliran Ries Mulder」「laboratorium Eropa（Barat）」という
  命名で、現在通用する「Mazhab Bandung」表記への移行時期・行為者は未確認
- 1954年の展覧会（バレ・ブダヤ、ジャカルタ）の正確な開催日、出品作家11名の全員の氏名、
  トリスノ・スマルジョの批評の一次資料（放送台本または掲載紙）
- 1948年にリース・ミュルダーを招いた「教育省」がどの統治機構（オランダ側の連邦国家機構か、
  独立インドネシア共和国政府か）に属していたか。バンドンは当時オランダ軍の実効支配下にあった
  地域であり、独立インドネシア共和国政府（ジョグジャカルタに拠点）とは別の行政機構だった
  可能性が高いが、確認できていない
- ジョグジャカルタ派（Mazhab Yogyakarta）のmovement化。インドネシア語版Wikipediaに単独項目が
  無いため、ASRIジョグジャカルタ側の資料を別に探す必要がある。本調査では「バンドン対
  ジョグジャカルタ」の対立の枠組みだけを、バンドン側の資料から扱った
- PERSAGI（インドネシア絵画家連合）、ASRIジョグジャカルタ、LEKRA、文化宣言（Manifesto
  Kebudayaan）派のmovement化・org化。いずれも本文中で対抗関係として言及したが、関係エッジは
  張っていない
- 第一世代がITBの教員として具体的にいつからカリキュラム・人事の決定権を持つに至ったかの
  正確な年（1959年のオランダ人教員離任と同時か、それ以前から段階的だったか）
- パブリックドメインの画像: Art Institute of Chicago・Metropolitan Museum・Cleveland Museumの
  公開APIで、アフマド・サダリ・スリハディ・スダルソノ・ムフタル・アピン・ブット・ムフタル・
  ポポ・イスカンダル・リース・ミュルダーの名で検索したが、いずれの所蔵館にも該当する作品は
  見つからなかった（2026-08-09時点）。20世紀の画家であり著作権が存続している可能性が高いことも
  あり、`images`は付けていない
