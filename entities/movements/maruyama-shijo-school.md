---
id: movement/maruyama-shijo-school
uri: urn:ahn:movement/maruyama-shijo-school
type: movement
kind: retrospective
label_ja: 円山四条派
label_en: Maruyama-Shijō School
authority:
  wikidata: Q11394761
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "17XX"
  end: null
  display: "日本語版ウィキペディアは「江戸中期から京都で有名になった」とする。英語版ウィキペディアは四条派の成立を「late 18th century」とする。開祖の生没年は円山応挙 1733–1795、松村呉春 1752–1811。正確な成立年・終期は一次資料で確認していない"
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: 円山四条派
  note: "円山派（祖: 円山応挙）と四条派（祖: 松村呉春）という別々に成立した2つの画派を、後代がまとめて呼ぶようになった名称。Wikidata Q11394761 の説明文（ja）は『円山派と四条派の総称』と明記し、has part（P527）で円山派（Q11394770）・四条派（Q3577704）を別項目として保持する。日本語版ウィキペディアも『後世になってまとめて「円山・四条派」と呼ばれるようになった』と記す（いずれも二次情報）。命名者・命名年は未確認"
claims:
  - {field: kind, source: "https://www.wikidata.org/wiki/Q11394761", certainty: scholarly}
space:
  - {role: originated_in, target: place/kyoto}
relations:
  - {type: influenced_by, target: movement/nanga, certainty: scholarly, source: "https://kyoto-museums.city.kyoto.lg.jp/en/feature-column/painting/"}
  - {type: diffused_to, target: place/chicago, certainty: scholarly, source: "https://api.artic.edu/api/v1/artworks/196928"}
  - {type: diffused_to, target: place/chicago, certainty: scholarly, source: "https://api.artic.edu/api/v1/artworks/50560"}
sources:
  - url: "https://www.wikidata.org/wiki/Q11394761"
    kind: authority
  - url: "https://www.wikidata.org/wiki/Q11394770"
    kind: authority
  - url: "https://www.wikidata.org/wiki/Q3577704"
    kind: authority
  - url: "https://ja.wikipedia.org/wiki/円山・四条派"
    kind: reference
  - url: "https://en.wikipedia.org/wiki/Shij%C5%8D_school"
    kind: reference
  - url: "https://kyoto-museums.city.kyoto.lg.jp/en/feature-column/painting/"
    kind: institutional
  - url: "https://www.fujibi.or.jp/collection/artwork/09092/"
    kind: institutional
  - url: "https://api.artic.edu/api/v1/artworks/196928"
    kind: institutional
  - url: "https://api.artic.edu/api/v1/artworks/50560"
    kind: institutional
images:
  - url: https://www.artic.edu/iiif/2/19669877-89b4-a950-a918-3c3c4af312fa/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/196928
    license: public-domain
    note: "円山応挙《応挙習画帖（Okyo Shubi Gafu）》11ページ、1892年（応挙没後の木版複製画帖）。シカゴ美術館蔵（is_public_domain: true）"
  - url: https://www.artic.edu/iiif/2/0022f3ce-cc71-83c2-542e-30d57d74d9ec/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/50560
    license: public-domain
    note: "松村呉春《鍾馗図（Shoki the Demon Queller）》17〜19世紀、シカゴ美術館蔵（is_public_domain: true）"
status: draft
updated: 2026-08-13
---

# 円山四条派 / Maruyama-Shijō School

## 定義と範囲

円山四条派は、円山応挙（1733–1795）を祖とする円山派と、応挙の門人であった松村呉春（1752–1811）が
興した四条派という、別々に成立した2つの京都の画派をまとめて指す名称である。

