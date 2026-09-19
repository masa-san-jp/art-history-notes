---
id: movement/serbian-baroque-painting
uri: urn:ahn:movement/serbian-baroque-painting
type: movement
kind: period-style
label_ja: セルビア・バロック絵画
label_en: Serbian Baroque Painting
authority:
  wikidata: null
  aat: null
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidataの『Baroque painting』（Q808561）は様式全般を指す広すぎる項目であり、
    セルビア・バロック絵画という地域様式単位の項目ではないため採用しなかった。地域様式
    単位のWikidata項目は検索で特定できなかった"
time:
  start: "17XX"
  end: "1803"
  display: "18世紀末（1770年代〜1780年代）にディミトリエ・バチェヴィッチ、テオドル・
    クラチュン、ヤコヴ・オルフェリンらの世代でバロック様式が顕著となった。クラチュンの
    没年（1781年）とオルフェリンの没年（1803年）を範囲の目安とした"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: "Serbian Baroque painting"
  note: "『セルビア・バロック絵画』は後代の美術史記述による様式区分。当事者（画家たち）
    自身がこの名で自らの様式を運動として名乗った記録は無い"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun", certainty: scholarly}
  - {field: kind, source: "https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun", certainty: scholarly}
evidence: []
space:
  - {role: originated_in, target: place/sremski-karlovci}
relations:
  - {type: influenced_by, target: movement/rococo, certainty: scholarly, source: "https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun"}
sources:
  - url: "https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun"
    kind: reference
    note: "『Teodor Kračun』の項。1730年スレムスカ・カメニツァ生、1781年没。ディミトリエ・
      バチェヴィッチに師事した後、修道誓願を立て1769年にウィーン・アカデミーへ入学したと
      記す。1771〜1781年に制作したスレムスキ・カルロヴツィの聖ニコラ大聖堂のイコノスタシス
      2点が代表作とされ、『北セルビアにおけるバロック・ロココ様式の最も著名な画家』と
      記す。エル・グレコとの類似（明暗の効果、震えるような動き、衣文と背景の相互作用）が
      指摘され、ロカイユ的要素も見られると記す"
  - url: "https://en.wikipedia.org/wiki/Jakov_Orfelin"
    kind: reference
    note: "『Jakov Orfelin』の項。ヴコヴァルまたはスレムスキ・カルロヴツィ生（当時ハプスブルク
      帝国領）、1803年没。1766年にウィーン美術アカデミーへ留学し、ヤーコプ・マティアス・
      シュムッツァー主宰の版画アカデミーでも学んだと記す。1780〜1781年にはクラチュンと
      共同でスレムスキ・カルロヴツィの聖ニコラ大聖堂のイコノスタシス制作に携わったと記す"
  - url: "https://www.wikidata.org/wiki/Q808561"
    kind: reference
    note: "『Baroque painting』の項。バロック様式全般を指す項目であり、セルビア・バロック
      絵画という地域様式単位の項目ではないため、authority.wikidataには採用しなかった"
status: draft
updated: 2026-09-16
---

# セルビア・バロック絵画 / Serbian Baroque Painting

## 定義と範囲

英語版Wikipedia「[Teodor Kračun](https://en.wikipedia.org/wiki/Teodor_Kra%C4%8Dun)」
（参考資料）はこう記す（二次情報）。18世紀のハプスブルク帝国領ヴォイヴォディナ
（現セルビア北部）で、ディミトリエ・バチェヴィッチ、テオドル・クラチュン（1730-1781年）、
ヤコヴ・オルフェリン（18世紀半ば生-1803年）らの世代が、セルビア正教会のイコン・
イコノスタシス画にバロック・ロココ様式を取り入れた。中心地は[スレムスキ・カルロヴツィ](../places/sremski-karlovci.md)
——当時セルビア正教会総主教座が置かれた町——で、クラチュンとオルフェリンが1771〜1781年
にかけて手がけた聖ニコラ大聖堂のイコノスタシスは、セルビア科学芸術アカデミーにより
「ヴォイヴォディナにおけるバロック絵画の頂点」と評される。

## kind の判定

`period-style`とした。単一の血縁・工房ではなく、ウィーン・アカデミーで学んだ複数世代の
画家（バチェヴィッチ、クラチュン、オルフェリン）が、セルビア正教会の伝統的なイコン画に
バロック・ロココという西欧の様式語彙を取り入れ続けた点を、
[モスクワ派イコン画](moscow-school-icon-painting.md)と同型の構造と見た。

## ウィーン・アカデミーとの接続

クラチュンは1769年、オルフェリンは1766年にそれぞれウィーン・アカデミーへ入学し、
西欧の絵画様式を直接学んだ。クラチュンは「北セルビアにおけるバロック・ロココ様式の
最も著名な画家」と評される。これに基づき`relations`へ`influenced_by movement/rococo`
を張り、europe-east発生の様式がeurope-west（ロココの発生地パリ）からの影響を受けた
接続を記録した。

## 未着手

- ディミトリエ・バチェヴィッチ、ヤコヴ・オルフェリンを person エンティティとして
  立てるかどうか
- 聖ニコラ大聖堂のイコノスタシスを work エンティティとして立てるかどうか
- セルビア国立博物館・マティツァ・スルプスカ美術館所蔵作品の一次資料での確認
