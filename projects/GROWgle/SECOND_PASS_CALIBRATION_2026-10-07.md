# GROWgle — Second Pass Calibration

Date: 2026-10-07
State: IN_PROGRESS / DEPTH_CALIBRATION
Pilot: Okayama / Kibi-Chuo

## 1. Purpose

Second Pass開始時に、First Pass / Cross-Category Re-scanの既存ログと照合しながら、

- 重複探索を増やしていないか
- 探索深度が浅すぎないか
- 1 SOURCEを掘りすぎて全体カバレッジを落としていないか

を校正する。

参照:
- `projects/GROWgle/RESEARCH_RULES.md`
- `projects/GROWgle/CHECKPOINT_OKAYAMA_V1_2026-10-04.md`
- `projects/GROWgle/CROSS_CATEGORY/OKAYAMA_SOUTH_RESCAN_V0_1.md`
- `projects/GROWgle/ENTRE/OKAYAMA_SOUTH_RESEARCH_V0_1.md`

## 2. Initial assessment of existing Okayama South research

Overall judgment: **NOT SHALLOW, BUT UNEVEN**

既存調査は以下には強い:
- 自治体の公開イベント
- 博物館 / 科学館 / 自然施設等の常設SOURCE
- ENTRE / WORKS / STEAM / NATURE等の代表的な地域資産
- 一般公開 / 学校限定の区別
- 地域固有資産からの代表例抽出

一方で薄い層:
- 自治体の事務事業概要に載る通年プログラム
- 放課後教育 / 地域学校協働
- 公民館・図書館の小規模継続プログラム
- 学校外から学校へ入る地域人材 / 大学 / 高校 / NPOのネットワーク
- 「単発イベント」ではなく毎週・通年で体験を生む制度型SOURCE

Second Passでは、既知の大型施設やイベント名を再検索するより、この薄い層を優先する。

## 3. Second Pass depth rule — calibration v0.1

### Before search
自治体 / 小ブロックごとに既存ログから以下を先に抽出:
- KNOWN_SOURCE
- KNOWN_ACTIVITY
- BACKLOG
- UNDEREXPLORED_ROUTE

### Search depth

#### Layer 1 — Differential current check
既知SOURCEのうち、
- 現在募集中
- 次回開催
- 継続性未確定
のみ確認する。

既知情報の再構築だけでは1件と数えない。

#### Layer 2 — Hidden-source search
First Passで薄かった:
- 教育委員会
- 事務事業概要
- 公民館
- 図書館
- 放課後事業
- 地域学校協働
- 青少年事業
- 大学 / 高校側の地域連携
を確認する。

#### Layer 3 — Reverse relationship search
新しい制度 / PROGRAMを見つけたら、
主催者だけでなく
- 参加企業
- 大学
- 高校
- NPO
- 地域団体
側から1段だけ逆引きする。

新しいSOURCE / NETWORKが出なければそこで停止する。

### Stop rule
- 異なる探索経路を追加しても既知SOURCE中心になったら SATURATED_FOR_SECOND_PASS
- 同じSOURCEに細部確認だけで3回以上戻らない
- 小規模イベントが多数あるSOURCEは、全件収集せず
  1. SOURCEの継続性
  2. 代表ACTIVITY
  3. 現在参加可能なACTIVITY
  を優先する

## 4. Calibration field — Kibi-Chuo

### Existing known from Cross-Category v1
- 国立吉備青少年自然の家
- 星空の学校 / 吉備中央町観光協会
- 吉備中央町図書館「きのこの教室」
- 吉備高原都市さんさん祭り
- 自然科学 / 農業体験
- スポーツ支援
など。

Major asset layerは既に十分に取れている。

## 5. New / undercaptured SOURCE layer

### A. 吉備中央町アフタースクール事業 — HIGH-VALUE SOURCE

2026年度も通年実施。
各小学校で週1回、1時間程度。

目的:
幅広い地域住民・企業・団体等の参画により豊かな体験活動を実施し、
子どもが得意分野に気づき、社会の未来を切り開く「生きる力」を育てる。

町公式では、
スポーツ / デジタルアート / ドローン / 大学生との交流等を例示。

放課後NPOアフタースクールの2026年報告では、
町内3小学校で低学年・高学年に分け、
- スポーツ
- モノづくり
- 文化芸術
- 国際教育
- 地域交流
の5領域を設計。
令和7年度は町内児童の約8割が登録、各回30〜70名程度が参加。

Classification:
- SCHOOL / LOCAL_CHILDREN
- CONSTANT / WEEKLY
- CROSS_CATEGORY_SOURCE
- STEAM / SPORTS / CREATIVE / GLOBAL / COMMUNITY / CAREER_CONNECTION
- hands_on: HIGH

Evidence:
- https://www.town.kibichuo.lg.jp/soshiki/27/16912.html
- https://npoafterschool.org/archives/blog/2026/04/49822/

Assessment:
First Passで未捕捉だったが、イベント単発より重要。
Second Passで拾うべき深さの代表例。

### B. ちびっ子チャレンジ教室 — CURRENT 2026 / PROGRAM SOURCE

令和8年度町事務事業概要:
- 通年
- 町内体験施設を活用
- 子どもの体験・交流
- 郷土愛醸成
- 小学生向け
- 5月から年6回程度

Classification:
- ELEMENTARY
- RECURRING / PROGRAM
- PARTICIPATION_SCOPE要個別募集確認
- COMMUNITY / NATURE / CREATIVE / LIFE_SKILLS等へ展開可能

Evidence:
- https://www.town.kibichuo.lg.jp/uploaded/life/19937_53114_misc.pdf

Assessment:
既存ログの「個別イベント」より上位にある年間プログラム。
これもSecond Passの適正深度。

### C. ヤングボランティア事業 — CURRENT 2026 / GROWTH ROUTE

令和8年度町事務事業概要:
- 中学生
- 5月から年10回程度
- ボランティア事業

Classification:
- STUDENT / LOCAL
- RECURRING
- COMMUNITY / CIVIC / VOLUNTEERING
- GROWTH_ROUTE候補

小学年代の体験から、中学生の社会参加へ接続する可能性がある。

Evidence:
- https://www.town.kibichuo.lg.jp/uploaded/life/19937_53114_misc.pdf

### D. 地域学校協働活動 — SYSTEM SOURCE

2026-04-14町公式:
地域学校協働活動推進員を中心に、
地域と学校が協働。
読み聞かせ、ゲストティーチャー、授業補助等を実施。

令和8年度は地域ボランティア参加人数を
50人 → 100人へ増やす目標。

Classification:
- SCHOOL_ONLY / SUPPORTING_NETWORK
- CONSTANT
- COMMUNITY / WORKS / CULTURE / SKILL_TRANSFER

Evidence:
- https://www.town.kibichuo.lg.jp/soshiki/27/19997.html

GROWgle note:
個別EVENTではなく、将来の体験ACTIVITYを生み出すNETWORK SOURCEとして保持。

## 6. New ACTIVITY but not new SOURCE

### 吉備中央町図書館 — 体験！ブッククラブ
2026-10-10
ハロウィンのおはなし会 + リース作り。
小学生以下、10名、要申込。

Evidence:
- https://www.pal.pref.okayama.jp/pal/search/searchdtl.aspx?ht=1&knd=1&pageNum=1&pageSiz=10&stdycd=14182
- https://www.town.kibichuo.lg.jp/site/kibichuolibrary/

Judgment:
図書館SOURCE自体は既知。
このACTIVITYはCURRENT inventoryには有用だが、
図書館の工作・読み聞かせを全件深掘りするのはOVERDEEP。
代表例 + 現在参加可能情報だけ保持する。

