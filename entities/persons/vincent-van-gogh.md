---
id: person/vincent-van-gogh
uri: urn:ahn:person/vincent-van-gogh
type: person
label_ja: フィンセント・ファン・ゴッホ
label_en: Vincent van Gogh
authority:
  wikidata: Q5582
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1853-03-30"
  end: "1890-07-29"
  display: "1853年3月30日 オランダ・ズンデルト生まれ – 1890年7月29日 オーヴェル＝シュル＝オワーズ没（Wikidata Q5582・いずれも precision 11＝日単位）"
space: []
relations:
  - {type: grouped_as, target: movement/post-impressionism, certainty: scholarly, source: "https://www.tate.org.uk/art/art-terms/p/post-impressionism"}
sources:
  - url: "https://www.wikidata.org/wiki/Q5582"
    kind: authority
  - url: "https://www.tate.org.uk/art/art-terms/p/post-impressionism"
    kind: institutional
  - url: "https://www.vangoghmuseum.nl/en/collection/s0114V1962"
    kind: institutional
  - url: "https://www.vangoghmuseum.nl/en/collection/s0115v1962"
    kind: institutional
  - url: "https://collectionapi.metmuseum.org/public/collection/v1/objects/55433"
    kind: institutional
status: draft
updated: 2026-08-09
---

# フィンセント・ファン・ゴッホ / Vincent van Gogh

オランダの画家（1853年3月30日 ズンデルト生まれ – 1890年7月29日 オーヴェル＝シュル＝オワーズ没）。
[ポスト印象派](../movements/post-impressionism.md)として後年ロジャー・フライに括られた4人の一人。

**このKBに置いたのは、日本の版画と西欧の絵画という2つの括りの間で、物が実際に動いた経路を
この人物が持っているからである**（`docs/schema.md` の person 作成基準2）。

1886年から1887年にかけてのパリ滞在中、画商ジークフリート・ビングの店で日本の木版画を大量に
購入した（点数は資料により約660点とされる。ビングは当時パリで日本美術を扱った中心的な画商）。
1887年2月から3月にかけて、その一部をパリのカフェ「ル・タンブラン」で展示したが、売れ残った
（**未確認**: 購入点数の正確な値、購入時期、展示の正確な会期。いずれも二次情報からの記述で、
一次資料に当たれていない）。

売れ残った版画は手元に残り、1887年10月から11月にかけて、ファン・ゴッホはそのうち2点を油彩で
模写した。

| 模写 | 原作 |
|---|---|
| 《雨の橋（広重による）》1887年、アムステルダム・ファン・ゴッホ美術館 [s0114V1962](https://www.vangoghmuseum.nl/en/collection/s0114V1962) | 歌川広重《大はしあたけの夕立》1857年、『名所江戸百景』第58図 |
| 《花咲く梅の木（広重による）》1887年、同美術館 [s0115v1962](https://www.vangoghmuseum.nl/en/collection/s0115v1962) | 歌川広重《亀戸梅屋舗》『名所江戸百景』 |

広重は[歌川派](../movements/utagawa-school.md)の絵師である（歌川豊春門下の豊広の弟子）。
原作の版画はメトロポリタン美術館にも所蔵があり、同館の公開APIは作者を "Utagawa Hiroshige"、
制作年を1857年、受入番号を JP2522、`isPublicDomain` を `true` と返す
（[collectionapi.metmuseum.org/.../55433](https://collectionapi.metmuseum.org/public/collection/v1/objects/55433)）。

**未確認**: ファン・ゴッホ美術館の作品ページは JavaScript で描画されるため、本KBは同館の
解説文そのものを機械で読めていない（URLの生存とオブジェクト番号のみ確認）。模写の制作月
（1887年10〜11月）は二次情報による。彼が所有した版画のうち歌川派の絵師の作が何点あったかも
確認できていない。
