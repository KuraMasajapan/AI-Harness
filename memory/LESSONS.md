# Lessons / 教訓

## 1. Purpose / 目的

Lessons record meaningful discoveries, failures, and improvements
identified through actual use of the AI-Harness.

Lessonsは、AI-Harnessを実際に使用する中で発見された
重要な問題、失敗、改善点を記録します。

Lessons are proposals for improvement, not automatic rules.

Lessonsは自動的にルールになるものではなく、
改善候補として扱います。

---

## 2. What Is a Lesson? / 教訓とは

A lesson should explain:

教訓には以下を含めます。

- What happened
  / 何が起きたか

- Why it happened
  / なぜ起きたか

- What was learned
  / 何を学んだか

- What should change
  / 何を変えるべきか

---

## 3. Lesson Format / 記録形式

```text
## LESSON-001 Title

- Date:
- Context:
- What Happened:
- Root Cause:
- Lesson:
- Suggested Change:
- Related Files:
- Status:

```

Status should be one of:
-Proposed
  / 提案中
-Reviewed
  / 確認済み
-Promoted
  / 反映済み
-Rejected
  / 採用しない
-Obsolete
  / 古くなった

## 4. Example: / 例

```## MEM-001 Example Project Decision

- Type: Decision
- Topic: Architecture
- Content: Use Markdown files as the project source of truth.
- Source: Human-approved project decision
- Confidence: High
- Last Updated: YYYY-MM-DD
- Status: Active

```
## 5. Prmotion Process / 反映プロセス

Lessons should follow this process:
レッスンは以下の流れで行います。

```
Observation
観察
    ↓
Lesson
教訓
    ↓
Review
人間による確認
    ↓
Decision
採用判断
    ↓
Promotion
必要なファイルへ反映

```

Possible destinations include:
-core/ROLE.md
-core/RULES.md
-core/WORKFLOW.md
-memory/MEMORY.md
-skills/
-evaluation/

## 6. Do Not Overfit / 過学習を避ける

A single unusual event should not automatically create a new rule.

一度だけ発生した特殊な事象から、
すぐに新しいルールを作ってはいけません。

Prefer changes that address:

-Repeated failures
  / 繰り返し発生する失敗
-Important risks
  / 重要なリスク
-Clear inefficiencies
  / 明確な非効率
-Stable patterns
  / 継続的に確認されるパターン
  
## 7. Lesson Quality / 教訓の質

A useful lesson should be:

-Specific
  / 具体的
-Reproducible when possible
  / 可能なら再現可能
-Actionable
  / 行動に結びつく
-Relevant
  / Harnessに関係する
-Minimal
  / 必要以上に複雑でない

## 8. Core Principle / 基本原則

Observe → Learn → Review → Improve

観察 → 学習 → 確認 → 改善

The Harness learns from experience,
but does not rewrite itself without review.

Harnessは経験から学びます。

しかし、人間による確認なしに
自分自身の基本ルールを書き換えません。

これで、かなり重要な4層ができました。

```text
HARNESS.md
    ↓
ROLE.md       ← AIは何者か
RULES.md      ← 何を守るか
WORKFLOW.md   ← どう仕事をするか
    ↓
MEMORY.md     ← 何を長期的に覚えるか
LESSONS.md    ← 何を学び、改善候補にするか
