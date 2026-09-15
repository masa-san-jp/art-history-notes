---
id: movement/moai
uri: urn:ahn:movement/moai
type: movement
kind: retrospective
label_ja: モアイ
label_en: Moai
authority:
  wikidata: Q20350
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "10XX"
  end: "16XX"
  display: "彫像の科学的年代測定例は無いとされ（英語版Wikipedia「Hoa Hakananai'a」）、資料間で
    起点の幅がある。英語版Wikipedia「moai」は制作期間を『紀元1000年頃から17世紀後半まで』とし、
    887体のうち多くが1250〜1500年頃に集中して切り出されたとする記述もある。個別像（例：
    ホア・ハカナナイア）は1000〜1200年頃と推定される。終期は17世紀後半（部族間抗争・資源枯渇に
    よる社会変動が背景とされる）"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "moai"
  note: "『モアイ』はラパ・ヌイ語で『像』を意味する語で、当事者（ラパ・ヌイの人々）自身が用いる
    呼称である。ただし『運動・様式』としての集団的な名乗り・綱領があったわけではなく、個々の像に
    与えられた対象名である点で、西洋の-ismのような宣言的movementとは性質が異なる"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Moai", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Moai", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q20350", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/rapa-nui}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Hoa_Hakananai%27a"}
sources:
  - url: "https://www.wikidata.org/wiki/Q20350"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Moai"
    kind: reference
    note: "『moai』の項。祖先を記念して彫られたと考えられ、紀元1000年頃から17世紀後半まで、
      887体が数百年かけて切り出され・彫られ・立てられたと記す"
  - url: "https://en.wikipedia.org/wiki/Hoa_Hakananai%27a"
    kind: reference
    note: "『Hoa Hakananai'a』の項。1000〜1200年頃の制作と推定されるが科学的年代測定は無いとし、
      1868年に英国艦船HMSトパーズの乗組員がラパ・ヌイのオロンゴから持ち去り、1869年に大英博物館
      （ロンドン）へ収蔵された経緯を記す"
status: draft
updated: 2026-09-16
---

# モアイ / Moai

## 定義と範囲

英語版Wikipedia「[moai](https://en.wikipedia.org/wiki/Moai)」はこう記す（二次情報、原文引用）。

> The moai were carved by the Rapa Nui people ... probably to commemorate ancestors.

887体の巨石像が、[ラパ・ヌイ](../places/rapa-nui.md)（通称イースター島）のラノ・ララクという
火山口内外の凝灰岩採石場から、玄武岩製の手斧を使って切り出された。1995年、ラパ・ヌイ国立公園として
UNESCO世界遺産に登録された（WebSearch経由、二次情報）。

## kind の判定

`kind`は`retrospective`とした。`original_label`欄に記した通り、『モアイ』自体はラパ・ヌイ語で
当事者が使う語だが、これは個々の像を指す名称であって、西洋の-ismのような『運動』を宣言する語では
ない。単一の担い手・工房・血縁による継承ではなく、ラパ・ヌイ社会が数百年かけて生み出した慣習的な
造形実践を、後代の研究が一つの括りとしてまとめたものである。

## 時間

年代づけには資料間の幅がある。英語版Wikipedia「Hoa Hakananai'a」の項はこう記す（原文引用）。

> No Easter Island statues have been scientifically dated.

「moai」の項は制作期間全体を紀元1000年頃から17世紀後半までとする。この幅の広さと個別像の
年代不確実性をそのまま`time.display`に残した。

## ロンドンでの収蔵

代表的な個別像「[ホア・ハカナナイア](https://en.wikipedia.org/wiki/Hoa_Hakananai%27a)」
（1000〜1200年頃と推定）は、1868年に英国艦船HMSトパーズの乗組員がオロンゴから持ち去り、
ヴィクトリア女王の意向により1869年に大英博物館へ収蔵された。これに基づき`relations`へ
`diffused_to place/london`を張り、oceania起源からeurope-westへの接続を記録した。

## 未着手

- 個別の像（ホア・ハカナナイアなど）を work エンティティとして立てるかどうか
- UNESCO世界遺産登録（1995年）の一次資料への到達
- 年代測定・社会変動（17世紀後半の終期）の学術論文への到達
