---
id: movement/zimbabwe-stone-architecture
uri: urn:ahn:movement/zimbabwe-stone-architecture
type: movement
kind: retrospective
label_ja: ジンバブエ石造建築
label_en: Zimbabwe Stone Architecture
authority:
  wikidata: Q209217
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "11XX"
  end: "15XX"
  display: "11世紀にショナ人の祖先によって建設が始まり、300年以上かけて拡張された。主要な
    建設は15世紀まで続き、16〜17世紀に放棄されたとされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "zimbabwe"
  note: "『ジンバブエ（石の家）』という語自体はショナ語由来で、同種の石造遺跡400以上に共通して
    用いられる呼称。ただし『建築movement』として一つの様式運動にまとめたのは後代の考古学・
    美術史記述である"
claims:
  - {field: time, source: "https://www.metmuseum.org/essays/great-zimbabwe-11th-15th-century", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/essays/great-zimbabwe-11th-15th-century", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Great_Zimbabwe", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/great-zimbabwe}
relations:
  - {type: diffused_to, target: place/berlin, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Zimbabwe_Bird"}
sources:
  - url: "https://www.wikidata.org/wiki/Q209217"
    kind: authority
  - url: "https://www.metmuseum.org/essays/great-zimbabwe-11th-15th-century"
    kind: institutional
    note: "メトロポリタン美術館Heilbrunn Timelineの『Great Zimbabwe (11th-15th Century)』essay。
      ショナ人の祖先による11世紀の建設開始と、300年以上にわたる拡張を記す"
  - url: "https://en.wikipedia.org/wiki/Great_Zimbabwe"
    kind: reference
    note: "『Great Zimbabwe』の項。目地を使わない乾式石積みの技法、高さ36フィート・全長820
      フィートに及ぶ『大囲壁（Great Enclosure）』をサハラ以南最大の古代構造物とし、1986年
      UNESCO世界遺産に登録されたと記す"
  - url: "https://en.wikipedia.org/wiki/Zimbabwe_Bird"
    kind: reference
    note: "『Zimbabwe Bird』の項。グレート・ジンバブエから出土した8体の滑石鳥像のうち、
      1体の台座が1907年、あるドイツ人宣教師を経てベルリン民族学博物館へ売却されたと記す。
      別の1体は1889年にウィリー・ポッセルトが持ち去りセシル・ローズが所有、4体は1981年に
      南アフリカからジンバブエへ返還、残り1体（『チャプング』）は2026年4月に返還された"
status: draft
updated: 2026-09-16
---

# ジンバブエ石造建築 / Zimbabwe Stone Architecture

## 定義と範囲

メトロポリタン美術館Heilbrunn Timelineの「[Great Zimbabwe (11th-15th Century)](https://www.metmuseum.org/essays/great-zimbabwe-11th-15th-century)」
（機関資料）は、ショナ人の祖先による11世紀の建設開始と、300年以上にわたる拡張を記す。
目地を使わない乾式石積み（ドライストーン・メーソンリー）が特徴で、高さ36フィート・全長820
フィートに及ぶ「大囲壁（Great Enclosure）」は、サハラ以南アフリカ最大の古代構造物とされる。
1986年、UNESCO世界遺産に登録された。

## kind の判定

`retrospective`とした。「ジンバブエ（石の家）」という語自体はショナ語由来だが、400を超える
同種の遺跡群を一つの建築movementとして束ねたのは後代の考古学記述である。単一の血縁・工房
ではなく、300年以上にわたり複数世代の建設者が石積みを拡張し続けた点を重視した。

## ベルリンでの収蔵

グレート・ジンバブエから出土した8体の滑石鳥像のうち、1体の台座が、あるドイツ人宣教師を経て
1907年にベルリン民族学博物館へ売却された。これに基づき`relations`へ`diffused_to place/berlin`
を張り、africa-sub起源からeurope-westへの接続を記録した。**未確認**: このドイツ人宣教師が
どのような経緯で台座を入手したかの詳細。残る鳥像の多くは南アフリカのグローテ・スキュール
（セシル・ローズ邸）へ渡り、1981年に4体、2026年4月に最後の1体（チャプング）がジンバブエへ
返還された——これらは同じアフリカ域内（africa-sub）の移動であるため4経路監査の接続には
数えていない。

## 未着手

- 8体の滑石鳥像のうち残る個々の像を work エンティティとして立てるかどうか
- 2026年4月の返還式典の一次資料での確認
- ショナ人の建設者を担い手集団としてどこまで具体的に特定できるか
