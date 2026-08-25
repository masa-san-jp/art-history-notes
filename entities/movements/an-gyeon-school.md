---
id: movement/an-gyeon-school
uri: urn:ahn:movement/an-gyeon-school
type: movement
kind: retrospective
label_ja: 安堅派
label_en: An Gyeon school
authority:
  wikidata: null
  aat: null
  ndl: null
  jpsearch: null
  none_reason: "Wikidata を「안견파」（ko）「An Gyeon school」（en）で検索したが該当項目なし（安堅本人 Q1036353 は取れたが、流派側の項目は無い）。AAT は www.getty.edu/vow/AATServlet 経由での検索がいずれも 400 Bad Request で到達できず——docs/investigation-task.md が既知の問題として挙げる範囲。NDL は「安堅派」でクエリすると SPARQL パーサエラー、Japan Search は横断検索ページが JS 描画で内容を取得できず、いずれも docs/investigation-task.md が既知の未確認事項として挙げる到達性問題と一致する"
time:
  start: "14XX"
  end: "16XX"
  display: "15世紀（世宗代〜世祖代、安堅の画院・画署活動期）に成立し、朝鮮中期（16〜17世紀、金明国ら後継世代の活動期）まで画壇に影響"
naming:
  self_identified: false
  named_by: person/ahn-hwi-joon
  named_when: "1980"
  original_label: 安堅派
  note: "한국민족문화대백과사전「안견파」（執筆者は安輝濬本人）は「'안견파'라는 용어는 안휘준…에 의해 명명되었다」（「安堅派」という用語は安輝濬によって命名された）と明記する。安輝濬の主著『韓国絵画史』（一志社、1980年）が用語の学術的な確立を示す最も具体的な年代の分かる文献だが、それ以前の1974年論文「安堅과 그의 画風—夢遊桃源図を中心으로」（『震檀学報』38）で既に同語を用いていた可能性があり、named_when を1980年と特定できるかは**未確認**"
claims:
  - {field: kind, source: "https://encykorea.aks.ac.kr/Article/E0069639", certainty: scholarly}
  - {field: originated_in, source: "https://encykorea.aks.ac.kr/Article/E0034491", certainty: scholarly}
  - {field: time, source: "https://encykorea.aks.ac.kr/Article/E0069639", certainty: scholarly}
space:
  - {role: originated_in, target: place/hanseong}
  - {role: active_in, target: place/hanseong}
relations:
  - {type: influenced_by, target: movement/song-academy-painting, certainty: scholarly, source: "https://encykorea.aks.ac.kr/Article/E0069639"}
sources:
  - url: "https://encykorea.aks.ac.kr/Article/E0069639"
    kind: institutional
  - url: "https://encykorea.aks.ac.kr/Article/E0034491"
    kind: institutional
  - url: "https://encykorea.aks.ac.kr/Article/E0018824"
    kind: institutional
  - url: "https://ko.wikipedia.org/wiki/%EB%AA%BD%EC%9C%A0%EB%8F%84%EC%9B%90%EB%8F%84"
    kind: reference
  - url: "https://www.wikidata.org/wiki/Q1036353"
    kind: authority
  - url: "https://www.wikidata.org/wiki/Q12595455"
    kind: authority
  - url: "https://www.khan.co.kr/article/202607201829001/"
    kind: reference
  - url: "https://commons.wikimedia.org/wiki/File:Mongyudowondo.jpg"
    kind: reference
images:
  - url: https://upload.wikimedia.org/wikipedia/commons/e/e4/Mongyudowondo.jpg
    source_page: https://commons.wikimedia.org/wiki/File:Mongyudowondo.jpg
    rights_source: https://commons.wikimedia.org/wiki/File:Mongyudowondo.jpg
    license: pdm
    note: "安堅《夢遊桃源図（몽유도원도）》1447年、絹本淡彩。安堅派という括りの起点となった安堅自身の代表作。現在は日本・天理大学附属天理図書館蔵。Wikimedia Commons は CC-PD-Mark／PD-old-100-expired を付し、出典を韓国著作権委員会「공유마당」（gongu.copyright.or.kr）および Google Arts & Culture とする"
