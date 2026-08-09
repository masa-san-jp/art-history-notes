---
id: movement/negritude
uri: urn:ahn:movement/negritude
type: movement
kind: self-declared
label_ja: ネグリチュード
label_en: Négritude
authority:
  wikidata: Q852544
  aat: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1935~"
  end: null
  display: "1931年（サンゴール・セゼール・ダマスがパリで出会う）〜1934年または1935年（雑誌『L'Étudiant noir（黒人学生）』創刊、この語の初出）〜。終期を示す資料は確認できていない（本文『時間』参照）"
naming:
  self_identified: true
  named_by: person/aime-cesaire
  named_when: "1935~"
  original_label: "Négritude"
  note: "語をつくったのは当事者自身。エメ・セゼール（マルティニーク出身の詩人）が雑誌『L'Étudiant noir』の創刊にあたって作った語で、フランス語で黒人を指し人種差別語に堕していた『nègre』を、当事者の側からあえて名乗り直したもの（[plato.stanford.edu/entries/negritude/](https://plato.stanford.edu/entries/negritude/)）。年は資料間で割れる——スタンフォード哲学百科事典は『1934–1935』、アメリカ詩人アカデミーは創刊を『1934年』とする。本KBは EDTF で `1935~`（およそ1935年）を採り、幅を display に残した。命名の年が確定しないため named_when も `1935~` にしている"
founding_control: internal   # パリ在学中の当事者（セゼール＝マルティニーク、サンゴール＝セネガル、ダマス＝仏領ギアナ）自身が語をつくり雑誌を出した。宗主国の機関が設けた枠組みではない
claims:
  - {field: kind, source: "https://plato.stanford.edu/entries/negritude/", certainty: attested}
  - {field: time, source: "https://poets.org/text/brief-guide-negritude", certainty: scholarly}
  - {field: originated_in, source: "https://www.tate.org.uk/art/art-terms/n/negritude", certainty: scholarly}
space:
  - {role: originated_in, target: place/paris}
relations:
  - {type: influenced_by, target: movement/harlem-renaissance, certainty: scholarly, source: "https://plato.stanford.edu/entries/negritude/"}
sources:
  - https://www.wikidata.org/wiki/Q852544
  - https://plato.stanford.edu/entries/negritude/
  - https://www.tate.org.uk/art/art-terms/n/negritude
  - https://poets.org/text/brief-guide-negritude
status: draft
updated: 2026-08-09
---

# ネグリチュード / Négritude

## 定義と範囲

