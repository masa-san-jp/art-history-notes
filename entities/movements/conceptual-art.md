---
id: movement/conceptual-art
uri: urn:ahn:movement/conceptual-art
type: movement
label_ja: コンセプチュアル・アート
label_en: Conceptual Art
authority:
  wikidata: Q203209
  aat: "300264827"
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1967"
  end: null
  display: "1967年、ルウィットが「Paragraphs on Conceptual Art」で自身の実践を名指した年を起点とした。Wikidata P571のprecision 8（196X）は同じ10年代を指す"
kind: self-declared
naming:
  self_identified: true
  named_by: person/sol-lewitt
  named_when: "1967"
  original_label: conceptual art
  note: "ルウィット自身が1967年の論考で「I will refer to the kind of art in which I am involved as conceptual art」と自らの実践を名指した。ただし1961年、Henry Flyntが私的講演で近い語「concept art」を先に使っている——Flyntの定義は「音楽の材料が音であるように、その材料が概念であるアート」であり、ルウィットの定義（アイデアが計画のすべてを決め実行が形式的作業になる）とは異なる。Flyntはルウィットのこの運動を名指したわけではないため named_by は person/sol-lewitt のままとした（surrealism.mdのアポリネール先行使用と同じ処理）"
claims:
  - {field: time, source: "https://www.kim-cohen.com/Assets/CourseAssets/Texts/LeWitt_Paragraphs%20(1967).pdf", certainty: attested}
  - {field: kind, source: "https://www.kim-cohen.com/Assets/CourseAssets/Texts/LeWitt_Paragraphs%20(1967).pdf", certainty: attested}
evidence:
  - {target: person/sol-lewitt, supports: [kind, time]}
space:
  - {role: originated_in, target: place/new-york-city}
relations:
  - {type: created_by, target: person/sol-lewitt}
sources:
  - url: "https://www.wikidata.org/wiki/Q203209"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300264827"
    kind: authority
  - url: "https://www.kim-cohen.com/Assets/CourseAssets/Texts/LeWitt_Paragraphs%20(1967).pdf"
    kind: primary
    note: "ルウィット「Paragraphs on Conceptual Art」全文（Artforum, 1967年6月号）"
  - url: "http://www.multimedialab.be/doc/citations/sol_lewitt_sentences.pdf"
    kind: primary
    note: "ルウィット「Sentences on Conceptual Art」全文（1969年）"
  - url: "https://henryflynt.org/aesthetics/conart.html"
    kind: reference
    note: "Henry Flyntによる「concept art」の先行使用（1961年講演、1963年論考掲載）"
status: draft
updated: 2026-09-15
---

# コンセプチュアル・アート / Conceptual Art

## 定義と範囲

Getty AAT の scope note は次のように記す（[AAT 300264827](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300264827)、原文引用）。

> The genre emerged in the late 1960s and early 1970s, arising at virtually the same time in North
> America, Europe and Latin America... The term entered common art parlance through an article by
> Sol LeWitt, "Paragraphs on Conceptual Art" published in Artforum in 1967.

[ソル・ルウィット](../persons/sol-lewitt.md)は1967年の同論考で、自身の実践を次のように定義した
（一次資料、原文引用）。

> I will refer to the kind of art in which I am involved as conceptual art. In conceptual art the
> idea or concept is the most important aspect of the work. When an artist uses a conceptual form
> of art, it means that all of the planning and decisions are made beforehand and the execution is
> a perfunctory affair. The idea becomes a machine that makes the art.

1969年の「Sentences on Conceptual Art」（35の文、一次資料）では、実行段階の位置づけをさらに明確に
書く。

> The process is mechanical and should not be tampered with. It should run its course.

## kind の判定

`self-declared` とした。ルウィット自身が論考で自分の実践を名指し、定義を与えている点が根拠になる。

ただし判定には迷いがある。Getty AAT は「北米・欧州・ラテンアメリカでほぼ同時に出現したジャンル」と
記述しており、単独の宣言というより複数の作家群への事後的な適用に近い性格も併せ持つ。**self-declared
と retrospective の中間的な性格**であることを、ここに明記する。ルウィットの1967年論考が語を
一般化させた起点であることは AAT 自身が認めているため、名指しの起点として self-declared を選んだ。

**先行使用がある。** 1961年6月、Henry Flynt が La Monte Young のアパートでの私的講演で「concept
art」という語を先に使い、1963年の *An Anthology of Chance Operations* に論考を掲載した
（[henryflynt.org](https://henryflynt.org/aesthetics/conart.html)）。Flynt の定義は「音楽の材料が
音であるように、その材料が概念であるアート」であり、ルウィットの「計画がすべてを決め実行は形式的
作業になる」という定義とは異なる。Flynt がルウィットのこの運動を名指したわけではないため、
`named_by` はルウィットのまま残した。

## 時間

`start` はルウィットの論考発表年（1967年）とした。Wikidata `P571` は precision 8（196X）で、
同じ10年代を指すにとどまる。

## 空間

`originated_in` はニューヨーク（[place/new-york-city](../places/new-york-city.md)）。ルウィットの
活動拠点であり、1967年の論考発表地である。**未確認**: AAT が言う「北米・欧州・ラテンアメリカでの
同時発生」の他地域の担い手・場所は今回未調査。

## 構想と実行の区別（issueの主張との関係）

issue #394 が求めるのは、「AIが人間に芸術の契機をもたらす」という主張との差分の記述である。
コンセプチュアル・アートの構造は、**指示書（アイデア）を作家が書き、実行を他者・機械的過程に
委ねる**という点で今回の4領域の中でも独自の先行例になる。ルウィットの「The idea becomes a machine
that makes the art」という一節は、アイデアそのものを機械に見立てる比喩である。ただし、ここでの
「機械」は比喩であり、実際にコンピュータや人工知能が使われているわけではない——実行を担うのは
助手という**人間**である（Wall Drawings の制作構造、二次情報）。したがって、この先行例における
「契機」は常に作家自身のアイデアに由来し、外部の機械や人工知能に由来するものではない。issueが扱う
主張とは、**契機の出どころが人間（作家自身）か、人間の外部（機械）か**という一点で分かれる。

## 未着手

- Getty AAT が言う「北米・欧州・ラテンアメリカでの同時発生」の、ルウィット以外の担い手・地域
- Henry Flynt の1961年講演そのものの一次資料（講演録・正確な日付）
- Wall Drawings の指示書と実行の分離を直接裏付ける一次資料（本人インタビュー等）