status: draft
updated: 2026-08-10
---

# 安堅派 / An Gyeon school

朝鮮王朝前期の宮廷画員・安堅（안견、生没年不詳、15世紀）の画風と、それを追従した著名・無名の画家群を
指す美術史上の括り。한국민족문화대백과사전「안견파」は「산수화의 대가 안견과 그의 화풍을 추종했던
유명, 무명 화가들을 가리키는 미술유파」（山水画の大家・安堅とその画風を追従した著名・無名の画家を
指す美術流派）と定義する（<https://encykorea.aks.ac.kr/Article/E0069639>、二次情報）。

## 定義と範囲

同記事は様式的特徴として、画面の一方に重心を置き他方を軽く描く**編波構図**（편파구도）、近景・遠景の
2段構成から16世紀に近景・中景・遠景の3段構成へ発展した**編波2段／3段構図**、筆致の跡が目立たないよう
筆を継いで用いる淡白な墨法、雲のような山容を表す**雲頭皴法**（운두준법）、蟹の爪のような木の枝を表す
**蟹爪描法**（해조묘법）、16世紀に創出された短い線と点による質感表現**短線点皴**（단선점준）を挙げる
（同、二次情報）。安堅派は「북송대 곽희파 화풍을 위주로 하고 남송대 마하파 화풍도 수용하여 절충하면서
한국적 화풍을 창출한 결과물」（北宋・郭熙派の画風を主としつつ、南宋・馬夏派の画風も受容し折衷して
朝鮮的な画風を創出した結果）とされる（同）。

### 宋代院体画との形成関係

この記述に基づき、本項では安堅派の形成層に限って `influenced_by movement/song-academy-painting`
を記録する。関係の実体は、安堅が安平大君の所蔵する古画に接し、北宋・郭熙派を主軸に
南宋・馬夏派を取り入れて朝鮮的な山水画へ折衷したという、画風語彙の受容である。これは
中国の宋代院体画が安堅派の全作品を一律に規定したという主張でも、安堅が中国の画家から
直接師事したという主張でもない。