1930年代のパリで、アフリカ・カリブ海のフランス語圏から来た留学生たちが立ち上げた反植民地の
文化・政治運動。テート美術館は「1930年代のパリで、黒人であることとアフリカ文化の価値を
取り戻そうとしたアフリカ系・カリブ海系の学生たちの集団によって創られた、反植民地の文化的・
政治的運動」と定義する（[tate.org.uk](https://www.tate.org.uk/art/art-terms/n/negritude)、
二次情報）。中心の3人（*Les Trois Pères*）は、エメ・セゼール（マルティニーク）、
レオポール・セダール・サンゴール（セネガル）、レオン＝ゴントラン・ダマス（仏領ギアナ）で、
1931年にパリで出会った（[poets.org](https://poets.org/text/brief-guide-negritude)、二次情報）。

美術史の側からこの運動を外せないのは、これが理論のまま終わらず**国家の文化政策と美術教育の
制度になった**からである。サンゴールは1960年に独立したセネガルの初代大統領となり、この立場から
美術学校・タピスリー工房・美術館を設け、1966年にダカールで第1回世界黒人芸術祭を開いた
（[plato.stanford.edu](https://plato.stanford.edu/entries/negritude/)、
[tate.org.uk](https://www.tate.org.uk/art/art-terms/n/negritude)、二次情報）。
その制度から出た作家群が、後に[ダカール派](ecole-de-dakar.md)と呼ばれる。テートは同芸術祭を
「多くの黒人の美術家・音楽家・作家・詩人・俳優にとって、アフリカ文化の世界規模の検証に
参加する最初の機会となった」と記す（同資料）。

## kind の判定 — なぜ `self-declared` か

語をつくったのが当事者自身である点で判定に迷いがない。セゼールは、フランス語で黒人を指し
人種差別語として使われてきた「nègre」をあえて引き受け直す形でこの語を作り、雑誌
『L'Étudiant noir（黒人学生）』の創刊とともに世に出した（[plato.stanford.edu](https://plato.stanford.edu/entries/negritude/)）。
外部の批評家が後から与えた括りではなく、当事者が名乗るために作った名である。

`named_by` はセゼール（[person/aime-cesaire](../persons/aime-cesaire.md)）とした。ただし
この語を**誰が最初に活字にしたか**と、3人のうち誰がいつ使い始めたかの細部は資料により幅がある
——**未確認**。

## 時間

`time.start` は `1935~`。スタンフォード哲学百科事典は語の成立を「1934–1935年、雑誌
『L'Étudiant noir』を作るとき」とし、アメリカ詩人アカデミーは同誌の創刊を「1934年」と書く。
両者は1年ずれており、どちらかを断定できる材料が無いため、EDTF の「およそ」（`~`）で
1935年を採り、幅は `time.display` に残した。3人がパリで出会った1931年は運動の前史に当たる。

`time.end` は空欄にした。**終期を示す資料が見つからないのではなく、終期の立て方が対象によって
違う。** 文学運動としての盛期は1930〜1960年代とされるが、サンゴールの大統領在任は1980年まで続き、
理念としてのネグリチュードはその後も批判と再評価の対象であり続けている。「いつ終わったか」を
一つの年で書ける状態にない——**未確認**。

## 空間

`originated_in` は[パリ](../places/paris.md)。この運動の担い手はアフリカ・カリブ海の出身だが、
運動が形になった場所は宗主国の首都である。**発生地と、担い手が帰属を主張した文化圏が一致しない。**
テート、スタンフォード哲学百科事典、アメリカ詩人アカデミーはいずれも成立の場をパリとする。

この一致しなさは偶然ではなく、運動の成り立ちそのものに属している。3人がハーレム・ルネサンス
（[movement/harlem-renaissance](harlem-renaissance.md)）の書き手たちに出会ったのもパリだった。
スタンフォード哲学百科事典は、彼らがマルティニーク出身のナルダル姉妹がパリで開いていたサロンを
通じてアメリカの運動を知り、そこでラングストン・ヒューズやクロード・マッケイと出会ったこと、
アラン・ロックの編んだアンソロジー『The New Negro』が「サンゴールとその友人たちにきわめて強い
印象を与えた」ことを記す（[plato.stanford.edu](https://plato.stanford.edu/entries/negritude/)、
二次情報）。アメリカ詩人アカデミーは端的に「この運動はハーレム・ルネサンスから着想を得た」と書き、
サンゴールがクロード・マッケイを「ネグリチュードの精神的な創設者」と称えたと記す
（[poets.org](https://poets.org/text/brief-guide-negritude)、二次情報）。テートも影響源として
シュルレアリスムとハーレム・ルネサンスを挙げる（[tate.org.uk](https://www.tate.org.uk/art/art-terms/n/negritude)）。
Wikidata Q852544 の `P737`（influenced by）も、ハーレム・ルネサンス（Q829895）・シュルレアリスム
（Q39427）・パン・アフリカ主義（Q282739）の3つを挙げる。

`influenced_by` を[ハーレム・ルネサンス](harlem-renaissance.md)に張り、`certainty` は
`scholarly` とした。サンゴール本人がマッケイを名指しで称えた発言は `attested`（当事者の言明）に
当たりうるが、本KBが確認できたのは二次資料に引かれた形の要約であって、発言の原典（どの文章の
どこか）を押さえられていない——**未確認**。原典に届いたら `attested` に上げる。

## 未着手

- サンゴールがクロード・マッケイを「ネグリチュードの精神的な創設者」と呼んだ発言の原典
  （著作・講演・年）。押さえられれば `influenced_by` の `certainty` を `attested` に上げられる
- 『L'Étudiant noir』創刊号（1934年か1935年か）の現物または書誌。創刊年が確定すれば
  `time.start` の `~` を外せる
- ナルダル姉妹（ポーレット・ナルダル）の person 化。パリで開かれていたそのサロンは、ハーレム・
  ルネサンスとネグリチュードという2つの運動を実際に繋いだ場であり、`docs/schema.md` の
  person 作成基準2（2つ以上の movement を繋ぐ）に当たる。レオポール・セダール・サンゴール、
  レオン＝ゴントラン・ダマスも同様に未作成（セゼールのみ `named_by` の根拠として立てた）
- シュルレアリスム、パン・アフリカ主義との関係。Wikidata は影響源として挙げるが、本調査では
  出典を押さえていないため関係を張っていない
- 雑誌『Présence Africaine』（1947年創刊）の org 化。ネグリチュードの発表媒体であり、
  パパ・イブラ・タルがパリ在学中に挿絵を寄せた先でもある
- ネグリチュードへの批判（ウォーレ・ショインカ、フランツ・ファノンら）の位置づけ。批判は
  この運動の受容史の一部だが、本調査では出典を押さえていない
