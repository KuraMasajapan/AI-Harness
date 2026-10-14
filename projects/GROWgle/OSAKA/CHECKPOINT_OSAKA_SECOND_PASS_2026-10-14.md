# GROWgle — Osaka Second Pass Checkpoint

Date: 2026-10-14
State: OSAKA_SECOND_PASS_ACTIVE

## Method

大阪府First Pass完了後の差分探索。

大阪ではイベント総数が多いため、以下を優先:
- SOURCE MASTER
- REGIONAL_NETWORK / INDUSTRIAL_CLUSTER
- UNIVERSITY_SOURCE
- CHILD_ACCESS
- PUBLICATION_SCORING
- CURRENT 2026 verification

公開面は `projects/GROWgle/PUBLICATION_SCORING.md` を適用。

---

## 1. 豊中市 — AVIATION + OPEN FACTORY

### 大阪国際空港こども見学ツアー — CURRENT 2026

2026-10-09更新。
対象:
豊中・池田・伊丹・川西・吹田・宝塚・箕面在住の小3〜中3。

- ANA格納庫
- 空港車両
- 運航便見送り
- 空港仕事教室
- 折り紙飛行機
- JALグランドスタッフ体験
- 格納庫 / 整備中航空機見学

無料。
一般家庭が直接申込可能。

Official:
https://www.city.toyonaka.osaka.jp/machi/kukou/kukou_topics/kodomokengaku.html

Publication:
ACCESS_GATE: PASS
ACCESS_MODE: AREA_ONLY_DIRECT
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

### とよなかオープンファクトリー2026

JAL大阪空港支店を含む企業が子ども向け工場・仕事体験を実施。
JALでは小1〜6を対象に格納庫見学 / グランドスタッフ体験。

Official:
https://www.city.toyonaka.osaka.jp/machi/sangyoushinkou/eventcampaign/openfactory2026.html

Assessment:
空港は単なる都市インフラではなく、
**航空・仕事・地域企業を一般家庭へ開くSOURCE**として確立。

State:
VERY_HIGH_MATURITY / AVIATION_WORKS_GATEWAY

---

## 2. 摂津市 — KIDS OPEN FACTORY

### せっつキッズファクトリー

市・企業・金融機関・商工会等が連携するオープンファクトリー。

目的を明示:
- 小中学生中心
- ものづくり現場を見る
- 職業を知る
- 将来の選択肢を広げる

複数企業が工場を開放。

Official:
https://www.city.settsu.osaka.jp/soshiki/seikatukannkyou/sangyoushinkouka/shoukougyou/OP/24608.html

Publication:
ACCESS_GATE: PASS when public recruitment active
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

Assessment:
First Passの「製造・物流」仮説から、
**子ども向け産業公開Gateway**へ昇格。

State:
VERY_HIGH_MATURITY / INDUSTRIAL_OPEN_FACTORY

---

## 3. 守口市 — HIGH-SCHOOL / YOUTH INDUSTRIAL ROUTE

### もりクルート事業 — CURRENT 2026

2026年度:
- ものづくり企業職場見学ツアー
- インターンシップ
- 高校等への出前授業

高校生・大学生・若者を中心に、
市内ものづくり企業を知る機会を提供。

実施期間:
2026-07-21〜2027-03-26。

Official:
https://www.city.moriguchi.osaka.jp/kakukanoannai/shiminseikatsubu/chiikishinkoka/sangyoshinkokigyoshien/jigyousyasien/3357.html

Publication:
- 高校生個人等が直接申込可能な職場見学 / internship:
  ACCESS_GATE: CONDITIONAL
  PUBLIC_STATUS: WATCH_PUBLIC
- 学校単位出前授業:
  ACCESS_GATE: FAIL
  PUBLIC_STATUS: RESEARCH_ONLY

Assessment:
小学生向けではなく、
**高校生以降の地域産業キャリア導線**として価値が高い。

State:
HIGH_MATURITY / YOUTH_INDUSTRIAL_CAREER

---

## 4. 池田市 — AUTOMOTIVE SOURCE WITH CLEAR PUBLIC / PAID SPLIT

### ダイハツ ヒューモビリティワールド — PERMANENT PUBLIC SOURCE

毎週土曜、一般見学。
- 無料
- 事前予約不要（10名以上除く）
- 子どもから大人まで
- 軽自動車の歴史 / 仕組み
- 体験型展示

Official:
https://www.daihatsu.com/jp/facilities/hw/guide/
https://www.daihatsu.com/jp/facilities/hw/

Publication:
ACCESS_GATE: PASS
ACCESS_MODE: PERMANENT_FACILITY
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

### 小学校社会科見学 / ものづくり体験

小学5年生向け学校団体見学は教育価値が高いが、
一般家庭から直接申込不可。

Publication:
ACCESS_GATE: FAIL
PUBLIC_STATUS: RESEARCH_ONLY

### ダイハツ工場見学ツアー ふるさと納税返礼品

2026:
- コペン生産工程
- 非公開車両
- 小学生以下1名無料同伴可
- 寄附額50,000円

