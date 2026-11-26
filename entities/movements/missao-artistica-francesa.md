---
id: movement/missao-artistica-francesa
uri: urn:ahn:movement/missao-artistica-francesa
type: movement
kind: self-declared
label_ja: フランス美術使節団
label_en: Missão Artística Francesa
authority:
  wikidata: Q3316787
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1816"
  end: null
  display: "1816年3月、フランス人芸術家・職人の一団がリオデジャネイロに到着した。ジョアキン・
    ルブルトンが率い、ドン・ジョアン6世が資金を出した。ナポレオン失脚後のボナパルト派芸術家を
    含んでいたとされる"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Missão Artística Francesa"
  note: "『フランス美術使節団』という呼称が当時から公的に使われていたのか、後代の歴史記述に
    よる呼称なのかを区別する一次資料に本調査では到達していない。王室の招聘による公的な性格を
    持つ集団だったことは確実だが、self_identifiedは慎重にfalseとした"
claims:
  - {field: time, source: "https://doi.org/10.1590/S0101-47142006000200009", certainty: scholarly}
  - {field: originated_in, source: "https://doi.org/10.1590/S0101-47142006000200009", certainty: scholarly}
  - {field: kind, source: "https://doi.org/10.11606/issn.2176-8099.pcso.2007.75459", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/rio-de-janeiro}
relations:
  - {type: diffused_to, target: place/paris, certainty: scholarly, source: "http://arts-graphiques.louvre.fr/detail/artistes/0/757-DEBRET-Jean-Baptiste"}
  - {type: derives_from, target: movement/neoclassicism, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Miss%C3%A3o_Art%C3%ADstica_Francesa"}
sources:
  - url: "https://www.wikidata.org/wiki/Q3316787"
    kind: authority
  - url: "https://en.wikipedia.org/wiki/Miss%C3%A3o_Art%C3%ADstica_Francesa"
    kind: reference
    note: "『Missão Artística Francesa』の項。1816年3月、ジョアキン・ルブルトンに率いられ
      リオデジャネイロに到着したフランス人芸術家・職人の一団とし、ドン・ジョアン6世の招聘・
      資金提供によると記す。画家ジャン＝バティスト・デブレ、風景画家ニコラ・アントワーヌ・
      トーネー、彫刻家オーギュスト・マリー・トーネー、建築家グランジャン・ド・モンティニーらを
      構成員とする"
  - url: "https://doi.org/10.1590/S0101-47142006000200009"
    kind: scholarly
    note: "Elaine Dias『Correspondências entre Joachim Le Breton e a corte portuguesa na Europa: o nascimento da Missão Artística de 1816』Anais do Museu Paulista 14(2), 2006。リスボンのトーレ・ド・トンボ国立文書館の書簡を扱う査読論文。1816年3月のフランス人のリオデジャネイロ到着と、ルブルトンが宮廷と交わした招聘の経緯を述べる。取得日2026-11-24、SciELO本文（scielo.br）から確認"
  - url: "https://doi.org/10.11606/issn.2176-8099.pcso.2007.75459"
    kind: scholarly
    note: "Anderson Ricardo Trevisan、Plural（サンパウロ大学）2007掲載のデブレ論。デブレが1816年に画家として渡ブラジルし1831年まで滞在した『Missão Artística Francesa』の歴史画家だったと記す。取得日2026-11-24、revistas.usp.brの論文ページから確認"
  - url: "http://arts-graphiques.louvre.fr/detail/artistes/0/757-DEBRET-Jean-Baptiste"
    kind: institutional
    note: "ルーヴル美術館版画素描部門のジャン＝バティスト・デブレのコレクションページ"
status: verified
updated: 2026-11-24
---

# フランス美術使節団 / Missão Artística Francesa

## 定義と範囲

英語版Wikipedia「[Missão Artística Francesa](https://en.wikipedia.org/wiki/Miss%C3%A3o_Art%C3%ADstica_Francesa)」
はこう記す（二次情報、原文引用）。

> The French Artistic Mission ... was a group of French artists, artisans, and architects who
> arrived in Rio de Janeiro in March 1816.

1808年、ナポレオン軍の侵攻を逃れてポルトガル王室がリスボンからリオデジャネイロへ遷都した後、
ドン・ジョアン6世がフランス美術アカデミーに倣った美術学校を組織するためこの一団を招聘したと
される。構成員は、画家ジャン＝バティスト・デブレ、風景画家ニコラ・アントワーヌ・トーネー、
彫刻家オーギュスト・マリー・トーネー、建築家グランジャン・ド・モンティニー、版画家シャルル・
シモン・プラディエ、作曲家ジグムント・ノイコムなど。デブレは王族の肖像・祝典装飾・王立劇場の
舞台美術を手がけ、レオポルディーナ王女の上陸やペドロ1世の戴冠などブラジル史の場面も描いた。

## kind の判定

`self-declared`とした。単一の様式運動というより、王室の招聘に応じて結成され、ブラジルに
西欧式の美術アカデミー教育制度を導入するという明確な目的・団体性を持つ集団だった点を重視した。

## パリでの収蔵

デブレは1831年にフランスへ帰国し、その旅行記『Voyage pittoresque et historique au Brésil』
（1834-39年）を刊行した。ルーヴル美術館版画素描部門はデブレの作品を所蔵する。これに基づき
`relations`へ`diffused_to place/paris`を張り、americas-latin起源からeurope-westへの接続を
記録した。

## ネオクラシシズムとの関係

英語版Wikipedia「[Missão Artística Francesa](https://en.wikipedia.org/wiki/Miss%C3%A3o_Art%C3%ADstica_Francesa)」
（参考資料）は、フランス使節団がブラジルにおける[ネオクラシシズム（新古典主義）](neoclassicism.md)
の強化に結びついているとし、使節団の芸術家・職人たちがブラジルにこの様式を導入・定着させる
決定的な役割を果たしたと記す。トーネーをはじめとする画家たちが新古典主義様式で制作したとも
記す。これに基づき`relations`へ`derives_from movement/neoclassicism`を張った。

## 一次寄りの確認（2026-11-24）

Elaine Dias（2006、[doi:10.1590/S0101-47142006000200009](https://doi.org/10.1590/S0101-47142006000200009)）は、
リスボンのトーレ・ド・トンボ国立文書館に残るジョアキン・ルブルトンと宮廷の往復書簡から「1816年の
美術使節団」の成立を辿る。同論文は、フランス人の到着を1816年3月のリオデジャネイロとし、書簡の中で
ブラジル人芸術家を計画に含める提案が出ていたことも述べる。Trevisan（2007、
[doi:10.11606/issn.2176-8099.pcso.2007.75459](https://doi.org/10.11606/issn.2176-8099.pcso.2007.75459)）は、
デブレを使節団が作った教育計画の歴史画家とする。これらは`time`の開始年・`originated_in`・団体としての
性格の根拠として`claims`に使った。

## 未着手

- **未確認**: 使節団の名称が当時の公文書にあったかは、上の2論文からは判別できていない。
  `naming.self_identified`をfalseのままにしている理由である

- ジャン＝バティスト・デブレ、ニコラ・アントワーヌ・トーネーらを person エンティティとして
  立てるかどうか
- リオデジャネイロの王立美術学校（現ブラジル国立美術学校）を org エンティティとして立てる
  かどうか
- 使節団の解散・活動終了年（`time.end`が未確定）の一次資料での確認
