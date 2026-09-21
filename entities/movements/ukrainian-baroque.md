---
id: movement/ukrainian-baroque
uri: urn:ahn:movement/ukrainian-baroque
type: movement
kind: period-style
label_ja: ウクライナ・バロック
label_en: Ukrainian Baroque
authority:
  wikidata: Q1542287
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "16XX"
  end: "17XX"
  display: "17〜18世紀、コサック・ヘーチマン国家（Hetmanate）の時代に広まった。ヘーチマン、
    イヴァン・マゼーパの治世（1687-1708年）に最盛期を迎えたとされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Українське бароко"
  note: "『ウクライナ・バロック』（別名『コサック・バロック』『マゼーパ・バロック』）は後代の
    美術史記述による呼称。『マゼーパ・バロック』はヘーチマン、イヴァン・マゼーパの個人名に
    由来するが、マゼーパ自身がこの様式を自らの名で名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Ukrainian_Baroque", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Ukrainian_Baroque", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Ukrainian_Baroque", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/kyiv}
relations:
  - {type: derives_from, target: movement/baroque, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Ukrainian_Baroque"}
sources:
  - url: "https://www.wikidata.org/wiki/Q1542287"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Ukrainian_Baroque"
    kind: reference
    note: "『Ukrainian Baroque』の項。17〜18世紀にウクライナで広まった様式とし、ヘーチマン、
      イヴァン・マゼーパの治世（1687-1708年）に最盛期を迎えたと記す。キーウ・チェルニーヒウを
      中心地とし、西欧バロックより装飾が控えめで単純な形態を特徴とすると記す"
  - url: "https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CP%5CA%5CPortraiture.htm"
    kind: reference
    note: "ウクライナ百科事典の『Portraiture』項。ラテン語persona由来の『パルスナ（parsunnyi）』
      肖像画が、フメリニツキー・マゼーパら歴代ヘーチマンを正装で描いたと記す"
status: draft
updated: 2026-09-21
---

# ウクライナ・バロック / Ukrainian Baroque

## 定義と範囲

英語版Wikipedia「[Ukrainian Baroque](https://en.wikipedia.org/wiki/Ukrainian_Baroque)」は
こう記す（二次情報、原文引用）。

> Ukrainian Baroque ... also known as Cossack Baroque ... or Mazepa Baroque, is an artistic style
> that was widespread in Ukraine in the 17th and 18th centuries.

コサック・ヘーチマン国家の時代、地元の伝統と西欧[バロック](baroque.md)が融合して生まれた
様式で、西欧のバロックに比べ装飾が控えめで単純な形態を特徴とする（同項）。この記述に基づき
`relations`へ`derives_from movement/baroque`を張った。キーウ（[place/kyiv](../places/kyiv.md)）・
チェルニーヒウが中心地とされ、キエフ・ペチェールシク大修道院などの教会建築群が代表例とされる。
イコン画も17世紀初頭に東部ウクライナで復興し、教会だけでなく台頭するコサック上層階級も
発注者となった（同項）。

世俗の肖像画としては、ラテン語「persona」に由来する「パルスナ（parsunnyi）」と呼ばれる形式が
発達し、ボフダン・フメリニツキー、イヴァン・マゼーパ、イヴァン・スコロパードシクィイら歴代
ヘーチマンを正装・儀礼具とともに描いた（ウクライナ百科事典「Portraiture」項、二次情報）。

## kind の判定

`period-style` とした。単一の血縁・工房ではなく、コサック・ヘーチマン国家という政体の存続期間を
通じて、複数の担い手（建築家、イコン画家、パルスナの画家）が制作し続けた点を、
[タルノヴォ画派](tarnovo-artistic-school.md)・[サンテロ](santero.md)と同型の構造と見た。

## 未着手

- イヴァン・マゼーパ、ボフダン・フメリニツキーら歴代ヘーチマンを person エンティティとして
  立てるかどうか（今回は本文中の記述にとどめた）
- 代表的な建築物（キエフ・ペチェールシク大修道院など）を work エンティティとして立てるかどうか
- ~~文化圏間接続（4経路）: 検索した範囲では、海外美術館収蔵などeurope-east外への文書化された
  接続は見つけられなかった~~ → 2026-09-21解消。`derives_from movement/baroque`
  （発生地パリ、europe-west）を張ったことでmovement-relation経路が成立し、
  `config/cross-region-reviews.yaml`の当該エントリは削除した
