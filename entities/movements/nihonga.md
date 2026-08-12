---
id: movement/nihonga
uri: urn:ahn:movement/nihonga
type: movement
label_ja: 日本画
label_en: Nihonga
authority:
  wikidata: Q1989975
  aat: "300114441"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1882"
  end: null
  display: "1882年（明治15年・フェノロサが龍池会で行った講演《美術真説》で「油絵」と「日本画」を対比させた＝語の初出）〜。語が一般に使われ始めるのは明治20年代末から。終期は無い（大学の専攻区分・展覧会の部門名として現在も使われている）。Wikidata Q1989975 の P571 は 1860・precision 8＝1860年代を指し、語の成立より前を取る"
kind: retrospective
naming:
  self_identified: false
  named_by: person/ernest-fenollosa
  named_when: "1882"
  original_label: "日本画"
  note: "名づけたのは描いた側ではなく、外から来た一人の講師である。中村賢一（セレネ美術館）の論考は『「日本画」という言葉が使われる契機となったのは、明治15年(1882年)に「龍池会」でフェノロサが行った《美術真説》という講演である。この講演でフェノロサは、｢油絵｣と「日本画」を明確に対比させ、「油絵」よりも「日本画」の方が優れていることを説いた』と書き、さらに『つまり「日本画」は、自然と生じたのでもなく、日本人が危機意識から生み出したのでもなく、まずフェノロサという西洋人の眼によって打ち立てられたのである』と結論する。ただし後代の史家による括りではない——名づけられた時、対象となる絵画は同時代に描かれていた。同論考は語の一般化を『明治20年代末から』とする"
claims:
  - {field: kind, source: "http://museums.toyamaken.jp/documents/documents007/", certainty: scholarly}
  - {field: time, source: "http://museums.toyamaken.jp/documents/documents007/", certainty: scholarly}
  - {field: originated_in, source: "https://nihonbijutsuin.or.jp/his_tenshsin.php", certainty: scholarly}
space:
  - {role: originated_in, target: place/tokyo}
  - {role: active_in, target: place/kyoto}
relations:
  - {type: influenced_by, target: movement/yamato-e, certainty: scholarly, source: "https://www.yamatane-museum.jp/en/nihonga/"}
images:
  - url: https://upload.wikimedia.org/wikipedia/commons/4/48/Hishida_Shuns%C5%8D_-_Fallen_Leaves_%28Eisei_Bunko_Museum%29_2.jpg
    source_page: https://commons.wikimedia.org/wiki/File:Hishida_Shuns%C5%8D_-_Fallen_Leaves_(Eisei_Bunko_Museum)_2.jpg
    license: public-domain
    note: "菱田春草《落葉》1909年、永青文庫蔵。Wikimedia Commons の権利表示は Public domain（春草の没年1911年）。輪郭線を引かずに空気の層を描く手つきが1点で見える——これが批判の側から「朦朧体」と呼ばれた描き方で、1903年にインドへ、1900年代後半に東京へ来た中国人留学生を通じて広東へ渡ったのも、この手つきである"
sources:
  - https://www.wikidata.org/wiki/Q1989975
  - https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300114441
  - https://www.yamatane-museum.jp/en/nihonga/
  - http://museums.toyamaken.jp/documents/documents007/
  - https://nihonbijutsuin.or.jp/his_tenshsin.php
  - https://www.wikidata.org/wiki/Q4346814
  - https://amis-musee-cernuschi.org/en/les-liens-artistiques-et-culturels-entre-linde-et-le-japon-vers-1890-1940-2/
  - https://kyoto-museums.city.kyoto.lg.jp/feature-column/painting/
status: draft
updated: 2026-08-10
---

# 日本画 / Nihonga

## 定義と範囲

