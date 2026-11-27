---
id: movement/baroque
uri: urn:ahn:movement/baroque
type: movement
kind: period-style
label_ja: バロック
label_en: Baroque
authority:
  wikidata: Q37853
  aat: "300021147"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "15XX"
  end: "17XX"
  display: "16世紀後半（イタリアでの初期形成）〜18世紀半ば頃"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Baroque"
  note: "後世の美術史が、劇的な空間、運動感、光、古典・宗教的伝統の再編を横断して括った文化運動・様式。地域別の実践を一つの均質な作風とはみなさない"
claims:
  - {field: time, source: "https://www.metmuseum.org/ko/essays/baroque-rome", certainty: scholarly}
  - {field: originated_in, source: "https://www.metmuseum.org/ko/essays/baroque-rome", certainty: scholarly}
  - {field: kind, source: "https://www.metmuseum.org/ko/essays/baroque-rome", certainty: scholarly}
space:
  - {role: originated_in, target: place/rome}
relations:
  - {type: diffused_to, target: place/mexico-city, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Baroque"}
  - {type: diffused_to, target: place/lima, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Baroque"}
sources:
  - url: "https://www.wikidata.org/wiki/Q37853"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021147"
    kind: authority
  - url: "https://www.metmuseum.org/ko/essays/baroque-rome"
    kind: institutional
  - url: "https://en.wikipedia.org/wiki/Baroque"
    kind: reference
    note: "『Baroque』の項（2026-11-28取得、MediaWiki API）。「Baroque in the Spanish and Portuguese Colonial Americas」の節で、バロックが新大陸へ移り、メキシコ・ペルーが主要な中心であること、メキシコ市のラ・プロフェサ教会、リマ、クスコのイエズス会教会・サン・フランシスコ聖堂などを例に挙げる。二次情報"
status: verified
updated: 2026-11-28
---

# バロック / Baroque

16世紀後半のイタリアで形成され、17世紀のローマを重要な中心としてヨーロッパと植民地世界へ広がった
文化運動・様式。建築、絵画、彫刻、都市計画を統合し、劇的な光、運動、身体性、宗教的・世俗的な観者の
経験を組織した。

## kind の判定

`period-style` とした。Baroque は単一の自称集団ではなく、複数地域の実践を後世にまとめる名称である。
メトロポリタン美術館は、17世紀のローマが教会・都市・芸術の総合的な表現としてバロックの中心になったと
説明する。

## 空間と時間

イタリアでの初期形成を含めて始点を `15XX`、Wikidata の1750年代という終期を包含するよう `17XX` とした。
ローマを起源・制度・制作の主要結節点として登録し、各地域の受容は今後分解する。

### ラテンアメリカへの伝播

`diffused_to` を `place/mexico-city` と `place/lima` に張った（いずれも `scholarly`）。英語版Wikipediaの『Baroque』は、
バロックがスペイン・ポルトガルの植民地アメリカへ移り、現存する主要な中心としてメキシコ、ペルー、ブラジルなどを
挙げ、メキシコ市のラ・プロフェサ教会の正面とリマのサン・フランシスコ聖堂・修道院を例に引く
（2026-11-28取得、二次情報）。ここで記録するのは建築・絵画が植民地都市に展開した事実で、現地の
様式がヨーロッパの規範の写しだったという主張ではない。同じ項は、クリオーリョと先住民の職人が独自の特徴を
与えたと書く。個々の建物の年代と、ローマで成立した造形との直接の系譜は未確認。

## 未着手

- カラヴァッジョ、ベルニーニ、ボッロミーニらの人物・作品ノード
- スペイン、フランドル、フランス、ラテンアメリカの地域別展開
