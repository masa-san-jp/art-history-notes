---
id: movement/kisalian-culture-art
uri: urn:ahn:movement/kisalian-culture-art
type: movement
kind: retrospective
label_ja: キサレ文化美術
label_en: Kisalian Culture Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "movement単位のWikidata項目は検索で特定できなかった。キサレ古墓群
    そのものを指す項目（英語版Wikipedia『Kisalian Graves』）にも対応するWikidata項目が
    見つからなかった"
time:
  start: "0900"
  end: "1200"
  display: "土器・放射性炭素年代測定により、初期キサレ期（700-900年）と古典期キサレ期
    （900-1200年）の2段階が確認される。本項では、副葬品の豊かさ・多様性が最も高まる
    古典期の開始（900年）を起点とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Kisalian culture"
  note: "『キサレ（Kisalian）』はウペンバ低地の地名（キサレ）を借りた後代の考古学記述による
    呼称。当事者自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Kisalian_Graves", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Kisalian_Graves", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Kisalian_Graves", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/upemba-depression}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q681743"
    kind: reference
    note: "originated_inの対象地（ウペンバ低地）のWikidata項目"
  - url: "https://en.wikipedia.org/wiki/Kisalian_Graves"
    kind: reference
    note: "『Kisalian Graves』の項。ウペンバ低地北部の墓所群を、土器・放射性炭素年代測定に
      基づき初期キサレ期（700-900年）と古典期キサレ期（900-1200年）に区分すると記す。
      副葬品として土器・鉄・銅・骨・象牙が見られ、銅製品の数が被葬者の地位を反映したと記す。
      土器・象牙・銅・宝貝・彫刻を施した骨製人形など豊かな副葬品が交易網の存在を示すと記す。
      長く反った刃物も同時期の特徴とし、地位や富の象徴だったと推測されると記す"
status: draft
updated: 2026-09-17
---

# キサレ文化美術 / Kisalian Culture Art

## 定義と範囲

英語版Wikipedia「[Kisalian Graves](https://en.wikipedia.org/wiki/Kisalian_Graves)」
（参考資料）はこう記す（二次情報）。現コンゴ民主共和国、[ウペンバ低地](../places/upemba-depression.md)
北部の墓所群は、土器・放射性炭素年代測定に基づき、初期キサレ期（700-900年）と古典期
キサレ期（900-1200年）の2段階に区分される。副葬品として土器・鉄・銅・骨・象牙が見られ、
銅製品の数が被葬者の地位を反映したとされる。彫刻を施した骨製人形を含む豊かな副葬品は、
広範な交易網の存在を示す。長く反った刃物も同時期の特徴とされ、地位や富の象徴だったと
推測される。

## kind の判定

`retrospective`とした。『キサレ』はウペンバ低地の地名を借りた後代の考古学記述による
呼称であり、当事者自身がこの名で自らの様式を運動として名乗った記録は無い。単一の
血縁・工房による継承か、複数世代にわたる慣習かは出土状況からは判然としないが、墓所群
という埋葬慣行の集合的性質を重視し、[イグボ・ウクウ青銅器](igbo-ukwu-bronze.md)と
同様の判定とした。

## 時間の判定

副葬品の豊かさ・多様性が最も高まる古典期キサレ期の開始（900年）を起点とした。より古い
初期キサレ期（700-900年）が存在することはtime.displayに残した。

## 空間的接続の判定

検索した範囲では、キサレ文化の副葬品がコンゴ民主共和国域外の博物館等へ拡散した文書化
された記録を見つけられなかった。よって`relations`に`diffused_to`は張らず、
`config/cross-region-reviews.yaml`に「文化圏をまたぐ接続の記録なし」として記録した。

## 未着手

- 個々の墓所・副葬品を work エンティティとして立てるかどうか
- ベルギー王立中央アフリカ博物館など、旧宗主国の博物館所蔵品の一次資料での確認
- 発掘を主導した考古学者（ジャック・ネンカン、ピエール・ド・マレ）を person エンティティ
  として立てるかどうか
