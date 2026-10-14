# GROWgle — Osaka Second Pass Progress Checkpoint

Date: 2026-10-14
State: CHECKPOINT / OSAKA_SECOND_PASS_IN_PROGRESS

## Purpose

大阪府Second Passの現在地を固定し、
新規チャット / 分岐 / 再開時に同じ深度・判断基準から続行できるようにする。

First Pass:
- COMPLETE

Second Pass:
- ACTIVE
- 重点地域の差分探索を進行中
- Publication Gate導入済み
- 全件再検索はしない

---

## Read first on resume

1. `projects/GROWgle/RESEARCH_RULES.md`
2. `projects/GROWgle/PUBLICATION_SCORING.md`
3. `projects/GROWgle/OSAKA/CHECKPOINT_OSAKA_V1_2026-10-05.md`
4. `projects/GROWgle/OSAKA/CHECKPOINT_OSAKA_SECOND_PASS_2026-10-14.md`
5. 本Checkpoint

---

## Second Pass method

大阪はイベント総数が多いため、個別イベント件数を増やすことを目的にしない。

優先:
- SOURCE_MASTER
- REGIONAL_NETWORK
- INDUSTRIAL_CLUSTER
- UNIVERSITY_SOURCE
- CHILD_ACCESS
- CURRENT 2026
- PUBLICATION_SCORING

原則:
**地域資産 → 一般家庭がアクセスできるGateway**
を見つける。

---

## Publication rule

調査と公開を分離する。

### Research Layer
価値のあるSOURCE / ACTIVITYは広く保存する。

### Public Layer
一般家庭が実際に参加を検討できるものだけを掲載候補にする。

主状態:
- `PUBLIC_LIST_PRIORITY`
- `PUBLIC_LIST`
- `WATCH_PUBLIC`
- `RESEARCH_ONLY`
- `SPONSORED_ELIGIBLE`

Hard override:
- SCHOOL_ONLY
- PARTNER_ONLY
- GROUP_ONLY
- 高額専門体験
- 一般家庭が直接申込不可

は原則 `RESEARCH_ONLY`。

広告費で通常掲載へ昇格させない。
広告依頼時のみPR / Sponsor Layerで別表示を検討する。

---

## Current confirmed PUBLIC_LIST_PRIORITY examples

### Industry / WORKS
- 豊中: 大阪国際空港こども見学ツアー
- 摂津: せっつキッズファクトリー
- 池田: ダイハツ ヒューモビリティワールド
- 門真: FactorISM系工場公開
- 東大阪: モノづくり教育 / 公開ものづくりSOURCE
- 八尾: FactorISM / こども未来創造系
- 柏原: キッズ・ワークエキスポ

### Science / Nature
- 吹田: 大阪大学連携科学
- 岸和田: きしわだ自然資料館
- 貝塚: 自然遊学館 / 子ども博士育成講座
- 和泉: 森林・木工・収穫体験
- 熊取: 大学連携SOURCE

### Heritage
- 河南: 大阪府立近つ飛鳥博物館
- 藤井寺・羽曳野・堺: 古墳REGIONAL_NETWORK
- 堺: 企業による学びの応援プログラム / 歴史文化SOURCE

### Marine
- 阪南: 海・漁業体験
- 泉南: 海の生き物 / 飼育体験

---

## Current confirmed RESEARCH_ONLY examples

- 池田: ふるさと納税5万円のダイハツ特別工場見学
- 泉佐野: 1人35,000円の航空業界特別体験ツアー
- 学校単位の工場見学
- 学校限定出前授業
- GROUP_ONLY教育プログラム

These remain valuable for:
- 地域分析
- SOURCE NETWORK
- 行政 / 企業交渉
- 将来のPR / Sponsor候補

but are not normal GROWgle listings.

---

## Osaka-specific structural finding

大阪では、
**高価値だが高障壁な産業体験が多い。**

したがって
Research Value
と
Public Value
を分離する必要性が非常に高い。

有効な管理単位:

### Industrial Gateway
- 豊中
- 摂津
- 門真
- 東大阪
- 八尾
- 柏原
- 高石

### Science / Nature Gateway
- 吹田
- 岸和田
- 貝塚
- 熊取
- 和泉

### Heritage Gateway
- 堺
- 藤井寺
- 羽曳野
- 河南

### Marine Gateway
- 阪南
- 泉南

---

## Current selective gaps

### High priority remaining

#### 泉佐野
航空 / 物流資産は強い。
CURRENT flagshipは高額でResearch Only。
必要:
- 関空現地
- 低負担
- 一般家庭から直接申込可能
な子ども航空 / 物流体験。

#### 大阪狭山
狭山池博物館は2026-09-01再開。
必要:
- CURRENT hands-on
- 小中高向け公開講座
- 水 / 土木 / 歴史体験

#### 田尻
空港・海・漁業資産は強い。
必要:
- 小中高向け
- 空港 / 漁業 / 物流
- direct public access

#### 忠岡
毛布 / 繊維資産。
必要:
- 子ども向け一般公開hands-on
- 工場 / 繊維 / デザイン体験

#### 松原
広報 / 公民館SOURCEは確認済み。
必要:
- ものづくり
- 中高生
- 地域企業
の公開Gateway。

### Medium priority remaining

- 四條畷: 里山 → 小中高hands-on
- 箕面: 森林・昆虫 → より深いhands-on
- 高石: 工場公開の継続性
- 岸和田: だんじり → child access
- 和泉: 継続CURRENT
- 貝塚: 染色 / 地場産業接続の継続
- 泉南: marine events recurrence

---

## Do not over-search

大阪では以下を避ける。

- 大都市イベント一覧を無差別に件数化
- 既知SOURCE内の小イベントを全件収集
- SCHOOL_ONLYをPublic候補として増やす
- 高額体験を教育価値だけで通常掲載へ昇格
- 地域資産の存在だけで掲載判断
- 同じGatewayを別キーワードで何度も再発見する

Stopping:
異なる検索経路でも既知SOURCE中心になり、
新しいPUBLIC Gatewayが出なくなったらSecond Pass飽和。

---

## Exact next action

1. 泉佐野 — 低負担 aviation / logistics public access
2. 大阪狭山 — 狭山池 hands-on
3. 田尻 — airport / fishery direct access
4. 忠岡 — blanket / textile child access
5. 松原 — manufacturing / youth public gateway
6. 必要なら四條畷・箕面をselective補完
7. 大阪Second Pass closeout
8. 次県へ移行

---

## Current project state

- 岡山 Second Pass: COMPLETE
- 広島 Second Pass: COMPLETE
- 兵庫 Second Pass: COMPLETE_SELECTIVE
- 大阪 Second Pass: IN_PROGRESS

大阪終了後も、
全件を再探索するのではなく
新制度 / CURRENT募集 / PUBLIC access改善 / 新Gateway
のみ差分更新する。
