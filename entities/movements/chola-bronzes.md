---
id: movement/chola-bronzes
uri: urn:ahn:movement/chola-bronzes
type: movement
kind: period-style
label_ja: チョーラ朝ブロンズ
label_en: Chola Bronzes
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "『チョーラ朝ブロンズ』全体を指すWikidata項目は検索で特定できなかった。代表作
    《舞踏の王シヴァ（ナタラージャ）》個別像のWikidata項目（Q117069756）は別途参考として
    sourcesに記載した"
time:
  start: "0880"
  end: "1279"
  display: "メトロポリタン美術館は所蔵作の帰属年代をチョーラ朝期（880-1279年）とする。ブロンズ
    鋳造自体は8世紀から16世紀まで作られ続けたとする資料もあるが、チョーラ王朝の存続期間
    （9〜13世紀）に絞った"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Chola bronzes"
  note: "王朝名『チョーラ』を冠した後代の美術史記述による括り。当事者（タンジャーヴール・
    ティルチラーパッリの鋳造職人）自身がこの名で自らの制作を呼んだ記録は無い"
claims:
  - {field: time, source: "https://www.metmuseum.org/art/collection/search/39328", certainty: scholarly}
  - {field: originated_in, source: "https://www.bmimages.com/preview.asp?image=00033974001", certainty: scholarly}
  - {field: kind, source: "https://www.metmuseum.org/art/collection/search/39328", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/thanjavur}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://www.bmimages.com/preview.asp?image=00033974001"}
  - {type: diffused_to, target: place/new-york-city, certainty: scholarly, source: "https://www.metmuseum.org/art/collection/search/39328"}
sources:
  - url: "https://www.wikidata.org/wiki/Q117069756"
    kind: authority
    note: "個別像《ナタラージャ（初期チョーラ期のブロンズ）》の項目"
  - url: "https://www.metmuseum.org/art/collection/search/39328"
    kind: institutional
    note: "メトロポリタン美術館収蔵《舞踏の王シヴァ（ナタラージャ）》。タミル・ナードゥ州、
      チョーラ朝期（880-1279年）と帰属年代を記す"
  - url: "https://www.bmimages.com/preview.asp?image=00033974001"
    kind: institutional
    note: "大英博物館収蔵《ナタラージャ像》（登録番号1987,0314.1）。タンジャーヴール、
      チョーラ朝、c.1100年、高さ89.50cmの一鋳造品と記す"
status: draft
updated: 2026-09-16
---

# チョーラ朝ブロンズ / Chola Bronzes

## 定義と範囲

南インド・タミル・ナードゥ州のチョーラ朝期（880-1279年）に、蝋型鋳造（ロストワックス、
マドゥチュチシュタ・ヴィダーナ）で作られたヒンドゥー教神像のブロンズ彫刻。代表的な図像が
シヴァ神を舞踏の王として表す「ナタラージャ」で、10〜12世紀のチョーラ王権下で特に盛んに
作られたとされる（WebSearch経由、複数の二次情報）。祭礼の行列に担がれる神体として、
装身具をまとわせて崇拝された。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、チョーラ王朝という政体の存続期間を通じて、
[タンジャーヴール](../places/thanjavur.md)・ティルチラーパッリ地域の複数世代の鋳造職人が
制作し続けた点を、[クメール美術](khmer-art.md)・[サンテロ](santero.md)と同型の構造と見た。
既存の[tanjore-painting](tanjore-painting.md)（タンジョール絵画、後代の絵画様式）とは
時代・媒体（絵画とブロンズ彫刻）の両方で異なる別のmovementとして扱った。

## ロンドン・ニューヨークでの収蔵

大英博物館は「タンジャーヴール、チョーラ朝、c.1100年」のナタラージャ像（登録番号1987,0314.1、
高さ89.50cm）を所蔵する。メトロポリタン美術館も「タミル・ナードゥ州、チョーラ朝期
（880-1279年）」のナタラージャ像を所蔵する。これに基づき`relations`へ`diffused_to`を
`place/london`・`place/new-york-city`の双方に張り、asia-south起源からeurope-west・
americas-northへの接続を記録した。

## 未着手

- 個別のナタラージャ像を work エンティティとして立てるかどうか
- ブロンズ鋳造が8〜16世紀まで続いたとする資料と、チョーラ王朝の存続期間（9〜13世紀）に
  限定した本項の範囲との関係の整理（王朝滅亡後も同じ鋳造伝統が続いたのか、別movementとして
  分けるべきかは今回未確認）
- 蝋型鋳造の技法（マドゥチュチシュタ・ヴィダーナ）の一次資料での確認
