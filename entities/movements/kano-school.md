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
relations:
  - {type: influenced_by, target: movement/song-academy-painting, certainty: scholarly, source: "https://ja.wikipedia.org/wiki/%E7%8B%A9%E9%87%8E%E5%85%83%E4%BF%A1"}
sources:
  - https://www.wikidata.org/wiki/Q252801
  - https://www.getty.edu/research/tools/vocabularies/aat/
  - https://ja.wikipedia.org/wiki/%E7%8B%A9%E9%87%8E%E5%85%83%E4%BF%A1
  - https://www.metmuseum.org/art/collection/search/36005
  - https://www.comuseum.com/painting/schools/zhe-school/
images:
  - url: https://images.metmuseum.org/CRDImages/as/original/LC-29_100_495gh_002.jpg
    source_page: https://www.metmuseum.org/art/collection/search/45219
    license: cc0
    note: "狩野永徳《中国の女性たちのいる宮廷庭園（Chinese Women in a Palace Garden）》16世紀後半、メトロポリタン美術館蔵（isPublicDomain: true）"
  - url: https://images.metmuseum.org/CRDImages/as/original/DP-12434-004.jpg
    source_page: https://www.metmuseum.org/art/collection/search/53009
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

発生地・活動地を京都とした。**これは通説（狩野正信の活動地）であり、一次資料・典拠IDでの裏は取れていない。**
Wikidata が持つのは country（日本）までで、都市の情報がない。江戸期には江戸へ移り、
奥絵師として幕府に仕えた系統が生まれる——**この移動（`diffused_to` / `patronized_by`）は未着手**。

### 中国からの受容——動いたのは物、そして起きたのは整理

`influenced_by` を[院体画](song-academy-painting.md)（中国・翰林図画院の画風、asia-east-china）へ
1本張った。**動いたのは人ではなく、日本に渡っていた中国絵画そのものである。**

日本語版Wikipedia「狩野元信」は、2代・元信（1476-1559）が直面した状況をこう書く——「当時の絵師は
牧谿様、夏珪様など宋や元時代の中国画人の作風で描くことを求められたが、日本にある彼らの作品は小品が
多く障壁画や屏風絵のような大画面の構成に不向きであった。そこで元信は、彼らの筆様の整理・統合し、
書体になぞらえた『真』『行』『草』の3種類の画体を確立、これを弟子たちに学ばせて、幅広い注文主の
要求に応えた」。そして「**真体は馬遠と夏珪、行体は牧谿、草体は玉澗の画風を元としている**」と明記する
（<https://ja.wikipedia.org/wiki/狩野元信>、二次情報）。

**この3画体のうち、`真体` の典拠として名指される馬遠・夏珪が院体画の担い手である。** 夏珪は
メトロポリタン美術館が「Chinese, active ca. 1195–1230」とする南宋画院の画家で、同館蔵
《山市晴嵐図》は本KBの[院体画](song-academy-painting.md)が代表図版として持つ作品でもある
（<https://www.metmuseum.org/art/collection/search/36005>）。

同記事はこの受容の性質も示している。**渡ってきた作品は小品ばかりで、日本側が必要としていた障壁画・
屏風という大画面には寸法が合わなかった。** だから狩野派がしたのは模倣ではなく、筆様を格付けして
再編成し、工房で分担生産できる体系に変えることだった——「多種多様な絵を大量制作できるこの方法は、
後の狩野派の制作体制を決定づける事になる」（同）。様式が渡ったのではなく、**渡った物の寸法の不一致が
制度を作った**という筋道になる。

**この1本の限界を書いておく。** 3画体のうち院体画に対応するのは `真体` だけで、`行体` の牧谿・
`草体` の玉澗は南宋の禅僧画家であり画院の画家ではない。牧谿・玉澗を含む禅林の水墨画を指す movement は
本KBに無いため、その2本は張れていない。また明代の[浙派](zhe-school.md)についても、
[comuseum.com](https://www.comuseum.com/painting/schools/zhe-school/) は浙派の様式が
「eventually influencing even Japanese artists of the Muromachi period」（室町時代の日本の画家にまで
影響した）と書くが、**狩野派を名指してはいない**。狩野派と浙派を直接結ぶ出典は今回得られなかったため、
浙派へのエッジは張らなかった。

## 未着手

- 担い手（狩野正信・元信・永徳・探幽）の person エンティティ
- 作品（証拠）の work エンティティ
- 幕府との関係（`patronized_by`）と、江戸への移動
- 琳派・土佐派との関係（同時代の並行は時間×空間から生成されるので、エッジは張らない）
- **禅林水墨画（牧谿・玉澗の系統）の movement 化。** 元信の3画体のうち `行体`・`草体` の典拠が
  ここに当たるが、本KBに該当する movement が無いため2本が張れていない。立てば狩野派から
  さらに2本、中国圏へのエッジが増える
- **狩野派と明代・浙派を直接結ぶ出典。** 浙派側の記述は「室町時代の日本の画家に影響した」までで
  狩野派を名指さない。日本側の記述（元信の3画体）が名指すのは南宋の馬遠・夏珪・牧谿・玉澗であって
  明代の画家ではない。両者を繋ぐ研究があるかは未調査
- 元信が実際に見た中国絵画の所在——東山御物（足利将軍家の唐物コレクション）を経由したのか、
  禅宗寺院の所蔵品だったのか。日本語版Wikipedia「狩野元信」には受容経路への具体的な言及が無い
