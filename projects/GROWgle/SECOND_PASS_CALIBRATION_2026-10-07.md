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
