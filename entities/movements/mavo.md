---
id: movement/mavo
uri: urn:ahn:movement/mavo
type: movement
kind: self-declared
label_ja: マヴォ
label_en: Mavo
authority:
  wikidata: Q11231120
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1923-06"
  end: "1925"
  display: "1923年6月（東京で結成）〜1925年"
naming:
  self_identified: true
  named_by: null
  named_when: "1923-06"
  original_label: "マヴォ / MAVO"
  note: "村山知義を中心とするグループがこの名を掲げ、同名の機関誌を刊行した。語の最初の選択者・命名行為の詳細は未確認"
claims:
  - {field: time, source: "https://artplatform.go.jp/ja/artists/A5349", certainty: scholarly}
  - {field: originated_in, source: "https://artplatform.go.jp/ja/artists/A5349", certainty: scholarly}
  - {field: kind, source: "https://artplatform.go.jp/ja/artists/A5349", certainty: scholarly}
space:
  - {role: originated_in, target: place/tokyo}
relations:
  - {type: influenced_by, target: movement/dada, certainty: scholarly, source: "https://museum.geidai.ac.jp/exhibit/2005/06/dada.html"}
  - {type: influenced_by, target: movement/constructivism, certainty: scholarly, source: "https://museum.geidai.ac.jp/exhibit/2005/06/dada.html"}
sources:
  - url: "https://www.wikidata.org/wiki/Q11231120"
    kind: authority
  - url: "https://artplatform.go.jp/ja/artists/A5349"
    kind: institutional
  - url: "https://museum.geidai.ac.jp/exhibit/2005/06/dada.html"
    kind: institutional
  - url: "https://artplatform.go.jp/ja/artists/A1970"
    kind: institutional
  - url: "https://artscape.jp/dictionary/modern/1198381_1637.html"
    kind: reference
status: verified
updated: 2026-08-25
---

# マヴォ / Mavo

## 定義と範囲

マヴォ（MAVO）は、村山知義を中心に1923年6月、東京で結成された日本の前衛芸術グループと、
その名を冠した機関誌である。Art Platform Japanの『日本アーティスト事典』は、結成年を1923年6月、
結成地を東京府、活動の終わりを1925年として、絵画・版画・デザイン・舞台芸術・詩・パフォーマンスを
活動領域に挙げている（[マヴォ](https://artplatform.go.jp/ja/artists/A5349)）。

東京藝術大学大学美術館は、ベルリン滞在を終えて帰国した村山が1923年に東京でマヴォを創設したと説明し、
絵画・活版印刷物・構成物・装飾を組み合わせたハプニングやパフォーマンスを生み出したグループとして
位置づけている（[「日本におけるダダ：マヴォ／メルツ」](https://museum.geidai.ac.jp/exhibit/2005/06/dada.html)）。
1924年には機関誌『マヴォ』の刊行、展覧会、復興期の東京を舞台にした制作が活動の頂点となり、
1925年には新興美術運動の再編と内部対立の中で活動の重心が移った
（[村山知義](https://artplatform.go.jp/ja/artists/A1970)、Art Platform Japan）。

## kind の判定

`self-declared` とした。これは後世の批評家が作品の共通性だけをまとめた名称ではなく、当時のグループが
「マヴォ」という名を掲げ、同じ名の機関誌を発行し、展覧会や複数媒体の共同活動を行ったためである。
Art Platform Japanはマヴォを「日本のダダ運動の先駆をなすグループ」として収録し、東京藝術大学大学美術館も
「グループおよび機関誌」と明記している。語を最初に選んだ個人や命名の手続きについては、確認できる資料が
不足しているため特定しない。

## ダダとの接続

東京藝術大学大学美術館の展覧会資料は、マヴォについて、村山が生み出した「構成派 constructionnisme」が
ダダイスムと構成主義を取り入れた独自のヴィジョンであると説明する。また同資料は、村山をダダイスムの
「日本における継承者」と明記している。したがって、ここでの `influenced_by movement/dada` は、
マヴォの全参加者が欧州ダダを同じ経路で受け取ったという意味ではなく、村山を中心に再編されたグループの
造形・印刷・パフォーマンス実践にダダの方法と問題意識が取り込まれたことを指す。

## 構成主義との接続

村山知義は1922年のベルリン滞在を経て帰国し、1923年に「意識的構成主義」を掲げた小品展を東京で開催した。
Art Platform Japanは、ベルリンで村山がエル・リシツキーの構成主義的作品に触れ、その後マヴォを結成した経緯を
記録している。東京藝術大学大学美術館も、マヴォに先行する村山の「構成派」が構成主義を取り入れたと説明する。
このため、`influenced_by movement/constructivism` は村山を媒介に形成されたマヴォの構成物・タイポグラフィ・
舞台・建築的実践に限定して記録する。

## 時間

`time.start` は、Art Platform Japanが結成年月として示す1923年6月を採った。村山の帰国直後には、同年5月の
「意識的構成主義的小品展覧会」という前史があるが、マヴォというグループの成立とは区別した。
`time.end` は、同事典が活動の終わりとして示す1925年を採った。村山個人の制作や、その後の三科など別の
前衛活動まで含めるものではない。

## 空間

発生地は東京（[place/tokyo](../places/tokyo.md)）。Art Platform Japanは結成地を東京府とし、
東京藝術大学大学美術館も1923年に東京で創設されたグループとして記述している。

## 未着手

**未確認**: マヴォという名称を最初に選んだ人物、1923年の結成会合の正確な日付、および1925年の活動終止を
確定させる単一の出来事。