### 図書館フェスティバル
2026年も図書館フェスティバルと絵本作家ワークショップを確認。

Evidence:
- https://www.town.kibichuo.lg.jp/site/kibichuolibrary/list40-98.html

Judgment:
図書館が単なる貸出施設ではなく、継続的な体験SOURCEであることの補強材料。

## 7. Existing SOURCE current-status refresh

### 国立吉備青少年自然の家

既知SOURCEのためSOURCE新規ではない。

2026-10-07時点で確認できるCURRENT:
- 「～君たちはどう生き延びるか～防災キャンプ」
  - 2026-10-24〜25
  - 1泊2日
  - 25名程度
  - 募集中
- 「出発！きびトラベル」
  - 2026-11-07〜08
  - 1泊2日
  - 18名程度
  - 募集中

Evidence:
- https://kibi.niye.go.jp/event/detail.php?id=358
- https://kibi.niye.go.jp/event/detail.php?id=359

Judgment:
Known SOURCEは「次に参加できる機会」だけ更新する。
過去イベント全件再構築はしない。

## 8. Reverse-link findings

### 放課後NPOアフタースクール
吉備中央町アフタースクールの制度設計・運営支援。
町内の学校だけでなく、地域企業・団体・外部講師をつなぐ中間SOURCE。

### 吉備国際大学
2026年、加賀東小学校アフタースクールの国際理解教育プログラムへ学生が参加。

Evidence:
https://kiui.jp/news/

### 吉備高原学園
2026-07-01に「Project 繋 吉備中央町アフタースクール」の活動記録あり。

Evidence:
https://kibikogengakuen.ed.jp/kibilog/

Assessment:
地域教育ネットワークは
町教育委員会 → アフタースクール → 大学 / 高校 / NPO / 地域人材
という構造を持つ。
これは個別イベント検索だけでは見えない。

## 9. Depth judgment after calibration

### Too shallow
以下で止める調査:
- 「吉備中央町 子ども イベント」
- 自然の家 / 星空 / 祭りを見つけて終了
- 図書館イベントを1件見つけて図書館SOURCEの構造を見ない

これでは通年制度を落とす。

### Appropriate depth
- 自治体事務事業 / 教育委員会まで見る
- 通年PROGRAMをSOURCEとして抽出
- 参加者側 / 協力者側を1段だけ逆引き
- 現在募集中ACTIVITYを代表的に確認
- 成長ルート候補を保持

### Too deep
- 図書館の小規模工作を全年度・全件収集
- 自然の家の既知イベントを過去まで全件再整理
- 同じアフタースクールの参加団体を無限に芋づる式探索
- SOURCE価値が増えない細部確認を続ける

## 10. Calibration conclusion

Second Passでは、
**EVENT件数追加より「見落としていた制度型SOURCE / NETWORK」を発見する方が価値が高い。**

Kibi-Chuoでは既存First Passの代表資産は十分だったが、
教育委員会・事務事業・放課後領域を掘ることで、
新しい高価値SOURCEが複数見つかった。

Therefore:
Second Pass depth = APPROPRIATE when it reaches
「自治体の表面イベント → 隠れた通年制度 → 連携主体を1段逆引き」
まで。

Next calibration block:
- 早島町
- 里庄町

両地域で同じ手法を適用し、
新規SOURCE増加率が低ければ岡山南部はSATURATED_FOR_SECOND_PASSへ移行する。


## 11. Calibration field — Hayashima

### Duplicate control result

既存ログをCross-CategoryだけでなくENTRE側まで横断照合したところ、
2026年の「チャレンジ図書館員」はENTREログですでにCROSS_CATEGORYとして回収済みだった。

Therefore:
- Webで再発見しても NEW_SOURCE / NEW_ACTIVITY として二重計上しない
- Second Pass開始前の重複確認は、地域ログ1ファイルだけでなく関連カテゴリログを横断する

This is an important calibration result.

### Current detail update — 2026はやしま生涯学習まつり

既存Cross-Categoryログでは生涯学習まつり自体はWATCH済みだったが、
2026-11-01「いきいき広場」の具体内容が更新された。

Current details:
- 中央公民館ほか
- 初開催を含む複数の体験コーナー
- 中学生・一般ボランティア募集
- ロスフラワーワークショップ
- こけ玉づくり
- 子ども屋台
- 模擬店等

Evidence:
- https://www.town.hayashima.lg.jp/soshiki/syogai_gakusyu/bosyu/event/6016.html
- https://www.town.hayashima.lg.jp/soshiki/syogai_gakusyu/bosyu/event/6005.html

Judgment:
SOURCE自体は既知。
NEW_SOURCEではなく CURRENT_DETAIL_UPDATE。
個別コーナーを別イベントとして大量分割しない。

### Hayashima saturation judgment

追加探索でも主に
- 既知の図書館
- 既知の生涯学習課
- 既知の生涯学習まつり
- スポーツ / 文化イベント
へ戻る割合が高かった。

高価値の新制度型SOURCEは今回の差分探索では確認できず。

State:
**NEAR_SATURATED_FOR_SECOND_PASS**

ただし新規の通年制度・学校外ネットワークが別経路から出た場合のみ再開する。

## 12. Calibration field — Satosho

### A. さとしょう未来塾 — HIGH-VALUE SYSTEM SOURCE

里庄町の子ども・子育て支援計画および振興計画で、
教育委員会の継続施策として確認。

構成:
- 里ちゃんチャレンジ・ワールド
- 里ちゃん寺子屋

里ちゃんチャレンジ・ワールド:
- 小・中学生等
- 冒険キャンプ
- 暁天座禅
- 昔遊び
- 科学体験等
- 土日 / 長期休暇中
- 継続実施方針

里ちゃん寺子屋:
- 自学自習
- 土日 / 長期休暇
- 地域・学生ボランティアが支援
- 継続型の子どもの居場所 / 学習支援

町の振興計画では、
地域の人や地元企業の協力を得て子どもの活動機会を拡大する方針を明記。

Classification:
- SYSTEM_SOURCE
- RECURRING / MULTI_ACTIVITY
- ELEMENTARY / JUNIOR_HIGH
- COMMUNITY / STEAM / NATURE / CULTURE / LIFE_SKILLS
- LOCAL_NETWORK
- hands_on: HIGH

Evidence:
- https://www.town.satosho.okayama.jp/uploaded/attachment/9565.pdf
- https://www.town.satosho.okayama.jp/uploaded/attachment/9732.pdf
- https://www.town.satosho.okayama.jp/uploaded/attachment/9658.pdf

Assessment:
First Passでは仁科会館・ロボットコンテスト等の代表資産は取れていたが、
その上位にある「町全体の継続体験プログラムSOURCE」を十分に構造化できていなかった。

Second Passで拾うべき典型例。

### B. わくわく科学ランド＆木のおもちゃ広場＠里庄2026 — CURRENT OPENING

2026-10-07時点:
- 参加申込: 2026-10-05開始
- 締切: 2026-10-30 17:15
- ボランティアスタッフも同期間募集中

過去実績では、
児童・幼児と保護者が科学の不思議、工作、木のおもちゃ等を体験し、
小・中・高校生がボランティア側として関わった実績もある。

Classification:
- CURRENT / APPLICATION_OPEN
- CHILD / FAMILY
- STEAM / MAKING
- VOLUNTEER_GROWTH_ROUTE
- Activity under 里ちゃんチャレンジ・ワールド

Evidence:
- https://apply.e-tumo.jp/town-satosho-okayama-u/offer/offerList_initDisplayTop
- https://www.town.satosho.okayama.jp/site/kumiai/

Judgment:
個別EVENTとして有力だが、
より重要なのは上位SOURCE「さとしょう未来塾 / 里ちゃんチャレンジ・ワールド」と紐付けること。

