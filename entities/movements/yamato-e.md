---
id: movement/yamato-e
uri: urn:ahn:movement/yamato-e
type: movement
kind: period-style
label_ja: 大和絵
label_en: Yamato-e
authority:
  wikidata: Q597365
  aat: "300018589"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "08XX"
  end: null
  display: "Getty AAT は様式としての分岐を9世紀半ばに置くが、語「やまと絵」の文献上の初出は長保元年（999年）10月30日（藤原行成の日記『権記』）。両者は指しているものが違う可能性がある（後述）。終期は特定できず null"
naming:
  self_identified: true
  named_by: null
  named_when: "0999"
  original_label: やまと絵
  note: "後付けの学術用語ではなく、対象が制作されていた同時代（少なくとも999年時点）から当事者（宮廷・貴族社会）が使っていた語。ただし語義は一定ではない——平安時代は「日本の物語・人物・風物を主題とした絵画」という画題の概念で、対義語の「唐絵」は中国の主題を描いた絵を指した（様式・技法の話ではない）。14世紀以降に「様式」を指す概念へ転じ、唐風を基本に据えつつ北宋以降の中国画様式も部分的に取り込んだ伝統的様式を指すようになった（ja.wikipedia「大和絵」、二次情報、秋山光和『平安時代世俗画の研究』に拠るとされるが該当文への脚注番号の対応は確認できていない）"
