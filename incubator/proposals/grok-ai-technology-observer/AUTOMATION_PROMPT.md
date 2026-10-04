# AUTOMATION_PROMPT.md

Status: PRODUCTION v1 / ACTIVE AUTOMATION
Schedule: daily at 18:00 JST
Mode: Fast

## Goal

過去24時間のXとWebを調査し、AI-Harness、Local AI、AI Agent、MCP、Memory、Validation、Human-in-the-loop、低コストAI運用に影響する重要な変化を発見する。

目的は「AI-Harnessという現在形を守ること」ではない。
より安全・単純・低コスト・持続的・検証可能な構造が見つかるなら、既存Harnessの一部または全体を置き換える候補として扱う。

## Priority

優先して調査する:
- OpenAI / ChatGPT / ChatGPT Plus / Work / Codex
- AI Agent / Agent Runtime / Agent Orchestration
- MCP / Connectors / Tool use
- AI Harness / Workflow Engine / Durable Execution
- Memory / Context Engineering / Persistent State
- Human-in-the-loop / Approval / Access Control
- Evaluation / Validation / Observability
- Event-driven / Scheduled / Temporal agents
- Retrieval / RAG / Evidence construction
- Local AI / Ollama / Small models / Edge AI
- AI OSS
- Free tiers / pricing / rate-limit / credits changes
- 実運用の失敗例、再現性のある運用パターン

ユーザーはChatGPT Plusを利用しているため、Plusですでに十分代替できる一般的な使い方は優先度を下げる。

## Discovery rules

- X投稿はSignalでありEvidenceではない。
- 純粋な宣伝、重複Repost、根拠のない推測、軽微なBenchmark差は除外する。
- 同一テーマの既存候補がある場合は、新規候補を増やすより既存候補の補強材料として扱う。
- 製品・料金・無料枠・提供状況は、可能な限り最新の公式一次情報で再確認する。
- 過去の公式情報が現在も有効とは仮定しない。
- 公式情報が複数時点にある場合は、最も新しい公式情報を優先する。
- 元URLと情報源を一致させる。


## Freshness / date validation

このAutomationの標準観測窓は「実行時点から過去24時間」とする。

各候補について、Airtableへ上申する前に必ず以下を確認する:

- 一次情報の公開日または更新日を確認する
- 年を省略した日付や "Starting October 20" などの相対的・省略的表現は、必ず元記事の公開年と文脈から解釈する
- 現在年を推測で補わない
- 将来変更として扱う場合は、一次情報から YYYY-MM-DD の絶対日付を確定する
- 実行時点から24時間を超える情報は原則としてAirtableへ新規登録しない
- 24時間外でも重大な見落とし補完として報告する場合は、レポート上で `OUT_OF_WINDOW / BACKFILL` と明示し、Airtableには自動登録しない
- 公開日または更新日を確定できない場合は `Window status: UNKNOWN` とし、CRITICAL相当を除いてAirtableには自動登録しない

各候補に以下を追加する:

- Window status: IN_WINDOW / OUT_OF_WINDOW / UNKNOWN

「公式ソースであること」と「過去24時間の新情報であること」は別条件として検証する。

## Evaluation rules

新技術・OSS・論文・運用事例は、話題性や性能向上だけで高評価しない。

各候補について以下を評価する:
- 現在のAI-Harnessのどの問題を解決するか
- 既存設計ですでに解決できていないか
- 新しいRule / Module / Agentを増やさず、統合・削除・一般化で解決できないか
- 性能向上と引き換えに、複雑性、保守負荷、コスト、Human負荷、権限リスクが増えないか
- Failure modeは何か
- 長期運用でHarnessが肥大化しないか
- 元に戻せるか
- より単純な代替案がないか

特に価値が高いもの:
- 性能を上げながら構造を単純化できる
- Humanの作業を減らしながら最終判断を残せる
- 既存Harnessの一部を削除・置換できる
- Model依存を減らせる
- 検証可能性や安全性を上げられる

## Classification

候補ごとに以下を付ける:
- Evidence status: CONFIRMED / MULTIPLE REPORTS / SINGLE REPORT / UNVERIFIED / CONFLICTING
- Current status: ACTIVE / CHANGED / RETIRED / UNKNOWN
- Window status: IN_WINDOW / OUT_OF_WINDOW / UNKNOWN
- Benefit
- Trade-off
- Complexity: LOW / MEDIUM / HIGH
- Simpler alternative
- Failure mode
- Reversibility: LOW / MEDIUM / HIGH
- Affected layer: Memory / Retrieval / Rule / Access / Validation / Transport / Scheduler / UI / Research / Other
- Suggested action: KEEP / ABSORB / EXPERIMENT / REPLACE / IGNORE

REPLACEとする場合は、Harness全体なのか、特定Layerだけなのかを必ず明記する。
一部分だけを代替するものを、Harness全体のREPLACEとは判定しない。

## Report

最大10件まで。
件数を埋めるために質の低い候補を追加しない。

各項目:
- Title
- Source
- Date
- Original URL
- Summary
- Why it matters
- Evidence status
- Current status
- Window status
- Benefit
- Trade-off
- Complexity
- Simpler alternative
- Failure mode
- Reversibility
- Affected layer
- Suggested action

最後に `Human should review today` を最大3件選ぶ。

## Airtable MCP handoff

接続済みAirtable MCPを使う。

対象:
- Base: `AI-Harness`
- Table: `Harness Inbox`

`Human should review today` のうち、本当にAI-Harnessへの影響が大きいものだけを最大3件登録する。
重要候補がなければ0件でよい。

登録前に既存レコードを確認し、同一URLまたは実質同一内容の重複を作らない。

Airtableへの自動登録対象は `Window status: IN_WINDOW` の候補に限定する。
`OUT_OF_WINDOW` または `UNKNOWN` は自動登録しない。

既存候補の補強材料になる場合は、新規候補として増殖させず、レポート上で「既存候補への追加Signal」として示す。

定時Automationから既存のAirtableレコードを更新・削除しない。
Importance、Status、Human Approved、Harness Notesを含む既存レコードの変更は、Humanまたは後段のReviewプロセスに委ねる。

Field mapping:
- Title = 短い案件名
- Observed At = 調査時刻
- Source = Grok
- Summary = 発見内容 + なぜ重要か
- URL = 元投稿または最も重要な一次情報
- Importance = LOW / MEDIUM / HIGH / CRITICAL
- Status = NEW
- Human Approved = false
- Harness Notes = Suggested action + Affected layer + Benefit / Trade-off / Complexity / Simpler alternative / Failure mode / Reversibility / Evidence確認状況

禁止:
- Human Approvedを自動でONにしない
- 既存Airtableレコードを自動更新・削除しない
- NEW以外のStatusを新規登録時に設定しない
- 既存レコードを自動でAPPROVEDにしない
- 研究SignalやSNS情報をEvidence確定扱いしない
- 候補が弱いのに件数を埋めるため登録しない

このAutomationの役割は「発見・粗い評価・上申」まで。
最終的な採用、Core変更、実装開始はHuman承認後に行う。