### C. Satosho Halloween Party 2026 — CURRENT STATUS UPDATE

2026参加募集:
- 参加申込: 2026-08-19〜09-18
- ボランティア申込: 2026-08-19〜10-01
- 2026-10-07時点では双方終了

Classification:
- RECURRING候補
- CURRENT_2026 / CLOSED
- ACTIVITY
- SOURCE = 里庄町教育委員会

Evidence:
- https://apply.e-tumo.jp/town-satosho-okayama-u/offer/offerList_initDisplayTop
- https://www.town.satosho.okayama.jp/site/kumiai/

### D. Depth judgment — Satosho

Satoshoは **NOT SATURATED**。

Reason:
First Passで主要施設SOURCEは取れていたが、
教育委員会の制度型SOURCEを掘ることで、
複数ACTIVITYを束ねる継続プログラムが新規に見えた。

今後Satoshoを掘る場合は、
各小イベントを無限に拾うのではなく、
「さとしょう未来塾」の年間構成と連携主体を1段確認した時点で停止する。

## 13. Calibration result after 3 test areas

### Kibi-Chuo
Result: **DEPTH WAS INSUFFICIENT IN SYSTEM LAYER**
- 新規高価値SOURCEあり
- 通年制度 / 放課後 / 地域学校協働を追加

### Hayashima
Result: **NEAR_SATURATED**
- 再発見の多くが既知SOURCE
- 2026イベント詳細の更新は有用
- 新制度SOURCE増加率は低い

### Satosho
Result: **DEPTH WAS INSUFFICIENT IN SYSTEM LAYER**
- さとしょう未来塾 / 里ちゃんチャレンジ・ワールドを構造化
- CURRENT科学体験募集へ接続

## 14. Revised Second Pass operating rule

各自治体で必ず以下の順にする。

1. GitHub既存ログ横断照合
   - ENTRE
   - CROSS_CATEGORY
   - 地域Checkpoint
   - 個別branch
2. KNOWN_SOURCE / KNOWN_ACTIVITY / BACKLOGを抽出
3. 隠れた制度層を1回走査
   - 教育委員会
   - 子ども・子育て計画
   - 生涯学習計画
   - 事務事業
   - 放課後 / 青少年 / 地域学校協働
4. 新しいSYSTEM SOURCEが出た場合だけ1段逆引き
5. CURRENT OPEN活動を代表的に更新
6. 新規SOURCE増加が止まれば SATURATED_FOR_SECOND_PASS

Do not:
- 既知イベントを別検索語で再度1件計上する
- 小規模イベントを全件カタログ化する
- 同じSOURCEの過去年度を無期限に掘る

Goal:
**First Passの地域資産地図に、Second Passで「機会を生み続ける制度・ネットワーク層」を足す。**


## 15. Differential sweep — Tamano / Ibara / Yakage / Asakuchi

### A. 玉野市 — REGION-WIDE SYSTEM SOURCE FOUND

#### 玉野市地域子ども楽級 — HIGH-VALUE SYSTEM SOURCE

2026 current official page confirms:
- 対象: 市内小学生
- 土日: 半日程度（月1〜2回）
- 平日: 放課後〜17時
- 場所: 各地区公民館、学校、地域施設
- 内容: 体験活動・交流活動
- 地域住民、青少年育成団体、コミュニティ、PTA、ボランティア団体等が協働
- 市内全14小学校区で展開した実績あり

市の「たまのっ子育成支援事業」の中核として、
地域学校協働本部・家庭教育支援・放課後活動等と接続。

Classification:
- SYSTEM_SOURCE
- ELEMENTARY
- RECURRING / LOCAL_AREA_NETWORK
- COMMUNITY / CULTURE / SPORTS / CREATIVE / NATURE / STEAM候補
- LOCAL_PARTICIPATION
- hands_on: HIGH

Evidence:
- https://www.city.tamano.lg.jp/soshiki/35/14619.html
- https://www.city.tamano.lg.jp/soshiki/35/39421.html

Assessment:
First Passではキッズビジネスタウン・自然環境体験公園等の代表資産は取れていたが、
市域全体で継続的な体験活動を発生させる仕組みは未構造化だった。
Second Passで拾う価値が高い。

#### 玉野市地域子ども楽級「おさらい会」

2026 current:
- 希望する小学3年生
- 放課後
- 算数学習支援
- 地域ボランティアが支援
- 学習だけでなく地域交流の場

Evidence:
- https://www.city.tamano.lg.jp/soshiki/35/17903.html

Judgment:
地域子ども楽級の別枝。
独立SOURCEではなく PROGRAM_COMPONENT。

#### たまのスチューデントガイドプログラム — CURRENT GROWTH ROUTE

2026-11-08:
- 中高生
- 宇野港周辺・直島
- 英語練習
- 外国人観光客へのプレゼン / コミュニケーション
- 国際理解 + 地域創生 + 主体性育成

Classification:
- STUDENT
- CURRENT_2026
- GLOBAL / COMMUNICATION / COMMUNITY / LOCAL_IDENTITY
- OPEN/LOCAL_STUDENT program

Evidence:
- https://www.city.tamano.lg.jp/soshiki/35/58166.html

Judgment:
地域子ども楽級とは別の中高生向け成長ルート。
玉野は「小学生地域体験 → 中高生地域発信」という年齢接続が見える。

### B. 井原市 — YOUTH ACTION SYSTEM FOUND

#### ふるさと井原“夢＆志”アクション助成 — HIGH-VALUE CURRENT SOURCE

2026 current:
- 市内在住・在学・在勤の中学生、高校生、大学生等の若者（原則20代まで）
- 若者自身が発案し、主体的に企画・実践する活動を支援
- 1組あたり最大10万円
- 2026年度は10組程度想定
- 7月〜1月の各月募集
- 最終申請締切: 2027-01-22
- R6: 4申請4助成
- R7: 12申請10助成

Classification:
- OPEN_APPLICATION / LOCAL_YOUTH
- CURRENT_2026
- ENTRE / COMMUNITY / CIVIC / PROJECT_BASED_LEARNING
- YOUTH_ACTION
- hands_on: VERY_HIGH

Evidence:
- https://www.city.ibara.okayama.jp/soshiki/35/21104.html

Assessment:
これはイベントではなく、
若者が自分で活動を「作る」ための基盤。
GROWgleの成長ルートとして非常に価値が高い。

#### ふるさと井原の未来を創るひとづくり事業 — SYSTEM NETWORK

2026市長方針で拡充を確認:
- “夢＆志”アクション助成
- Team夢源
- ユースセンターいばら
- 若者のチャレンジ支援
- 地域・企業との連携
を多角的に展開。

Evidence:
- https://www.city.ibara.okayama.jp/site/mayor/19607.html
- https://www.edu.city.ibara.okayama.jp/soshiki/22/

Classification:
- SYSTEM_SOURCE
- YOUTH_NETWORK
- ENTRE / COMMUNITY / CAREER / LOCAL_IDENTITY
- GROWTH_ROUTE_CORE

#### 地域学校協働 / ひとづくりネットワーク

学校単位では、
地域土曜学習「マナボー」、地域文化伝承、読み聞かせ、学習支援等を実施する実績を確認。

Evidence:
- https://www.edu.city.ibara.okayama.jp/site/ebarasho/tiiki.html

Judgment:
SYSTEMとしては有力だがSCHOOL_ONLY色が強いため、
公開GROWgle表示より SOURCE NETWORKとして保持する。

### C. 矢掛町 — EXISTING EVENTS ABOVE A LARGER CHILD-YOUTH SYSTEM

#### 水曜日学習会 / 夏休み・土曜日学習会

町子育て支援サイトで継続制度として確認。

