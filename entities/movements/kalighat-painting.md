---
id: movement/kalighat-painting
uri: urn:ahn:movement/kalighat-painting
type: movement
kind: retrospective
label_ja: カーリーガート絵画
label_en: Kalighat Painting
authority:
  wikidata: Q6352595
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "18XX"
  end: "19XX"
  display: "紙・顔料の物質的証拠から19世紀前半に遡るとされる。V&Aは1830年代から1930年代の
    100年間にわたり制作・収集されたと記す"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Kalighat painting"
  note: "『カーリーガート』はコルカタのカーリー女神を祀る寺院の名を借りた後代の美術史記述
    による呼称。無名の絵師たちが寺院参詣者向けに制作した大衆絵画であり、当事者自身が
    一つの様式movementとして名乗った記録は無い"
claims:
  - {field: time, source: "https://www.vam.ac.uk/articles/kalighat-painting", certainty: scholarly}
  - {field: originated_in, source: "https://www.vam.ac.uk/articles/kalighat-painting", certainty: scholarly}
  - {field: kind, source: "https://www.vam.ac.uk/articles/kalighat-painting", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/kolkata}
relations:
  - {type: diffused_to, target: place/london, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Kalighat_painting"}
  - {type: diffused_to, target: place/moscow, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Kalighat_painting"}
sources:
  - url: "https://www.wikidata.org/wiki/Q6352595"
    kind: authority
  - url: "https://www.vam.ac.uk/articles/kalighat-painting"
    kind: institutional
    note: "V&Aの解説記事（最終更新2024-04-17）。2026-11-16に取得。19世紀コルカタ（旧カルカッタ）で
      発達した独自のジャンルとし、1830年代から1930年代の100年間に制作・収集された約645点を
      所蔵すると記す。制作者は寺院参詣者向けに安価な絵を売って生計を立てたパトゥア（画工）で、
      Kalighatはフーグリー川沿いの沐浴場（ガート）に由来する地名と記す"
  - url: "https://collections.vam.ac.uk/item/O432772/"
    kind: institutional
    note: "V&A《Vishnu as Narasimha avatar》（IS.196-1950）。2026-11-16にV&A API
      （museumobject/O432772）で様式欄「Kalighat」、制作地「Kolkata」、制作年「ca. 1830」を確認。
      同館のO71567（IS.32-1952、ca. 1900）も様式欄「Kalighat」・制作地「Kolkata」。
      1930年代までの下限と、kindの根拠にあたる命名の経緯は、この資料では確認できていない"
  - url: "https://en.wikipedia.org/wiki/Kalighat_painting"
    kind: reference
    note: "『Kalighat painting』の項。用紙・顔料の物質的証拠から19世紀前半に遡るとし、
      コルカタのカーリー女神寺院周辺で発達したと記す。大胆な輪郭線・鮮やかな色調・
      最小限の背景を特徴とし、手漉き紙・機械漉き紙の両方に、神話的な図像・ヒンドゥーの
      神々に加え、社会が変容していく当時の世相を映す同時代の日常場面も描いたと記す。
      V&Aは1830年代から1930年代の100年間にわたり制作・収集されたコレクションを持ち、
      世界最大の645点を所蔵すると記す。他にオックスフォード大学ボドリアン図書館110点、
      モスクワのプーシキン美術館62点、ペンシルベニア大学博物館57点、プラハのナープルステク
      博物館26点、カーディフの国立ウェールズ博物館25点、大英図書館（インド・オフィス・
      ライブラリー）17点を所蔵すると記す"
status: verified
updated: 2026-11-16
---

# カーリーガート絵画 / Kalighat Painting

## 定義と範囲

英語版Wikipedia「[Kalighat painting](https://en.wikipedia.org/wiki/Kalighat_painting)」
（参考資料）はこう記す（二次情報）。用紙・顔料の物質的証拠から19世紀前半に遡るとされる
カーリーガート絵画は、[コルカタ](../places/kolkata.md)のカーリー女神寺院周辺で、参詣者
向けの土産として無名の絵師たちにより制作された。大胆な輪郭線・鮮やかな色調・最小限の
背景を特徴とし、神話的図像・ヒンドゥーの神々に加え、植民地期の社会変容を映す同時代の
日常場面も描いた。

## kind の判定

`retrospective`とした。『カーリーガート』は寺院の地名を借りた後代の美術史記述による
呼称であり、無名の絵師たちが寺院参詣者向けに制作した大衆絵画である。単一の血縁・工房
ではなく、複数世代の絵師が同じ様式的慣行（大胆な輪郭線・鮮やかな色調）を共有し続けた点を、
[アカン金分銅](akan-goldweights.md)と同型の構造と見た。

## ロンドン・サンクトペテルブルクでの収蔵

ヴィクトリア&アルバート博物館（ロンドン）は、1830年代から1930年代にかけて収集された
世界最大のカーリーガート絵画コレクション（645点）を所蔵する。モスクワのプーシキン美術館
も62点を所蔵する。これに基づき`relations`へ`diffused_to`を`place/london`・
`place/moscow`の双方に張り、asia-south起源からeurope-westおよびeurope-east
（本KBのregionバケット上、ロシア）への接続を記録した。

## 未着手

- オックスフォード大学ボドリアン図書館、ペンシルベニア大学博物館、プラハのナープルステク
  博物館、カーディフの国立ウェールズ博物館、大英図書館の各コレクションの一次資料での確認
- 代表的な個々の絵師・作品を person/work エンティティとして立てるかどうか
- 19世紀前半という起点年代の学術論文での確認
- **未確認**: 「Kalighat painting」という呼称を誰がいつ付けたか。V&Aの記事は地名の由来と制作者が
  無名のパトゥアだったことは記すが、命名者は記さない
