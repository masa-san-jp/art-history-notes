---
id: movement/de-stijl
uri: urn:ahn:movement/de-stijl
type: movement
kind: self-declared
label_ja: デ・ステイル
label_en: De Stijl
authority:
  wikidata: Q207445
  aat: "300021259"
  ndl: "00561490"
  jpsearch: null
  none_reason: null
time:
  start: "1917"
  end: "1931"
  display: "1917年（ライデンで雑誌・結社が成立）〜1931年（運動の解散）"
naming:
  self_identified: true
  named_by: null
  named_when: "1917"
  original_label: "De Stijl"
  note: "テオ・ファン・ドゥースブルフが1917年にライデンで創刊した雑誌の名称が、その周囲に形成された芸術家・建築家・デザイナーの運動名になった。雑誌名と運動名のどちらも当事者の公的な活動基盤として使われたため、自称として扱う"
claims:
  - {field: time, source: "https://sammlung.staedelmuseum.de/en/person/de-stijl", certainty: scholarly}
  - {field: originated_in, source: "https://www.lakenhal.nl/en/story/de-stijl", certainty: scholarly}
  - {field: kind, source: "https://www.moma.org/collection/terms/de-stijl?sanity_preview=true&sanity_preview_secret=d51b1526-f689-4f33-b7c5-896dca252e7a", certainty: scholarly}
space:
  - {role: originated_in, target: place/leiden}
relations:
  - {type: influenced_by, target: movement/cubism, certainty: scholarly, source: "https://assets.moma.org/documents/moma_catalogue_2748_300086869.pdf"}
images:
  - url: "https://commons.wikimedia.org/wiki/Special:FilePath/Stijl_vol_03_nr_01_p_003.jpg"
    source_page: "https://commons.wikimedia.org/wiki/File:Stijl_vol_03_nr_01_p_003.jpg"
    license: public-domain
    note: "テオ・ファン・ドゥースブルフが編集した『De Stijl』1919年11月号のページ。Commonsのファイルページでパブリックドメインと確認できる"
sources:
  - https://www.wikidata.org/wiki/Q207445
  - https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021259
  - https://sammlung.staedelmuseum.de/en/person/de-stijl
  - https://www.lakenhal.nl/en/story/de-stijl
  - https://www.moma.org/collection/terms/de-stijl?sanity_preview=true&sanity_preview_secret=d51b1526-f689-4f33-b7c5-896dca252e7a
  - https://www.moma.org/documents/moma_catalogue_1798_300159061.pdf
  - https://assets.moma.org/documents/moma_catalogue_2748_300086869.pdf
  - https://commons.wikimedia.org/wiki/File:Stijl_vol_03_nr_01_p_003.jpg
status: draft
updated: 2026-08-11
---

# デ・ステイル / De Stijl

## 定義と範囲

1917年にオランダのライデンでテオ・ファン・ドゥースブルフが雑誌『De Stijl』を創刊し、その周囲に
形成された画家・建築家・デザイナーの国際的な運動。MoMAは、自然主義的表現を離れ、直線、矩形の面、
原色を中心とする抽象を推進した運動として説明する。

デ・ステイルは絵画だけの様式ではない。メンバーは、建築、家具、室内、タイポグラフィまでを含む生活
環境全体を、要素的な形態と色彩の秩序によって再構成しようとした。雑誌は理念を共有するための媒体で
あり、運動の境界を固定した単一の学校や工房ではない。

## kind の判定

`self-declared` とした。運動の名称は、ファン・ドゥースブルフが自ら編集・刊行した雑誌の題名であり、
その雑誌を活動基盤として参加者が理念を公表した。後世の批評家が便宜的に付けた括りではなく、当事者が
使った名称を中心に成立している。

## 時間

始点は1917年。ライデンで雑誌『De Stijl』が創刊され、そこに画家・建築家・デザイナーが集まって運動が
形成された時期である。雑誌は1928年まで刊行されたが、運動の結社・集団としての終点は資料により1931年
または1932年と揺れる。このエントリでは、シュテーデル美術館の整理に合わせて1931年とする。

この終点は、直交する線、原色、非対称の構成という原理が後世のデザインへ影響し続けたことを否定しない。
1931年以後の受容は、運動そのものの活動期間とは分けて扱う。

## 空間

発生地はライデン。ファン・ドゥースブルフによる雑誌創刊地であり、運動名が成立した場所である。

その後の活動はオランダ一都市に閉じず、参加者の移動と雑誌の国際的な寄稿を通じて広がった。ただし、
本エントリでは未調査の都市を `active_in` として増やしていない。

## キュビスムからネオ・プラスティシスムへ

MoMAの『Cubism and Abstract Art』カタログは、1910年にパリへ移ったピート・モンドリアンがピカソの
影響を受け、1911年から1915年にかけて構成を抽象化していった経路を示す。これはデ・ステイル全体が
キュビスムの単純な後継だったという意味ではなく、運動の主要な形成要素であるモンドリアンのネオ・
プラスティシスムに限定した `influenced_by` である。

## バウハウスとの関係

デ・ステイルからバウハウスへの影響を記録する。MoMAの展覧会カタログは、テオ・ファン・ドゥースブルフの
講義やデ・ステイルの幾何学的構成が、バウハウスの建築・タイポグラフィ・家具などに影響したと論じる。
したがって、既存の [バウハウス](bauhaus.md) 側に `influenced_by → movement/de-stijl` を追加した。

ここで記録するのは、両運動が同じだったという意味ではない。デ・ステイルの抽象的な秩序と、バウハウスが
後に展開した機能・素材・工房教育の統合は重なる部分を持つが、同一視はしない。

## 未着手

- ファン・ドゥースブルフ、ピート・モンドリアン、バルト・ファン・デル・レック、ヘリット・リートフェルトらの人物エンティティ化
- 雑誌各号と1918年の宣言・論文の一次資料化
- ユトレヒト、パリ、ワイマールなど、参加者・講義・建築作品に即した活動地の追加
- 構成主義、ダダとの関係。類似だけで影響線を増やさない
- 1931年／1932年の終点の差を、結社・雑誌・理念のどの単位で区切るかの精密化
