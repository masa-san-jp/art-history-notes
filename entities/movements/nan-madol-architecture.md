---
id: movement/nan-madol-architecture
uri: urn:ahn:movement/nan-madol-architecture
type: movement
kind: period-style
label_ja: ナンマドール建築
label_en: Nan Madol Architecture
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "ナンマドールの巨石建築様式そのものを指すWikidata項目は検索で特定できなかった。
    遺跡自体の項目（Q846967）は place/nan-madol の authority として別途登録した"
time:
  start: "1200"
  end: "1628~"
  display: "ウラン系列年代測定により、サウデレウル朝による島全体の政治的統合は西暦1180-1200年
    頃に確立したとされる。石造の宮殿・神殿・墓・居住区の建設は1200-1500年に及ぶとする資料と、
    13〜17世紀に及ぶとする資料がある。サウデレウル朝の都としての機能は1628年頃までとされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Nan Madol"
  note: "『ナンマドール』は現地の言葉で『間の中に』を意味し、遺跡を刻む水路への言及とされる
    （地名としては当事者由来）。ただし様式・建築技法を一つの美術運動として束ねる名としては
    後代の考古学記述による"
claims:
  - {field: time, source: "https://www.heritagedaily.com/2020/07/nan-madol-capital-of-the-saudeleur-dynasty/134102", certainty: scholarly}
  - {field: originated_in, source: "https://www.heritagedaily.com/2020/07/nan-madol-capital-of-the-saudeleur-dynasty/134102", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Saudeleur_dynasty", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/nan-madol}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q846967"
    kind: authority
  - url: "https://www.heritagedaily.com/2020/07/nan-madol-capital-of-the-saudeleur-dynasty/134102"
    kind: reference
    note: "ナンマドールをサウデレウル朝の都とし、サウデレウル朝の墓のウラン系列年代測定から
      島全体の政治統合を西暦1180-1200年頃と記す。石造の宮殿・神殿・墓・居住区が1200-1500年に
      及ぶと記す"
  - url: "https://en.wikipedia.org/wiki/Saudeleur_dynasty"
    kind: reference
    note: "サウデレウル朝が12世紀から17世紀初頭まで統治し、ナンマドールを政治・儀礼の中心地に
      押し上げたと記す。同朝の都としての機能は1628年頃までとする"
status: draft
updated: 2026-09-16
---

# ナンマドール建築 / Nan Madol Architecture

## 定義と範囲

ミクロネシア連邦[ポンペイ島](../places/nan-madol.md)沖の潟に築かれた100を超える人工島から
なる遺跡で、目地を使わず積み上げられた玄武岩の柱状節理・玉石・サンゴ礫を用いる巨石建築様式で
知られる。玄武岩は島の反対側の火山岩脈から切り出され、潟まで運ばれたとされる（WebSearch経由、
複数の二次情報）。

英語版Wikipedia「[Saudeleur dynasty](https://en.wikipedia.org/wiki/Saudeleur_dynasty)」は、
同朝が12世紀から17世紀初頭まで統治し、ナンマドールを推定人口2万5千人のポンペイ島を統一する
政治・儀礼の中心地に押し上げたと記す。2016年、UNESCO世界遺産に登録された。

## kind の判定

`period-style`とした。単一の血縁的な工房ではなく、サウデレウル朝という政体の存続期間を通じて、
複数世代の建設者が石造建築を築き続けた点を、[クメール美術](khmer-art.md)・
[スコータイ美術](sukhothai-art.md)と同型の構造と見た。

## 時間

ウラン系列年代測定により、サウデレウル朝による島全体の政治的統合は西暦1180-1200年頃に
確立したとされる。石造建築の建設年代には資料間で幅があり（1200-1500年とする資料、13〜17世紀と
する資料）、`time.display`に両方を残した。同朝の都としての機能は1628年頃まで続いたとされる。

## 未着手

- サウデレウル朝の歴代統治者を person エンティティとして立てるかどうか
- 個別の遺構（イサケレケル島など）を work または別のplaceとして立てるかどうか
- 文化圏間接続（4経路）: 遠隔の孤立した遺跡であり、検索した範囲では海外美術館収蔵などの
  域外への文書化された接続は見つけられなかった
