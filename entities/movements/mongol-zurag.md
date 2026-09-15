---
id: movement/mongol-zurag
uri: urn:ahn:movement/mongol-zurag
type: movement
kind: retrospective
label_ja: モンゴル・ズラグ
label_en: Mongol Zurag
authority:
  wikidata: Q6899568
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1912"
  end: ".."
  display: "1912〜13年、バルドギーン・シャラヴ（愛称マルザン・シャラヴ）の代表作《モンゴルの一日》
    （当初は『日常の出来事』の題）を起点年とした。ただし英語版Wikipediaの『Mongol zurag』項は
    『1921年革命の余波で（シャラヴらにより）様式が切り開かれた』と記しており、この作品自体の
    制作年（1912〜13年）と食い違う。**未確認**: このずれの原因（シャラヴの活動期全体を指すか、
    様式としての確立時期を指すかの違いなど）。QAGOMA・Sapar Contemporary Galleryなど複数の
    情報源が『Contemporary Mongol Zurag』として21世紀の継続的な実践を記録しており、`end`は
    継続中とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Монгол зураг"
  note: "『zurag（ズラグ）』はモンゴル語で単に『絵』を意味する語であり、シャラヴ自身がこの様式を
    自派の名として名乗った記録は無い。『Urga school（イフ・フレー派）』という呼称もdocumenta 14の
    キュレーション資料に見られる後代の分析的な括りであり、当事者由来ではない"
claims:
  - {field: time, source: "https://www.documenta14.de/en/artists/21988/baldugiin-sharav", certainty: scholarly}
  - {field: originated_in, source: "https://www.documenta14.de/en/artists/21988/baldugiin-sharav", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Mongol_zurag", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/ulaanbaatar}
relations:
  - {type: diffused_to, target: place/kassel, certainty: scholarly, source: "https://www.documenta14.de/en/artists/21988/baldugiin-sharav"}
sources:
  - url: "https://www.wikidata.org/wiki/Q6899568"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Mongol_zurag"
    kind: reference
    note: "『Mongol zurag』の項。20世紀初頭に発達した、チベットのタンカに似た鉱物顔料・綿布の技法で
      世俗的・民族的主題を描く様式とし、1921年革命後にシャラヴらが切り開いたと記す"
  - url: "https://www.documenta14.de/en/artists/21988/baldugiin-sharav"
    kind: scholarly
    note: "documenta 14（2017年）のキュレーション資料。シャラヴ（1869-1939）を『Urga school
      （19世紀末〜20世紀初頭のモンゴル絵画様式）』の担い手とし、代表作《モンゴルの一日》を
      1912〜13年制作とする。作品はカッセルのノイエ・ガレリーで展示されたと記す"
  - url: "https://en.wikipedia.org/wiki/Marzan_Sharav"
    kind: reference
    note: "バルドギーン・シャラヴ（愛称マルザン＝『機知に富む』）の項。近代絵画様式のモンゴルへの
      導入者とされる一方、代表作《モンゴルの一日》はより伝統的なズラグ様式で描かれたと記す"
status: draft
updated: 2026-09-15
---

# モンゴル・ズラグ / Mongol Zurag

## 定義と範囲

英語版Wikipedia「[Mongol zurag](https://en.wikipedia.org/wiki/Mongol_zurag)」はこう記す
（二次情報、原文引用）。

> Mongol zurag is a style of painting in Mongolian art. Developed in the early 20th century,
> zurag is characterised by the depiction of secular, nationalist themes in a traditional
> mineral-paint–on–cotton medium similar to Tibetan thangka.

チベット仏教の伝統的なタンカ画の技法を用いながら、宗教的主題ではなく世俗的な日常生活・民族的主題を
描く点が特徴とされる。代表的な担い手が[バルドギーン・シャラヴ](https://en.wikipedia.org/wiki/Marzan_Sharav)
（愛称マルザン・シャラヴ、1869-1939）で、代表作《モンゴルの一日（One Day in Mongolia）》は、遊牧民の
一生を誕生から死まで、結婚・フェルト作り・山岳信仰・狩猟・牧畜などの場面を通じて描く（documenta 14
キュレーション資料、二次情報）。

## kind の判定

`retrospective` とした。「ズラグ」はモンゴル語で単に「絵」を意味する一般語であり、シャラヴ自身が
この様式を集団の名として名乗った記録は見出せなかった。documenta 14の資料が使う「Urga school
（イフ・フレー派）」という呼称も、後代のキュレーター・研究者による分析的な括りである。

## 時間

`start`の年代づけには資料間の食い違いがある。documenta 14の資料は代表作《モンゴルの一日》の制作を
1912〜13年とする一方、英語版Wikipediaは様式そのものが「1921年革命の余波で切り開かれた」と記す。
本項では、具体的な制作年が特定できる1912年を`start`として採用し、この食い違いを`time.display`に
明記した。**未確認**: 食い違いの原因（シャラヴの活動期全体を指すか、様式としての確立・命名時期を
指すかなど）。

`end`は継続中（`..`）とした。QAGOMA（クイーンズランド州立美術館）の「Contemporary Mongol Zurag」、
ヴェネツィアでの展覧会「Mongol Zurag: The Art of Resistance」、Sapar Contemporary Galleryの
展示など、21世紀に入っても同じ名でこの様式の継承・展開が語られている（WebSearch経由、二次情報、
個別の一次資料は本調査では未確認）。

## 空間

`originated_in`はウランバートル（[place/ulaanbaatar](../places/ulaanbaatar.md)、当時の名称は
イフ・フレー／ウルガ）。

## カッセルでの展示

documenta 14（2017年、ドイツ・[カッセル](../places/kassel.md)）は、シャラヴの《モンゴルの一日》を
含む作品群をノイエ・ガレリーで展示した（documenta 14公式キュレーション資料、二次情報）。これに
基づき`relations`へ`diffused_to place/kassel`を張り、asia-central起源からeurope-westへの接続を
記録した。documenta 5（1972年）に[コンセプチュアル・アート](conceptual-art.md)が出品された記録
（[event/documenta-5-1972](documenta-5-1972.md)）とは別の、documenta 14（2017年）という
異なる回への出品である。

## 未着手

- バルドギーン・シャラヴを person エンティティとして立てるかどうか
- 《モンゴルの一日》を work エンティティとして立てるかどうか
- 1912年と1921年革命という2つの起点候補の食い違いの一次資料での解消
- documenta 14の会期そのもののevent化（今回は既存のplace/kasselへの`diffused_to`にとどめた）
