---
id: movement/mapuche-silverwork
uri: urn:ahn:movement/mapuche-silverwork
type: movement
kind: retrospective
label_ja: マプチェ銀細工
label_en: Mapuche Silverwork
authority:
  wikidata: Q17068381
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "17XX"
  end: "19XX"
  display: "英語版Wikipedia『Mapuche silverwork』は、18世紀後半にマプチェの銀細工師が
    大量の銀装身具を制作し始め、18世紀末から19世紀初頭にかけて制作量・意匠の多様性が
    頂点に達したと記す。1869年以降、戦争と疫病によりマプチェ社会が大きな打撃を受け
    伝統は大きく衰退し、1980年代までに実質的に途絶えたと記す"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Mapuche silverwork"
  note: "『マプチェ銀細工』は民族名を借りた後代の美術史・民族誌記述による括り。制作者
    自身がこの名で自らの実践を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Mapuche_silverwork", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Mapuche_silverwork", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Mapuche_silverwork", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/araucania}
relations:
  - {type: diffused_to, target: place/washington-dc, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Mapuche_silverwork"}
sources:
  - url: "https://www.wikidata.org/wiki/Q17068381"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Mapuche_silverwork"
    kind: reference
    note: "『Mapuche silverwork』の項。18世紀後半にマプチェの銀細工師が大量の銀装身具を
      制作し始め、18世紀末から19世紀初頭に制作量・意匠の多様性が頂点に達したと記す。
      素材はスペイン植民地時代の銀貨（特にポトシ銀山産）を用いたと記す。代表的な装身具
      （トゥポなど）は、平たく打ち延ばした銀の輪を3列に連ね正方形の輪で交互に繋いだ構造で、
      上部に平たい双頭の鳥の意匠、下部に半円または台形（小円盤が連なる）を持つと記す。
      1869年以降の戦争・疫病によるマプチェ社会への打撃を経て伝統は大きく衰退し、1980年代
      までに実質的に途絶えたと記す。スミソニアン協会国立アメリカ・インディアン博物館
      （NMAI）のコレクションにマプチェ銀細工が所蔵されると記す"
status: draft
updated: 2026-09-21
---

# マプチェ銀細工 / Mapuche Silverwork

## 定義と範囲

英語版Wikipedia「[Mapuche silverwork](https://en.wikipedia.org/wiki/Mapuche_silverwork)」
（参考資料）はこう記す（二次情報）。18世紀後半、[アラウカニア](../places/araucania.md)を
中心地とするマプチェの銀細工師たちは、大量の銀装身具を制作し始めた。素材はスペイン
植民地時代の銀貨（特にポトシ銀山産）を打ち延ばして用いた。18世紀末から19世紀初頭にかけて
制作量・意匠の多様性が頂点に達し、代表的な装身具（トゥポ＝留め針など）は、平たく打ち延ばした
銀の輪を3列に連ね正方形の輪で交互に繋ぐ構造を持ち、上部に平たい双頭の鳥の意匠、下部に半円
または台形（小円盤が連なる）を配した。1869年以降、戦争と疫病によりマプチェ社会は大きな
打撃を受け、伝統は大きく衰退し、1980年代までに実質的に途絶えたとされる。

## パタゴニア先住民美術としての位置づけ

マプチェは、テウェルチェ・セルクナム・ハウシュ・ヤーガンなど、パタゴニア地域により古くから
居住していた諸民族とは区別される——英語版Wikipedia「[Patagonia](https://en.wikipedia.org/wiki/Patagonia)」
は、マプチェ語を話す農耕民が16世紀末にアンデス西麓から東の平原・さらに南方へ進出し、対立と
技術力を通じて短期間のうちにこの地域の他の諸民族を圧倒し、現在ではパタゴニアの主要な先住民
共同体になったと記す。本項では、この記述に基づき、マプチェ銀細工を「パタゴニア先住民美術」の
一例として扱いつつ、マプチェが同地域への後発の到来者であるという歴史的経緯を明記した。

## kind の判定

`retrospective`とした。『マプチェ銀細工』は民族名を借りた後代の美術史・民族誌記述による
括りであり、制作者自身がこの名で自らの実践を運動として名乗った記録は無い。単一の
血縁・工房ではなく、複数世代のマプチェの銀細工師が同じ様式的語彙（トゥポの構造・双頭の鳥の
意匠）を約100年にわたり共有し続けた点を、[アカン金分銅](akan-goldweights.md)と同型の
構造と見た。

## ワシントンでの収蔵

スミソニアン協会国立アメリカ・インディアン博物館（NMAI、ワシントンD.C.）のコレクションに
マプチェ銀細工が所蔵される。これに基づき`relations`へ`diffused_to place/washington-dc`を張り、
americas-latin起源からamericas-northへの接続を記録した。

## 未着手

- 個々の装身具（トゥポなど）を work エンティティとして立てるかどうか
- ポトシ銀山との交易関係を通じたmena/asia-southを含む広域交易網との接続の調査
- NMAIコレクションの一次資料（収蔵品個別ページ）での確認
- 1869年以降の衰退の経緯（占領・強制移住との関係）の一次資料での確認
