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
- Proposed
  / 提案中
- Reviewed
  / 確認済み
- Promoted
  / 反映済み
- Rejected
  / 採用しない
- Obsolete
  / 古くなった

---

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

---

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

反映先としては以下のようなものがあります。

- `core/ROLE.md`
- `core/RULES.md`
- `core/WORKFLOW.md`
- `memory/MEMORY.md`
- `skills/`
- `evaluation/`

---

## 6. Do Not Overfit / 過学習を避ける

A single unusual event should not automatically create a new rule.

一度だけ発生した特殊な事象から、
すぐに新しいルールを作ってはいけません。

Prefer changes that address:

以下の点に対処する変更を優先します。

- Repeated failures
  / 繰り返し発生する失敗
- Important risks
  / 重要なリスク
- Clear inefficiencies
  / 明確な非効率
- Stable patterns
  / 継続的に確認されるパターン
  
---

## 7. Lesson Quality / 教訓の質

A useful lesson should be:

有益な教訓は次のとおりである。

- Specific
  / 具体的
- Reproducible when possible
  / 可能なら再現可能
- Actionable
  / 行動に結びつく
- Relevant
  / Harnessに関係する
- Minimal
  / 必要以上に複雑でない

---

## 8. Core Principle / 基本原則

Observe → Learn → Review → Improve

観察 → 学習 → 確認 → 改善

The Harness learns from experience,
but does not rewrite itself without review.

Harnessは経験から学びます。

しかし、人間による確認なしに
自分自身の基本ルールを書き換えません。

```text
HARNESS.md
    ↓
ROLE.md       ← AIは何者か
RULES.md      ← 何を守るか
WORKFLOW.md   ← どう仕事をするか
    ↓
MEMORY.md     ← 何を長期的に覚えるか
LESSONS.md    ← 何を学び、改善候補にするか


---

## LESSON-001 Resume Brief for Human-AI Continuity / 再開時の人間とAIの連続性

- Date: 2026-09-16
- Context: Long-running collaborative projects are often resumed after many hours or days with short phrases such as "今日もよろしく", "続きをやろうか", or "再開しよう".
- What Happened: A technically correct AI can recover the project checkpoint and immediately resume the next task. However, the human collaborator may have been away from the work for many hours and may need a short reconstruction of the previous session before acting.
- Root Cause: Existing continuity design focused mainly on restoring AI context. It did not explicitly restore the human collaborator's working context.
- Lesson: Memory should not only help the AI remember. At meaningful resume points, the AI should use reliable project state to help the human remember what was accomplished, what was decided, what remains unresolved, why the work stopped, and what should happen next.
- Suggested Change: Introduce a lightweight "Resume Brief" behavior for continuing project work. When a resume-intent phrase is detected and a meaningful interruption is likely, prefer:
  1. Previous progress / 前回の進捗
  2. Decisions and verified results / 決まったこと・確認できた結果
  3. Current unresolved state / 未解決の現在地
  4. Reason for stopping when relevant / 中断理由
  5. Recommended first action / 最初に再開する作業

  For tracked projects, use the current project checkpoint/source of truth rather than relying only on conversational memory. Keep the brief short enough to restore context without becoming a full session log. After the brief, continue naturally into the work.

  This is not intended for every greeting. It applies when the wording and project context indicate resumption of ongoing work.
- Related Files: HARNESS.md, core/WORKFLOW.md, memory/MEMORY.md, projects/*
- Status: Proposed

### Design Note / 設計メモ

A useful distinction is:

- Memory = index that helps locate relevant continuity
- Project checkpoint = current source of truth
- Technical report / Git history = historical record
- Resume Brief = human-facing reconstruction of the current working context

The goal is not to simulate emotion. The goal is continuity of collaboration: the AI remembers enough to help both sides return to the same workbench.

AIが覚えているだけではなく、その記憶を人間が作業へ戻るためにも使う。
これは「情報の継続」から「協働関係の継続」へHarnessを発展させる候補である。

---

## LESSON-002 Checkpoint Brief for Constrained AI Agents / 制約のあるAIエージェントへのチェックポイント要約

- Date: 2026-09-17
- Context: During a difficult Google AI Studio debugging task, repeated broad investigation of MediaPipe initialization and large bundle files consumed substantial execution time and eventually encountered quota/overload interruptions.
- What Happened: The implementation agent repeatedly re-entered expensive investigation. Once the task was narrowed to a known checkpoint and a single question, it returned a concrete cause candidate: the model was successfully fetched into an ArrayBuffer, but STEP 6 used a separate modelAssetPath route instead of the already verified model buffer.
- Root Cause: The agent was allowed to reconstruct too much context and combine investigation, diagnosis, modification, and verification in one working turn. Platform quota/overload may also have contributed, so the Harness should not attribute all interruptions to prompt design.
- Lesson: A project checkpoint can serve a second purpose beyond human continuity: it can constrain an implementation agent's search space. For limited or unstable agents, explicitly provide the known current state and ask for only the next observable operation rather than repeatedly reconstructing project history.
- Suggested Change: When useful, provide a compact "Checkpoint Brief" containing:
  - Verified state
  - Current failure/unresolved point
  - One current objective
  - Search boundary
  - Allowed/forbidden changes
  - Stop condition

  Prefer short cycles such as: investigate one point → report → human/lead-AI review → modify one point → report → real verification. Reuse already verified evidence instead of requesting the same exploration again.
- Related Files: agents/Google-AI-Studio/HARNESS.md, core/WORKFLOW.md, projects/*
- Status: Proposed

### Design Note / 設計メモ

Resume Brief and Checkpoint Brief share the same source-of-truth philosophy but serve different collaborators:

- Resume Brief restores the human collaborator's working context.
- Checkpoint Brief reduces reconstruction and search cost for an AI collaborator.

Do not assume that changing models or prompts alone resolves platform quota or overload behavior. Record observations separately from inferred causes.

---

## LESSON-003 Agent Status Is Not Progress / エージェントの状態表示は進捗そのものではない

- Date: 2026-09-17
- Context: Google AI Studio repeatedly displayed a working state while long tasks later ended in interruption, quota, or error conditions. From the outside it was unclear whether useful work was progressing, waiting on a model/tool request, or stalled.
- What Happened: A visible status such as "Working" did not provide enough evidence to know whether the requested implementation had advanced.
- Root Cause: Interface activity indicators describe agent/session state, not necessarily completion of an observable project checkpoint.
- Lesson: Do not treat an agent's busy/working indicator as proof of progress. Judge progress by observable artifacts or verified state transitions.
- Suggested Change: For long or unreliable agent operations, define small observable checkpoints such as:
  - target file read
  - cause reported
  - exact line changed
  - file saved
  - diagnostic step passed
  - real-device result verified

  If an operation repeatedly stalls, reduce it to the smallest meaningful read/write/test action before retrying broader work.
- Related Files: agents/Google-AI-Studio/HARNESS.md, core/WORKFLOW.md, evaluation/*
- Status: Proposed

### Design Note / 設計メモ

Agent Status ≠ Progress.

This lesson is intentionally generic. The observed incident occurred in Google AI Studio, but the principle may apply to other autonomous or long-running AI agents. It should remain Proposed until repeated use confirms that the distinction improves reliability.