**片方だけでは意味を持たない語である。** 「日本画」は「洋画（油絵）」と対になって初めて成り立つ。
中村賢一（セレネ美術館）は、大学の専攻区分を数え上げたうえでこう書く——「『洋画』が油絵の具という
画材によって認識されているのに対し、『日本画』は、単純な画材による分類以外のなにかによって
認識されていると考えられる」（[富山県博物館協会・電子紀要「日本画の成立とその名称」](http://museums.toyamaken.jp/documents/documents007/)）。

画材の側から言えば、絹や紙に毛筆で描き、主として岩絵の具（顔料）と膠を用いる。ただし「膠絵」と
呼ぶ大学の学科は無い、と同論考は指摘する。**画材が同じでも「日本画」と呼ばれない絵はあり、
呼ばれる絵の範囲は画材では決まらない。**

## 大和絵との関係

山種美術館は、近世以降の日本の絵画が狩野派・円山四条派・大和絵系の土佐派などの流派で分類され、
西洋画の影響が加わって今日の日本画が成立・発展したと説明している
（[山種美術館「About Nihonga」](https://www.yamatane-museum.jp/en/nihonga/)）。この整理は、近代の
日本画を大和絵そのものと同一視するものではなく、複数の日本の絵画伝統のうち大和絵系統が日本画の
形成に接続したことを示す。そのため、日本画から[大和絵](yamato-e.md)へ `influenced_by` を張る。

Getty AAT の scope note は範囲をかなり狭く取る——"Refers to the work of a school of painters whose
careers spanned the Edo period (1600-1868) to the early part of the Meiji period (1868-1912)."
（[AAT 300114441](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300114441)）。
**これは語の成立の経緯と食い違う。** 語が生まれたのは1882年（明治15年）で、江戸期の画家が
自らをそう呼んだ記録は無い。AAT は画材と技法（鉱物・貝・植物から作る墨や絵具を紙や絹に用いる）を
基準に範囲を取っており、名前の成立を基準にしていない。本項は名前の成立を基準に採った。

## kind の判定

`retrospective` とした。名づけたのが描いた側ではないためである。1882年（明治15年）、龍池会での
講演《美術真説》で、アーネスト・フェノロサ（[person/ernest-fenollosa](../persons/ernest-fenollosa.md)）が
「油絵」と「日本画」を対比させ、油絵より日本画が優れていると説いた。中村はこう結論する——
「つまり『日本画』は、自然と生じたのでもなく、日本人が危機意識から生み出したのでもなく、まず
フェノロサという西洋人の眼によって打ち立てられたのである」（同論考）。

**ただし「後代」ではない。** 名づけられた時、対象となる絵画は同時代に描かれていた。外から来た
批評家が同時代の制作に名を与え、後から当事者と制度がそれを引き受けた形である。語が一般に
使われ始めるのは明治20年代末からで、その後、美術学校の科名・展覧会の部門名として定着した。

**この括りには血縁も工房も無い。** 狩野派や土佐派のような世襲の継承体ではなく、流派を横断する
上位の区分として作られた。だから `lineage-school` は当たらない。

## 担い手と制度

名が定着していく過程は、1つの組織の設立と重なる。日本美術院（[Wikidata Q4346814](https://www.wikidata.org/wiki/Q4346814)、
P571＝1898年10月15日・precision 11＝日単位）である。同院自身の沿革はこう書く——「明治31年、
天心を中傷する怪文書が配布され、いわゆる東京美術学校騒動が起こります。天心は、東京美術学校長の
職を退き、橋本雅邦、横山大観、菱田春草、下村観山らと日本美術院を創設して」
（[公益財団法人 日本美術院](https://nihonbijutsuin.or.jp/his_tenshsin.php)）。

この院に集まった横山大観・菱田春草が試みたのが、輪郭線を引かずに色の層で空気を描く手つきである。
当時これは批判の側から「朦朧体」と呼ばれた。パリのチェルヌスキ美術館友の会は、後にインドへ渡った
この手つきを "their new work of colors without contours to render the atmosphere in colored washes
and gradients: this style is called *Morotai*" と説明する
（[amis-musee-cernuschi.org](https://amis-musee-cernuschi.org/en/les-liens-artistiques-et-culturels-entre-linde-et-le-japon-vers-1890-1940-2/)）。

## 時間

`start` は1882年（語の初出＝フェノロサの講演）。`end` は空欄にした。大学の専攻区分としても
展覧会の部門名としても現在使われており、終わった括りではない。

**Wikidata の値は採らなかった。** `P571` は1860年・precision 8（＝1860年代）で、語の成立より
20年ほど前を指す。何を数えた値かは同項目からは読めない——**未確認**。

## 空間

`originated_in` は東京（[place/tokyo](../places/tokyo.md)）。名づけの場（龍池会の講演）も、
制度化の場（東京美術学校・日本美術院）も東京である。

**未確認**: 京都には円山四条派の系譜を引く別の展開があり、東京だけを発生地とすることが
適切かどうかは、京都側の一次資料に当たっていない。京都市の博物館協会は、明治期の京都府画学校と
竹内栖鳳・上村松園らの京都画壇を近代日本画の展開として説明している（[「日本画の都・京都」](https://kyoto-museums.city.kyoto.lg.jp/feature-column/painting/)）。
したがって、東京を語の成立・制度化の中心である `originated_in` としつつ、京都を近代日本画が活動した
主要地として `active_in` に加える。これは京都側を東京の下位系譜とみなすことではない。

## 外へ出た手つき — 同じ技法が2つの方向へ渡った

この括りは受け取っただけでなく、**送り出した側**として2つの文化圏に繋がっている。関係はどちらも
受け取った側に書いてある。

| 受け取った側 | 年 | 動いたもの |
|---|---|---|
| [ベンガル派](bengal-school.md)（インド） | 1903年 | 人——横山大観と菱田春草がカルカッタに滞在し、墨と筆の技法と朦朧体を伝えた |
| [嶺南画派](lingnan-school.md)（中国・広東） | 1906〜1908年 | 人——高剣父らが東京美術学校に学び、朦朧体の没骨の手つきを持ち帰った |

**どちらも運んだのは人で、運ばれたのは同じ手つきである。** 岡倉天心は1901年末にインドを通過した
際、シスター・ニヴェディタの紹介でラビンドラナート・タゴールに会った。タゴール側の依頼を受けて
岡倉が画家を送り、1903年1月に横山大観と菱田春草がカルカッタに着いたが、当初の仕事（宮殿の装飾）は
中止になった。2人はそのまま滞在し、技法を伝えた。チェルヌスキ美術館友の会は
"This Japanese style marks the first production of the School of Bengal." と書く（同資料）。

## 未着手

- フェノロサ《美術真説》（1882年）の講演記録そのもの。現状は中村論考経由の二次情報
- 「日本画」の語が明治20年代末に一般化した過程の一次資料（展覧会の出品区分・新聞記事）
- 日本美術院を `org` として立てるかどうか。1898年の設立は名の定着と重なる出来事だが、
  この括り全体を代表する組織ではない（京都の系譜も官展も外れる）
- 横山大観・菱田春草の `person` 化。2人はインドへ渡って別の movement に技法を渡しており、
  `docs/schema.md` の作成基準2（2つ以上の movement を繋ぐ）に当たる。今回は movement 間の関係と
  本文の記述に留めた
- 「朦朧体」を `concept` として立てるかどうか。インドと中国へ渡ったのはこの技法そのものであり、
  2つの関係が共有する実体になっている
- 京都側（円山四条派の系譜・竹内栖鳳ら）の個別担い手・制度の整理と、東京を発生地とすることの妥当性
- Japan Search・Web NDL Authorities の典拠ID（2026-08-10 時点で本KBは両者の正しい呼び方を
  確認できていない）
