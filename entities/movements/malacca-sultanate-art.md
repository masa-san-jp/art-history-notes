---
id: movement/malacca-sultanate-art
uri: urn:ahn:movement/malacca-sultanate-art
type: movement
kind: period-style
label_ja: マラッカ王国美術
label_en: Malacca Sultanate Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Malacca Sultanate』（Q46652）は王国（政体）そのものを指す項目
    であり、美術・様式単位の項目ではないため採用しなかった。movement単位のWikidata項目は
    検索で特定できなかった"
time:
  start: "1400"
  end: "1511"
  display: "パラメスワラ（イスカンダル・シャー）による建国を1400年頃とする通説を起点とし、
    1511年のポルトガルによる征服を終期とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Malacca Sultanate art"
  note: "王国名『マラッカ』自体は当事者由来だが、これを美術movementとして括る呼称は後代の
    美術史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Malacca_Sultanate", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Malacca_Sultanate", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Malacca_Sultanate", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/malacca}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q46652"
    kind: reference
    note: "『Malacca Sultanate』の項。1400-1511年、マレー半島に存在した国家とする。
      movement単位の項目ではない点はauthority.none_reasonに記載した"
  - url: "https://en.wikipedia.org/wiki/Malacca_Sultanate"
    kind: reference
    note: "『Malacca Sultanate』の項。通説ではパラメスワラによる建国を1400年頃とする。
      王マンスール・シャー代の王宮建築が『マラッカの富・繁栄・権力を反映し、マレー建築の
      卓越性と独自の特徴を体現した』と記す。ラマダン27夜（ライラト・アル＝カドル）の祝祭
      では、テメングンが象に乗って行列を先導したと記す。文学・建築・料理・伝統衣装・
      芸能・武術・宮廷儀礼にわたりマレー文化の慣行を標準化したと記す。1405年、明の永楽帝
      が使者尹慶を派遣し、2年後にはアドミラル鄭和が最初の訪問を行い、パラメスワラを伴い
      中国へ帰還した（マラッカ統治者としての地位の承認）と記す。1411年にはパラメスワラ
      自身が540人の使節団を率い鄭和とともに明の宮廷を訪れたと記す。1511年、ポルトガルの
      征服により王国が滅亡し、アルブケルケが宝石をちりばめた腰掛け・黄金の獅子4体・
      黄金の腕輪（出血を防ぐ魔力があるとされた）などの王家の宝物を接収し、20万クルザード
      余りが王室に還元されたと記す（宝物の最終的な所在は同記事に記載無し）"
status: draft
updated: 2026-09-16
---

# マラッカ王国美術 / Malacca Sultanate Art

## 定義と範囲

英語版Wikipedia「[Malacca Sultanate](https://en.wikipedia.org/wiki/Malacca_Sultanate)」
（参考資料）はこう記す（二次情報）。通説ではパラメスワラ（イスカンダル・シャー）が
1400年頃に[マラッカ](../places/malacca.md)王国を建国した。王マンスール・シャー代の
王宮建築は「マラッカの富・繁栄・権力を反映し、マレー建築の卓越性と独自の特徴を体現した」
とされる。同王国は、文学・建築・料理・伝統衣装・芸能・武術・宮廷儀礼にわたりマレー文化の
慣行を標準化したと評される。1405年に明の永楽帝が使者を派遣して以降、鄭和の来訪
（1407年）、パラメスワラ自身による540人規模の朝貢使節団の派遣（1411年）など、明朝との
活発な外交関係が続いた。1511年、ポルトガルの征服により王国は滅亡し、征服者アルブケルケは
宝石をちりばめた腰掛け・黄金の獅子・黄金の腕輪などの王家の宝物を接収した。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、マラッカ王国という政体の存続期間
（1400-1511年）を通じて、複数世代の王・職人が王宮建築・宮廷儀礼・文学を発展させ続けた点を、
[ラーンサーン美術](lan-xang-art.md)・[チャンパ美術](champa-art.md)と同型の構造と見た。

## 空間的接続の判定

明朝との朝貢関係、ポルトガルによる1511年の征服と王家の宝物接収という2つの対外接続を
記録に見つけたが、いずれも本movementの様式・作品そのものが域外の博物館等へ拡散した
文書化された記録には至らなかった——朝貢は外交上の訪問であり作品の移動を伴う記録が
見当たらず、ポルトガルが接収した宝物は「王室に還元された」とのみ記され、その後の所在
（博物館収蔵の有無を含む）は出典に記載が無い。よって`relations`に`diffused_to`は張らず、
`config/cross-region-reviews.yaml`に「文化圏をまたぐ接続の記録なし」として記録した。

## 未着手

- パラメスワラ、マンスール・シャーを person エンティティとして立てるかどうか
- 1511年にポルトガルが接収した王家の宝物（腰掛け・黄金の獅子・腕輪）のその後の所在の
  一次資料での確認
- 鄭和の航海に伴う明朝・マラッカ間の贈答品の一次資料での確認
