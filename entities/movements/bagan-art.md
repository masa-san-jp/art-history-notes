---
id: movement/bagan-art
uri: urn:ahn:movement/bagan-art
type: movement
kind: period-style
label_ja: バガン美術
label_en: Bagan Art
authority:
  wikidata: Q29317
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1044"
  end: "1297"
  display: "王アノーヤター（1044年に最初のビルマ王国を形成）から、建設の最盛期（1057-1287年）
    を経て、1297年頃のパガン王国の実質的な終焉までを範囲とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Bagan art"
  note: "地名『バガン（パガン）』を冠した後代の美術史記述による様式区分。当事者（王・職人）
    自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://www.smithsonianmag.com/travel/the-architectural-wonders-of-bagan-11363805/", certainty: scholarly}
  - {field: originated_in, source: "https://www.smithsonianmag.com/travel/the-architectural-wonders-of-bagan-11363805/", certainty: scholarly}
  - {field: kind, source: "https://whc.unesco.org/en/list/1588/", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/bagan}
relations:
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/39188"}
sources:
  - url: "https://www.wikidata.org/wiki/Q29317"
    kind: authority
  - url: "https://www.smithsonianmag.com/travel/the-architectural-wonders-of-bagan-11363805/"
    kind: reference
    note: "『The Architectural Wonders of Bagan』の記事。王アノーヤターが1044年に最初のビルマ
      王国を形成し、1057-1287年の建設ラッシュで1万を超える仏教建造物が作られたと記す"
  - url: "https://whc.unesco.org/en/list/1588/"
    kind: institutional
    note: "UNESCO世界遺産センターのバガン登録ページ（2019年登録）。仏教美術・建築の卓越した
      集積とし、塔・寺院・僧院・巡礼地・壁画・彫刻を含む8つの構成資産・3,595件の記録された
      建造物を記す"
  - url: "https://www.metmuseum.org/art/collection/search/39188"
    kind: institutional
    note: "メトロポリタン美術館収蔵《立像仏》（ビルマ、パガン期）"
  - url: "https://www.metmuseum.org/art/collection/search/65015"
    kind: institutional
    note: "メトロポリタン美術館収蔵《蓮華座の坐仏》（ビルマ、パガン期、11世紀末、銀・銅象嵌の
      ブロンズ）"
status: draft
updated: 2026-09-16
---

# バガン美術 / Bagan Art

## 定義と範囲

Smithsonian Magazineの記事はこう記す（二次情報）。バガンは9〜13世紀、パガン王国の都で、
王アノーヤターが1044年に最初のビルマ王国を形成した後、1057-1287年の建設ラッシュで1万を超える
仏教の塔・寺院・僧院が建てられた。代表例が、王チャンシッター（在位1084-1113年）により1105年頃
建立されたアーナンダ寺院で、バガンで最も優美で保存状態の良い寺院とされる。2019年、UNESCO
世界遺産に登録された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、パガン王国という政体の存続期間（1044-1297年頃）
を通じて、複数世代の王・職人が仏塔・寺院・壁画・彫刻を制作し続けた点を、
[クメール美術](khmer-art.md)・[スコータイ美術](sukhothai-art.md)と同型の構造と見た。

## ニューヨークでの収蔵

メトロポリタン美術館は、パガン期のブロンズ仏像を複数所蔵する。11世紀末の《蓮華座の坐仏》
（銀・銅象嵌）、12〜13世紀の《立像仏》（銀象嵌）などを含む。これに基づき`relations`へ
`diffused_to place/new-york-city`を張り、asia-southeast起源からamericas-northへの接続を
記録した。

## 未着手

- 王アノーヤター、チャンシッターを person エンティティとして立てるかどうか
- 代表的な寺院（アーナンダ寺院など）を work エンティティとして立てるかどうか
- インド・ヒンドゥー寺院からの影響を`relations`の`influenced_by`で明示するかどうか（今回は
  本文の記述にとどめた）
