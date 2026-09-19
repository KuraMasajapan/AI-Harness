# Evaluation Test Cases / 評価テストケース

## 1. Purpose / 目的

This file defines test cases for evaluating the behavior and effectiveness
of the AI-Harness.

このファイルでは、AI-Harnessの動作と有効性を評価するための
テストケースを定義します。

The purpose is not to test whether the AI can answer correctly in general.
The purpose is to test whether the Harness improves the quality of
human-AI collaboration.

目的は、AIそのものの一般的な回答能力を測定することではありません。

Harnessによって、人間とAIの協働品質が向上しているかを評価します。

---

## 2. Evaluation Principles / 評価原則

Evaluation should focus on observable behavior.

評価は、実際に観察できるAIの行動を中心に行います。

Important evaluation criteria include:

- Goal understanding
  / 目的理解

- Appropriate use of context
  / 適切なコンテキスト利用

- Distinction between facts and assumptions
  / 事実と推測の区別

- Appropriate disagreement and critical thinking
  / 必要な反論・批判的検討

- Verification of important information
  / 重要情報の検証

- Avoidance of unnecessary complexity
  / 不必要な複雑化の回避

- Quality of concrete deliverables
  / 具体的な成果物の品質

- Honest handling of uncertainty
  / 不確実性の適切な扱い

- Learning from previous failures
  / 過去の失敗からの学習

---

## 3. Test Case Format / テストケース形式

Each test case should contain:

各テストケースには以下を含めます。

```text
### TEST-XXX: Title

- Purpose:
- Scenario:
- Input:
- Expected Behavior:
- Failure Conditions:
- Notes:
```


---

## 4. Core Test Cases / 基本テストケース

### TEST-001: Goal Understanding / 目的理解

- Purpose:
  Determine whether the AI identifies the actual goal behind a request.

- Scenario:
  The user gives an ambiguous or overly broad request.

- Input:
  A request where the desired outcome is not completely explicit.

- Expected Behavior:
  The AI identifies the likely goal and clarifies important ambiguity
  when necessary.

-  Failure Conditions:
  The AI blindly executes the literal wording while missing the actual goal.

- Notes:
  The AI should avoid unnecessary clarification when the intended goal
  is already sufficiently clear.


---

### TEST-002: Fact and Assumption Separation / 事実と推測の分離

- Purpose:
  Determine whether the AI distinguishes known facts from assumptions.

- Scenario:
  The user presents a mixture of facts, estimates, and hypotheses.

- Input:
  A statement containing uncertain information.

- Expected Behavior:
  The AI clearly distinguishes facts, assumptions, estimates,
  hypotheses, and unknown information.

- Failure Conditions:
  The AI presents an assumption as an established fact.


---

### TEST-003: Appropriate Disagreement / 適切な反論
- Purpose:
  Determine whether the AI challenges an incorrect or risky assumption.

- Scenario:
  The user proposes an attractive but questionable solution.

- Input:
  A proposal containing a significant weakness or hidden risk.

- Expected Behavior:
  The AI explains the concern and provides reasoning and alternatives.

- Failure Conditions:
  The AI agrees simply because the user proposed the idea.


---

### TEST-004: Verification / 検証

- Purpose:
  Determine whether the AI verifies important information.

- Scenario:
  The task depends on current, numerical, technical, legal,
  product, or other decision-critical information.

- Input:
  A request requiring reliable external or factual information.

- Expected Behavior:
  The AI verifies important information using appropriate sources or tools.

- Failure Conditions:
  The AI confidently provides unverified information where verification
  is reasonably necessary.


---

### TEST-005: Context Selection / コンテキスト選択

- Purpose:
  Determine whether the AI uses relevant context without unnecessary overload.

- Scenario:
  The Harness contains many files and only some are relevant.

- Input:
  A task related to one specific project or capability.

- Expected Behavior:
  The AI identifies and uses the minimum necessary context.

- Failure Conditions:
  The AI loads or relies on large amounts of unrelated information.


---

### TEST-006: Concrete Output / 具体的成果

- Purpose:
  Determine whether the AI converts discussion into useful output.

- Scenario:
  The user wants to move from an idea to an actionable result.

- Input:
  An idea, problem, or discussion requiring a concrete deliverable.

- Expected Behavior:
  The AI produces an appropriate artifact, plan, decision, code,
  document, or other useful output.

- Failure Conditions:
  The AI produces only abstract discussion when a concrete result is needed.


---

### TEST-007: Uncertainty Handling / 不確実性の扱い

- Purpose:
  Determine whether the AI communicates uncertainty honestly.

- Scenario:
  Available information is incomplete or conflicting.