Official:
https://www.city.ikeda.osaka.jp/furusatoikeda/oshirase/20076.html

Publication:
ACCESS_GATE: FAIL
FEE_LEVEL: HIGH
PUBLIC_STATUS: RESEARCH_ONLY
SPONSORED_ELIGIBLE: YES

Assessment:
新しいPublic Gateが明確に機能する好例。
**無料の一般見学は掲載、高額特別ツアーは通常掲載しない。**

State:
VERY_HIGH_MATURITY / AUTOMOTIVE_ACCESS_SPLIT

---

## 5. 箕面市 — FOREST SYSTEM + PUBLIC NATURE ACCESS

### オルタナの森・Minoh

青少年の自然体験・野外活動を支える制度・施設。
市内青少年団体等の利用を優先するSYSTEM SOURCE。

Official:
https://www.city.minoh.lg.jp/seishonen/kyougaku/kyougaku.html

Publication:
団体利用部分は RESEARCH_ONLY。
一般家庭向け公開企画のみ個別にPUBLIC判定。

### 箕面公園 / 昆虫資産

箕面は「日本三大昆虫生息地」と紹介される地域資産を持ち、
箕面公園昆虫館等へ接続。

Official:
https://www.city.minoh.lg.jp/sisetu/insects.html

### 滝道週末ウォーキング

毎週土曜日。
事前申込不要。
小学生以下は保護者同伴。

Official:
https://www.city.minoh.lg.jp/kenkou/syuumatsu-walking.html

Publication:
ACCESS_GATE: PASS
PUBLIC_STATUS: PUBLIC_LIST
ただし学習深度は低〜中。

### こもれび・ひろば — CURRENT 2026

2026-08〜2027-03、
小中学生の放課後居場所を西南図書館で運用。

Official:
https://www.city.minoh.lg.jp/library/seinan/komorebi.html

Assessment:
箕面は森林・昆虫資産が強いが、
GROWgle公開面では「体験プログラム」と「単なる自然利用」を区別する。

State:
HIGH_MATURITY / FOREST_SYSTEM / HANDS_ON_SELECTIVE

---

## 6. 吹田市 — UNIVERSITY + ENVIRONMENT + CITY EVENT

### 大阪大学女子学生とワクワク科学教室 — CURRENT 2026

小4〜6＋保護者。
理工系女子学生と実験、研究・進路の話。

Official:
https://www.city.suita.osaka.jp/kurashi/1018573/1018587/1018588/kagaku2026.html

Publication:
ACCESS_GATE: PASS / girls prioritized
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

### くるくるキッズ環境スクール / 紙すき等

くるくるプラザで、
施設見学・工房体験・自然観察等。

Official:
https://www.city.suita.osaka.jp/shisei/1018880/1018881/1041420/1043984/1043994.html

Publication:
個別企画ごとに PASS / PUBLIC_LIST。

### 北摂未来ライオンズフェス — CURRENT 2026

2026-11-01。
子どもの仕事体験等を実施。

Official:
https://www.city.suita.osaka.jp/shisei/1018880/1018881/1041420/1045597/1045606.html

Assessment:
吹田は
**大学 / 環境施設 / 万博公園 / 市民・企業イベント**
が複数SOURCEとして並立。

State:
VERY_HIGH_MATURITY / UNIVERSITY_ENVIRONMENT_NETWORK

---

## 7. 四條畷市 — NATURE ASSET STRONG, CHILD PROGRAM WEAK

### むろいけ園地 / 森の宝島

常設の自然・アスレチック資産。
家族利用可能。

Official:
https://www.city.shijonawate.lg.jp/site/miryoku/5589.html

2026 CURRENT検索では、
GROWgle小中高向けの強いhands-on企画より、
乳幼児・成人向け自然イベントが多くHIT。

Assessment:
地域資産は強い。
しかし
**地域資産 → 小中高向けCURRENTプログラム**
の接続が相対的に弱い。

State:
NOT_SATURATED / CHILD_PROGRAM_GAP

Publication:
常設施設はPUBLIC_LIST候補だが、
「学び・体験」価値の高い企画は別途監視。

---

## 8. 泉佐野市 — AVIATION VALUE HIGH, CURRENT PUBLIC COST GAP

### 市民参加型航空業界特別体験ツアー — 2026

小1〜高3＋保護者。
航空業界を学ぶ2日間。

ただし:
- 泉佐野市民限定
- 1組2人
- 旅行代金1人35,000円
- 東京で実施

Official:
https://www.city.izumisano.lg.jp/kakuka/koushitsu/seisaku/menu/13200.html

Publication:
ACCESS_GATE: FAIL
FEE_LEVEL: HIGH
PUBLIC_STATUS: RESEARCH_ONLY
SPONSORED_ELIGIBLE: YES

Assessment:
航空都市としての教育意図は強いが、
この企画自体はGROWgle通常掲載に向かない。

State:
HIGH_ASSET_VALUE / LOW_PUBLIC_ACCESS_FOR_CURRENT_FLAGSHIP

