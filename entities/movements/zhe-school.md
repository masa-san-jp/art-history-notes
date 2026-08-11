---
id: movement/zhe-school
uri: urn:ahn:movement/zhe-school
type: movement
kind: retrospective
label_ja: 浙派
label_en: Zhe school
authority:
  wikidata: Q1150941
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "14XX"
  end: "1550~"
  display: "15世紀（戴進の活動期）〜16世紀中頃（後世に「ほとんど消滅した」とされる）。Wikidata の movement 項目 (Q1150941) には開始・終了年の claim が P571/P576 とも1つも無く、時間軸は二次情報（日本語版Wikipedia）と開祖・戴進の生没年（Wikidata Q741512、1388年〜1462年、precision 9）から組んだ"
naming:
  self_identified: false
  named_by: person/dong-qichang
  named_when: null
  original_label: 浙派
  note: "董其昌『画禅室随筆』に由来するとされる（二次情報、日本語版Wikipedia）。浙派の画家が活動していた時代（15〜16世紀）には「浙派」という名称自体が存在しなかった。命名者・董其昌（1555-1636）は浙派が「16世紀中葉にはほとんど消滅した」とされる時期にまだ生まれてすらいない。『画禅室随筆』の成立年は未確認"
claims:
  - {field: kind, source: "https://ja.wikipedia.org/wiki/%E6%B5%99%E6%B4%BE", certainty: scholarly}
  - {field: originated_in, source: "https://www.wikidata.org/wiki/Q741512", certainty: scholarly}
space:
  - {role: originated_in, target: place/hangzhou}
relations:
  - {type: influenced_by, target: movement/song-academy-painting, certainty: scholarly, source: "https://www.hkpm.org.hk/en/visit/audio-guide/g4-stories-untold"}
sources:
  - https://www.wikidata.org/wiki/Q1150941
  - https://ja.wikipedia.org/wiki/%E6%B5%99%E6%B4%BE
  - https://en.wikipedia.org/wiki/Zhe_school_(painting)
  - https://www.wikidata.org/wiki/Q741512
  - https://www.wikidata.org/wiki/Q537211
  - https://www.hkpm.org.hk/en/visit/audio-guide/g4-stories-untold
images:
  - url: https://www.artic.edu/iiif/2/7739a403-99b6-d151-c892-e93a0b17e4ef/full/843,/0/default.jpg
    source_page: https://www.artic.edu/artworks/150406
    license: cc0
    note: "戴進《道士対局図》（Landscape with Daoist Immortals Playing Weiqi）、明代15-16世紀。シカゴ美術館蔵（is_public_domain: true）"
  - url: https://images.metmuseum.org/CRDImages/as/original/DP204373_CRD.jpg
    source_page: https://www.metmuseum.org/art/collection/search/45680
    license: cc0
    note: "蒋嵩《冬景山水図》（Winter landscape）、16世紀前半。メトロポリタン美術館蔵（isPublicDomain: true）"
status: draft
updated: 2026-08-09
---

# 浙派 / Zhe school

**`overviews/japan-school-types.md` が反証候補として名指しした1件。** 「派」の kind を分けるのは
名乗ったかどうかではなく制度的な継承が続いたかどうか、という仮説（狩野派・土佐派・琳派の3件から
一般化）に対して、中国圏・地縁で括られた画派がどう振る舞うかを見る。

## 定義と範囲

