---
id: movement/kano-school
uri: urn:ahn:movement/kano-school
type: movement
kind: lineage-school
label_ja: 狩野派
label_en: Kanō school
authority:
  wikidata: Q252801
  aat: "300018653"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "14XX"
  end: "1868~"
  display: 15世紀（室町後期）〜明治維新。Wikidata の inception は +1500-00-00 / precision 7 ＝「15. century」（1401–1500）で、年ではなく世紀の主張
naming:
  self_identified: true
  named_by: null
  named_when: null
  original_label: 狩野派
  note: 家名がそのまま呼称になっており、命名という行為が存在しない型。西洋の -ism のように誰かが名付けた運動ではない
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q252801", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q252801", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
  - {role: active_in, target: place/kyoto}
  - {role: active_in, target: place/tokyo}
relations:
  - {type: influenced_by, target: movement/song-academy-painting, certainty: scholarly, source: "https://www.kyohaku.go.jp/jp/assets/press/2027_kano_press_0608-02ver.pdf"}
sources:
  - url: "https://www.wikidata.org/wiki/Q252801"
    kind: authority
  - url: "https://www.getty.edu/research/tools/vocabularies/aat/"
    kind: authority
  - url: "https://www.kyohaku.go.jp/jp/assets/press/2027_kano_press_0608-02ver.pdf"
    kind: scholarly
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/LC-29_100_495gh_002.jpg
    source_page: https://www.metmuseum.org/art/collection/search/45219
    rights_source: https://www.metmuseum.org/art/collection/search/45219
    license: cc0
    note: "狩野永徳《中国の女性たちのいる宮廷庭園（Chinese Women in a Palace Garden）》16世紀後半、メトロポリタン美術館蔵（isPublicDomain: true）"
  - url: https://images.metmuseum.org/CRDImages/as/original/DP-12434-004.jpg
    source_page: https://www.metmuseum.org/art/collection/search/53009
    rights_source: https://www.metmuseum.org/art/collection/search/53009
    license: cc0
    note: "狩野探幽《四季山水図（Landscapes of the Four Seasons）》1630年代、メトロポリタン美術館蔵（isPublicDomain: true）"
status: draft
updated: 2026-08-08
---

# 狩野派 / Kanō school

## 定義と範囲

室町後期から明治維新まで約400年続いた日本絵画の画派。狩野正信に始まり、血縁と養子縁組、
工房の徒弟制度によって継承された。

典拠: Wikidata [Q252801](https://www.wikidata.org/wiki/Q252801)／Getty AAT `300018653`

## 南宋院体画との関係

京都国立博物館の公式資料は、狩野正信が足利将軍家の所蔵する中国絵画を手本に制作したと説明し、
図様の類似する模本の存在から、正信がその中の**南宋院体画などに学んだ**と推定している。
ここで記録するのは、狩野派全体が院体画だけから成立したという意味ではなく、狩野派の始祖・正信が
日本へ移入されていた南宋院体画を具体的な参照対象として受け取った経路である。

このため、受け取り側である狩野派から[院体画](song-academy-painting.md)へ
`influenced_by` を張った。根拠は、作品の図様と模本、足利将軍家のコレクションという具体的な
媒介を挙げた京都国立博物館の資料である。

## kind の判定 — なぜ `lineage-school` か

`self-declared`（当事者が名乗った運動）でも `retrospective`（後付けの括り）でもない。
**血縁と工房の継承体**であり、制度としての実体を持つ。Wikidata は Q252801 に
`art movement`（Q968159）と並んで **`family`（Q8436）** を付けており、この二重性がそのまま
「運動ではなく家系」という性質を示している。

西洋の「-ism」のように誰かが唱えて名乗った運動ではなく、家と職が続いた集団である。

## 時間

- Wikidata の inception は **+1500-00-00 / precision 7**。これは「1500年」ではなく**世紀の主張**で、
  Wikidata 自身の描画は「15. century」（＝1401–1500）。だから EDTF は `14XX`。
  英語記述の "late 15th century" とも一致する。当初 `1500~`（およそ1500年）と書いていたのは
  precision を見ていなかったための誤り（2026-08-08 に土佐派を調べた際に発覚し、訂正）。
- 終期は明治期の解体。`1868~` として持つ。**未確認**: 「いつ終わったか」は解体の定義次第で、
  一次資料に当たっていない。

## 空間

発生地を京都、活動地を京都と江戸（現在の東京）とした。京都は狩野正信の活動地という通説に基づき、
一次資料・典拠IDでの都市レベルの裏付けは未確認である。江戸期には活動を江戸へ広げ、狩野探幽を筆頭とする
一門が幕府御用絵師として活動した。京都国立博物館は、この系統を「江戸狩野」と呼び、幕末まで画壇の中心だったと説明する
（[京都国立博物館「京都の狩野派―狩野永納・永敬」](https://www.kyohaku.go.jp/jp/exhibitions/collection/2026/02/?date=03)）。
ここでは都市間の活動拡散を `active_in` で記録する。幕府による具体的な庇護関係の `patronized_by` は、幕府側の組織エンティティと個別の奥絵師職の典拠を確認してから追加する。

## 未着手

- 担い手（狩野正信・元信・永徳・探幽）の person エンティティ
- 作品（証拠）の work エンティティ
- 幕府との関係（`patronized_by`）の組織・職制レベルでの記録
- 琳派・土佐派との関係（同時代の並行は時間×空間から生成されるので、エッジは張らない）