水曜日学習会:
- 小3〜6（塾に通っていない児童） + 中学生
- 毎週水曜
- やかげ文化センター
- 無料
- 教員OBが支援

夏休み / 土曜日学習会:
- 町内小学生
- 各地区公民館
- 年5回程度
- 地域での学習機会

Evidence:
- https://www.town.yakage.okayama.jp/kosodate/manabi/

Classification:
- LOCAL_CHILDREN
- RECURRING
- LEARNING_SUPPORT / COMMUNITY
- SYSTEM_PROGRAM

Judgment:
学習支援中心なのでGROWgleの体験価値としては中程度。
ただし地区公民館ネットワークへの入口として重要。

#### 地区公民館 — HIDDEN DISTRIBUTED SOURCE

2026の各地区公民館には、
夏休み学習会に加えて、
- 3B体操
- 習字
- 健康教室
- 竹あかりづくり
- 絵画教室
- こども食堂
等の実活動が確認できる。

Evidence:
- https://sites.google.com/yakage-kyouiku.info/kouminkan/yakage_kouminkan
- https://sites.google.com/yakage-kyouiku.info/kouminkan/kawamo
- https://kouminkan.yakage-kyouiku.info/nakagawa

Judgment:
イベントを全件回収するのはOVERDEEP。
「地区公民館ネットワーク」をSOURCEとして保持し、
代表ACTIVITYのみ残す。

#### こどもみらい学校 — RECURRING FAMILY EXPERIENCE SOURCE

2026年度も町の地域少子化対策事業として計画掲載を確認。
過去実績では、
竹を使った工作・遊び等を通じた親子交流を複数回実施。

2025年度にも開催継続が確認されており、
制度として継続性が高い。

Evidence:
- https://www.town.yakage.okayama.jp/life/info/plan.html
- https://www.pref.okayama.jp/page/1033716.html

Classification:
- FAMILY / CHILD
- RECURRING
- NATURE / CREATIVE / COMMUNITY
- LOCAL_PARENT_CHILD
- WATCH_CURRENT_DETAILS

Judgment:
既存の伝統文化体験 / 防災アウトドアとは別のSOURCE線として価値あり。
ただし2026の具体的な開催回・募集条件は別途CURRENT確認が必要。

### D. 浅口市 — CHILD ACTIVITY TO REGIONAL CLUB TRANSITION

#### 子ども体験活動教室 — EXISTING ACTIVITY, SYSTEM VALUE UPGRADED

既存ログではACTIVITYとして回収済み。

2026 official details:
- 週末を利用した継続体験
- 地域ボランティアが指導
- コーラス、和太鼓、茶道等
- 幼児〜中学生まで複数年齢

Evidence:
- https://www.city.asakuchi.lg.jp/page/10836.html

Second Pass judgment:
単発教室ではなく、
「地域ボランティアが年間で複数の子ども体験を担うSYSTEM」として格上げ。

#### 浅口市地域クラブ — NEW SYSTEM SOURCE / CURRENT 2026

2026秋から、
休日の中学校部活動を地域クラブへ展開。

目的:
- 子どもがスポーツ・文化芸術活動に継続して親しめる機会を確保
- 地域とともに健全育成
- 地域指導者が活動

2026年5月には参加生徒募集を開始。

Classification:
- JUNIOR_HIGH
- CURRENT_2026
- RECURRING / SYSTEM_SOURCE
- SPORTS / CULTURE / CREATIVE
- COMMUNITY_INSTRUCTOR_NETWORK
- GROWTH_ROUTE

Evidence:
- https://www.city.asakuchi.lg.jp/page/16736.html
- https://www.city.asakuchi.lg.jp/page/20503.html
- https://www.city.asakuchi.lg.jp/page/18975.html

Assessment:
「小学生〜中学生の子ども体験活動教室」
→「中学生の地域クラブ」
という年齢接続が見える。

## 16. Depth judgment — 4 areas

### 玉野
State: **NOT SATURATED**
Reason:
地域子ども楽級という市域SYSTEM SOURCEを新規発見。
中高生のスチューデントガイドまで成長接続あり。

### 井原
State: **NOT SATURATED**
Reason:
“夢＆志”アクション助成は高価値。
若者が参加するイベントを探す段階から、
若者が自分でプロジェクトを作る段階へ接続している。

### 矢掛
State: **PARTIALLY SATURATED**
Reason:
主要な地域資産・高校連携は既にかなり取得済み。
新規は公民館・学習会・こどもみらい学校等の制度層。
これ以上各公民館イベントを全件掘る必要はない。

### 浅口
State: **NOT SATURATED IN GROWTH-ROUTE LAYER**
Reason:
既知の天文・体験教室に加え、
2026から地域クラブという中学生向け継続SYSTEMが立ち上がっている。

## 17. Emerging conclusion

Second Passで特に価値が高いのは、
「イベントをさらに増やすこと」ではなく、
以下の3タイプを見つけること。

1. **SYSTEM SOURCE**
   - 玉野市地域子ども楽級
   - さとしょう未来塾
   - 吉備中央町アフタースクール

2. **YOUTH ACTION SOURCE**
   - 井原 “夢＆志”アクション助成
   - 若者が自分で企画・実践できる仕組み

3. **GROWTH ROUTE**
   - 小学生体験 → 中高生地域活動
   - 子ども体験活動教室 → 地域クラブ
   - 地域体験 → 若者主体プロジェクト

この層が見つかった自治体はSecond Passの追加価値が高い。

Next:
- 岡山南部の残り自治体を同じSYSTEM / YOUTH_ACTION / GROWTH_ROUTE軸で差分走査
- 新規SOURCE増加率が落ちた地域からSATURATED_FOR_SECOND_PASSへ移す


## 18. Differential sweep — Okayama / Kurashiki / Soja / Kasaoka / Akaiwa / Setouchi / Bizen

### A. 岡山市 — CITY-WIDE CHILD EXPERIENCE INFRASTRUCTURE

#### 岡山市放課後子ども教室推進事業 — HIGH-VALUE SYSTEM SOURCE

2026年度開設申請が現行で、事業継続を確認。

Structure:
- 小学校区単位
- 地域住民主体の実行委員会
- 年間最低25日
- 放課後 / 学校休業日
- 体験学習 / 交流 / 奉仕活動
- 算数、昔遊び、囲碁将棋、料理、天体観測、スポーツ、読み聞かせ、川遊び、里山、和太鼓等

Evidence:
- https://www.city.okayama.jp/kurashi/0000012923.html

Classification:
- SYSTEM_SOURCE
- RECURRING / SCHOOL_DISTRICT
- CHILD
- STEAM / NATURE / SPORTS / CULTURE / LIFE_SKILLS / COMMUNITY
- LOCAL_NETWORK

Assessment:
First Passでサイピア等の大型SOURCEは十分取得済みだったが、
市域の小学校区を基盤にした継続体験網は別レイヤーとして保持すべき。

#### 地域と学校協働活動推進事業 — SYSTEM NETWORK

2026-04-01時点:
- 28団体
- 中学校11校
- 小学校42校
- 義務教育学校1校
- 幼稚園・認定こども園20園
をカバー。

地域の高齢者、保護者、PTA、NPO、民間企業、団体等が参画。

Evidence:
- https://www.city.okayama.jp/kurashi/0000003118.html
- https://www.city.okayama.jp/kurashi/0000049325.html

Judgment:
個別ACTIVITYを全件回収するのではなく、
学校区ネットワークをSOURCE MASTERとして保持する。

State: **PARTIALLY SATURATED**
大型施設 + 地域制度の両方が見えたため、
今後は明確な新SYSTEM / YOUTH ACTIONのみ差分追加。

