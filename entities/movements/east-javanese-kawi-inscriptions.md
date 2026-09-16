---
id: movement/east-javanese-kawi-inscriptions
uri: urn:ahn:movement/east-javanese-kawi-inscriptions
type: movement
kind: period-style
label_ja: 東ジャワ王朝カウィ碑文
label_en: East Javanese Kawi Royal Inscriptions
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Calcutta Stone』（Q9025028）は個別の石碑1点を指す項目であり、
    東ジャワ王朝期のカウィ文字碑文という様式・movement単位の項目ではないため採用しなかった。
    movement単位のWikidata項目は検索で特定できなかった"
time:
  start: "0929"
  end: "1041"
  display: "929年、ムプ・シンドクが中部ジャワからブランタス川流域の東ジャワ（ワトゥガルー、
    現ジョンバン県）へマタラム王国の都を遷したことを起点とした。カルカッタ・ストーン
    碑文は1041年、シンドクの子孫である王アイルランガの治世に刻まれ、この王朝の系譜を
    伝える。終期は同碑文の年とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "East Javanese Kawi inscriptions"
  note: "『カウィ』は古ジャワ語による碑文用の文語・書体を指す当事者由来の語だが、これを
    王朝の碑文制作という一つのmovementとして括るのは後代の碑文学・美術史記述による"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Mpu_Sindok", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Mpu_Sindok", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Calcutta_Stone", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/jombang}
relations:
  - {type: diffused_to, target: place/kolkata, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Calcutta_Stone"}
sources:
  - url: "https://www.wikidata.org/wiki/Q9025028"
    kind: authority
    note: "カルカッタ・ストーン（個別の石碑1点）の項目。movement単位ではない点は
      authority.none_reasonに記載した"
  - url: "https://en.wikipedia.org/wiki/Mpu_Sindok"
    kind: reference
    note: "『Mpu Sindok』の項。929年頃に即位し、メラピ山噴火またはスリーヴィジャヤの
      侵攻を受けて中部ジャワから東ジャワ（ブランタス川沿いのワトゥガルー、現ジョンバン
      県付近）へマタラム王国の都を遷したと記す。治世中に『カカウィン・ラーマーヤナ』
      『サンヒャン・カマハーヤーニカン』が書かれたと記す。現カルカッタのインド博物館に
      所蔵される碑文が、シンドクの子孫を11世紀のアイルランガに至るまで記すと記す"
  - url: "https://en.wikipedia.org/wiki/Calcutta_Stone"
    kind: reference
    note: "『Calcutta Stone』の項。サンスクリット語と古ジャワ語でカウィ文字により刻まれた
      碑文で、1041年、カフリパン王国の王アイルランガが、1016年の反乱（前王ダルマヴァンシャ
      の死・都の破壊）を経て自らの正統性を主張するために制作させたと記す。トーマス・
      スタンフォード・ラッフルズがプナングンガン山の斜面で発見し、1812年、感謝のしるし
      としてサングラン碑文とともにインド総督ミント卿へ送り、以来19世紀から現在まで
      カルカッタのインド博物館に保管されていると記す"
status: draft
updated: 2026-09-16
---

# 東ジャワ王朝カウィ碑文 / East Javanese Kawi Royal Inscriptions

## 定義と範囲

英語版Wikipedia「[Mpu Sindok](https://en.wikipedia.org/wiki/Mpu_Sindok)」（参考資料）は
こう記す（二次情報）。929年頃、王ムプ・シンドクは、メラピ山噴火またはスリーヴィジャヤの
侵攻を受けて、マタラム王国の都を中部ジャワから東ジャワのブランタス川沿い（ワトゥガルー、
現[ジョンバン](../places/jombang.md)県付近）へ遷した。この遷都以降、東ジャワの王朝は
カウィ文字（古ジャワ語の碑文用書体）による石碑碑文を通じて王権の正統性・系譜を記録する
慣行を発展させた。「Calcutta Stone」の項は、シンドクの子孫にあたる王アイルランガが
1041年、1016年の反乱（前王ダルマヴァンシャの死・都の破壊）を経て自らの正統性を主張する
ために制作させた碑文——サンスクリット語と古ジャワ語を両面に刻む——を代表例として挙げる。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ムプ・シンドクからアイルランガに至る
複数世代の王朝が、カウィ文字による碑文制作という同じ様式的慣行を100年余りにわたり
共有し続けた点を、[ホイサラ美術](hoysala-art.md)・[カーカティーヤ美術](kakatiya-art.md)
と同型の構造と見た。

## カルカッタでの収蔵

トーマス・スタンフォード・ラッフルズは、プナングンガン山の斜面でこの碑文（後に
『カルカッタ・ストーン』と呼ばれる）を発見し、1812年、感謝のしるしとしてサングラン
碑文とともにインド総督ミント卿（カルカッタ）へ送った。以来19世紀から現在まで、
カルカッタのインド博物館に保管されている。これに基づき`relations`へ
`diffused_to place/kolkata`を張り、asia-southeast起源からasia-southへの接続を記録した。

## 未着手

- ムプ・シンドク、アイルランガを person エンティティとして立てるかどうか
- カルカッタ・ストーンそのものを work エンティティとして立てるかどうか
- サングラン碑文（同じくカルカッタへ送られた）の一次資料での確認
- カフリパン王国（アイルランガが分割・統治した王国）を独立のmovementとして立てるべきか
  どうか
