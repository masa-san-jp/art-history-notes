---
id: movement/hoysala-art
uri: urn:ahn:movement/hoysala-art
type: movement
kind: period-style
label_ja: ホイサラ美術
label_en: Hoysala Art
authority:
  wikidata: Q2361582
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1117"
  end: "13XX"
  display: "ヴィシュヌヴァルダナ王が1117年にベルールのチェンナケーシャヴァ寺院建立を
    命じたことを起点とした。王は後にハレビドゥへ遷都し、ホイサレーシュヴァラ寺院の建設は
    王の没年（1140年）を超えて子孫の代まで続いた。ホイサラ朝自体はc.1000-1346年に及ぶが、
    寺院建築・彫刻の様式的最盛期は12〜13世紀とされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Hoysala art / Hoysala architecture"
  note: "『ホイサラ美術』はホイサラ朝（政体）の名を借りた後代の美術史記述による様式区分。
    当事者（王・彫刻師）自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Chennakeshava_Temple,_Belur", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Chennakeshava_Temple,_Belur", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q2361582", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/belur}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://www.britishmuseum.org/collection/object/A_1967-1016-1"}
sources:
  - url: "https://www.wikidata.org/wiki/Q2361582"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Chennakeshava_Temple,_Belur"
    kind: reference
    note: "『Chennakeshava Temple, Belur』の項。1110年に即位したヴィシュヌヴァルダナ王が
      1117年にヴィシュヌ神を祀るチェンナケーシャヴァ寺院建立を命じ、同年に本殿が竣工・
      開眼したが、複合施設全体は以後100年余りにわたり拡張が続いたと記す。ホイサラ朝は
      c.1000-1346年に958の中心地で約1500の寺院を建てたと記す。ヴィシュヌヴァルダナは
      後にハレビドゥへ遷都し、ホイサレーシュヴァラ寺院の建設は王の没年（1140年）を超えて
      子孫の代（13世紀）まで続いたと記す"
  - url: "https://en.wikipedia.org/wiki/Hoysala_architecture"
    kind: reference
    note: "『Hoysala architecture』の項。11〜14世紀、現カルナータカ州のホイサラ朝統治下で
      発達した建築様式とし、寺院表面全体を覆う超写実的な彫刻・周回可能な基壇・多層の
      フリーズを特徴とすると記す。彫刻師の多くが自らの作品に署名したとも記す"
  - url: "https://www.britishmuseum.org/collection/object/A_1967-1016-1"
    kind: institutional
    note: "大英博物館収蔵《バイラヴァ神像》（花崗岩、カルナータカ、ホイサラ様式、
      1200-1250年頃）。シヴァ神の恐怖相バイラヴァを表し、剣・両面太鼓・生首・髑髏杯・
      三叉戟を持つ姿で、装身具に厚く覆われる点がホイサラ様式の特徴と記す"
status: draft
updated: 2026-09-16
---

# ホイサラ美術 / Hoysala Art

## 定義と範囲

英語版Wikipedia「[Chennakeshava Temple, Belur](https://en.wikipedia.org/wiki/Chennakeshava_Temple,_Belur)」
（参考資料）はこう記す（二次情報）。ホイサラ朝（c.1000-1346年、現カルナータカ州）の王
ヴィシュヌヴァルダナ（1110年即位）は、1117年に都[ベルール](../places/belur.md)にヴィシュヌ神を
祀るチェンナケーシャヴァ寺院の建立を命じ、本殿は同年に竣工・開眼したが、複合施設全体は
その後100年余り拡張が続いた。「Hoysala architecture」の項はさらに、王が後にハレビドゥへ
遷都し、ホイサレーシュヴァラ寺院の建設が王の没年（1140年）を超えて子孫の代（13世紀）まで
続いたと記す。ホイサラ様式は、寺院の外壁全体を覆う超写実的な彫刻・周回式の基壇・多層の
フリーズを特徴とし、ラーマーヤナ・マハーバーラタ・バーガヴァタ・プラーナなどの神話や
宮廷生活の場面を刻む。彫刻師の多くが自らの作品に署名を残したことでも知られる。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ホイサラ朝という政体の存続期間
（c.1000-1346年）を通じて、ベルール・ハレビドゥ・ソーマナータプラなど複数の中心地で
複数世代の王・彫刻師が同じ様式語彙を発展させ続けた点を、[チョーラ朝ブロンズ](chola-bronzes.md)・
[クメール美術](khmer-art.md)と同型の構造と見た。

## ロンドンでの収蔵

大英博物館は、カルナータカ産・ホイサラ様式（1200-1250年頃）の花崗岩製バイラヴァ神像を
所蔵する。これに基づき`relations`へ`diffused_to place/london`を張り、asia-south起源から
europe-westへの接続を記録した。

## 未着手

- ヴィシュヌヴァルダナ王を person エンティティとして立てるかどうか
- チェンナケーシャヴァ寺院・ホイサレーシュヴァラ寺院を work/place エンティティとして
  個別に立てるかどうか（本ファイルではベルールをoriginated_inの代表地とした）
- 2023年UNESCO世界遺産登録（「ホイサラの聖なる建築群」）の一次資料での確認
- メトロポリタン美術館所蔵のホイサラ関連彫刻の一次資料での確認
