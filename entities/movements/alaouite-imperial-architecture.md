---
id: movement/alaouite-imperial-architecture
uri: urn:ahn:movement/alaouite-imperial-architecture
type: movement
kind: self-declared
label_ja: アラウィー朝帝都建築
label_en: Alaouite Imperial Architecture
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "この様式区分全体を指すWikidata項目は検索で特定できなかった。中心地
    メクネス自体の項目（Q178663）はplace側のauthorityとして別途登録した"
time:
  start: "1672"
  end: "1727"
  display: "スルターン、ムーレイ・イスマーイール（在位1672-1727年）の治世を範囲とした"
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: "Alaouite architecture"
  note: "王朝名『アラウィー』は当事者（アラウィー朝スルターン家）自身が名乗る王朝名であり、
    ムーレイ・イスマーイールが自らの建設事業をこの王朝の名のもとに行ったことは確実である。
    ただし『建築様式』としての運動名を当事者が名乗った記録は確認していない"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Meknes", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Meknes", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Meknes", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/meknes}
relations: []
sources:
  - url: "https://www.wikidata.org/wiki/Q178663"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Meknes"
    kind: reference
    note: "『Meknes』の項。11世紀にアルモラビド朝の軍事拠点として建設され、ムーレイ・
      イスマーイール（1672-1727年）の治世に帝都となったと記す。イスラーム様式と
      ヨーロッパ様式の融合を特徴とすると記す"
  - url: "https://whc.unesco.org/en/list/793/"
    kind: institutional
    note: "UNESCO世界遺産センターのメクネス歴史都市の登録ページ。17世紀の帝都としての
      都市構造の保存状態を評価根拠とすると記す"
status: draft
updated: 2026-09-16
---

# アラウィー朝帝都建築 / Alaouite Imperial Architecture

## 定義と範囲

英語版Wikipedia「[Meknes](https://en.wikipedia.org/wiki/Meknes)」はこう記す（二次情報）。
メクネスは11世紀にアルモラビド朝の軍事拠点として建設されたが、アラウィー朝の建国者の子、
スルターン、ムーレイ・イスマーイール（在位1672-1727年）がこれを帝都とし、フランスの
ヴェルサイユ宮殿に着想を得たとされる帝都を築いた。イスラーム様式とヨーロッパ様式が融合した
「スペイン＝ムーア様式」の都市で、高さ15メートル・全長40キロメートルに及ぶ城壁に囲まれる。
王宮区画にはムーレイ・イスマーイール廟・モスク、数千頭の馬を収容できるヘリ・エッ＝ソウアニ
厩舎、巨大な穀物庫がある。1996年、UNESCO世界遺産に登録された。

## kind の判定

`self-declared`とした。単一の統治者（ムーレイ・イスマーイール）の治世という明確な期間・
発注主体に紐づき、[ブルンコヴェネスク様式](brancovenesc-art.md)と同様、スルターン自身が
王朝の名のもとに多数の建設事業を自ら主導した点を重視した。

## 時間・空間

`originated_in`はメクネス（[place/meknes](../places/meknes.md)）。`time`はムーレイ・
イスマーイールの治世（1672-1727年）とした。

## 未着手

- ムーレイ・イスマーイールを person エンティティとして立てるかどうか
- 代表的な建造物（バーブ・マンスール門、ヘリ・エッ＝ソウアニ厩舎など）を work エンティティ
  として立てるかどうか
- 文化圏間接続（4経路）: ルイ14世からの外交贈答品（時計）がメクネスに現存する記録は見つけたが、
  これはフランスからモロッコへの一方向の贈答であり、本movement自体がeurope-westへ拡散した
  記録ではないため接続には数えなかった。検索した範囲では、海外美術館収蔵などmena外への
  文書化された接続は確認できない