中国・明代の画派。戴進（1388-1462、Wikidata [Q741512](https://www.wikidata.org/wiki/Q741512)）を
祖とする職業画家の集団とされる（日本語版Wikipedia「浙派」、二次情報）。戴進が浙江省杭州の出身
だったため「浙派」と呼ばれた——**呼称の由来は地名（地縁）**。後には南京・開封・福建省・広東省
出身の画家も加わっており、**担い手の出身地は浙江に限定されていない**。

Wikidata [Q1150941](https://www.wikidata.org/wiki/Q1150941) の `P31`（instance of）は
`art movement`（Q968159）と `artistic school`（Q2736610）。`founded by`（P112）に戴進
（Q741512）を挙げているが、`P571`（inception）・`P576`（dissolved）はどちらも値が無い——
狩野派・土佐派・琳派の3件がいずれも持っていた「世紀精度の時間 claim」がこの対象には無い。

画法上の特色は、筆墨の粗放さ、点景のフォルム、墨面と余白の対比、律動感の強調とされ、南宋画院
（馬遠・夏珪の様式）の系譜を引く。**独自の新様式を立ち上げたのではなく、南宋の院体様式を継承・
発展させた**（英語版Wikipedia「Zhe school (painting)」も同旨: "painters did not formulate a new
distinctive style, preferring instead to further the style of the Southern Song"）。

主要な担い手（日本語版Wikipedia、二次情報）: 前期は戴進（宣徳画院に招かれ後に失脚）、呉偉
(1459-1508、南京で活躍)、王諤、倪端、夏芷（戴進の弟子）。後期は張路(1490-1563?)、鍾礼、
蒋嵩(1475-1565?)、鄭文林、汪肇、張復陽など。16世紀後期以降の文人批評家からは「狂態邪学」と
貶められ評価が低かったが、近年再評価されているという（二次情報）。

## 南宋院体画との関係

香港故宮文化博物館は、宮廷で活動した院体画と民間で活動した浙派を別々の担い手として説明しつつ、
両者の伝統がともに南宋の宮廷絵画にさかのぼるとしている
（[香港故宮文化博物館](https://www.hkpm.org.hk/en/visit/audio-guide/g4-stories-untold)）。
同館の整理は、浙派を南宋院体画の単なる同義語とするものではなく、明代の職業画家がその構図・技法の
伝統を受け継いだという歴史的な系譜を示す。そのため、浙派から宋代の[院体画](song-academy-painting.md)
へ `influenced_by` を張る。対象となるのは南宋の宮廷画院そのものではなく、そこから継承された画風で
あり、浙派を宋代の制度の一部とする意味ではない。

**未確認**: これらの担い手個々の一次資料（伝・年譜）には当たっていない。`docs/schema.md` の
person 作成基準（movement の kind/time/originated_in の根拠になる／2movement を繋ぐ／作品を分解して
読んだ）のどれにも単独では当たらないため、本文に名前を書くだけに留め、person エンティティ化はしない。

## kind の判定 — なぜ `retrospective` か

### 1. 継承の形は何か

複数の軸で見て、狩野派・土佐派とは異質。

| 軸 | 浙派 | 出典 |
|---|---|---|
| 血縁 | **無い**。戴進から呉偉・張路らへ家系としての継承は記述されていない | 日本語版Wikipedia「浙派」 |
| 工房・師弟 | **希薄**。「画派としては、師承関係が希薄で」と明記される | 同上（原文まま） |
| 官職 | 部分的にある。戴進は宣徳画院（明の宮廷画院）に招かれたが後に失脚。他の担い手にも画院画家がいる。ただし**この官職は世襲ではない**——各世代の画家が個別に宮廷へ出入りしただけで、狩野派の奥絵師・土佐派の絵所預のように「一つの家・地位が代々継承された」わけではない | 同上 |
| 地縁 | **名称の由来としては強い**（戴進の出身地・浙江省杭州から「浙派」）。ただし後代の担い手は南京・開封・福建・広東の出身も含み、**集団としての居住地の連続ではない** | 同上 |
| 様式 | **これが実質的な括りの軸**。馬遠・夏珪ら南宋院体様式の継承という一点で括られている | 日本語版・英語版Wikipedia双方 |

### 2. kind の判定

上記から、浙派は「家・工房・官職が世代を超えて継承された制度体」ではない。官職（画院）という
制度自体は存在したが、**それは世襲されておらず、狩野派・土佐派の「制度としての実体」とは性質が
違う**——個々の画家が個別に出入りする開かれた官職であり、家系や工房が代々占有した地位ではない。

括りの実質は「戴進という個人に由来し、南宋院体様式を継いだ」という**様式的な同質性**であり、
これは後世の美術史記述（董其昌『画禅室随筆』）が付けた括りである。日本語版Wikipediaは
「後世に美術史的観点からグループ分けされた集団である」と明言し、「浙派の画家が活動していた
時代には、『浙派』という名称はない」とも書く。命名者・董其昌（1555-1636）は、浙派が
「16世紀中葉にはほとんど消滅してしまった」とされる時期にはまだ生まれていない——**当事者の
時代に括りは存在せず、括った側は当事者と同時代人ですらない**。

以上から `self-declared`（当事者の宣言）でも `lineage-school`（血縁・工房の継承体）でもなく、
`retrospective`（後代に外部が付けた括り）と判定した。

### 3. 仮説への適合性 — **当てはまる。ただし呼称の由来には第3の軸が要る**

`overviews/japan-school-types.md` の仮説は「制度的な継承がある→当事者由来の呼称→
`lineage-school`／制度的な継承がない→後代由来の呼称→`retrospective`」というものだった。
浙派はこの2値のどちらに落ちるかで見れば、**仮説を崩さない**。制度的な継承（家・工房の
世襲）は無く、呼称は後代（董其昌）による——きれいに `retrospective` 側に落ちる。**中国圏の
地縁で括られた画派が仮説を崩す**という当初の想定は、この1件については外れた。

ただし、それとは別の軸で興味深い違いが出た。**「後代由来の呼称」の中身が、琳派と浙派で異なる。**
琳派は人名の一字（尾形光琳）に由来する。浙派は地名（浙江）に由来する。どちらも `retrospective`
だが、名付けの材料が「誰か」（人）と「どこか」（地）で分かれている。これは `kind` を動かす軸
ではなく、`retrospective` 内部の**呼称の由来の下位区分**として見える——制度が無いとき、
括りの名前は「慕われた個人の名」か「発生地の地名」のどちらかに落ちる、という仮説がここから
新たに立てられる（**これは琳派・浙派の2件だけから作った新しい仮説であり、まだ検証されていない**）。

もう1点、当初の想定（「制度が無いので kind では説明できない第3の原理＝地縁が要るはず」）を
裏切ったのは、**地縁が「呼称の由来」であって「集団を成立させた原理」ではなかった**点。
後期の担い手が浙江省出身に限られない以上、浙派を実際に束ねているのは地縁ではなく様式
（南宋院体様式の継承）だった。地縁は名前だけに残り、集団の実体を規定してはいない。

## 時間

Wikidata の movement 項目 (Q1150941) には `P571`（inception）・`P576`（dissolved）のどちらも
claim が無い。狩野派・土佐派・琳派はいずれも `P571` に世紀精度の値を持っていたので、**これは
このKBで初めて時間の典拠がゼロの movement**。

代わりに次の2つから時間軸を組んだ:

- 開祖とされる戴進の生没年（Wikidata Q741512: 1388–1462, precision 9・年単位）。戴進が宣徳画院
  に招かれたのは宣徳年間（1426–1435）とされ、浙派の活動が本格化するのはこの頃からと見て、
  `start` を戴進の活動期を含む世紀精度 `14XX`（15世紀）とした
- 日本語版Wikipediaの「浙派は16世紀中葉にはほとんど消滅してしまった」という記述。後期の担い手
  張路(1490-1563?)・蒋嵩(1475-1565?)の活動年代とも整合するため、`end` を近似の `1550~` とした

**未確認**: 戴進の活動開始年そのもの（生年1388年と宣徳画院への出仕年の間に一次資料の裏が無い）。
「16世紀中葉」がいつを指すかも二次情報止まりで、具体的な年（例: 1550年）への根拠は無い。
藍瑛（17世紀、浙江省銭塘出身）が「浙派の殿将」とされることがあるが、日本語版Wikipediaは
「画風的には、ほとんど関係がない」と明記しており、`end` の延長根拠には使わなかった。

## 空間

発生地を杭州（[place/hangzhou](../places/hangzhou.md)）とした。根拠は戴進の出身地
（Wikidata Q741512 の `P19` born in = Q4970 Hangzhou）。ただし、これは**開祖1人の出身地**であって、
浙派という集団全体の活動拠点ではない。実際の活動場所は日本語版Wikipediaによれば「北京と浙江省、
南京、開封など幅広い」——集団としての空間的な中心は、戴進の出身地という象徴的な地縁より広い。

**未確認**: 浙派の活動が最も集中した都市（北京か南京か）を特定する一次資料には当たっていない。
`space.role: active_in` を追加で張るかは、その特定ができてから判断する。

## 未着手

- 董其昌『画禅室随筆』の成立年（`naming.named_when` を埋める一次資料）
- 主要な担い手（呉偉・張路・蒋嵩ら）の person エンティティ化。現状は
  `docs/schema.md` の作成基準（kind/time/originated_in の根拠になる／2movement を繋ぐ／作品を
  分解して読んだ）のどれにも単独で当たらないため保留している。もし呉偉が浙派と他の画派（宮廷内の
  他系統）を繋ぐ一次資料が見つかれば基準2に当たる
- 南宋画院（馬遠・夏珪）・元代の李郭派との `derives_from` — 現状 movement として立てていないため
  張れない。南宋院体を movement/concept のどちらで持つかは別途判断が要る
- 日本の室町水墨画・李氏朝鮮絵画への影響（日本語版Wikipediaが触れている）——`diffused_to` の
  候補だが、対象側の movement が未整備（室町水墨画は現状このKBに無い）
- 「後代由来の呼称は人名／地名のどちらかに落ちる」という、本ファイルの kind 判定で新たに
  立てた仮説の検証（次の反例候補: 呉派——地縁か号か未確認、次に調べる価値がある）
- 呉派（同じく明代・地域名を冠する画派とされる）との対比。`overviews/japan-school-types.md` は
  浙派と呉派を並べて反証候補に挙げていたが、本タスクは浙派1件のみを扱う
