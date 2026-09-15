---
id: movement/computer-art
uri: urn:ahn:movement/computer-art
type: movement
label_ja: コンピュータ・アート
label_en: Computer Art
authority:
  wikidata: Q1376265
  aat: "300069478"
  ulan: null
  tgn: null
  ndl: null
  jpsearch: null
  none_reason: null
time:
  start: "1965"
  end: null
  display: "1965年11月、フリーダー・ナケとゲオルク・ニースのシュトゥットガルトでの展示を、確認できる範囲で最初期の公開実践とした。ただし同時多発的な起源を持ち、単一の開始点には代表させられない"
kind: retrospective
naming:
  self_identified: false
  named_by: null
  named_when: null
  original_label: コンピュータ・アート / computer art
  note: "Getty AAT は「digital art works that emphasize the computer's role in their creation and apprehension」への適用語とし、created_by を「computer artists」とする。単一の宣言や単一グループの自称ではなく、1960年代に北米・欧州で独立に始まった複数の実践へ事後的に適用された括り。ただしナケやモーアは自らをcomputer artistと呼んだ形跡があり、括り自体への異議は確認していない"
claims:
  - {field: time, source: "https://en.wikipedia.org/wiki/Frieder_Nake", certainty: scholarly}
  - {field: originated_in, source: "https://en.wikipedia.org/wiki/Frieder_Nake", certainty: scholarly}
  - {field: kind, source: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300069478", certainty: scholarly}
evidence:
  - {target: person/harold-cohen, supports: [kind]}
  - {target: person/frieder-nake, supports: [time, kind]}
space:
  - {role: originated_in, target: place/stuttgart}
  - {role: originated_in, target: place/paris}
  - {role: active_in, target: place/la-jolla}
relations:
  - {type: created_by, target: person/harold-cohen}
  - {type: created_by, target: person/frieder-nake}
sources:
  - url: "https://www.wikidata.org/wiki/Q1376265"
    kind: authority
  - url: "https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300069478"
    kind: authority
  - url: "https://cs.uml.edu/~fredm/courses/91.548-spr04/papers/furtherexploits.pdf"
    kind: primary
    note: "Harold Cohen本人の論考"
  - url: "https://en.wikipedia.org/wiki/Frieder_Nake"
    kind: reference
  - url: "https://en.wikipedia.org/wiki/Vera_Moln%C3%A1r"
    kind: reference
  - url: "https://en.wikipedia.org/wiki/Manfred_Mohr"
    kind: reference
  - url: "https://senate.universityofcalifornia.edu/_files/inmemoriam/html/HaroldCohen.html"
    kind: institutional
    note: "UC Academic Senate In Memoriam。1968年UCSD着任（visiting lecturer）から1994年退官までを記す"
  - url: "https://visarts.ucsd.edu/people/in-memoriam/harold-cohen.html"
    kind: institutional
    note: "UC San Diego Visual Arts学科によるIn Memoriam。学科在籍とProfessor Emeritusの肩書を記す"
status: draft
updated: 2026-09-15
---

# コンピュータ・アート / Computer Art

## 定義と範囲

Getty AAT の scope note はこう定義する（[AAT 300069478](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&english=Y&subjectid=300069478)、原文引用）。

> Term applied to digital art works that emphasize the computer's role in their creation and
> apprehension. Specifically used for artworks that employ computer terminals or technology for
> display, distribution, or interaction, so that the machinery is an integral part of the work.

1960年代、北米・欧州で複数の作家が独立にコンピュータを制作の中心に据え始めた。代表的な担い手として
[ハロルド・コーエン](../persons/harold-cohen.md)（英国生、AARON の開発者）、ヴェラ・モルナール
（1924年ブダペスト生、1959年に手作業のアルゴリズム的手法「machine imaginaire」を開始し1968年から
コンピュータを併用）、マンフレート・モーア（1938年プフォルツハイム生、1969年独学でプログラミングを
始めキューブを反復モチーフに使用）、[フリーダー・ナケ](../persons/frieder-nake.md)（1938年
シュトゥットガルト生、1963年からコンピュータ使用）がいる。モルナール・モーアはいずれも活動拠点を
パリに持つ（[place/paris](../places/paris.md)）。ヴェラ・モルナールとマンフレート・モーアは、
今回の調査では movement の kind / time / originated_in の直接の根拠にはしておらず、担い手として
本文に名前のみ記した（`docs/schema.md` の person 作成基準に照らし、ファイル化は見送った）。

## kind の判定

`retrospective` とした。Getty AAT の created_by が「computer artists」という総称であり、単一の
宣言文や単一グループの自称ではなく、独立に始まった複数の実践に事後的に適用された括りだと判断した。
ただし、この括りに対して当事者が異議を唱えた形跡は確認していない——ナケやモーアが自身の実践を
computer art と呼ぶことを拒んだという記録はない。

## 時間

`start` は、確認できた範囲で最も早い**公開**実践であるナケ／ニースの1965年11月シュトゥットガルト
展示を採った。**未確認**: これが本当に最初の公開展示かどうかは裏を取っていない。ナケ自身は1963年
から制作を始めており、モルナールも1959年から手作業のアルゴリズム的手法（コンピュータ使用前段階）を
始めている。**単一の開始点に代表させられない同時多発的な起源であることを、ここに明記する。**

## 空間

複数起源として扱う。[place/stuttgart](../places/stuttgart.md)（ナケ／ニース）と
[place/paris](../places/paris.md)（モルナール／モーアの活動拠点）を `originated_in` に持つ。
コーエンの拠点だったカリフォルニア大学サンディエゴ校（米国）は、今回は place エンティティを
作らずに本文の記述にとどめた。

## 構想と実行の区別（issueの主張との関係）

このKB登録の主目的は、「AIが人間に芸術の契機をもたらす」という主張と、コンピュータ・アートの
先行実践との違いを言えるようにすることである。核心は、機械が**構想**（何を描くか）を担ったのか、
**実行**（描く動作）だけを担ったのかの区別にある。

ハロルド・コーエンは AARON について、1994年の論考でこう書いている（一次資料、原文引用）。

> All its decisions about how to proceed with a drawing, from the lowest level of constructing a
> single line to higher-level issues of composition, were made by considering what it wanted to do
> in relation to what it had done already.

構図レベルの決定まで AARON 自身が担っていたとコーエンは明言する。**機械が実行だけでなく、構想の一部
までも担っていた事例**である。同時にコーエンは、これが AARON に思考や創造性が存在することの証明には
ならないと自ら限定しており、「人間が機械から芸術の契機を受け取る」という構造とも異なる——コーエンの
記述では、機械は**人間の代わりに描く主体**として位置づけられており、人間に霊感を与える側としては
描かれていない。

## 文化圏間の接続

起源はシュトゥットガルト／パリ（ともに europe-west）だが、担い手の一人ハロルド・コーエンは1968年に
米国カリフォルニア州の[ラホヤ](../places/la-jolla.md)（UC San Diego 所在地、americas-north）へ
visiting lecturer として着任し、1994年の退官まで在籍した（UC Academic Senate In Memoriam、
機関資料、原文引用）。

> Brought to UC San Diego in 1968 as a visiting lecturer, Cohen was a mainstay of the Visual Arts
> Department until he retired in 1994.

AARON の開発はUCSD在籍期間中に進んだため、`space.active_in` に la-jolla を追加し、
europe-west 起源から americas-north への活動の広がりを機械可読に記録した。

## 未着手

- ヴェラ・モルナール、マンフレート・モーア本人の論考・一次資料への到達（今回は二次情報どまり）
- 1983年 Tate Gallery での AARON 展示の一次アーカイブ記録
- マックス・ベンゼの情報美学とコンピュータ・アートの理論的な結びつき（ナケ・モーア双方が影響を
  受けたとされるが、ベンゼ自身の一次資料は未確認）