### B. 倉敷市 — CITY-WIDE AFTERSCHOOL NETWORK

#### 放課後子ども教室推進事業 — TOP-TIER SYSTEM SOURCE

市内60小学校区すべてで実施。
うち44小学校区は地域連携による学校支援事業と統合。

Activities:
- 読み聞かせ
- 算数
- サッカー / ニュースポーツ
- 地域祭り
- 昔遊び
- 料理
- 将棋
- 花
等。

全小学生が参加可能（未就学児・中学生も可）。
案内は学校経由。

Evidence:
- https://www.city.kurashiki.okayama.jp/kosodate/youth/1011760/1013007/1007585.html

Classification:
- SYSTEM_SOURCE
- CITY_WIDE / SCHOOL_DISTRICT
- SCHOOL_DISTRIBUTED
- RECURRING
- CROSS_CATEGORY

#### 地域学校協働活動推進事業

2026-08-17更新。
地域住民の特技・経験を学校教育へ接続。
学習支援、昔遊び、親子料理、囲碁将棋、工作、読み聞かせ、農業体験等。

Evidence:
- https://www.city.kurashiki.okayama.jp/kosodate/youth/1011760/1013007/1007584.html

Assessment:
企業枝で倉敷の企業SOURCEを深掘りしている一方、
地域本線では「学校区×地域住民」の巨大SYSTEM SOURCEとして管理する。
企業×学校接続の重複は後で統合。

State: **PARTIALLY SATURATED / NETWORK-RICH**
個別教室の全件収集はOVERDEEP。
企業枝との接続が見えた時のみ追加価値が高い。

### C. 総社市 — YOUTH ACTION SYSTEM CONFIRMED

#### 市民提案型事業 ジュニア部門 — CURRENT / RECURRING YOUTH ACTION

既存ログでSOURCE自体は確認済み。
Second Passでは2026実績と2027募集を確認。

2026採択:
- Soja Youth Summit
- 「多世代交流グラウンドゴルフDay」
- 総社高校と総社南高校の交流
- 高校生視点で地域活性化
- 多世代交流

2027年度募集:
- 12〜17歳相当
- 3人以上
- 上限10万円
- 補助率10/10
- 2026-09-25〜11-25募集

Evidence:
- https://www.city.soja.okayama.jp/soshiki/14/19970.html
- https://www.city.soja.okayama.jp/soshiki/14/23395.html

Assessment:
単なる制度存在ではなく、
実際に高校生チームが地域事業を実行する成長ルートとして機能していることを確認。

#### 学校自主防災コンソーシアムSoja — MULTI-AGE EDUCATION NETWORK

2026採択事業として、
市内の
- 中学校
- 義務教育学校
- 高校
- 大学
が連携し、防災・減災活動を推進。

Evidence:
- https://www.city.soja.okayama.jp/soshiki/14/19970.html

Classification:
- SCHOOL_NETWORK
- LIFE_SKILLS / COMMUNITY
- JUNIOR_HIGH → HIGH_SCHOOL → UNIVERSITY
- GROWTH_ROUTE

State: **HIGH MATURITY / SECOND PASS VALUE CONFIRMED**
今後はジュニア部門の新規案件と成長ルートだけWATCH。

### D. 笠岡市 — YOUTH AS PROVIDER / COMMUNITY PARTICIPANT

#### 中高生によるスマホお助け教室 — CURRENT RECURRING YOUTH ACTION

2026年7月から:
- 毎月第1・第3水曜日
- 16:00〜18:00
- 中央公民館
- 地域の中高生が高齢者へマンツーマンでスマホ支援
- 無料 / 予約不要

Evidence:
- https://www.city.kasaoka.okayama.jp/soshiki/40/72583.html

Classification:
- YOUTH_ACTION
- RECURRING
- DIGITAL / COMMUNITY / INTERGENERATIONAL
- STUDENT_AS_PROVIDER

Assessment:
「子どもが体験を受ける側」ではなく、
中高生が地域へ価値提供する成長段階。
GROWgleの成長ルート設計で重要。

#### 青少年海外交流事業

2026:
韓国固城郡の中学生16名を受入。
相互派遣・ホームステイ・文化交流を継続。

Evidence:
- https://www.city.kasaoka.okayama.jp/soshiki/9/77142.html

Classification:
- GLOBAL / COMMUNICATION
- JUNIOR_HIGH
- RECURRING_CIVIC_EXCHANGE

#### 市民活動未来づくり事業 — SUPPORTING SOURCE

市民活動団体への補助制度。
2025採択では
- 離島の子どもサッカー
- 不登校児童生徒向けプラモデル教室
- 中学生中心の地域交流 / 防災キャンプ
等の子ども向け事業を支援。

2026制度も継続。

Evidence:
- https://www.city.kasaoka.okayama.jp/soshiki/9/63095.html
- https://www.city.kasaoka.okayama.jp/soshiki/9/72171.html

Judgment:
制度自体は子ども専用ではないためSUPPORTING SOURCE。
採択案件から子ども機会を逆引きする。

State: **NOT FULLY SATURATED**
特に公民館・市民活動採択案件から新しい若者主体SOURCEが出る可能性あり。

### E. 赤磐市 — YOUTH REGIONAL REVITALIZATION PROGRAM

#### 中高生の地域活性化事業 — HIGH-VALUE YOUTH ACTION SOURCE

2026年7月にも
「中高生の地域活性化事業ボランティア募集
～赤磐市を若者の力で元気にしよう～」
を市が告知。

過年度の教育振興重点目標では、
- 地域課題を調査
- 市民と交流
- 行政と「市の課題」「まちづくり」WS
- 公民館まつり / 市イベント参加
- SDGs
- 防災学習
等を通じ、
中高生が地域で考え行動する設計が明記されている。

2026年度教育振興重点目標も継続。

Evidence:
- https://www.city.akaiwa.lg.jp/annai/sougouseisaku/hishokikaku/shisei/kouhou/houdou/13446.html
- https://www.city.akaiwa.lg.jp/material/files/group/25/jyutenmokuhyoR8.pdf

Classification:
- YOUTH_ACTION
- JUNIOR_HIGH / HIGH_SCHOOL
- COMMUNITY / CIVIC / SDGs / LIFE_SKILLS
- RECURRING

Assessment:
First Passの「あかいわジオシティ」「中学生商品開発」だけではなく、
若者を地域活性化の担い手にするSYSTEMが存在。

State: **NOT SATURATED IN YOUTH-ACTION LAYER**

### F. 瀬戸内市 — ALL-SCHOOL COMMUNITY NETWORK + REGIONAL CLUB

#### 地域学校協働活動 — CITY-WIDE SYSTEM SOURCE

瀬戸内市では2011年から一部学校で開始。
現在は全小中学校に地域学校協働本部を設置。

Activities:
- 郷土学習
- 地域課題解決
- 地域行事への参画
- 学校を核とした地域づくり

Evidence:
- https://www.city.setouchi.lg.jp/soshiki/38/2138.html

Classification:
- SYSTEM_SOURCE
- ALL_ELEMENTARY_JUNIOR_HIGH
- COMMUNITY / LOCAL_IDENTITY / CIVIC
- SCHOOL_NETWORK

#### 地域クラブ / 部活動地域展開

2026現在、社会教育課が
- 認定地域クラブ
- 参加費助成
- 地域展開基本方針
- 専用サブサイト
を運用。

Evidence:
- https://www.city.setouchi.lg.jp/soshiki/38/
- https://www.city.setouchi.lg.jp/soshiki/38/index-2.html

Classification:
- JUNIOR_HIGH
- RECURRING / SYSTEM_SOURCE
- SPORTS / CULTURE
- COMMUNITY_INSTRUCTOR_NETWORK
- GROWTH_ROUTE

