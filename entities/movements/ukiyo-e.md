---
id: movement/ukiyo-e
uri: urn:ahn:movement/ukiyo-e
type: movement
label_ja: 浮世絵
label_en: Ukiyo-e
authority:
  wikidata: Q185905
  aat: "300106769"
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1672"
  end: "1868~"
  display: "1672年頃、菱川師宣の一枚絵が評判を得た時期を起点とした。江戸時代（1600〜1868年）の枠内の様式とするGetty AATの記述に合わせ、終期は明治維新（1868年）とした"
kind: retrospective
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: 浮世絵
  note: "「浮世絵師」という呼称は、菱川師宣が歌舞伎・遊里を主題に大衆の支持を得た後にまもなく与えられたと千葉市美術館の解説にあるが、命名者個人は特定できない。同時代の呼称ではあるが、単一の宣言や特定個人による命名ではなく社会が与えた呼称であるため self_identified は false とした"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Hishikawa_Moronobu", certainty: scholarly}
  - {field: originated_in, source: "https://www.town.kyonan.chiba.jp/site/hishikawamoronobukinenkan/2460.html", certainty: scholarly}
  - {field: kind, source: "https://www.getty.edu/vow/AATFullDisplay?find=ukiyo-e&logic=AND&note=&english=Y&subjectid=300106769", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/tokyo}
relations:
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Japonisme"}
sources:
  - url: "https://www.wikidata.org/wiki/Q185905"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=ukiyo-e&logic=AND&note=&english=Y&subjectid=300106769"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Hishikawa_Moronobu"
    kind: reference
    note: "菱川師宣が1672年までに評判を得て、以降作品に署名するようになったと記す"
  - url: "https://www.town.kyonan.chiba.jp/site/hishikawamoronobukinenkan/2460.html"
    kind: institutional
    note: "菱川師宣記念館（鋸南町立）公式ページ。師宣を『浮世絵の祖』とし、江戸で活動したことを記す"
  - url: "https://www.ccma-net.jp/exhibitions/special/18-4-6-5-20-2/"
    kind: institutional
    note: "千葉市美術館の企画展解説。師宣が肉筆画・版本・一枚絵の流通を通じて浮世絵文化の礎を作ったと記す"
  - url: "https://en.wikipedia.org/wiki/Japonisme"
    kind: reference
    note: "1860年代以降、浮世絵版画が西洋の芸術家に影響を与え、1862年ロンドン・1867年パリの万国博覧会で日本の工芸品が公開されたと記す。1872年にフィリップ・ビュルティが「ジャポニスム」の語を作った"
status: draft
updated: 2026-09-15
---

# 浮世絵 / Ukiyo-e

## 定義と範囲

Getty AAT の scope note はこう定義する（[AAT 300106769](https://www.getty.edu/vow/AATFullDisplay?find=ukiyo-e&logic=AND&note=&english=Y&subjectid=300106769)、原文引用）。

> Distinctive genre in painting and other media, but most prominently in woodblock printing. It
> arose in the Edo period (1600-1868) and built up a broad popular market among the middle classes.
> Subject matter typically focused on brothel districts and kabuki theatres, with formats ranging
> from single sheet prints to book illustrations.

「浮世絵の祖」とされるのが[菱川師宣](https://ja.wikipedia.org/wiki/%E8%8F%B1%E5%B7%9D%E5%B8%AB%E5%AE%A3)
（生年不詳、1694年没）である。鋸南町立菱川師宣記念館の公式ページはこう記す（機関資料）。

> 肉筆画においても、歌舞伎や吉原遊里の風俗をこまやかに、色鮮やかに描き、『見返り美人図』に見られる
> ような独自の女性美を追求し、『浮世』と呼ばれた当時の世相にマッチした新しい絵画様式を確立しました。

千葉市美術館の企画展解説も同様に、師宣が「肉筆画や版本、さらに版画の一枚絵を流通させ、誰もが絵を
楽しむことができるという浮世絵文化の礎を形成」したと記す（機関資料）。師宣は「歌舞伎や遊里を主な
題材に大衆の支持を得て、まもなく『浮世絵師』という新しい呼称が与えられた」。

## kind の判定

`retrospective` とした。Getty AAT は個人の宣言ではなく江戸時代を通じた「様式・ジャンル」として
定義しており、複数世代・複数の絵師集団（[歌川派](../movements/utagawa-school.md)を含む）に
またがる括りである。「浮世絵師」という呼称自体は同時代に生まれたが、単一の当事者による名乗り・
綱領ではなく、社会から与えられた呼称であるため、`self-declared` ではなく `retrospective` を選んだ。

## 時間

`start` は1672年とした。英語版Wikipediaの菱川師宣の項は、師宣が1672年までに評判を確立し、以降
作品に署名するようになったと記す（二次情報、[出典](https://en.wikipedia.org/wiki/Hishikawa_Moronobu)）。
**未確認**: この年が「浮世絵の始まり」の学術的な定説として広く固定された年かどうかは、複数の
一次・学術資料での裏取りをしていない。`end` はGetty AATが江戸時代（1600〜1868年）内の様式とする
記述に合わせ、[狩野派](../movements/kano-school.md)と同じ明治維新の年を採った。

## 空間

`originated_in` は江戸（現在の[東京](../places/tokyo.md)）。菱川師宣記念館・千葉市美術館の
解説はいずれも師宣の活動地を江戸とする。

## 他のmovementとの関係

このKBには既に、浮世絵の一流派である[歌川派](../movements/utagawa-school.md)が`verified`として
登録されている。歌川派は浮世絵という大きな括りの中の一系統であり、両者は別のmovementとして併存する
（`docs/schema.md`の「movement 1件 = 1つの集合的な括り」という方針に沿う）。

## 文化圏間の接続

1860年代以降、浮世絵版画は西洋の芸術家に影響を与えた。英語版Wikipediaの「Japonisme」項はこう記す
（二次情報、原文引用）。

> These items were widely visible in nineteenth-century Europe: a succession of world's fairs
> displayed Japanese decorative art to millions.

1862年ロンドン万博・1867年パリ万博で日本の工芸品が初めて公開の場に出て、浮世絵版画は好事家の店
（La Porte Chinoiseなど）を通じて流通し、ホイッスラー、マネ、ドガら西洋の画家に渡った。フランスの
批評家フィリップ・ビュルティが1872年に「ジャポニスム」の語を作った。この経路を`relations`の
`diffused_to`で[パリ](../places/paris.md)（europe-west）に接続し、asia-east-japan起源からの
広がりを機械可読に記録した。**未確認**: 1867年パリ万博の日本展示が浮世絵版画そのものを公式に
出品したのか、工芸品一般の展示を通じて版画が別経路（好事家の店・個人収集）で流通したのかは、
今回は一次資料での区別をしていない。

## 未着手

- 菱川師宣を person エンティティとして立てるかどうか（今回は本文中の記述にとどめた）
- 1672年という起点年の、複数の学術資料での裏取り
- 土佐派・南画など、他の日本の流派との関係の記述
- 1867年パリ万博での浮世絵版画展示の有無を一次資料で確認