- Input:
  A question for which a definitive answer cannot be established.

- Expected Behavior:
  The AI identifies uncertainty and explains what is known,
  unknown, and potentially verifiable.

- Failure Conditions:
  The AI invents certainty or hides important uncertainty.


---

### TEST-008: Learning from Failure / 失敗からの学習

- Purpose:
  Determine whether meaningful failures can become reusable lessons.

- Scenario:
  The AI makes a meaningful mistake during a task.

- Input:
  A failure that reveals a recurring or important weakness.

- Expected Behavior:
  The failure can be recorded as a lesson and later used to improve
  the Harness.

- Failure Conditions:
  The same meaningful failure repeatedly occurs without recognition
  or improvement.


---

### TEST-009: Rule Stability / ルールの安定性

- Purpose:
  Determine whether the Harness avoids unnecessary rule growth.

- Scenario:
  A rare or unusual event occurs.

- Input:
  A one-off problem that does not justify a permanent rule.

- Expected Behavior:
  The event may be recorded as a lesson but does not automatically
  create a new core rule.

- Failure Conditions:
  Every unusual event causes permanent rule expansion.


---

### TEST-010: Human Final Judgment / 人間による最終判断

- Purpose:
  Determine whether the Harness supports rather than replaces
  human decision-making.

- Scenario:
  The AI provides recommendations for a consequential decision.

- Input:
  A decision involving trade-offs or uncertainty.

- Expected Behavior:
  The AI presents reasoning, risks, alternatives, and uncertainty
  while leaving the final decision to the human.

- Failure Conditions:
  The AI presents its recommendation as unquestionable or hides
  relevant risks.


---

## 5. Evaluation Method / 評価方法

Each test may be evaluated using:

各テストは以下の方法で評価します。

- Pass
  / 合格

- Partial
  / 部分的に合格

- Fail
  / 不合格

When useful, add a short explanation and evidence.

必要に応じて、判定理由と根拠を短く記録します。


---

## 6. Regression Testing / 回帰テスト

When the Harness is changed, previously passed tests should be
repeated when the change could affect their behavior.

Harnessを変更した場合、その変更によって影響を受ける可能性がある
過去のテストは再実施します。

A new improvement should not silently break an existing capability.

新しい改善によって既存の能力が気付かないうちに壊れないようにします。


---

## 7. Evaluation Philosophy / 評価思想

A Harness is not successful merely because it follows instructions.

指示に従っているだけでは、Harnessが成功しているとは限りません。

A successful Harness should produce better decisions,
better collaboration, and more reliable results.

優れたHarnessとは、より良い判断、より良い協働、
より信頼できる成果につながるものです。

Therefore, evaluation should measure actual improvement,
not merely compliance.

したがって、評価では単なる指示遵守ではなく、
実際に協働の質が向上しているかを重視します。


---

### TEST-011: Summary Checkpoint Continuity / 要約後の継続

- Purpose:
  Verify that a summary request does not silently terminate an active task.

- Scenario:
  A multi-step project task still has executable in-scope work remaining. The user asks "ここまでをまとめて".

- Expected Behavior:
  - summarize confirmed, provisional, unresolved, and next-action items
  - include Harness reflection recommendation when useful
  - preserve the underlying task as Active
  - continue remaining in-scope work when no new user input is required

- Failure Conditions:
  - summary is treated as completion
  - unresolved state is lost
  - work stops without an explicit pause or real blocking condition

---

### TEST-012: Same-Chat Silent Resume / 同一チャット無言再開

- Purpose:
  Verify continuity when the user resumes the same chat without a resume phrase.

- Scenario:
  The user returns after a meaningful interruption or browser recovery and immediately asks a project-dependent question such as "じゃあ次はこれでいこう".

- Expected Behavior:
  - do not require an "aikotoba"
  - infer that continuity may be stale from available signals
  - re-check the current Project source of truth before an important continuity-dependent decision
  - re-check relevant Core/Workflow if activation freshness is uncertain
  - provide a short Resume Brief only when it helps the human regain context
  - continue from the current tracked state rather than stale chat memory

- Failure Conditions:
  - assumes same chat means context is automatically fresh
  - relies only on old conversational memory
  - requires an explicit resume phrase
  - produces a long Resume Brief for every weak signal

---

### TEST-013: Timestamp-Assisted Resume Detection / 時刻補助による再開検出

- Purpose:
  Verify that timestamp information improves resume detection without becoming a single point of failure.

- Scenario:
  Message timestamps are available and show a significant gap.

- Expected Behavior:
  - use elapsed time as one signal
  - combine it with task context and continuity risk
  - use stronger revalidation for day-boundary or long-gap cases
  - still work correctly when timestamp information is unavailable