#### SAMURAIアントレクラブ — EXISTING TOP YOUTH SOURCE

既存ログでSランク。
小5・6 → ENTRE入口。
地域学校協働 / 地域クラブと組み合わせると、
小学生から中学生への接続構造が見える。

State: **NETWORK-RICH / SECOND PASS VALUE HIGH**
個別学校活動を全件回収せず、全校ネットワークと代表活動を保持。

### G. 備前市 — NPO-LED YOUTH INFRASTRUCTURE

#### NPO法人 f.saloon — TOP-TIER SYSTEM SOURCE

既存ログではSランクSOURCEとして取得済み。
Second PassでSOURCE内部構造を確認。

Current activity domains:
- 体験学習
- ユースセンター
- 放課後児童クラブ
- キャリア教育
- まちづくり

Evidence:
- https://fsaloon.com/
- https://fsaloon.com/events/

#### ユースセンター網

- 放課後スペースINBase
- 校内ユースセンター
  - 備前中学校
  - 日生中学校
  - 片上高校
- 朝活サポート

10代が安心して集まり、
自分たちでプロジェクトを企画できる。

Evidence:
- https://fsaloon.com/youthcenter/

#### INBase実行委員 — YOUTH ACTION

中高生が自分たちの「やりたい」と地域ニーズの接点を探し、
地域を巻き込みながらプロジェクトを実行。
音楽祭、イルミネーション、謎解き等の実績。

Evidence:
- https://fsaloon.com/recruit/

#### キャリア教育

- 備前市だっぴ
- 中高生と地域の大人の対話
- 中高のインターン / 職業体験を地域・企業とコーディネート

Evidence:
- https://fsaloon.com/carrieredu/

Assessment:
備前では行政単独SOURCEより、
NPOが
「居場所 → 体験 → 地域活動 → キャリア → 企業」
を束ねる中間支援インフラとして機能。

State: **HIGH MATURITY / SOURCE MASTER CONFIRMED**
今後はf.saloon内部の全イベントを追わず、
CURRENT OPEN機会と新規パートナーのみ差分更新。

## 19. Okayama South — Second Pass status

Second Pass calibration / differential sweep completed for:
- 岡山市
- 倉敷市
- 総社市
- 玉野市
- 早島町
- 井原市
- 矢掛町
- 浅口市
- 里庄町
- 笠岡市
- 赤磐市
- 瀬戸内市
- 備前市
- 吉備中央町

All 14 southern municipalities now have at least one Second Pass depth judgment.

### Saturation / maturity view

#### Near saturated / high maturity
- 岡山市: PARTIALLY_SATURATED
- 倉敷市: PARTIALLY_SATURATED / NETWORK_RICH
- 総社市: HIGH_MATURITY
- 早島町: NEAR_SATURATED
- 矢掛町: PARTIALLY_SATURATED
- 備前市: HIGH_MATURITY

#### Still valuable to deepen selectively
- 玉野市: NOT_SATURATED
- 井原市: NOT_SATURATED
- 浅口市: NOT_SATURATED_IN_GROWTH_ROUTE
- 里庄町: NOT_SATURATED
- 笠岡市: NOT_FULLY_SATURATED
- 赤磐市: NOT_SATURATED_IN_YOUTH_ACTION
- 瀬戸内市: NETWORK_RICH / selective deepening
- 吉備中央町: system layer newly expanded / selective deepening

## 20. Second Pass depth rule — now validated

Across 14 municipalities, the rule is stable:

1. First Pass finds visible regional assets and representative activities.
2. Second Pass must check hidden SYSTEM sources:
   - afterschool
   - community-school collaboration
   - youth centers
   - civic grants
   - public halls
   - regional clubs
   - educational administration plans
3. If a strong SYSTEM SOURCE appears, reverse-link only one level.
4. Capture representative CURRENT opportunities.
5. Stop once searches mostly return known sources.

The most valuable new findings were often not new events, but:
- systems
- networks
- youth action infrastructure
- cross-age growth routes

This validates the calibrated depth as neither too shallow nor excessively deep.

## 21. Next

岡山南部は全面的な無差別深掘りを停止。

Next priority:
1. 岡山県北部を同じSecond Pass方式で校正
2. 南部は NOT_SATURATED 判定地域だけ、明確な新SOURCEがある時に差分更新
3. Current参加可能情報は別レイヤーで更新
4. 企業枝との重複は統合時にSOURCE relationshipとして保持


## 22. Okayama North — Second Pass block 1

Target:
- 津山市
- 勝央町
- 奈義町
- 美咲町
- 鏡野町

### A. 勝央町 — SYSTEM LAYER CONFIRMED

#### 放課後子ども教室

第3期子ども・子育て支援事業計画で2026年度も継続。
- 小学生
- 各小学校区に1クラブ、計2クラブ
- 週1回
- 地域住民の参画
- 体験 / 交流 / 学習活動

Evidence:
- https://www.town.shoo.lg.jp/uploaded/attachment/2456.pdf

#### わくわくスクール

2026住民サービス事業一覧でCURRENT確認。
- 勝央北小1〜6年
- 毎週水曜日
- 植月コミュニティセンター
- 多様な体験メニュー
- 異年齢集団
- 毎年4月募集、5月開始予定

Evidence:
- https://www.town.shoo.lg.jp/uploaded/attachment/3177.pdf

#### 地域学校協働本部

2026も学校応援ボランティア / コーディネーターを募集。
学校・家庭・地域が一体となって地域全体で子どもを育てる仕組みを運用。

Evidence:
- https://www.town.shoo.lg.jp/site/kyoiku/4774.html

Assessment:
こども起業塾だけでなく、
放課後 / 学校協働という恒常的SYSTEM SOURCEが存在。

State: **NETWORK_RICH / SELECTIVE_DEEPENING**

### B. 美咲町 — TOWN-WIDE CHILD SUPPORT SYSTEM

#### みさきスタイルこども応援事業 — TOP-TIER SYSTEM SOURCE

2026-03-02更新。
町内全地域で、
- 地域学校協働活動
- 放課後子ども教室
- 土曜日教育支援
- 家庭教育支援
を組み合わせて実施。

地域学校協働本部は町内すべての学校区に設置。

Evidence:
- https://www.town.okayama-misaki.lg.jp/kakuka/shogaigakushu/gyomu/6/2/262.html
- https://www.town.okayama-misaki.lg.jp/kakuka/shogaigakushu/3647.html

Classification:
- SYSTEM_SOURCE
- TOWN_WIDE
- SCHOOL_DISTRICT
- COMMUNITY / LEARNING / EXPERIENCE
- RECURRING

#### 子ども第三の居場所 みさキッズあさひ

2026子育て支援プランに現行掲載。
- 無料
- 遊び / 学習
- 高校生年代も相談利用可能
- 日常型居場所

Evidence:
- https://www.town.okayama-misaki.lg.jp/kakuka/kodomoegao/gyomu/3691.html

Assessment:
Wacca. Projectの若者政策参加と、
日常の地域教育 / 居場所が両方存在。
美咲町はSYSTEM密度が高い。

State: **HIGH_MATURITY / NETWORK_RICH**

### C. 奈義町 — POLICY FOUNDATION STRONG, ACTIVITY LAYER STILL OPEN

#### 奈義町こども基本条例 — SYSTEM POLICY SOURCE

2026-04-01施行。

条例は、
- こどもの意見表明
- まちづくりへの反映
- 地域活動への参画
- 自然 / 文化 / スポーツ等の体験
- 挑戦できる環境
- 多様な居場所
を町・学校・地域・事業者の協働で整えることを明記。

Evidence:
- https://www.town.nagi.okayama.jp/reiki_int/reiki_honbun/m267RG00000995.html

