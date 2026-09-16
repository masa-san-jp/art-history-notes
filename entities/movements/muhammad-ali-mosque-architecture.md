---
id: movement/muhammad-ali-mosque-architecture
uri: urn:ahn:movement/muhammad-ali-mosque-architecture
type: movement
kind: self-declared
label_ja: ムハンマド・アリー朝モスク建築
label_en: Muhammad Ali Dynasty Mosque Architecture
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Muhammad Ali Mosque』（Q652046）は建造物1件を指す個別項目であり、
    様式・movement単位の項目ではないため採用しなかった。movement単位のWikidata項目は
    検索で特定できなかった"
time:
  start: "1830"
  end: "1848"
  display: "1830年に建設開始、1848年（Wikidataのinception年）完成。実際の建設は
    1857年頃まで続いたとする資料もある（英語版Wikipedia『Mosque of Muhammad Ali』）"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Muhammad Ali Mosque architecture"
  note: "モスクの名称『ムハンマド・アリー・モスク』自体は建立者の名を冠したものだが、
    これを様式movementとして括る呼称は後代の建築史記述による"
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q652046", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Mosque_of_Muhammad_Ali", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Mosque_of_Muhammad_Ali", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/cairo}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q652046"
    kind: authority
    note: "movement単位の項目ではなく建造物1件の項目である点はauthority.none_reasonに
      記載した"
  - url: "https://en.wikipedia.org/wiki/Mosque_of_Muhammad_Ali"
    kind: reference
    note: "『Mosque of Muhammad Ali』の項。1827年、フランス人建築家パスカル・コストが
      ネオ・マムルーク様式を提案したが、ムハンマド・アリーはこれを退けたと記す。1832年から
      進んだ実際の建設は『おそらくギリシャ人かアルメニア人』の建築家によるとし、様式は
      イスタンブールのシェフザーデ・モスク、スルタンアフメト・モスクと同じ配置を持つ
      『完全にオットマン様式』であり、カイロの伝統的建築様式からの意図的な断絶を通じて、
      ムハンマド・アリー自身がエジプトに新しい秩序を築こうとした意志の表れと解釈されると
      記す。中庭北西の壁上には、1846年頃にフランス王ルイ・フィリップからルクソール・
      オベリスクとの交換で贈られた鉄製の大時計塔（ネオ・ゴシックとオリエンタリズム様式の
      混交）があると記す"
status: draft
updated: 2026-09-16
---

# ムハンマド・アリー朝モスク建築 / Muhammad Ali Dynasty Mosque Architecture

## 定義と範囲

英語版Wikipedia「[Mosque of Muhammad Ali](https://en.wikipedia.org/wiki/Mosque_of_Muhammad_Ali)」
（参考資料）はこう記す（二次情報）。エジプト太守ムハンマド・アリー（在位1805-1848年）は、
1827年にフランス人建築家パスカル・コストが提案したネオ・マムルーク様式（カイロの伝統的な
マムルーク朝建築を踏襲する案）を退け、1832年から[カイロ](../places/cairo.md)の城塞に、
イスタンブールのシェフザーデ・モスク、スルタンアフメト・モスクと同じ配置を持つ『完全に
オットマン様式』のモスクを、おそらくギリシャ人かアルメニア人の建築家により建てさせた。
この様式選択は、カイロの伝統からの意図的な断絶であり、ムハンマド・アリー自身がエジプトに
新しい秩序（オスマン帝国からの事実上の自立を含む王朝の正統性）を築こうとした意志の
表れと解釈される。

## kind の判定

`self-declared`とした。単一の血縁・工房の継承や、後代の美術史記述による括りではなく、
ムハンマド・アリーというただ一人の統治者が、パスカル・コストの提案を退けてまで
明確な政治的意図のもとに単一の様式選択（イスタンブールのオットマン帝室モスク様式の
採用）を下した1回の宣言的な行為である点を重視した。

## 空間的接続の判定

モスク中庭のフランス製大時計塔（1846年、ルイ・フィリップからの贈答、ルクソール・
オベリスクとの交換）はeurope-westからの受け入れであり、本movement自身の様式・作品が
europe-westへ拡散した記録ではない。イスタンブールの様式を範としたという事実も、
イスタンブール自体がmena内（本KBのregionバケット上）であるため、region間の接続には
当たらない。検索した範囲では、このmovementの様式・作品自体が起源region外の博物館等へ
拡散した文書化された記録は見つからなかった。

## 未着手

- ムハンマド・アリーを person エンティティとして立てるかどうか
- モスクそのものを work エンティティとして立てるかどうか
- 実際の建築家（ギリシャ人かアルメニア人とされるが未確定）の特定
- 後継者（アッバース1世・サイード・イスマーイール）代のカイロ建築への様式の継承・
  変化の一次資料での確認