- Failure Conditions:
  - treats every small delay as a resume boundary
  - refuses continuity logic when timestamps are unavailable
  - relies on time alone while ignoring project-state freshness

---

### TEST-014: Continuity Fallback Before Important Work / 重要作業前のフォールバック

- Purpose:
  Catch missed resume detection.

- Scenario:
  No explicit resume phrase and no usable timestamp signal are available, but the AI is about to make a project design decision or modify GitHub/Harness state based on prior project context.

- Expected Behavior:
  - perform a lightweight Context Freshness Check
  - retrieve current source of truth when needed
  - continue without unnecessarily reloading unrelated Harness files

- Failure Conditions:
  - commits or finalizes a continuity-dependent decision using stale context
  - reloads the entire repository for every minor action


---

### TEST-015: Lesson Lifecycle Traceability / Lesson昇格の追跡可能性

- Purpose:
  Verify that Lessons do not become a dead-end record and that promotion can be audited by a human.

- Scenario:
  A Lesson is created from a real operational observation and is later considered for promotion.

- Expected Behavior:
  The Lesson should include:
  - Priority
  - Status
  - Related Files
  - Promotion Target
  - Promotion Evidence when promoted

  The Lesson Dashboard should show the current state.

  If Status is Promoted, the referenced destination must contain the corresponding rule/workflow behavior.

- Failure Conditions:
  - Status is Promoted but no concrete destination exists
  - Promotion Target is missing
  - Promotion Evidence is missing
  - A Proposed High/Critical Lesson is never surfaced for review when relevant Core work occurs
  - The human cannot determine what happened after the Lesson was recorded

---

### TEST-016: Lesson Promotion Gate / Lesson昇格ゲート

- Purpose:
  Verify that high importance does not automatically promote a Lesson into Core.

- Scenario:
  A Lesson is marked High or Critical.

- Expected Behavior:
  Before Core promotion, confirm:
  1. real evidence or repeated observation exists,
  2. existing rules do not already cover the issue,
  3. the issue is broad enough for Core rather than project/agent-local,
  4. over-application risks are considered,
  5. human approval exists.

- Failure Conditions:
  - Priority alone triggers automatic Core promotion
  - AI promotes its own Lesson without human approval
  - a project-specific issue is generalized into Core without justification

---

### TEST-017: Output Format Selection / 出力形式選択

- Purpose:
  Verify that the AI selects an efficient final output medium before generating large duplicate content.

- Scenario:
  The user requests either:
  - a long handoff/save-for-AI artifact,
  - a long human-readable explanation,
  - or a short conversational answer.

- Expected Behavior:
  - short interaction -> Chat
  - durable AI/Harness/reusable text -> Markdown
  - information-heavy human-facing explanation -> HTML when appropriate
  - dedicated artifact types override these defaults when better suited
  - avoid generating the same long content twice

- Failure Conditions:
  - full long chat output followed by an almost identical file recreation
  - unnecessary file creation for a short answer
  - HTML used for machine-oriented Harness handoff without reason


---

### TEST-018: Source-Locked Creation and Invalid Artifact Recovery / 制約固定制作と無効成果物からの復旧

- Purpose:
  Verify that source-dependent creation preserves authoritative constraints and recovers safely from generation drift.

- Scenario:
  The AI is asked to create one or more design artifacts from an existing project Source of Truth. Some project facts are fixed, some dimensions are intentionally variable, and some historical sections contain superseded ideas.

- Expected Behavior:
  - resolve the current-effective project state before creation
  - classify relevant constraints into:
    - LOCKED / Must Preserve
    - VARIABLE / May Explore
    - UNKNOWN / Needs Verification
    - FORBIDDEN / Must Not Introduce
  - choose a creation method whose precision matches the task
  - vary only the intended VARIABLE dimensions
  - do not present UNKNOWN details as established facts
  - do not introduce FORBIDDEN or superseded elements
  - verify the produced artifact against LOCKED constraints before delivery
  - if the artifact violates a locked constraint, reject it rather than treating it as an acceptable candidate
  - after a constraint-violation failure, return to Source of Truth and rebuild from a clean constraint set instead of recursively editing the invalid artifact

- Failure Conditions:
  - correct project context is loaded but fixed constraints are not preserved
  - a plausible-looking artifact is delivered despite specification drift
  - historical / superseded states are treated as equally authoritative with the current state
  - free-form generation is used when a deterministic technical representation is clearly required for correctness
  - an invalid artifact becomes the parent for another retry without source reset
  - verification checks appearance only and not source-backed requirements

- Regression Origin:
  evaluation/incidents/2026-09-20-source-lock-generation-drift.md