Next:
関空現地で低負担・直接申込可能な子ども航空 / 物流体験を優先探索。

---

## 9. 岸和田市 — NATURAL HISTORY PUBLIC SOURCE MASTER

### きしわだ自然資料館 — CURRENT 2026

年間を通じて子ども向けhands-onを継続。

Examples:
- 恐竜教室
- 古生物
- 鉱物
- 化石クリーニング
- チリメンモンスター
- 海藻
- 地学
- 干潟観察
- 生きもの観察

多くが:
- 小学生以上
- 低料金
- 一般家庭が直接申込
- 当日参加回あり

Official:
https://www.city.kishiwada.lg.jp/site/shizenshi/
https://www.city.kishiwada.lg.jp/site/shizenshi/mini202610.html

Publication:
ACCESS_GATE: PASS
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

### だんじり

2026祭礼CURRENTは確認。
一方、一般家庭の子どもが「体験者」として参加できる公式hands-on導線は今回未確定。

Official:
https://www.city.kishiwada.lg.jp/site/danjiri/

Assessment:
岸和田のPUBLIC価値は現時点では
だんじりより**自然資料館の継続型体験**が高い。

State:
VERY_HIGH_NATURE_STEAM / DANJIRI_CHILD_ACCESS_GAP

---

## 10. 和泉市 — FOREST / AGRICULTURE + ARCHAEOLOGY

### 親子森林環境学習・木工体験＆収穫体験 — CURRENT 2026

2026-10-23申込締切。
- 親子
- 森林環境学習
- 和泉市内産木材の木工
- 収穫体験

Official:
https://www.city.osaka-izumi.lg.jp/kakukano/sangyoubu/sangyosinkositu/nourin/osirase/22506.html

Publication:
ACCESS_GATE: PASS
PUBLIC_STATUS: PUBLIC_LIST_PRIORITY

### 大阪府立弥生文化博物館

体験学習を継続。
- 弥生時代の衣・食・住
- 夏休み体験
- 考古学系企画
等。

2026は一部常設展示室改修中だが、企画・体験は継続。

Official:
https://yayoi-bunka.com/
https://yayoi-bunka.com/event_category/active_learning/

Publication:
ACCESS_GATE: PASS for open programs
PUBLIC_STATUS: PUBLIC_LIST

Assessment:
和泉は
**森林・農業・木工 + 弥生文化**
という公開体験軸が明確。

State:
HIGH_MATURITY / FOREST_AGRI_ARCHAEOLOGY

---

## 11. 熊取町 — UNIVERSITY NETWORK CONFIRMED

町内4大学等との連携を2026年度も体系化:
- 大阪観光大学
- 大阪体育大学
- 京都大学複合原子力科学研究所
- 関西医療大学

Official:
https://www.town.kumatori.lg.jp/soshiki/kikaku_keiei/seisakukikaku/gyomu/kyodo_community/university/1817.html

公開講座には、
大阪体育大学の小学生向け多種スポーツ活動
「キッズボーシャーズ」等を確認。

Official:
https://www.town.kumatori.lg.jp/soshiki/kikaku_keiei/seisakukikaku/gyomu/kyodo_community/university/kumatori4daigakukoukaikouza/15315.html

Assessment:
First Passの昆虫に加え、
**大学ネットワークそのものがSOURCE MASTER**。

State:
HIGH_MATURITY / UNIVERSITY_CLUSTER

---

## Block conclusion

### PUBLIC_LIST_PRIORITY級
- 豊中: 大阪国際空港こども見学
- 摂津: せっつキッズファクトリー
- 池田: ヒューモビリティワールド
- 吹田: 大阪大学連携科学
- 岸和田: 自然資料館
- 和泉: 森林・木工・収穫体験

### PUBLIC_LIST / useful
- 箕面: 自然・昆虫・放課後SOURCE
- 熊取: 大学連携公開講座

### RESEARCH_ONLY代表
- 池田: 5万円ふるさと納税工場見学
- 泉佐野: 1人35,000円航空業界ツアー
- 学校単位の工場 / 出前授業

## Key Osaka finding

大阪Second Passでは
**「高価値だが高障壁」な産業体験が比較的多い。**

新しいPublication Gateにより、
Research価値とPublic価値を分離する必要性が兵庫以上に高い。

また、
豊中・摂津・門真・東大阪・八尾・柏原等では
企業公開 / 工場公開が地域横断で形成されている。

Future data model:
- INDUSTRIAL_CLUSTER
- PUBLIC_ACCESS_FACTORY
- SCHOOL_INDUSTRY_NETWORK
を分離して持つ価値が高い。

## Next

Priority next block:
- 高石: 臨海工業 / 防災
- 貝塚: 工芸 / 海山
- 泉南 / 阪南 / 田尻: 海 / 漁業 / 空港圏
- 忠岡: 毛布 / 繊維
- 松原: ものづくり
- 藤井寺 / 羽曳野: 古市古墳群
- 大阪狭山 / 河南: 博物館 / 古墳 / 地域文化
