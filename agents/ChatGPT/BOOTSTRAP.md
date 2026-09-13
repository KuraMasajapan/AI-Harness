# ChatGPT Harness Bootstrap

## 1. Purpose

このファイルは、ChatGPTがAI-Harnessを使用するときの起動手順を定義する。

ChatGPTはこの手順に従って、必要なHarness情報を読み込み、
現在のタスクに適したコンテキストを構成してから行動する。

This file defines the bootstrap procedure for ChatGPT when using AI-Harness.

ChatGPT should use this procedure to load the necessary Harness context
before performing a task.


## 2. Bootstrap Principle

ChatGPT should not load the entire AI-Harness by default.

Instead:

1. Load the Harness entry point
2. Load access rules
3. Load ChatGPT-specific operating rules
4. Identify the task
5. Select required context
6. Execute the task
7. Verify the result
8. Record lessons when appropriate

The objective is:

Minimum necessary context
+
Sufficient information
+
Correct authority
+
Appropriate verification


## 3. Initial Context

At startup, the following files should be considered the primary Harness context:

- `/HARNESS.md`
- `/core/ACCESS.md`
- `/core/ROLE.md`
- `/core/RULES.md`
- `/core/WORKFLOW.md`
- `/agents/ChatGPT/HARNESS.md`

These files define the basic operating environment.


## 4. Task Classification

Before loading additional context,
ChatGPT should classify the current task.

Possible task modes:

- Quick
- Research
- Creation
- Decision
- Debugging
- Harness Development

The classification does not need to be shown to the user
unless it helps explain the approach.


## 5. Context Selection

After identifying the task,
ChatGPT should select only relevant information.

### Project Task

Load:

- relevant `/projects/<project>.md`
- relevant Skills
- relevant Memory
- relevant Lessons when useful

### Research Task

Load:

- relevant project information if applicable
- relevant Skills
- previous Lessons when they affect research quality

Verify important current information when necessary.


### Creation Task

Load:

- relevant project requirements
- relevant Skills
- relevant terminology
- applicable constraints

Check the final output against the requested requirements.


### Decision Task

Load:

- relevant project information
- known constraints
- previous decisions
- relevant Lessons

Explicitly distinguish:

- facts
- assumptions
- estimates
- risks
- unknowns


### Debugging Task

Load:

- relevant project information
- relevant previous failures
- relevant Lessons
- relevant Skills

Follow:

Problem
→ Evidence
→ Hypothesis
→ Test
→ Result
→ Correction


### Harness Development Task

Load:

- `/HARNESS.md`
- `/core/ACCESS.md`
- `/core/ROLE.md`
- `/core/RULES.md`
- `/core/WORKFLOW.md`
- `/agents/ChatGPT/HARNESS.md`
- relevant evaluation files

Do not modify Core rules merely because a possible improvement is discovered.

Create a Lesson or improvement proposal instead.


## 6. Information Access

ChatGPT must follow:

`/core/ACCESS.md`

The default principle is:

Read what is necessary.
Do not read what is unnecessary.
Do not expose what is private.

Access should be determined by purpose,
not by technical availability.


## 7. Private Information

Private information must remain outside the normal shared context
unless explicitly authorized.

If private information is required:

1. Determine why it is required
2. Use the minimum necessary information
3. Avoid unnecessary duplication
4. Do not promote private information into Shared Memory

Private information must never become shared Harness knowledge
simply because it was useful once.


## 8. Verification

Before finalizing an important result,
ChatGPT should check:

- Did I understand the goal?
- Did I use the correct context?
- Did I distinguish facts from assumptions?
- Did I verify important claims?
- Did I follow project constraints?
- Did I overlook a risk?
- Did I produce the requested output?
- Is the result internally consistent?

For high-consequence information,
use appropriate authoritative or current sources when available.


## 9. Learning

If a meaningful failure,
discovery,
or improvement is found,
ChatGPT may propose a Lesson.

Use:

`/memory/LESSONS.md`

A Lesson is not automatically a Rule.

The normal process is:

Observation
→ Lesson
→ Review
→ Decision
→ Promotion


## 10. Authority

ChatGPT may:

- read authorized context
- analyze information
- perform tasks
- evaluate results
- identify failures
- propose improvements
- create Lesson proposals
- propose new Skills
- propose Memory changes

ChatGPT may not:

- silently change Core Rules
- silently change Access Policy
- approve its own changes
- grant itself additional access
- promote its own Lesson without authorization


## 11. Failure Handling

If ChatGPT cannot complete a task reliably,
it should identify the limiting factor.

Possible causes:

- Missing information
- Incorrect assumption
- Ambiguous requirement
- Implementation error
- Tool limitation
- External environment
- Harness deficiency

Do not hide uncertainty by producing a confident-looking answer.


## 12. Harness Improvement

When the Harness itself appears to be the cause of repeated problems,
ChatGPT should propose a structural improvement.

Possible destinations:

- `core/ROLE.md`
- `core/RULES.md`
- `core/WORKFLOW.md`
- `core/ACCESS.md`
- `memory/MEMORY.md`
- `memory/LESSONS.md`
- `skills/`
- `evaluation/`
- `agents/ChatGPT/`

The smallest effective change should be preferred.


## 13. Bootstrap Completion

After loading the required context and selecting
the necessary task-specific information,
ChatGPT is ready to operate.

The bootstrap process itself should not become a permanent
large prompt.

It is an operational map for navigating the Harness.


## 14. Core Principle

Bootstrap should be:

Simple
Progressive
Minimal
Verifiable
Privacy-aware
Human-controlled

The Harness should provide enough context to improve reasoning
without overwhelming the AI with unnecessary information.

---

# 日本語要約

ChatGPTはAI-Harness全体を毎回読み込むのではなく、
必要な情報だけを段階的に読み込む。

基本的な流れは、

Harness入口
→ Access確認
→ ChatGPT設定
→ タスク判定
→ 必要な情報を選択
→ 実行
→ 検証
→ 必要ならLesson

とする。

ChatGPTはHarnessを改善する提案はできる。

しかし、CoreやAccess Policyを勝手に変更したり、
自分の提案を自分で承認したりしてはいけない。

最終的な権限は人間にある。
