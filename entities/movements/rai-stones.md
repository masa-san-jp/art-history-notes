---
id: movement/rai-stones
uri: urn:ahn:movement/rai-stones
type: movement
kind: retrospective
label_ja: ライ・ストーン
label_en: Rai Stones
authority:
  wikidata: Q917019
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "0500~"
  end: "1932"
  display: "資料によれば紀元500年頃、パラオの採石場からヤップへ石灰岩の巨大な円盤が運ばれ始めた
    とされる。最後に採掘されたライは1931年にパラオで切り出され、1932年にヤップへ運ばれた"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "rai"
  note: "『ライ（rai）』はヤップの言葉で当事者が用いる語である。ヤップの伝承では、航海者
    アナグマングがパラオでこの石を発見したとされ、当初は魚の形、次に三日月形、最後に
    運びやすいよう中央に穴を開けた満月形にたどり着いたと伝えられる"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Rai_stones", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Rai_stones", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Rai_stones", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/palau}
  - {role: active_in, target: place/yap}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://www.britishmuseum.org/collection/object/Oc1980-Q-928"}
  - {type: diffused_to, target: place/washington-dc, certainty: scholarly, source: "https://www.si.edu/object/rai-stone:nmah_1967502"}
sources:
  - url: "https://www.wikidata.org/wiki/Q917019"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Rai_stones"
    kind: reference
    note: "『Rai stones』の項。紀元500年頃からパラオの石灰岩採石場から280マイル離れたヤップへ
      運ばれ始めたとし、航海者アナグマングによる発見伝承を記す。1931年にパラオで最後の
      ライが採石され、1932年にヤップへ運ばれたと記す"
  - url: "https://www.britishmuseum.org/collection/object/Oc1980-Q-928"
    kind: institutional
    note: "大英博物館収蔵のライ・ストーン標本（登録番号Oc1980,Q.928）"
  - url: "https://www.si.edu/object/rai-stone:nmah_1967502"
    kind: institutional
    note: "スミソニアン協会（国立自然史博物館、ワシントンD.C.）収蔵のライ・ストーン。1904年に
      パラオで採石されヤップへ運ばれた高さ6フィート・重さ4000ポンドの石が、同館ロビーに
      展示されていると記す"
status: draft
updated: 2026-09-16
---

# ライ・ストーン / Rai Stones

## 定義と範囲

英語版Wikipedia「[Rai stones](https://en.wikipedia.org/wiki/Rai_stones)」はこう記す
（二次情報、原文引用）。

> Beginning around 500 A.D., the megalithic stones were brought to Yap from the ancient crystal
> mines on the island of Palau, more than 280 miles away.

石灰岩を石灰岩から円盤状に加工し、中央に穴を開けて運搬・保管を容易にした巨石貨幣。産地は
[パラオ](../places/palau.md)北部バベルダオブ島の採石場で、原始的な道具で切り出され、
アウトリガーカヌーで約400キロメートル離れたヤップまで運ばれた。石の価値は、大きさや仕上がり
だけでなく、運搬の労苦（人命が失われた記録があれば、その石の価値はさらに高まった）によって
決まったとされる。1931年にパラオで最後のライが採石され、1932年にヤップへ運ばれたのを最後に
製作は終わった。

## kind の判定

`retrospective`とした。『ライ』自体は当事者由来の語だが（`self_identified: true`）、これを
一つの美術・工芸movementとして束ねたのは後代の人類学・経済史記述である。単一の血縁・工房
ではなく、1400年以上にわたり複数世代のヤップ・パラオの人々が同じ形式の巨石貨幣を作り・
運び続けた点を重視した。

## ロンドン・ワシントンでの収蔵

大英博物館は登録番号Oc1980,Q.928のライ・ストーン標本を所蔵する。スミソニアン協会
（国立自然史博物館、ワシントンD.C.）は、1904年にパラオで採石されヤップへ運ばれた高さ6フィート・
重さ4000ポンドの石を含む複数のライ・ストーンを所蔵し、同館ロビーで展示している。これに基づき
`relations`へ`diffused_to`を`place/london`・`place/washington-dc`の双方に張り、oceania起源
からeurope-west・americas-northへの接続を記録した。

## 未着手

- 航海者アナグマングを person エンティティとして立てるかどうか
- ヤップ（[place/yap](../places/yap.md)、`active_in`で参照）自体のplaceとしての詳細記述
- 紀元500年という起点年の一次資料での確認
