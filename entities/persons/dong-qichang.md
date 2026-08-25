---
id: person/dong-qichang
uri: urn:ahn:person/dong-qichang
type: person
label_ja: 董其昌
label_en: Dong Qichang
authority:
  wikidata: Q537211
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1555"
  end: "1636"
  display: 1555年 – 1636年（明末の文人・書画家・理論家）
space: []
relations:
  - {type: member_of, target: movement/songjiang-school}
sources:
  - url: "https://www.wikidata.org/wiki/Q537211"
    kind: authority
  - url: "https://ja.wikipedia.org/wiki/%E6%B5%99%E6%B4%BE"
    kind: reference
status: draft
updated: 2026-08-11
---

# 董其昌

浙派そのものの担い手ではなく、**浙派という名称を作った側**の人物として扱う（movement/zhe-school
の `kind` 判定の根拠になるため作成——`docs/schema.md` の「person をいつ作るか」基準1）。

生没年は Wikidata [Q537211](https://www.wikidata.org/wiki/Q537211)（precision 9・年単位）。
明末の文人画家・書家・美術理論家。

日本語版 Wikipedia「浙派」の記述（二次情報）によれば、「浙派」という呼称は董其昌の著書
『画禅室随筆』に始まるとされる。浙派の画家たちが活動していた時代（15世紀〜16世紀中頃）には
この名称自体が存在しなかった。董其昌は1555年生まれで、浙派が「16世紀中葉にはほとんど消滅した」
とされる時期にはまだ活動を始めていない——**命名者は括られた対象の同時代人ではない**。

**未確認**: 『画禅室随筆』の成立年（`naming.named_when` を埋めるための一次資料に当たっていない）。
董其昌自身の画論（南北宗論）と浙派評価の関係も未読。

movement/zhe-school の `naming.named_by` からこの id を参照している。「命名者」という関係は
既存の関係語彙（`created_by` / `grouped_as` など）のどれにも当事者性の面で正確には合わないため
（董其昌は浙派の内部から生まれた括りを作ったのではなく、外部の批評家として後から名付けた）、
graph の `relations` エッジは張らず、`naming` ブロックのプレーンな参照に留めた。

### 松江派との関係

**彼は名づける側と名づけられる側の両方に立っている。** [浙派](../movements/zhe-school.md)という
呼称は彼の『画禅室随筆』が出どころだが、彼自身が属する松江派の名は、対抗地域である蘇州（呉）の
人々が「松江派耳（松江派にすぎない）」と値踏みして呼んだものであり、その場面に「元宰」（董其昌の字）が
名指しで登場する（中国語版Wikipedia「松江画派」経由・二次情報）。
