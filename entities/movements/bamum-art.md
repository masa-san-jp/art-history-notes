---
id: movement/bamum-art
uri: urn:ahn:movement/bamum-art
type: movement
kind: period-style
label_ja: バムン美術
label_en: Bamum Art
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "『バムン美術』全体を指すWikidata項目は検索で特定できなかった。代表作『マンドゥ・
    イェヌ』王座の項目、バムン王国自体の項目は別途sourcesに記載した"
time:
  start: "1887~"
  end: "1933"
  display: "王イブラヒム・ンジョヤの治世（資料により1887年・1889年・1890年と幅がある）から、
    1933年の同王の死去までを、美術の隆盛期として扱う。フンバン王宮の建設は1917年"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Bamum art"
  note: "民族名『バムン（Bamum）』を冠した括りは後代の美術史・民族誌記述による呼称。当事者が
    自らの制作を『バムン美術』という運動名で名乗った記録は無い"
claims:
  - {field: time, source: "https://www.smb.museum/en/museums-institutions/ethnologisches-museum/collection-research/focus-on-collection-holdings/mandu-yenu-the-royal-throne-of-bamum/", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Foumban_Royal_Palace", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Kingdom_of_Bamum", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/foumban}
relations:
  - {type: diffused_to, target: place/berlin, certainty: scholarly, source: "https://www.smb.museum/en/museums-institutions/ethnologisches-museum/collection-research/focus-on-collection-holdings/mandu-yenu-the-royal-throne-of-bamum/"}
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "https://www.smb.museum/en/museums-institutions/ethnologisches-museum/collection-research/focus-on-collection-holdings/mandu-yenu-the-royal-throne-of-bamum/"}
sources:
  - url: "https://www.wikidata.org/wiki/Q1629505"
    kind: authority
    note: "Kingdom of Bamum（バムン王国）の項目"
  - url: "https://en.wikipedia.org/wiki/Kingdom_of_Bamum"
    kind: reference
    note: "『Kingdom of Bamum』の項。王ンジョヤ（在位ca.1887-1933年）が学校を設立し、絵文字を
      発明し、美術を庇護したと記す"
  - url: "https://en.wikipedia.org/wiki/Foumban_Royal_Palace"
    kind: reference
    note: "『Foumban Royal Palace』の項。宮殿の建設を1917年とし、王朝を1394年から現在までとする"
  - url: "https://www.smb.museum/en/museums-institutions/ethnologisches-museum/collection-research/focus-on-collection-holdings/mandu-yenu-the-royal-throne-of-bamum/"
    kind: institutional
    note: "ベルリン民族学博物館の公式ページ。王座『マンドゥ・イェヌ』の複製が1908年、ンジョヤ王から
      ドイツ皇帝ヴィルヘルム2世へ贈られ、現在同館所蔵であること、玉座がヨーロッパ産ガラスビーズと
      インド洋産の子安貝で装飾されていることを記す。パリのケ・ブランリー美術館にも別の玉座が
      所蔵されると記す"
status: draft
updated: 2026-09-16
---

# バムン美術 / Bamum Art

## 定義と範囲

英語版Wikipedia「[Kingdom of Bamum](https://en.wikipedia.org/wiki/Kingdom_of_Bamum)」はこう記す
（二次情報、原文引用）。

> Njoya (reigned 1890–1923), the best known of the Bamum kings, established schools, invented a
> system of pictographic writing, and patronized the arts.

王イブラヒム・ンジョヤ（在位年は資料により1887・1889・1890年と幅がある、1933年没）の庇護のもと、
ビーズ細工・木彫・象牙彫刻・金属工芸が花開いた。代表作が王座「マンドゥ・イェヌ（Mandu Yenu）」で、
ヨーロッパ産のガラスビーズとインド洋産の子安貝で全体が装飾され、双頭の蛇や大地の蜘蛛などバムン王権を
象徴する意匠が彫られている（ベルリン民族学博物館、機関資料）。

## kind の判定

`period-style` とした。バムン王朝自体は1394年に遡るとされるが、美術の隆盛はンジョヤ王一代の
庇護によるところが大きく、単一の血縁的な工房継承というより、王の庇護のもとで複数の専門職人
（ビーズ職人、木彫師、金属職人）が制作し続けた時代の枠として扱った。

## ベルリン・パリでの収蔵

1908年、ンジョヤ王は隣国ンソ王国への共同遠征の後、王座をドイツ皇帝ヴィルヘルム2世へ贈った。
現在この王座（の複製）はベルリンの民族学博物館が所蔵する。パリのケ・ブランリー美術館にも別の
バムン王座が所蔵される（同館公式ページ）。これに基づき`relations`へ`diffused_to`を
`place/berlin`・`place/paris`の双方に張り、africa-sub起源からeurope-westへの接続を記録した。

## 未着手

- 王イブラヒム・ンジョヤを person エンティティとして立てるかどうか
- 王座「マンドゥ・イェヌ」を work エンティティとして立てるかどうか
- ンジョヤの治世開始年（1887・1889・1890年）の食い違いの一次資料での解消
- バムン文字（Shümom）を concept として立てるかどうか（本項は視覚美術に絞り、文字体系は
  範囲外とした）