安堅自身の経歴は한국민족문화대백과사전「안견」に詳しい。本貫は池谷（지곡）、字は可度または得守、号は
朱耕または玄洞子。世宗年間（1418〜1450年）に最も活発に活動し、文宗・端宗を経て世祖代まで画員として
活躍した。図画院（도화원）の従6品・善画（선화）から遞児職の正4品・護軍にまで昇進しており、これは
朝鮮初期の画員が身分上の制約を超えた最初の事例とされる（<https://encykorea.aks.ac.kr/Article/E0034491>、
二次情報）。安平大君（Wikidata [Q624197](https://www.wikidata.org/wiki/Q624197)、1418-1453）に近侍し、
その所蔵する古画を渉猟したことが自らの画風形成の土台になったとも記す（同）。代表作に《八駿図》
（1446-1447年）・《四時八景図》（国立中央博物館蔵）・《赤壁図》（国立中央博物館蔵）・《大小駕儀仗図》
（1448年）・《墨竹図》（1464年）・《李蓑馬山水図》（1443年）、そして後述の《夢遊桃源図》（1447年）が
ある（同）。

追従した画家として、初期に石憼（석경）・梁彭孫（양팽손）・申師任堂（신사임당）、中期に金禔（김시）・
李廷根（이정근）・李興孝（이흥효）・李澄（이징）・金明国（김명국）の名を同記事は挙げる（同）。
申師任堂は士大夫層の女性画家であり画員ではない——追従者の身分は画員に限らない。**未確認**: これら
追従者それぞれが安堅から直接様式を学んだ経路（誰の作品を模したか、誰から手ほどきを受けたか）の
一次資料には当たっていない。本KBの作成基準（`docs/schema.md`「person をいつ作るか」）のいずれにも
単独では当たらないため、名前を本文に記すに留める。

## kind の判定

### 1. 誰がいつ「安堅派」という括りを作ったか

**明確に後代の学術用語である。** 한국민족문화대백과사전「안견파」の執筆者自身が「'안견파'라는 용어는
안휘준…에 의해 명명되었다」（「安堅派」という用語は[安輝濬](../persons/ahn-hwi-joon.md)によって
命名された）と明記する（<https://encykorea.aks.ac.kr/Article/E0069639>）。安堅本人や同時代・後代の
追従画家たちが自らを「안견파」と名乗った証拠は無い。安輝濬の主著『韓国絵画史』（一志社、1980年）が
用語の学術的確立を示す最も年代の特定できる文献であり、これを `naming.named_when` の根拠とした。
以上から `naming.self_identified: false`、`kind: retrospective` と判定した。

### 2. 継承の形——血縁でも師弟でもなく様式の追従

**血縁の継承体ではない。** 安堅自身の子孫が画業を継いだという記録は当たった出典には無く、狩野派
（[movement/kano-school](kano-school.md)）のような家系による継承の実体は確認できない。

**制度としての継承体でもない。** 安堅自身は図画院（[org/dohwaseo](../orgs/dohwaseo.md) の前身）の
画員だったが、追従者に挙がる申師任堂は士大夫層の在野の女性画家であり画員ではない。追従者全員が
図画院・図画署に属していたわけではないため、集団全体を組織的な継承体として扱うことはできない
（この点は下記「図画署との関係」で詳述）。

**様式の追従による継承である。** 한국민족문화대백과사전「안견파」は継承の形について師弟関係や血縁を
明記せず、代わりに「추종했던」（追従した）という語を繰り返し用いる——安堅の描く編波構図・雲頭皴法・
蟹爪描法という**手つきそのもの**を、身分も時代も異なる画家たちが模倣・追従したことで括りが成立して
いる。これは[真景山水画](jingyeong-sansuhwa.md)の kind 判定（担い手の身分・系統が一枚岩でなく、
様式的同一性だけが横断的に共有される軸）と同型の構造である。

### 3. 図画署との関係——張れるか

安堅自身は図画院（後の図画署の前身）の画員であり、종6품 善画から정4品 護軍まで昇進した
（<https://encykorea.aks.ac.kr/Article/E0034491>）。[org/dohwaseo](../orgs/dohwaseo.md) 本文も
安堅を代表的な画員の一人として挙げている。しかし安堅派全体を見ると、追従者の申師任堂は士大夫層の
在野画家であり画員ではない。**開祖個人は制度（図画院／図画署）に属したが、追従者全体は属さない**
という構造は、[真景山水画](jingyeong-sansuhwa.md)（開祖・鄭敾が士大夫の文官で図画署に無関係、
一部の後継世代のみ画員）と鏡合わせの関係にある——どちらも「movement 全体」対「org」の関係を
`belongs_to` 等の構造的関係語彙で1本には表せない。この理由により、事実は本文に明記した上で
`relations` にはエッジを張らなかった。

### 4. kind の判定と理由

用語の成立が明確に1980年前後の学術的命名であること（`naming.self_identified: false`）、継承が
血縁でも制度でもなく様式の追従によって成立していること、この2点から `kind: retrospective` と
判定した。

## 時間

`start` は安堅の画院・画署での活動期を根拠に世紀精度の `14XX`（15世紀）とした。
한국민족문화대백과사전「안견」は「세종 연간(1418∼1450년)에 가장 왕성하게 활동」と明記し、現存する
紀年作品も《李蓑馬山水図》（1443年）・《八駿図》（1446-1447年）・《夢遊桃源図》（1447年）・
《大小駕儀仗図》（1448年）・《墨竹図》（1464年）といずれも15世紀に収まる
（<https://encykorea.aks.ac.kr/Article/E0034491>）。

`end` は、`kind: retrospective` の movement は「括られた対象の活動期間」を持つという
`docs/schema.md` の規定に従い、追従世代の活動期まで含めて判定した。
한국민족문화대백과사전「안견파」は中期の追従者として金明国（김명국）を挙げ（同記事）、金明国は
1636年・1643年の朝鮮通信使に随行して日本へ渡った17世紀の画員として知られる（WebSearch経由・
二次情報、金明国自身の一次資料には当たっていない）。同記事が「조선초기는 물론 중기까지 크게
영향력을 발휘」（朝鮮初期はもとより中期まで大きな影響力を発揮）と記すこととあわせ、世紀精度の
`16XX`（17世紀）を `end` とした。

**未確認**: 用語としての「안견파」自体は後代の括りだが、様式的な追従がいつ途絶えたと言える具体的な
年（金明国以降にも追従が続いたか）は当たった出典からは特定できない。

## 空間

`originated_in` は漢城（[place/hanseong](../places/hanseong.md)）とした。根拠は安堅が図画院
（漢城に置かれた官署——[org/dohwaseo](../orgs/dohwaseo.md) 参照）の画員として活動し、後援者の
安平大君（Wikidata [Q624197](https://www.wikidata.org/wiki/Q624197)）に近侍したことである
（<https://encykorea.aks.ac.kr/Article/E0034491>）。安堅の出身地そのものは記録が無く
（생몰년 미상）、Wikidata（[Q1036353](https://www.wikidata.org/wiki/Q1036353)）の `P19`／`P20`
（出生地／死没地）は忠清南道（Q41070）を挙げるが、これは本貫・池谷（現在の忠清南道瑞山市付近と
される）を出生地と同一視した可能性が高く、活動拠点である漢城とは別軸のため `originated_in` には
採らなかった——**未確認**: 安堅の実際の出身地。

**未確認**: 追従者（石憼・梁彭孫・申師任堂・金禔・李廷根・李興孝・李澄・金明国）それぞれの活動拠点が
漢城に限定されるか、地方への広がりがあったか。

## 未着手

- **中国・北宋の郭熙様式との関係**: 한국민족문화대백과사전「안견파」は安堅派の画風を「북송대 곽희파
  화풍을 위주로 하고」（北宋・郭熙派の画風を主として）と明記し、안견自身が安平大君所蔵の郭熙様式の
  画（真筆ではなく金・元代の李郭派様式作とみられるものを含む、WebSearch経由・二次情報）に接して
  自らの様式を形成したという記述もある。しかし郭熙・李郭派を指す movement は本KBに存在しないため、
  `relations` の `influenced_by` としては張らなかった。北宋・李郭派の movement／person エンティティが
  作られた時点で、この関係を張ることを次の課題とする
- **日本・周文一派への影響**: 同記事は「15세기 일본의 슈분 일파에 영향」（15世紀日本の周文一派に影響）
  と記すが、周文一派を指す movement も本KBに存在しないため、同様に `relations` へは反映していない
- 《夢遊桃源図》がいつ・どのように日本へ渡ったかの経緯。ko.wikipedia「몽유도원도」は2つの異なる説を
  挙げる——(1) 壬辰倭乱（文禄の役）で第4陣として朝鮮に出兵した島津義弘（시마즈 요시히로）が京畿道
  高陽県・大慈庵からこの絵を略奪したという説（「추정만 할 뿐 확인된 사실은 아니다」＝推定のみで
  確認された事実ではない、と明記）、(2) 日本の収集家・島津久徴（도진구징）の生涯・活動から
  「1893년 이전에 이미 일본에 있었다」（1893年以前に既に日本にあった）と推定される説
  （<https://ko.wikipedia.org/wiki/%EB%AA%BD%EC%9C%A0%EB%8F%84%EC%9B%90%EB%8F%84>）。この2説の
  整合・一次資料での裏取りは未着手。天理大学の所蔵開始時期は「1955年頃から」とのみ記録がある（同）
- 安輝濬が「안견파」の語を最初に用いた文献が1974年論文か1980年『韓国회화사』かの一次確認
  （[person/ahn-hwi-joon](../persons/ahn-hwi-joon.md) 参照）
- Getty AAT・NDL・Japan Search での典拠ID（今回は到達できず。`authority.none_reason` に記載）
- 石憼・梁彭孫・申師任堂・金禔・李廷根・李興孝・李澄・金明国という追従者それぞれの活動拠点・
  安堅からの様式継承経路の一次資料での裏取り