日本語版ウィキペディアはこう定義する——「円山・四条派（まるやま・しじょうは）は、江戸中期から
京都で有名になった円山応挙を祖とする円山派と、呉春を祖とする四条派を合わせた呼び名である。
四条・円山派ともいう」（[ja.wikipedia.org/wiki/円山・四条派](https://ja.wikipedia.org/wiki/円山・四条派)、
二次情報）。

四条派の名は、松村呉春が拠点を置いた京都・四条通に由来する。英語版ウィキペディアは
「named after the Shijō Street ('Fourth Avenue') in Kyoto where many major artists were based」と記す
（[Shijō school](https://en.wikipedia.org/wiki/Shij%C5%8D_school)、二次情報）。呉春は元々、
与謝蕪村門下の文人画（南画）を出発点としており、その後、応挙の写生的画風の影響を受けて独自の画風を
確立したとされる（同）。

典拠: Wikidata [Q11394761](https://www.wikidata.org/wiki/Q11394761)（円山四条派）／
[Q11394770](https://www.wikidata.org/wiki/Q11394770)（円山派）／
[Q3577704](https://www.wikidata.org/wiki/Q3577704)（四条派）。**未確認**: Getty AAT には
「Maruyama School」単体の項目（`300018658`、SPARQLで確認）はあるが、円山四条派という結合した
括りに対応する AAT 項目は見つかっていない。円山派単体の ID を円山四条派に転用すると対象がずれるため、
本項の `authority.aat` は空欄のままにした。

## 南画との関係

京都市の博物館協会は、呉春・松村景文らの四条派が円山派の画風に南画（中国の南宗画）を加えたと説明
している。また東京富士美術館は、呉春が与謝蕪村に師事して画を学んだ後、円山応挙にも学び、蕪村の
詩情性と応挙の写実性を折衷して四条派の祖となったと記載する。

このエッジが表すのは、円山四条派という総称全体が一様に南画から影響を受けたという主張ではない。
現在のエンティティが円山派と四条派をまとめているため、**関係の実体はそのうち四条派側にある**。
将来、両派を別エンティティに分ける場合は、この `influenced_by` を四条派へ移すべきである。
現段階では、呉春が蕪村から学んだ南画を四条派の形成へ持ち込んだ経路を、総称側に注記付きで記録する。

## kind の判定 — なぜ `retrospective` か

日本語版ウィキペディアはこう記す——「円山派の祖である円山応挙の写生的画風に、四条派の祖である
呉春が影響を受けているため、後世になってまとめて『円山・四条派』と呼ばれるようになった」
（[同](https://ja.wikipedia.org/wiki/円山・四条派)、二次情報）。円山派（祖: 円山応挙）と
四条派（祖: 松村呉春）は別の人物がそれぞれ別に興した画派であり、当事者がこの2つを1つの名で
名乗った記録は見つかっていない。

Wikidata の構造もこれを裏づける。円山四条派 [Q11394761](https://www.wikidata.org/wiki/Q11394761)
の説明文（ja）は「円山派と四条派の総称」であり、has part（P527）で円山派
[Q11394770](https://www.wikidata.org/wiki/Q11394770)・四条派
[Q3577704](https://www.wikidata.org/wiki/Q3577704)をそれぞれ別項目として保持する。
Wikidata 自身のモデルにおいても、円山四条派は2つの別項目を束ねる上位の括りとして扱われている。

だから `self-declared`（当事者の宣言による運動）ではない。

`lineage-school`（血縁・工房の単一の継承体）でもない。円山派・四条派それぞれの内部には師弟関係に
よる継承の系図が伝わる（円山派: 応挙門下に円山応瑞・木下応受・島田元直ら／四条派: 呉春門下に
長沢芦雪・岸駒ら、[同](https://ja.wikipedia.org/wiki/円山・四条派)、二次情報）。だが円山四条派
という括り自体は、狩野派・土佐派のような単一の世襲の職・単一の家系ではなく、開祖も継承の線も
異なる2つの画派を後から1つの名でまとめたものである。

まとめる根拠になっているのは、呉春が応挙の写生的画風から影響を受けたという様式の近さである。
ただし同じ記事は続けて「実態としては、呉春は与謝蕪村の文人画（南画）を基礎としているため、
円山派と四条派は別の流派であるともされる」とも記しており（同、二次情報）、様式的な同一性
そのものにも異説がある。

**未確認**: 「円山・四条派」という呼称をいつ・誰が最初に使い始めたかは、日本語版・英語版
いずれのウィキペディアにも明記がなく、一次資料に当たっていない。

## 時間

日本語版ウィキペディアは「江戸中期から京都で有名になった」と記す（[同](https://ja.wikipedia.org/wiki/円山・四条派)、
二次情報）。英語版ウィキペディアは四条派の成立を「late 18th century」とする
（[Shijō school](https://en.wikipedia.org/wiki/Shij%C5%8D_school)、二次情報）。両者とも世紀単位の
記述にとどまり、年単位の精度は無い。開祖の生没年（円山応挙 1733–1795、松村呉春 1752–1811）は
確認できるが、これは開祖個人の生涯であって画派としての活動期間そのものではない。

Wikidata の3項目（円山四条派・円山派・四条派いずれも）に `P571`（inception）・`P576`（dissolved）の
値は無い——**未確認**。EDTF は世紀精度 `17XX`（18世紀）とした。

- `start`: `17XX`。応挙・呉春がともに活動した18世紀という点で日英2つの二次情報が一致する。
  **未確認**: 画派として何をもって「成立」とするか（応挙の写生様式確立／呉春の四条通進出／
  応挙没後の呉春の独立）は一次資料で切り分けていない
- `end`: 空欄（`null`）。**未確認**: この括りがいつ終わったと見なせるかの記述は見つかっていない。
  竹内栖鳳ら明治以降の京都画壇にこの系譜が続いたという言及が別項目（[日本画](nihonga.md)）にあるが、
  一次資料での裏は取れていない

## 空間

`originated_in` は京都（[place/kyoto](../places/kyoto.md)）とした。円山派・四条派とも京都で
成立し、四条派の名自体が京都・四条通という地名に由来する（[Shijō school](https://en.wikipedia.org/wiki/Shij%C5%8D_school)、
二次情報）。Wikidata は円山派の location of formation（P740）を京都
[Q740246](https://www.wikidata.org/wiki/Q740246)、四条派のそれを四条通
[Q7496525](https://www.wikidata.org/wiki/Q7496525)（京都市内の通り）としており、いずれも京都市内に
収まる。都市より細かい「四条通」単位の座標は本 KB の `place` エンティティとして持っていない。

### シカゴ美術館での作例

円山派・四条派の国外受容を示す作例として、シカゴ美術館は円山応挙の木版複製画帖と、
松村呉春の《鍾馗図》を収蔵している。前者は同館の記録で作者を「Maruyama Okyo」とし、
後者は「Matsumura Goshun」としている（[Art Institute of Chicago「Page 11 from the book Okyo Shubi Gafu」](https://api.artic.edu/api/v1/artworks/196928)、
[同「Shoki the Demon Queller」](https://api.artic.edu/api/v1/artworks/50560)）。これは、
**円山・四条派を構成する両系統の作例がシカゴの美術館コレクションに入っていること**を示すが、
シカゴの別の美術運動への影響を意味しない。そのため `diffused_to place/chicago` は収蔵地点を記録する。

## 未着手

- 円山派・四条派それぞれを独立した `movement` エンティティとして立てるかどうか。円山四条派という
  名前の単位と、円山派・四条派という担い手の系譜の単位はずれている（`docs/schema.md` の
  「名前の単位と担い手の単位がずれるとき」に当たる可能性がある）。本タスクでは円山四条派1件のみを
  対象とし、円山派・四条派の分割は行っていない
- 円山応挙・松村呉春の `person` エンティティ化。開祖として `kind` の根拠になっており、作成基準
  1（`kind`/`time`/`originated_in` の根拠）に当たる可能性があるが、本タスクでは見送った
- 「円山・四条派」という呼称の初出（誰が・いつ使い始めたか）の一次資料調査
- Getty AAT `300018658`（Maruyama School 単体）と本項の関係の整理。円山四条派全体を覆う AAT 項目が
  別に存在するかどうかの確認
- [日本画（nihonga.md）](nihonga.md)の「未着手」に記されている、竹内栖鳳ら京都画壇への系譜の接続。
  一次資料での裏が取れていないため、本項からも `relations` は張っていない
- Japan Search・Web NDL Authorities の典拠ID（2026-08-10 時点で本KBは両者の正しい呼び方を
  確認できていない）
