---
id: movement/lan-xang-art
uri: urn:ahn:movement/lan-xang-art
type: movement
kind: period-style
label_ja: ラーンサーン美術
label_en: Lan Xang Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Lan Xang』（Q853477）は王国（政体）そのものを指す項目であり、
    美術・様式単位の項目ではないため採用しなかった。movement単位のWikidata項目は検索で
    特定できなかった"
time:
  start: "1353"
  end: "1707"
  display: "英語版Wikipediaはファー・グムによる建国を1353年とし、Wikidataは1354年とする
    （出典間の1年の差）。1707年、王国が3王国（ルアンパバーン・ヴィエンチャン・
    チャンパーサック）に分裂した年を終期とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Lan Xang art"
  note: "『ラーンサーン（百万の象の意）』は王国自体の当事者由来の名だが、これを美術movement
    として括る呼称は後代の美術史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Lan_Xang", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Lan_Xang", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Lan_Xang", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/luang-prabang}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q853477"
    kind: reference
    note: "『Lan Xang』の項。1354-1707年に存続した統一王国とし、東南アジア最大級の王国の
      一つと記す。都は1354-1560年ルアンパバーン、1560-1707年ヴィエンチャンと記す。
      movement単位の項目ではない点はauthority.none_reasonに記載した"
  - url: "https://en.wikipedia.org/wiki/Lan_Xang"
    kind: reference
    note: "『Lan Xang』の項。1353年、ファー・グムによる建国とする。王ウィスン
      （在位1500-1520年）が『畏怖払拭』印を結ぶ仏立像プラバーンを王国の護持仏に定め、
      仏教説話（ジャータカ）・ラーマーヤナ（プララック・プララム）・三蔵のパーリ語から
      ラオ語への翻訳など古典文学が編まれたと記す。ワット・ウィスン（1513年、現存最古の
      継続使用される上座部寺院）、王セーターティラート（在位1548-1571年）代のワット・
      シエントーン（ルアンパバーン）・タート・ルアン（ヴィエンチャン、大規模改修）を
      代表的建造物として挙げる"
status: draft
updated: 2026-09-16
---

# ラーンサーン美術 / Lan Xang Art

## 定義と範囲

英語版Wikipedia「[Lan Xang](https://en.wikipedia.org/wiki/Lan_Xang)」（参考資料）はこう
記す（二次情報）。1353年、ファー・グムがラーンサーン王国（百万の象の意）を建国し、都を
[ルアンパバーン](../places/luang-prabang.md)に置いた。王ウィスン（在位1500-1520年）は、
『畏怖払拭』印を結ぶ仏立像プラバーンを王国の護持仏（パラディウム）に定め、その治世に
ジャータカ（仏教説話）、ラーマーヤナ（プララック・プララム）、パーリ語からラオ語への
三蔵翻訳などの古典文学が編まれた。同王は1513年にワット・ウィスン（現存最古の継続使用
される上座部寺院）を建立した。王セーターティラート（在位1548-1571年）代には、ルアン
パバーンのワット・シエントーンが建てられ、ヴィエンチャンのタート・ルアンが大規模改修
された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ラーンサーン王国という政体の存続期間
（1353-1707年）を通じて、複数世代の王・職人が仏像・寺院建築・写本文学を発展させ続けた点を、
[スコータイ美術](sukhothai-art.md)・[バガン美術](bagan-art.md)と同型の構造と見た。

## 空間的接続の判定

護持仏プラバーンは1778年・1828年の2度、シャム（現タイ）軍によりバンコクへ運ばれた
記録があるが（英語版Wikipedia「Phra Bang」）、シャム・タイも本KBのregionバケット上は
asia-southeast内であり、域外接続には当たらない。検索した範囲では、ラーンサーン王国の
美術・作品がasia-southeast外の博物館等へ拡散した文書化された記録は見つからなかった。
よって`relations`に`diffused_to`は張らず、`config/cross-region-reviews.yaml`に
「文化圏をまたぐ接続の記録なし」として記録した。

## 未着手

- ファー・グム、ウィスン、セーターティラートを person エンティティとして立てるかどうか
- プラバーン像、ワット・シエントーン、タート・ルアンを work/place エンティティとして
  個別に立てるかどうか
- フランス植民地期にラーンサーン王国美術がフランスの博物館（ギメ美術館など）へ収蔵
  された記録の調査
