---
id: movement/igbo-ukwu-bronze
uri: urn:ahn:movement/igbo-ukwu-bronze
type: movement
kind: retrospective
label_ja: イグボ・ウクウ青銅器
label_en: Igbo-Ukwu Bronzes
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Igbo-Ukwu』（Q4785495）は考古遺跡そのものを指す項目であり、
    青銅器制作の様式・movement単位の項目ではないため採用しなかった。movement単位の
    Wikidata項目は検索で特定できなかった"
time:
  start: "08XX"
  end: "12XX"
  display: "最初の放射性炭素年代測定と遺物の比較に基づき、長らく『9世紀の遺物群』と
    要約されてきた。近年の研究はより幅を持たせ、研究者はイグボ・ウクウの活動期を
    おおよそ9〜12世紀とすることが多いが、個々の埋納物が同時代とは限らないとも
    認識されている。本項では従来の9世紀説を起点として採用しつつ、この幅を
    time.displayに残した"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Igbo-Ukwu bronzes"
  note: "『イグボ・ウクウ青銅器』は考古遺跡の地名を借りた後代の考古学・美術史記述による
    括り。制作者自身の集団名・様式名としての当事者由来の呼称は記録されていない"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Igbo-Ukwu", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Igbo-Ukwu", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Igbo-Ukwu", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/igbo-ukwu}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Igbo-Ukwu"}
sources:
  - url: "https://en.wikipedia.org/wiki/Igbo-Ukwu"
    kind: reference
    note: "『Igbo-Ukwu』の項。最初の放射性炭素年代測定と遺物比較に基づき長らく『9世紀の
      遺物群』と要約されてきたが、近年の研究者はおおよそ9〜12世紀の活動期とすることが
      多く、個々の埋納物が同時代とは限らないと記す。蝋型鋳造により精巧な容器・儀礼具が
      作られ、職人は針金・鎖・取っ手・螺旋状の突起には不純銅を鍛造・焼鈍し、鋳造部品には
      合金を選んで用いるなど、部位ごとに意図的な材料選択をしたと記す。この発見により、
      ヨーロッパ人接触以前から現ナイジェリア南東部の森林地帯の共同体が高度な工芸生産と
      遠距離交易網に参加していたことが示されたと記す。植民地行政期の初期発見の一部
      （5点）は現在大英博物館に所蔵され、その他の出土品はナイジェリアの国立コレクション
      に保存されていると記す"
status: draft
updated: 2026-09-16
---

# イグボ・ウクウ青銅器 / Igbo-Ukwu Bronzes

## 定義と範囲

英語版Wikipedia「[Igbo-Ukwu](https://en.wikipedia.org/wiki/Igbo-Ukwu)」（参考資料）は
こう記す（二次情報）。現ナイジェリア、アナンブラ州の[イグボ・ウクウ](../places/igbo-ukwu.md)
遺跡から出土した青銅器群は、蝋型鋳造による精巧な儀礼用容器・王権具を含む。職人は、
針金・鎖・取っ手・螺旋状の突起には不純銅を鍛造・焼鈍する一方、鋳造部品には意図的に
合金を選ぶなど、部位ごとに異なる金属を使い分けた。この発見は、ヨーロッパ人との接触
以前から、現ナイジェリア南東部の森林地帯の共同体が高度な工芸生産と遠距離交易網に
参加していたことを示した。

## 時間の判定

最初の放射性炭素年代測定と遺物比較に基づき、長らく『9世紀の遺物群』と要約されてきたが、
近年の研究者はおおよそ9〜12世紀という幅のある活動期を採ることが多く、個々の埋納物が
同時代とは限らないとも認識されている。本項では、従来から広く引用される9世紀説を起点
（`time.start: "08XX"`）として採用しつつ、この学術的な幅と不確実性をtime.displayに
残した。

## kind の判定

`retrospective`とした。『イグボ・ウクウ青銅器』という括りは考古遺跡の地名を借りた後代の
考古学・美術史記述によるものであり、制作者自身の集団・様式の呼称としての当事者由来の
記録は無い。単一の血縁・工房による継承か、複数世代にわたる慣習かは出土状況からは
判然としないが、埋納物が同時代とは限らないという学術的な認識を踏まえ、単一の一回性の
出来事（`self-declared`）としてではなく、後代の括りとして扱った。

## ロンドンでの収蔵

植民地行政期の初期発見の一部（5点）は現在大英博物館に所蔵される。これに基づき
`relations`へ`diffused_to place/london`を張り、africa-sub起源からeurope-westへの
接続を記録した。

## 未着手

- 個々の青銅器（儀礼用容器・王権具など）を work エンティティとして立てるかどうか
- 発掘を主導したユーロパイオニア考古学者（ソーストン・シャウ）を person エンティティ
  として立てるかどうか
- 9〜12世紀という活動期の幅、個々の埋納物の年代差について一次資料（考古学論文）での
  確認