Classification:
- POLICY_SYSTEM_SOURCE
- CHILD_RIGHTS / CIVIC_PARTICIPATION / EXPERIENCE
- GROWTH_ROUTE_POTENTIAL

Assessment:
制度基盤は非常に強いが、
2026の具体的な「子ども社会参加プログラム」の公開導線はまだ薄い。
アート・スポーツは既知。

State: **NOT_SATURATED / POLICY_TO_ACTIVITY_GAP**

Next only:
条例を実装する具体的なこども意見反映 / 社会参加プログラムが見つかった時に昇格。

### D. 鏡野町 — POLICY / COMMUNITY SYSTEM CONFIRMED

#### 令和8年度教育基本目標

2026年度重点:
- おかやまこども応援事業
- 家庭共育支援チーム
- 地域学校協働活動
- 公民館講座
- 青年団等社会教育団体
- 中学校部活動の地域移行
を明記。

Evidence:
- https://www.town.kagamino.lg.jp/uploaded/attachment/16162.pdf

#### 第3次総合計画

2026年度開始。
基本構想は小学生・中学生・高校生の意見を反映して策定。

Evidence:
- https://www.town.kagamino.lg.jp/soshiki/2/11635.html

#### 高校生のための企業ガイダンス

2026-11-04 / 11-18。
県北高校1・2年生を対象に地域企業理解を促進。

Evidence:
- https://www.town.kagamino.lg.jp/soshiki/22/11993.html

Assessment:
政策参画 + 学校地域協働 + キャリアがつながる。
一方で公開型YOUTH ACTIONはまだ弱い。

State: **PARTIALLY_SATURATED / YOUTH_ACTION_GAP**

### E. 津山市 — SECOND PASS STILL OPEN

First Passで:
- 津山高専公開講座
- e-PROJECT
- 津山商業地域研究
- Homing
を取得済み。

今回のSYSTEM層検索では、
他4地域ほど明確な新しい市域SYSTEM SOURCEを確定できていない。

Judgment:
- 強い高専 / 高校 / 起業コミュニティの存在は既確認
- ただし市域の放課後 / 地域学校協働 / 若者参画SOURCEを追加確認する余地あり

State: **NOT_SATURATED / NEXT_BLOCK_REQUIRED**

## 23. North block 1 conclusion

### High maturity
- 美咲町
- 勝央町

### Selective / partial saturation
- 鏡野町

### Still valuable to deepen
- 奈義町: 条例→具体活動の接続
- 津山市: 市域SYSTEM層

Next:
- 津山市のSYSTEM層補完
- 真庭 / 新庄 / 美作 / 西粟倉
- 高梁 / 新見


## 24. Okayama North — Second Pass block 2 / closeout

Target:
- 津山市
- 真庭市
- 新庄村
- 美作市
- 西粟倉村
- 高梁市
- 新見市

### A. 津山市 — STRONG ECOSYSTEM, CURRENT SYSTEM VERIFICATION GAP

First Passで既確認:
- 津山高専公開講座
- e-PROJECT
- 津山商業高校 地域研究
- Homing
- 地域産業 / STEAM / ENTRE接続

津山市の教育行政には、
- 地域学校協働
- コミュニティ・スクール
- 放課後子ども教室
- つやま子ども未来塾
というSYSTEM系統の実績がある。

ただし今回、2026年度のSYSTEM全体を一括確認できる一次情報を十分に確保できなかった。

Historical official basis:
- https://www.city.tsuyama.lg.jp/common/photo/free/files/5563/202206301718350638637.pdf

Judgment:
SYSTEMの存在自体は強いが、
2026 CURRENTを確定せずに「全市で現行」とは断定しない。

State: **HIGH_POTENTIAL / CURRENT_SYSTEM_VERIFY**
Next only:
2026教育行政重点施策または現行の放課後・地域学校協働ページが見つかった時に更新。

### B. 真庭市 — DISTRIBUTED SCHOOL-COMMUNITY NETWORK + YOUTH ACTION

#### 高校生チャレンジ支援 — EXISTING CURRENT TOP SOURCE
2026-04-20更新。
探究の深掘り、社会実装、商品開発、動画制作、情報発信等を支援。
1チーム最大10万円。

Evidence:
- https://www.city.maniwa.lg.jp/soshiki/40/115867.html

#### 地域学校協働 — CURRENT LOCAL NETWORK

2026年の学校単位で、
地域学校協働活動が実際の体験へ接続していることを確認。

Example:
- 木山小「木山わくわくランド」
  - 2026-07-04
  - 校内各教室・体育館・運動場で複数体験講座
- 樫邑小
  - 地域学校協働本部
  - 紙すき等の地域体験
  - 地域と連携した郷育 / キャリア教育

Evidence:
- https://www.city.maniwa.lg.jp/pressrelease/pressrelease118208.html
- https://www.city.maniwa.lg.jp/site/kashimura-es/

Assessment:
真庭は市全体を一括したイベントSOURCEというより、
学校・地域単位の分散NETWORKと、
市の高校生チャレンジ支援を組み合わせた構造。

State: **NETWORK_RICH / SELECTIVE_DEEPENING**

Do not:
全学校の行事を無限に回収する。
代表的な地域学校協働 + 市制度をSOURCEとして保持。

### C. 新庄村 — VILLAGE-WIDE EDUCATION POLICY, PUBLIC ROUTE STILL THIN

#### ふるさと新庄学 — SYSTEM EDUCATION SOURCE

2025–2029振興計画 / 教育振興基本計画で、
全校で「ふるさと新庄学」に取り組む方針を確認。

学習対象:
- 地域
- 歴史
- 人物
- 文化
- 産業

目的:
- 主体的に社会と関わる
- 他者と課題解決
- 地域への誇り
- 学習成果の情報発信

加えて、
地域・家庭・学校が目標を共有し、
地域と一体となって子どもを育む学校への転換を明記。

Evidence:
- https://www.vill.shinjo.okayama.jp/assets/files/dai2kisinnkoukeikaku-sougousennryaku.pdf

#### 新庄村こども計画

自然環境を活かした体験活動と、
世代を越えた地域活動の機会を増やす方向を確認。

Evidence:
- https://www.vill.shinjo.okayama.jp/assets/files/20250214-070146.pdf

Assessment:
地域全体を教材化するSYSTEM思想は強い。
一方で、一般家庭が直接申し込めるCURRENT体験SOURCEはまだ薄い。

State: **NOT_SATURATED / POLICY_TO_PUBLIC_ACTIVITY_GAP**

### D. 美作市 — HIGH-MATURITY MULTI-LAYER SYSTEM

#### 地域学校協働活動 — CURRENT SYSTEM SOURCE

学校ごとに推進員を配置し、
地域ボランティアが
- 見守り
- 読み聞かせ
- 授業支援
- 体験活動
- 民話
- 部活動支援
等に参加。

Evidence:
- https://www.city.mimasaka.lg.jp/soshiki/kyouiku/shakaikyoiku/okayamakodomo/6188.html

#### 放課後子ども教室 — CURRENT

7教室。
読み聞かせ、工作、歌舞伎、囲碁、将棋等。

Evidence:
- https://www.city.mimasaka.lg.jp/soshiki/kyouiku/shakaikyoiku/okayamakodomo/houkagokodomokyousitu.html

#### 美作市地域クラブ — GROWTH ROUTE

「地域の子どもたちは、学校を含めた地域で育てる」を理念に、
中学校部活動を地域クラブへ展開。
スポーツ・文化芸術を地域住民と行う。
2025年度からモデル実施、2030年度までの段階移行を目指す。

2026夏には中学生向けスポーツ教室も実施。

