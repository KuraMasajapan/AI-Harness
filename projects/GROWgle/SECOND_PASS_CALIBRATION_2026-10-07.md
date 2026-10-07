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
