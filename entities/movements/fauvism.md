---
id: movement/fauvism
uri: urn:ahn:movement/fauvism
type: movement
kind: retrospective
label_ja: フォーヴィスム
label_en: Fauvism
authority:
  wikidata: Q166593
  aat: "300021300"
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1904"
  end: "1908"
  display: "1904年頃〜1908年頃。1905年のサロン・ドートンヌで名称が定着し、数年で個別の進路へ分岐"
naming:
  self_identified: false
  named_by: null
  named_when: "1905"
  original_label: "Fauvism"
  note: "1905年のサロン・ドートンヌをめぐる批評家ルイ・ヴォークセルの『野獣（les fauves）』という呼称から定着した、短期間のフランス絵画運動。参加者全員が自らを同じ組織名で呼んだわけではないため後世的な分類とする"
claims:
  - {field: time, source: "https://www.wikidata.org/wiki/Q166593", certainty: scholarly}
  - {field: originated_in, source: "https://shop.tate.org.uk/derain-the-pool-of-london/andder1703.html", certainty: scholarly}
  - {field: kind, source: "https://www.wikidata.org/wiki/Q166593", certainty: scholarly}
space:
  - {role: originated_in, target: place/paris}
relations:
  - {type: influenced_by, target: movement/post-impressionism, certainty: scholarly, source: "https://www.metmuseum.org/ja/essays/fauvism"}
  - {type: diffused_to, target: place/tokyo, certainty: scholarly, source: "https://www.momak.go.jp/English/collectionGalleryArchive/2017/collectionGallery2017No05.html"}
sources:
  - https://www.wikidata.org/wiki/Q166593
  - https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300021300
  - https://shop.tate.org.uk/derain-the-pool-of-london/andder1703.html
  - https://www.metmuseum.org/ja/essays/fauvism
  - https://www.momak.go.jp/English/collectionGalleryArchive/2017/collectionGallery2017No05.html
status: draft
updated: 2026-08-12
---

# フォーヴィスム / Fauvism

1904年頃から1908年頃まで、マティス、ドランらを中心にフランスで展開した短期間の絵画運動。自然の
色彩を写すよりも、強い純色、平面的な構成、荒々しい筆触によって画面の自律性と感情的な効果を押し出した。
1905年のサロン・ドートンヌで批評家ルイ・ヴォークセルが用いた「野獣」という呼称が運動名として定着した。

## kind の判定

`retrospective` とした。参加者には共有された展示機会と造形上の近接性があったが、単一の宣言や恒常的な
組織があったわけではなく、数年のうちにそれぞれの制作へ分岐したためである。

## 空間と時間

パリのサロンと画家ネットワークを起点ノードとして置く。マティスとドランが南仏コリウールで制作した経路や、
セザンヌ・ゴッホ・ゴーギャンからの受容は、人物・作品を追加した段階で別関係にする。

## ポスト印象派からの形成経路

メトロポリタン美術館は、マティスがフォーヴ様式へ到達する前に、ゴッホ、ゴーギャン、セザンヌらの
ポスト印象派の様式を試みていたと説明する。また、ヴラマンクが1905年にゴッホの回顧展を見たことも
フォーヴ様式への転換の契機として記録されている（[同館の解説](https://www.metmuseum.org/ja/essays/fauvism)）。
このため本項では、フォーヴィスム全体がポスト印象派の単一の様式を継承したと一般化せず、中心人物の
形成経路に限定して `influenced_by movement/post-impressionism` を記録する。

## 日本への波及

京都国立近代美術館は、フォーヴィスムが若い画家たちに大きな影響を与え、日本からの留学生もその例外では
なかったと説明する。同館は、中川紀元が1919年にマティスに、里見勝蔵が1921年にヴラマンクに師事し、帰国後に
日本の洋画界で新しい様式を広めた経路を挙げている。したがって、ここで記録するのは日本画（nihonga）への
影響ではなく、フォーヴィスムが日本の画家・洋画団体へ受容された**場所への波及**である。受け手側の
movementはまだ本KBに分離していないため、`diffused_to place/tokyo` として記録する。

## 未着手

- マティス、ドラン、ヴラマンク、デュフィの人物・作品
- サロン・ドートンヌ1905年とコリウール制作地のイベント・place分解