Evidence:
- https://www.city.mimasaka.lg.jp/soshiki/kyouiku/gakkoukyoiku/6947.html
- https://www.city.mimasaka.lg.jp/boshu/8988.html

#### ミライサク — POST-HIGH-SCHOOL ROUTE

18〜39歳が中心でGROWgle小中高の直接対象外だが、
地域での学び・活動・課題解決を支える若者エコシステムとして保持。

2026に制度化・補助金運用。

Evidence:
- https://www.city.mimasaka.lg.jp/soshiki/seisaku/sogoseisaku/info/8995.html

Assessment:
子ども体験
→ 中学生地域クラブ
→ 高校探究
→ 18歳以降の若者地域活動
という長い成長ルートが見える。

State: **HIGH_MATURITY / GROWTH_ROUTE_RICH**

### E. 西粟倉村 — MODEL REGION / EDUCATION FIELD

#### 百年の森林教育体験プログラム — CURRENT

2026:
- 親子で学校生活 / 放課後 / 村の暮らしを体験
- 2026-11-01〜11-14枠は募集中
- 子どものみの社会教育体験も実施

Evidence:
- https://www.vill.nishiawakura.okayama.jp/wp/%E7%99%BE%E5%B9%B4%E3%81%AE%E6%A3%AE%E6%9E%97%E6%95%99%E8%82%B2%E4%BD%93%E9%A8%93%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0/

#### 学校運営協議会 — CURRENT

幼稚園・小学校・中学校合同で運営。
2026年度は、生徒自身も一緒に話し合う場を設ける予定。

Evidence:
- https://www.vill.nishiawakura.okayama.jp/wp/%E8%A5%BF%E7%B2%9F%E5%80%89%E6%9D%91%E5%AD%A6%E6%A0%A1%E9%81%8B%E5%96%B6%E5%8D%94%E8%AD%B0%E4%BC%9A/

#### あわくらたんけんクラブ — LONG-RUN PROGRAM

2000年開始。
小中学生が村の山・川・星空・キャンプ等を体験。

Evidence:
- https://www.vill.nishiawakura.okayama.jp/wp/%E3%81%82%E3%82%8F%E3%81%8F%E3%82%89%E3%81%9F%E3%82%93%E3%81%91%E3%82%93%E3%82%AF%E3%83%A9%E3%83%96/

Assessment:
西粟倉はSOURCEを個別施設に分解しすぎると実態を失う。
村そのものを
**EDUCATION_FIELD / REGIONAL_EDUCATION_ECOSYSTEM**
として扱う価値がある。

State: **MODEL_REGION / HIGH_MATURITY**

### F. 高梁市 — CITY SYSTEM + NEW JUNIOR-HIGH ROUTE

#### たかはし子ども応援事業 — TOP-TIER SYSTEM SOURCE

2026-03-24更新。
各小学校区に地域学校協働活動推進員を配置。

- コミュニティ・スクール
- 地域学校協働
- 地域住民 / 企業 / 団体
- 放課後子ども教室
を一体運用。

Evidence:
- https://www.city.takahashi.lg.jp/soshiki/38/takahashi-okayamakodomo.html

#### 第4次教育振興基本計画

2026年3月策定。
- 地域学校協働
- 放課後子ども教室
- わくわくワーク
を全市的に広げる方針。

Evidence:
- https://www.city.takahashi.lg.jp/uploaded/attachment/34315.pdf

#### ジュニハイ・ホリメ — NEW CURRENT 2026 GROWTH ROUTE

2026年10月開始。
中学校休日部活動に代わり、
- スポーツ
- 文化芸術
- 地域活動
から自分に合った活動を選ぶ。

地域団体・地域クラブを登録 / 認定する制度も整備。

Evidence:
- https://www.city.takahashi.lg.jp/site/kyouikuiinkai/jyunihaihorime.html
- https://www.city.takahashi.lg.jp/reiki_int/reiki_honbun/r052RG00001505.html

Assessment:
小学生:
放課後 / わくわくワーク / 子どもの夢事業
↓
中学生:
ジュニハイ・ホリメ
↓
高校生・学生:
ミライイノベーション / 地域PBL
という明確な年齢接続が成立。

State: **VERY_HIGH_MATURITY / GROWTH_ROUTE_CONNECTED**

### G. 新見市 — CITY-WIDE SCHOOL NETWORK

#### 生涯学習課 2026主要事業

2026 CURRENT:
- 各公民館単位で放課後子ども教室
- 市内全小中学校で地域学校協働活動本部事業
- 公民館主催事業
- 青少年育成センター
- 出張おはなし会等

Evidence:
- https://www.city.niimi.okayama.jp/soshiki/soshiki_detail/index/46.html

Classification:
- CITY_WIDE_SYSTEM_SOURCE
- ALL_ELEMENTARY_JUNIOR_HIGH
- PUBLIC_HALL_NETWORK
- RECURRING

#### 中高生地域参加 — EMERGING YOUTH ACTION

地域審議会では、
「中高生が地域のイベント等に当事者として参加する取組」を議論。
中高生自身によるイベント企画案等が検討されている。

Evidence:
- https://www.city.niimi.okayama.jp/gyosei/gyosei_detail/index/187.html

Judgment:
現時点では制度検討段階。
CURRENT OPEN ACTIVITYとしては数えず、
YOUTH_ACTION_WATCHとする。

#### Existing routes
- 新しい特産品開発プロジェクト
- ミライイノベーション・プロジェクト
- 自然体験
等と接続。

State: **HIGH_MATURITY / YOUTH_ACTION_EMERGING**

## 25. Okayama North — Second Pass final view

Second Pass depth judgment completed for all 11 northern municipalities.

### Very high / model
- 高梁市: VERY_HIGH_MATURITY / GROWTH_ROUTE_CONNECTED
- 西粟倉村: MODEL_REGION / HIGH_MATURITY
- 美作市: HIGH_MATURITY / GROWTH_ROUTE_RICH
- 美咲町: HIGH_MATURITY / NETWORK_RICH

### Mature / selective
- 勝央町: NETWORK_RICH / SELECTIVE_DEEPENING
- 真庭市: NETWORK_RICH / SELECTIVE_DEEPENING
- 新見市: HIGH_MATURITY / YOUTH_ACTION_EMERGING
- 鏡野町: PARTIALLY_SATURATED

### Still open
- 奈義町: POLICY_TO_ACTIVITY_GAP
- 新庄村: POLICY_TO_PUBLIC_ACTIVITY_GAP
- 津山市: CURRENT_SYSTEM_VERIFY

## 26. Okayama Second Pass overall conclusion

岡山県:
- 南部14自治体
- 北部11自治体
合計25自治体についてSecond Pass深度判定を完了。

### Main conclusion

First Pass:
**見えるイベント / 地域資産 / 代表SOURCEを地図化**

Second Pass:
**機会を生み続けるSYSTEM / NETWORK / YOUTH ACTION / GROWTH ROUTEを追加**

この二層構造がGROWgle調査の標準として機能することを確認。

### Saturation principle validated

深掘り停止条件:
- 異なる検索経路でも既知SOURCE中心
- 新しいSYSTEM SOURCEが出ない
- 新規情報が小イベント詳細だけになる

再開条件:
- 新制度
- 新Gateway
- 新しい年齢接続
- 新しいCURRENT OPEN機会
- 地域空白を埋める新SOURCE

### Next geographic action

岡山はSecond Passの校正地域として一旦閉じる。

Next:
**広島 Second Pass**

Priority:
1. First Pass backlog（庄原等）
2. SYSTEM SOURCE / NETWORK層
3. YOUTH ACTION
4. GROWTH ROUTE
5. Saturation判定

岡山で確立した深度をそのまま適用する。
