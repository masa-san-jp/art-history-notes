---
id: movement/colonial-limner-painting
uri: urn:ahn:movement/colonial-limner-painting
type: movement
label_ja: 植民地期リムナー絵画
label_en: Colonial Limner Painting
authority:
  wikidata: Q1825525
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1670"
  end: "1728~"
  display: "1670年頃（フリーク＝ギブス画家の現存作の最初期）から、1728年のジョン・スミバート（植民地初の
    アカデミー教育を受けた画家）の渡米前後まで。地方では1728年以降もリムナーの活動が続いたため、終期は
    おおよその転換点として扱う"
kind: retrospective
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: limner
  note: "'limner'自体は当時（17〜18世紀）すでに肖像画家を指す職業語として使われていたが、無名・独学の
    植民地肖像画家群を一つの様式的括りとして扱う美術史上の区分は後代の研究者によるものである。単一の
    命名者は特定できないため named_by は null とした"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Freake_Painter", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Freake_Painter", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Limner", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/boston}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q1825525"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Limner"
    kind: reference
    note: "limnerの一般的な定義。植民地期アメリカで正規の美術教育を受けていない旅回りの肖像画家を指すと記す"
  - url: "https://en.wikipedia.org/wiki/Freake_Painter"
    kind: reference
    note: "『フリーク＝ギブス画家（Freake Painter）』の項。1670〜1674年、ボストンで活動し、現存する
      肖像約10点が帰属されると記す。「北米最初期の重要な画家」と評されることも記す"
  - url: "https://en.wikipedia.org/wiki/John_Smibert"
    kind: reference
    note: "ジョン・スミバートが1728年に植民地へ渡り、『植民地で活動した最初のアカデミー教育を受けた画家』
      とされると記す。これをリムナー中心の時代からの転換点として終期の目安に用いた"
status: draft
updated: 2026-09-15
---

# 植民地期リムナー絵画 / Colonial Limner Painting

## 定義と範囲

「limner」はもともと肖像画家一般を指す当時の職業語だが、美術史では特に、17世紀後半〜18世紀前半の
イギリス領北米植民地で活動した、正規の美術教育を受けていない旅回りの肖像画家群を指す括りとして
使われる。[Wikipediaの「Limner」項](https://en.wikipedia.org/wiki/Limner)はこう記す（二次情報）。

> In early 19th-century America, a limner artist was one who had little if any formal training and
> would travel from place to place to solicit commissions.

## kind の判定

`retrospective` とした。当事者が集団として名乗った運動ではなく、無名・匿名の複数の画家個人の実践に、
後代の美術史記述が「limner」という共通の括りを当てはめたものである。

**典拠についての注記**: Getty AATに'limner'に対応する項目IDを検索したが、検索結果から直接特定
できなかった。`authority.wikidata`に採用したQ1825525（limner）はWikidata上では様式・運動ではなく
職業（occupation）としての分類だが、本KBのmovement型は「集合的な芸術実践の括り」を職業横断の様式
区分に読み替える運用（`docs/schema.md`の狩野派の議論に準じる）としてこのIDを採用した。

## 時間・空間

`originated_in` はボストン（[place/boston](../places/boston.md)）。もっとも早期に具体的に特定
できる代表例が、1670年代のボストンで活動した匿名の画家「フリーク＝ギブス画家（Freake Painter /
Freake-Gibbs Painter）」である。[Wikipediaの該当項](https://en.wikipedia.org/wiki/Freake_Painter)
はこう記す（二次情報、原文引用）。

> About ten portraits, all painted between 1670 and 1674, showing residents of Boston, have been
> attributed to the Freake Painter.

この画家は「北米最初期の重要な画家（North America's first major artist）」と評されることもある。
代表作は商人ジョン・フリークとその妻子を描いた《Elizabeth Clarke Freake (Mrs. John Freake) and
Baby Mary》で、現在ウスター美術館が所蔵する。**未確認**: 本項では美術館側のページ（Worcester Art
Museum、Museum of Fine Arts Boston、Smithsonian National Portrait Gallery）へのアクセスが
今回いずれも403で失敗し、Wikipedia記事の記述にとどめている。今後アクセスできる環境で機関資料の
直接引用に置き換えることが望ましい。

`end` は1728年頃とした。[ジョン・スミバートの項](https://en.wikipedia.org/wiki/John_Smibert)は、
スミバートが1728年に植民地へ渡り「植民地で活動した最初のアカデミー教育を受けた画家」になったと記す。
これを機に、独学のリムナーに代わって正規の美術教育を受けた画家（スミバート、後のコプリーら）が
台頭したとされるが、地方では1728年以降もリムナーの活動が続いたため、この年はあくまでおおよその
転換点である。

## 未着手

- Worcester Art Museum・MFA Boston・Smithsonian NPGなど機関資料への直接アクセス（今回はいずれも
  403でブロックされた）
- フリーク＝ギブス画家以外の代表的なリムナー（Gansevoort Limnerなど）の個別調査
- 匿名画家を person エンティティとして立てるかどうか
- 文化圏間接続（4経路）の確認
