# GROWgle — Public Listing Scoring v0.1

更新: 2026-10-09
State: CURRENT
目的: Research Layerに保存した候補から、GROWgle通常公開面へ載せる価値があるものだけを一貫した基準で選ぶ。

## 0. 原則

**調査対象の広さと、公開対象の広さは分ける。**

- Research Layer: 広く保存
- Public Layer: 厳選
- Sponsored Layer: 通常掲載と分離

点数が高くても、参加障壁が高いものは通常公開へ出さない。
まずAccess Gateを通し、その後Value Scoreを付ける。

---

## 1. Access Gate — 先に足切りする

### PASS
以下をすべて満たす場合、Public Value Scoreへ進む。

- 子ども本人または保護者が一般家庭として申込・参加できる
- SCHOOL_ONLY / PARTNER_ONLY / GROUP_ONLY ではない
- 特殊資格・所属条件が原則不要
- 申込方法または当日参加方法が分かる
- 料金が一般家庭向けとして現実的、または無料
- 対象年齢がGROWgle利用者に合う
- 一次情報または主催者根拠が確認できる

### CONDITIONAL
以下は `WATCH_PUBLIC` または `HUMAN_REVIEW`。

- 地域住民限定だが一般家庭から直接申込可能
- 料金水準がやや高いが体験価値も高い
- 年齢条件が狭い
- 募集方法が毎年変わる
- 直近募集は終了したが継続性が高い
- 一次情報はあるが参加条件の一部が不明

### FAIL → RESEARCH_ONLY
以下は通常公開しない。

- SCHOOL_ONLY
- PARTNER_ONLY
- GROUP_ONLY
- 会員限定
- 個別交渉必須
- 高額な専門体験
- 特殊資格 / 所属必須
- 一般家庭が直接申込できない
- 子ども向けか不明
- 一次情報が弱く、参加条件を確認できない

※ FAILでも地域分析・SOURCE把握のため保存する。

---

## 2. Public Value Score — 100点

Access GateをPASS/CONDITIONALした候補のみ採点。

### A. 参加しやすさ — 25点
- 25: 誰でも / 直接申込 / 無料〜低負担 / 手続き簡単
- 20: 地域限定だが直接申込可、負担小
- 15: 予約・抽選・保護者同伴等の条件あり
- 10: 条件が複数、料金も中程度
- 0–5: CONDITIONALぎりぎり

### B. 体験の深さ — 20点
- 20: 実際に作る・操作する・働く・調査する・発表する
- 15: 専門家と実践体験
- 10: 見学 + 一部体験
- 5: 見学 / 鑑賞中心
- 0: 情報提供のみ

### C. 地域固有性 — 20点
- 20: その地域ならではの産業・自然・文化・人に直結
- 15: 地域資産との関連が明確
- 10: 地域開催だが内容は一般的
- 5: 地域性が弱い
- 0: 地域との関係がほぼない

### D. 学び / 成長接続 — 15点
- 15: 次の年齢・専門体験・仕事・地域活動へ明確に接続
- 10: 継続参加 / 発展コースあり
- 5: 単発だが学びが明確
- 0: 接続性が弱い

### E. 継続性 / 再現性 — 10点
- 10: 通年・毎年・常設
- 7: 複数回 / 継続実績あり
- 4: 単発だが再開催見込み
- 0: 一回限り / 不明

### F. 情報信頼性 / CURRENT性 — 10点
- 10: 主催者一次情報 + 現在募集中 / 現行
- 8: 一次情報 + 直近年度
- 5: 一次情報だが次回未確定
- 2: 二次情報中心
- 0: 根拠不足

---

## 3. 公開判定

### 80–100: `PUBLIC_LIST_PRIORITY`
GROWgleの核になる高価値コンテンツ。
地域固有で、参加しやすく、体験が深い。

### 65–79: `PUBLIC_LIST`
通常掲載候補。
利用者にとって十分価値が高い。

### 50–64: `WATCH_PUBLIC`
条件改善・次回募集・料金・対象年齢などを確認してから掲載判断。

### 0–49: `RESEARCH_ONLY`
通常掲載価値は低い。
Research Layerには保存。

---

## 4. Hard Override

以下はスコアに関係なく `RESEARCH_ONLY`。

- SCHOOL_ONLY
- PARTNER_ONLY
- GROUP_ONLY
- 高額専門体験
- 一般家庭から直接申込不可
- 広告依頼なしのSPONSORED_ELIGIBLE案件

以下はスコアに関係なくHuman確認:
- 料金が「高額」か判断困難
- 子ども向けと大人向けが混在
- 宗教 / 政治 / 強い勧誘等の境界事例
- 安全面の判断が必要
- PR色が強く教育価値が不明

---

## 5. Sponsored Layer

`SPONSORED_ELIGIBLE` はPublic Value Scoreとは別管理。

主催者・企業から広告依頼があった場合のみ:
- PR / スポンサー表記
- 通常検索結果と視覚的に分離
- 料金・対象・参加条件を完全表示
- 通常掲載順位を購入できない
- 子ども向け安全基準は通常掲載と同等以上

広告費で `RESEARCH_ONLY` を `PUBLIC_LIST` に変更しない。

---

## 6. Research logに追加する最小フィールド

今後の新規候補は可能な限り以下を持つ。

- ACCESS_GATE: PASS / CONDITIONAL / FAIL
- ACCESS_MODE
- FEE_LEVEL: FREE / LOW / MODERATE / HIGH / UNKNOWN
- DIRECT_APPLICATION: YES / NO / UNKNOWN
- PUBLIC_VALUE_SCORE: 0–100
- PUBLIC_STATUS
- SPONSORED_ELIGIBLE: YES / NO
- SCORE_REASON: 1–3行

過去ログは一括再採点せず、
Second Pass / CURRENT更新時に順次付与する。

---

## 7. 重要

GROWgleの強さは情報量ではない。

**「載っているものなら、本当に子どもと参加を検討できる」**

という信頼を作ることを最優先する。