claims:
  - {field: kind, source: "https://www.getty.edu/vow/AATFullDisplay?find=Yamato-e&logic=AND&note=&english=Y&subjectid=300018589", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/45428"}
sources:
  - url: "https://www.wikidata.org/wiki/Q597365"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=Yamato-e&logic=AND&note=&english=Y&subjectid=300018589"
    kind: authority
  - url: "https://ja.wikipedia.org/wiki/大和絵"
    kind: reference
  - url: "https://en.wikipedia.org/wiki/Yamato-e"
    kind: reference
  - url: "https://www.metmuseum.org/ja/essays/yamato-e-painting"
    kind: institutional
  - url: "https://www.metmuseum.org/art/collection/search/45428"
    kind: institutional
  - url: "https://www.tnm.jp/modules/r_free_page/index.php?id=570&lang=en"
    kind: institutional
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/DP244667_CRD.jpg
    source_page: https://www.metmuseum.org/art/collection/search/45428
    license: cc0
    note: "《北野天神縁起絵巻》（Illustrated Legends of the Kitano Tenjin Shrine）鎌倉時代・13世紀末。メトロポリタン美術館蔵（isPublicDomain: true）。ja.wikipedia「大和絵」が鎌倉時代の社寺縁起絵の代表例として同作を名指しで挙げている"
status: draft
updated: 2026-08-13
---

# 大和絵 / Yamato-e

## 定義と範囲

**「唐絵（からえ）」との対でしか成り立たない語である。** 片方だけを取り出しても意味を持たない。
平安時代の大和絵は、画題（何を描いたか）についての概念で、日本の故事・人物・事物・風景を主題とした
絵画を指した。対義語の唐絵は、唐（中国）の故事・人物・事物・山水を主題とした絵を指し、この段階では
様式・技法の違いを意味していなかった。障子絵・屏風絵のような大画面の絵画について使われた語で、
絵巻や冊子の絵は別に「紙絵」と呼ばれていた（[ja.wikipedia「大和絵」](https://ja.wikipedia.org/wiki/大和絵)、
二次情報）。

14世紀以降、語義が変わる。唐絵（漢画）が宋以降の中国画の技法そのもの、あるいは日本に輸入された
中国画自体を指す語になったのに合わせ、大和絵の側は唐風を基本に置きつつ北宋以降の中国絵画の様式も
部分的に取り込んで確立された伝統的絵画様式を指す語に転じた。この頃、土佐派のように大和絵を専門と
する流派が現れ、流派を指す語としても使われるようになった（同、二次情報。原資料は秋山光和
『平安時代世俗画の研究』とされるが、この記述に対応する脚注番号は ja.wikipedia の版では確認できず、
**未確認**）。

メトロポリタン美術館は、室町期には中国から新しい水墨画の様式が入り、古典的な大和絵と競合したと
説明している（[Yamato-e Painting](https://www.metmuseum.org/ja/essays/yamato-e-painting)）。さらに東京国立
博物館は、鎌倉時代・1299年の一遍上人絵伝について、伝統的な大和絵に中国の宋代絵画の伝統の影響が
融合した作例と説明する（[東京国立博物館「Three Friends of Winter」](https://www.tnm.jp/modules/r_free_page/index.php?id=570&lang=en)）。
この個別作例は中国・宋代絵画という広い伝統との接点を示すが、本KBの
`movement/song-academy-painting` は宋代の宮廷画院に対象を限定しているため、現段階では同movementへの
直接エッジは張らず、接触・融合の文脈として記録する。

Getty AAT の scope note は "first used in the mid-9th century to describe the works produced by
Japanese artists that differed at first in subject matter, and latter in style, from paintings
produced under Chinese influence" と書き、9世紀半ばという時期を挙げる一方、対象の広がりについては
"the present day usage of the term has taken on a much broader meaning, encompassing not only
Japanese themes, but also formats and styles considered to be uniquely Japanese" とする
（[Getty AAT 300018589](https://www.getty.edu/vow/AATFullDisplay?find=Yamato-e&logic=AND&note=&english=Y&subjectid=300018589)）。
唐絵に対する「やまと絵」の語そのものの文献上の初出は、藤原行成の日記『権記』長保元年（999年）
10月30日条とされ、能書家として知られた行成が「倭絵四尺屛風」に文字を書き入れたことが記されている
（[ja.wikipedia「大和絵」](https://ja.wikipedia.org/wiki/大和絵)、二次情報、『権記』原文は未確認）。

**未確認**: AAT の「9世紀半ば」と、ja.wikipedia が挙げる語の初出「999年（10世紀末）」は約1〜1.5世紀
のずれがある。前者が「様式・画題の分岐そのものの開始」、後者が「その分岐を指す語が文献に現れた
最初の時点」を指しているのだとすれば整合するが、AAT の scope note にはその根拠となる一次資料が
示されておらず、両者の関係は確認できていない。

代表的な作例として、鎌倉時代の社寺縁起絵《北野天神縁起絵巻》（メトロポリタン美術館蔵、13世紀末）が
挙げられる（同記事）。実物は未見。

## kind の判定 — なぜ `period-style` か

**`self-declared` ではない。** 大和絵という名は、当事者（絵師・工房）が綱領や宣言をもって掲げた
運動名ではない。999年の文献上の初出も、宮廷貴族社会が同時代の作品を分類するために使った語として
現れるのであって、制作者側からの宣言ではない。

**`retrospective` でもない。** 命名者が後代の外部（批評家・史家）である日本画（[movement/nihonga](nihonga.md)——
フェノロサが1882年に命名）とは異なり、大和絵の語は対象が実際に制作されていた同時代（少なくとも
999年時点）から使われている。ただし、後述のとおり「自称」の性質も単純ではない。

**`lineage-school` でもない。** 大和絵には、狩野派・土佐派のような単一の血縁・工房による継承体が
無い。平安時代前期〜中期の絵師としては巨勢金岡とその子・巨勢相覧、飛鳥部常則らの名が伝わるが
確実な遺品は無く、作風の変遷を実作品から辿ることができない。鎌倉時代には藤原隆信・信実父子らが
「似絵（にせえ）」と呼ばれる写実的な肖像画で名品を残し、室町時代には土佐光信が絵巻・肖像画の両方で
作域を広げ、江戸時代には土佐光起が絵所預職を回復して土佐派中興の祖と呼ばれた——**担い手は時代ごとに
入れ替わっており**、大和絵全体を一貫して担った単一の継承体は無い（[ja.wikipedia「大和絵」](https://ja.wikipedia.org/wiki/大和絵)、
二次情報）。血縁・工房の継承体として実体を持つのは大和絵の一部の系譜である土佐派の方であり、これは
既に [movement/tosa-school](tosa-school.md) として別に立っている。

残るのが `period-style` である。時代（平安の国風文化から中世）に紐づく様式で、担い手（宮廷絵師→
似絵の絵師→土佐派）が交代しながら様式の名だけが引き継がれていく構造は、この kind の定義
（王朝・時代に紐づく様式。担い手は交代する）に一致する。

## 時間

`start` は Getty AAT の「9世紀半ば」を採り、この KB の世紀バケット表記で `08XX`（801〜900年）とした。
**未確認**として上に書いたとおり、この値と「語の文献上の初出＝999年」の関係は一次資料では確認できて
いない。より確実な単一の日付としては999年（長保元年10月30日）があるが、これは「語が文献に現れた
時点」であって「様式としての大和絵が始まった時点」と同じとは限らないため、`naming.named_when` の側に
置いた。

`end` は空欄にした。ja.wikipedia は冒頭で「中世を通じて描き続けられ、近代・現代の日本画にも影響を
及ぼしている」と書くが、これは影響の継続についての記述であり、大和絵という括り自体がいつまで
「活動している」と数えられるかは一次資料で確認できていない。**未確認**。

## 空間

`originated_in` は京都（[place/kyoto](../places/kyoto.md)）とした。大和絵が現れたとされる平安時代の
舞台は平安京（現在の京都）の宮廷・貴族社会であり、藤原行成の日記に記録された999年の屏風も、当時の
宮廷社会の中で書かれている。**未確認**: これは平安京＝現在の京都という理解に基づく通説的な位置づけで
あり、Wikidata には都市レベルの座標情報は無く（`P17`＝日本の国レベルまで）、一次資料での座標的な
裏は取れていない。土佐派・狩野派の項目と同じ制約である。

### ニューヨークでの所蔵

大和絵の国外受容を示す具体例として、メトロポリタン美術館は《北野天神縁起絵巻》を日本の
鎌倉時代・13世紀末の作品として収蔵し、その解説で画中の屏風を「early type of yamato-e」と明記している
（[メトロポリタン美術館「Illustrated Legends of the Kitano Tenjin Shrine」](https://www.metmuseum.org/art/collection/search/45428)）。
これは、**大和絵の作例がニューヨークの美術館コレクションに入り、同館の解説で大和絵として
位置づけられていること**を示すが、ニューヨークの別の美術運動への影響は主張しない。そのため
`diffused_to place/new-york-city` は制度的な受容地点を記録する。

## 未着手

- 藤原行成『権記』長保元年（999年）10月30日条の原文・現代語訳の確認（現状は ja.wikipedia 経由の
  二次情報）
- Getty AAT の「9世紀半ば」という時期の根拠（原資料）
- 巨勢金岡・巨勢相覧・飛鳥部常則ら平安前中期の絵師の person エンティティ化。現存する確実な遺品が
  無いとされており、まず一次資料でその実在・活動年代を確認してからになる
- 藤原隆信・藤原信実（似絵）、土佐光信、土佐光起の person エンティティ化。土佐光信・光起は
  [movement/tosa-school](tosa-school.md) の担い手でもあり、大和絵と土佐派という2つの movement を
  繋ぐ根拠になり得る（`docs/schema.md` の person 作成基準2）
- 唐絵（からえ）を独立したエンティティとして立てるかどうか。今回は大和絵の本文中で対概念として
  説明するに留めた
- 《北野天神縁起絵巻》を work エンティティとして分解すること（今回は images 参照のみ）
