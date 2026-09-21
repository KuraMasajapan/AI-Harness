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



## Terminology / 用語定義

このHarnessで **LESSON** と大文字で表現する場合、原則として個別のLesson記録だけではなく、以下の改善プロセス全体を指す。

```text
発見
→ 改善候補
→ 記録
→ 重要度評価
→ Review
→ 人間による判断
→ Promotion
→ Core等への反映
→ Regression Test
→ 実運用
```

`LESSON-001` のような個別項目は、このLESSONプロセスの中で扱う記録単位である。

---

## Lesson Dashboard / Lesson一覧

| ID | Priority | Status | Promotion Target |
|---|---|---|---|
| LESSON-001 | High | Promoted | core/WORKFLOW.md |
| LESSON-002 | Medium | Proposed | agents/Google-AI-Studio/HARNESS.md / core/WORKFLOW.md |
| LESSON-003 | Medium | Proposed | agents/Google-AI-Studio/HARNESS.md / evaluation/* |
| LESSON-004 | High | Promoted | core/WORKFLOW.md |
| LESSON-005 | High | Promoted | HARNESS.md / core/RULES.md / core/WORKFLOW.md / agents/ChatGPT/* |
| LESSON-006 | Medium | Promoted | core/WORKFLOW.md |
| LESSON-007 | High | Promoted | core/WORKFLOW.md / memory/LESSONS.md |
| LESSON-008 | High | Proposed | core/RULES.md / HARNESS.md / evaluation/* |
| LESSON-009 | High | Proposed | core/WORKFLOW.md |
| LESSON-010 | High | Promoted | core/WORKFLOW.md / evaluation/* |
| LESSON-011 | High | Promoted | core/RULES.md / core/WORKFLOW.md / evaluation/* |
| LESSON-012 | High | Promoted | core/RULES.md / core/WORKFLOW.md / evaluation/* |
| LESSON-013 | High | Proposed | HARNESS.md / core/WORKFLOW.md / evaluation/* |

この表は人間向けの運用状況一覧である。

- Proposed = 記録済み、まだCore化判断前
- Reviewed = 人間が確認済み、昇格判断または追加証拠待ち
- Promoted = 実際の反映先まで確認済み
- Rejected = 検討したが採用しない
- Obsolete = 後の変更等により不要になった

Priorityは重要度であり、自動昇格を意味しない。

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
- Priority: Critical / High / Medium / Low
- Promotion Target:
- Promotion Evidence:
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
```

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
- Priority: High\n- Promotion Target: core/WORKFLOW.md\n- Promotion Evidence: Continuity & Context Freshness Check / Resume Brief\n- Status: Promoted

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
- Priority: Medium\n- Promotion Target: agents/Google-AI-Studio/HARNESS.md / core/WORKFLOW.md\n- Promotion Evidence: Pending review; insufficient evidence for Core promotion\n- Status: Proposed

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
- Priority: Medium\n- Promotion Target: agents/Google-AI-Studio/HARNESS.md / evaluation/*\n- Promotion Evidence: Pending additional cross-agent observation\n- Status: Proposed

### Design Note / 設計メモ

Agent Status ≠ Progress.

This lesson is intentionally generic. The observed incident occurred in Google AI Studio, but the principle may apply to other autonomous or long-running AI agents. It should remain Proposed until repeated use confirms that the distinction improves reliability.

---

## LESSON-004 Requirements-First Component Search / 要件起点の電子部品探索

- Date: 2026-09-18
- Context: During UIAP BASE LED-output architecture research, early investigation focused on familiar solutions such as 74HC595 and well-known LED driver ICs. A highly suitable low-cost 16-channel constant-current serial LED driver (SM16206S) appeared only after the search was reframed around the functional requirements and JLCPCB/LCSC ecosystem.
- What Happened: The initial search produced technically valid candidates, but failed to surface a potentially better-fit part early. The missed candidate combined several desired properties at once: 16 outputs in one IC, constant-current LED drive, 3.3 V compatibility, low unit price, and direct relevance to JLCPCB assembly.
- Root Cause: Candidate generation was too anchored to known part numbers, well-known global manufacturers, and familiar component categories. The search did not initially perform enough requirements-first category expansion, supplier-library reverse search, regional-manufacturer discovery, or adjacent-category exploration.
- Lesson: Component research should separate **candidate generation** from **candidate verification**. Candidate generation should deliberately maximize relevant search breadth from the requirements, not from the AI's familiarity. Verification should then aggressively narrow candidates using datasheets, live stock, price, assembly compatibility, total BOM cost, and fallback paths.
- Suggested Change: For important component selection, use the following pattern:
  1. Express the need as functions and constraints rather than known part numbers.
  2. Search several adjacent component categories and synonyms.
  3. Search both manufacturer sources and the actual distributor/assembly ecosystem used by the project.
  4. Include suitable regional or less-famous manufacturers during candidate generation.
  5. Before recommending a first good candidate, perform one explicit lateral-search pass for a lower-part-count or better-integrated alternative.
  6. Compare implemented BOM cost, not IC unit price alone.
  7. Treat stock as dynamic and evaluate fallback/re-design paths.
- Related Files: core/WORKFLOW.md, projects/UIAPduino/UIAP_BASE.md
- Priority: High\n- Promotion Target: core/WORKFLOW.md\n- Promotion Evidence: Component Research Task / Search Breadth Check\n- Status: Promoted

### Design Note / 設計メモ

The failure was not that the earlier candidates were wrong. The failure was that the search space was narrowed too early.

A useful distinction is:

- Candidate generation = search broadly from requirements.
- Candidate verification = narrow aggressively using evidence.

This prevents model familiarity from becoming an unintended filter on engineering decisions.


---

## LESSON-005 Summary and Resume Continuity / 要約・中断・再開の連続性

- Date: 2026-09-19
- Context: During ongoing UIAP BASE work, the user identified two continuity risks: (1) asking for a summary can accidentally terminate unfinished work, and (2) browser recovery or returning to the same chat may not look like a fresh startup even though human working context has been interrupted.
- What Happened: Existing logic treated startup and explicit resume phrases more strongly than silent or implicit resume. The user also noted that they may resume without a trigger phrase.
- Root Cause: Continuity detection was too event-based. It depended too much on fresh-session startup or explicit resume wording rather than checking whether the working context itself was still fresh.
- Lesson: Continuity should be modeled as **Context Freshness**, not only as startup/resume commands. The system should detect likely resume boundaries from multiple signals and also perform a fallback freshness check before continuity-dependent important work.
- Suggested Change:
  1. Preserve task state across summaries.
  2. Treat same-chat continuation after meaningful interruption as a possible resume boundary.
  3. Use multiple signals: explicit resume wording, browser/absence references, available timestamps, topic return, project-state uncertainty.
  4. Do not rely on an "aikotoba" or timestamp alone.
  5. Before important project decisions, GitHub writes, or other continuity-dependent actions, re-check current Core/Workflow/Project source of truth when freshness is uncertain.
  6. Use Resume Brief only when useful to restore the human's working context; do not spam it on every message.
  7. Add regression tests for silent resume and same-chat browser recovery.
- Related Files: HARNESS.md, core/RULES.md, core/WORKFLOW.md, agents/ChatGPT/START.md, agents/ChatGPT/BOOTSTRAP.md, evaluation/TEST_CASES.md
- Priority: High\n- Promotion Target: HARNESS.md / core/RULES.md / core/WORKFLOW.md / agents/ChatGPT/*\n- Promotion Evidence: Runtime Activation & Revalidation + Preserve Task State + Context Freshness Revalidation\n- Status: Promoted

### Design Note / 設計メモ

The continuity model is:

```text
Startup
Resume phrase
Browser recovery
Long pause
Topic return
Important continuity-dependent action
        ↓
Context Freshness Check
        ↓
Reload only what is needed
        ↓
Resume Brief when useful
        ↓
Continue task state
```

The fallback check before important work protects against missed resume detection.


---

## LESSON-006 Output Format Selection / 成果物形式を先に選ぶ

- Date: 2026-09-19
- Context: The user repeatedly found that long answers were easier to use as files. AI/Harness handoffs were best as Markdown, while information-heavy human-facing explanations would be easier to read as HTML. Producing the full answer in chat first and then rebuilding it as a file created duplicate work.
- What Happened: Output format was often decided only after the content had already been generated.
- Root Cause: The Workflow focused on content quality but did not explicitly choose the final delivery format before generation.
- Lesson: Select the output medium as part of planning. Use Chat for short interaction, Markdown for durable AI/Harness/reusable text, and HTML for information-heavy human-readable explanations when no more suitable dedicated format is requested.
- Suggested Change: Add Output Format Selection to Core Workflow and avoid generating the same long content twice.
- Related Files: core/WORKFLOW.md
- Priority: Medium
- Promotion Target: core/WORKFLOW.md
- Promotion Evidence: Output Format Selection / 出力形式の選択
- Status: Promoted


---

## LESSON-007 Lesson Promotion Needs Traceability / Lesson昇格には追跡可能性が必要

- Date: 2026-09-19
- Context: The user could follow the process up to adding items to LESSONS.md, but could not easily tell what happened afterward, whether importance was reconsidered, or whether a Lesson had actually reached Core.
- What Happened: Some Lessons were Promoted and others remained Proposed, but there was no compact dashboard, no explicit Priority field, and no requirement to record concrete promotion evidence.
- Root Cause: The Harness defined a conceptual Observation → Lesson → Review → Decision → Promotion flow, but did not operationalize review triggers or human-visible traceability.
- Lesson: A Lesson lifecycle needs observable state, review triggers, and evidence of the actual destination. Status=Promoted alone is insufficient.
- Suggested Change: Add Priority, Promotion Target, Promotion Evidence, a Lesson dashboard, review triggers, and a promotion gate to Core Workflow.
- Related Files: core/WORKFLOW.md, memory/LESSONS.md, evaluation/*
- Priority: High
- Promotion Target: core/WORKFLOW.md / memory/LESSONS.md
- Promotion Evidence: Lesson Review & Promotion Lifecycle / Lesson Dashboard
- Status: Promoted


---

## LESSON-008 External Permission Gate as Independent Human-Approval Layer / 外部Permission Gateを独立した人間承認層として利用する

- Date: 2026-09-19
- Context: While ChatGPT attempted to update `core/RULES.md` on the GitHub `development` branch, the GitHub integration displayed a permission warning to the human before allowing the write. The warning detected that the target content included instructions affecting AI behavior, such as priorities, continuation behavior, notifications, and decision criteria.
- What Happened: The Harness already requires human approval before Core-level self-modification. Independently, the external GitHub integration also inserted a human-facing approval gate before the write could proceed.
- Root Cause / Structural Observation: Files that govern AI behavior can resemble prompt-injection or self-modification instructions to an external safety layer. This can cause the platform/tool boundary to require explicit human authorization even when the change is intentional.
- Lesson: An external tool's permission gate can serve as a second, independent human-approval layer around Harness self-modification. This is valuable because the approval mechanism is outside the Harness itself and therefore does not rely solely on the AI obeying its own internal rules.
- Suggested Change:
  1. Treat external write-permission prompts as a potential safety feature rather than merely friction when modifying Core/Harness behavior.
  2. Prefer per-action or narrowly scoped authorization for Core/Harness changes when practical.
  3. Do not assume this behavior is universal across tools or future platform versions.
  4. If repeated observations confirm reliable behavior, consider formalizing an "External Approval Gate" as defense-in-depth for Core modification.
  5. Add a regression/evaluation case if this becomes part of the approved architecture.
- Related Files: core/RULES.md, HARNESS.md, evaluation/*
- Priority: High
- Promotion Target: core/RULES.md / HARNESS.md / evaluation/*
- Promotion Evidence: Pending repeated observation and human review
- Status: Proposed

### Design Note / 設計メモ

This creates a potentially valuable defense-in-depth pattern:

```text
Harness internal rule:
AI must not silently rewrite Core
        +
External integration permission gate:
Human must explicitly authorize the write
        =
Independent dual approval
```

The important property is **independence**. A safety control outside the Harness can protect against failures in the Harness's own self-governance.

However, one observed approval prompt is not enough to claim that every Core write will always be intercepted. This Lesson should remain Proposed until repeated use confirms the behavior and its scope.


---

## LESSON-009 Runtime Activation Is Distinct from Rule Existence / ルールの存在と実行時発火は別物

- Date: 2026-09-20
- Context: Latent Risk Scan V0.1 passed controlled high-risk / low-risk tests, but later real project work showed that relevant Latent Risk Scan context could already be available while the AI still failed to recall or trigger it until the human explicitly pointed to the hidden-risk topic.
- What Happened: The capability and its rationale existed, and relevant context was present, but the AI did not autonomously invoke the capability at the moment it was needed.
- Root Cause: The Harness still has a gap between declarative knowledge and runtime activation. A rule or capability can exist in a file, be available in context, and still fail to affect action because no sufficiently reliable trigger / recall / routing path activates it during the task.
- Lesson: Treat these as separate states:
  1. Rule or capability exists.
  2. It is available in current context.
  3. It is recalled for the current task.
  4. It is triggered.
  5. It changes the action or decision.
  
  Passing one state does not prove the next.
- Suggested Change:
  1. For capabilities that must operate at specific risk boundaries, define a minimal runtime trigger in the workflow rather than relying on file presence alone.
  2. Keep the trigger narrow enough that low-risk work is not blocked.
  3. For Latent Risk Scan, candidate trigger conditions include permission expansion, new or materially expanded external actions, Core / Source of Truth changes, and other high-impact or difficult-to-reverse operations.
  4. When triggered, ask only the minimal pre-failure questions needed to expose assumptions, failure consequences, and missing detection / verification / enforcement layers.
  5. Do not infer reliable activation merely because the rule was loaded once or because the model can explain it when prompted.
- Related Files: core/WORKFLOW.md, HARNESS.md, experiments/latent-risk-scan/*
- Priority: High
- Promotion Target: core/WORKFLOW.md
- Promotion Evidence: Controlled Latent Risk Scan Test A/B PASS + exploratory runtime activation-path finding + real-world Context-present / self-trigger-absent observation
- Status: Proposed

### Design Note / 設計メモ

The operational chain should be evaluated explicitly:

```text
Rule exists
    ↓
Available in context
    ↓
Recalled for this task
    ↓
Triggered
    ↓
Affects action
```

A failure can occur at any transition.

The purpose of this Lesson is not to make every rule constantly active. The goal is to identify which capabilities require a reliable activation path and to keep those paths minimal, observable, and proportionate to risk.


---

## LESSON-010 Source-Locked Creation / 制作物では確定仕様を固定する

- Date: 2026-09-20
- Context: During UIAP BASE PCB rough-placement exploration, several image-generation attempts materially drifted from project specifications even though the relevant project Source of Truth had already been loaded. A later re-check confirmed that several omitted requirements were explicitly present in `UIAP_BASE.md`, so the incident cannot be explained primarily by missing project documentation.
- What Happened: The generated artifacts silently changed fixed facts and invented unapproved details. Examples included replacing the intended UIAPduino CH32V003 V1.4 with an ESP32-like board, altering GPIO / LED counts and geometry, misrepresenting socket and connector structures, introducing unapproved power / USB details, and failing to create meaningfully distinct layout alternatives. After an initial bad result, a later retry edited the flawed artifact instead of resetting to the authoritative source.
- Root Cause:
  1. **Leading hypothesis: Constraint Handoff Loss.** Important source-backed relations, prohibitions, and spatial constraints appear to have lost fidelity or priority between ChatGPT's retrieved project context and the image-generation execution context. This is not yet proven and requires controlled testing.
  2. The existing Physical Grounding Check prevented some logical-to-physical inference errors, but did not explicitly compile current source information into an execution contract.
  3. The creation workflow did not separate fixed constraints from intentionally variable dimensions.
  4. Tool selection did not sufficiently consider that free-form image generation naturally invents plausible visual detail when the task actually requires constrained technical layout exploration.
  5. Verification did not compare the artifact against fixed constraints before delivery.
  6. Failure recovery did not require a reset to Source of Truth after a constraint-violation failure.
  7. Long-lived project files may contain superseded historical states, so "source loaded" is not equivalent to "current-effective constraints resolved." This is a secondary risk, not a sufficient explanation for the observed loss of constraints that were explicitly documented.
- Lesson: For creation tasks that depend on an existing Source of Truth, correctness requires a closed constraint loop, not merely context availability. The AI must distinguish four states: the constraint exists in the source, it has been retrieved, it has been handed across the creation-tool boundary, and it is actually enforced in the produced artifact. The AI should compile current-effective constraints before creation, choose a tool appropriate to the required precision, verify the artifact before delivery, and discard invalid artifacts rather than recursively editing specification drift.
- Suggested Change:
  1. Before source-dependent creation, identify:
     - **LOCKED / Must Preserve** — current authoritative facts that must not change.
     - **VARIABLE / May Explore** — dimensions intentionally open to variation.
     - **UNKNOWN / Needs Verification** — unresolved details that must not be presented as confirmed.
     - **FORBIDDEN / Must Not Introduce** — rejected, superseded, or unapproved elements.
  2. Resolve current-effective state when the source contains historical or superseded sections.
  3. Pass the compiled constraint set into the creation step.
  4. Treat **handoff fidelity** as a separate verification target:
     - confirm that relational constraints, prohibitions, counts, identity constraints, and spatial intent are included in the creation contract;
     - do not assume that information available to the reasoning context automatically reaches the creation tool with equal fidelity or priority;
     - when diagnosing failure, distinguish Source Missing, Retrieval Missing, Handoff Missing, Enforcement Failure, and Verification Failure.
  5. Perform a **Tool Fit Check**:
     - use deterministic diagrams / SVG / CAD-like methods when geometric or structural precision matters;
     - use image generation primarily when visual exploration is the goal and the locked structure can still be preserved.
  6. After creation, run an **Artifact Gate** against LOCKED and FORBIDDEN constraints before delivery.
  7. If the artifact violates locked constraints, reject it and return to Source of Truth. Do not use the invalid artifact as the default base for further editing.
  8. For serious source-locked failures, run a controlled handoff experiment before declaring the root cause fixed.
  9. Keep the process lightweight for standalone creative work that has no authoritative source constraints.
- Related Files: core/WORKFLOW.md, evaluation/TEST_CASES.md, evaluation/incidents/2026-09-20-source-lock-generation-drift.md, projects/UIAPduino/UIAP_BASE.md, projects/UIAPduino/UIAPduino.md, experiments/latent-risk-scan/candidates/01-operationalization-gap.md
- Priority: High
- Promotion Target: core/WORKFLOW.md / evaluation/*
- Promotion Evidence: Repeated UIAP BASE image-generation deviations + explicit human review + incident analysis + regression test added on 2026-09-20.
- Status: Promoted

### Design Note / 設計メモ

The minimal closed loop is:

```text
Current effective Source of Truth
        ↓
Constraint Compile
LOCKED / VARIABLE / UNKNOWN / FORBIDDEN
        ↓
Handoff Contract
verify what must cross the tool boundary
        ↓
Tool Fit Check
        ↓
Create
        ↓
Artifact Gate
        ↓
PASS → Deliver
FAIL → Reject → Source Reset
```

This lesson is adjacent to, but not identical with, the Operationalization Gap candidate.

The relevant operational failure is:

```text
Correct constraints exist
        ↓
constraints are available
        ↓
constraints are not enforced through creation
        ↓
artifact drifts
        ↓
verification fails to stop delivery
```

This incident demonstrates a more precise chain:

> **Exists in Source ≠ Retrieved ≠ Handed Off ≠ Enforced ≠ Verified**

The current unresolved root-cause question is the boundary between **Retrieved** and **Handed Off**.

### Controlled Evidence — 2026-09-20

A clean-room comparison provided behavioral support for the handoff hypothesis.

- Source-driven generation without a strongly explicit attribute contract produced:
  - CH32V003F4P6 instead of F4U6
  - too many through holes instead of 24
  - four mounting holes instead of three
  - generic Arduino-like invented details
- A second clean-room generation with explicit anchors for F4U6, exactly 24 through holes, exactly three mounting holes, USB-C, white PCB, and forbidden substitutions materially improved preservation of those discrete attributes.
- The second result still used an inaccurate generic physical package / component layout.

Current interpretation:

> Explicit handoff packaging improves discrete attribute retention, but deeper structural / relational fidelity remains an open problem.

Therefore LESSON-010 should not be considered fully validated merely because LOCKED constraints are written down. The next research target is **structure-preserving handoff**, including deterministic intermediate representations, reference geometry, or other public methods that can carry exact spatial relationships into image generation.



---

## LESSON-011 Ambiguous Source State Is Unknown / 曖昧なSource状態は不明である

- Date: 2026-09-20
- Context: Long-running Project Markdown accumulated candidate, freeze, decision, open-item, and historical records. In UIAP BASE work this repeatedly created situations where information existed but the AI either reopened a settled issue or risked choosing one interpretation from ambiguous records.
- What Happened: The failure pattern was broader than a single component. The Project source mixed current state and historical state in a way that sometimes required interpretation. The AI attempted to resolve state from available records instead of first asking whether the source itself was unambiguous.
- Root Cause:
  1. Context Freshness focused on retrieving current files, not on detecting whether the retrieved Markdown had become structurally ambiguous.
  2. Current specification and decision history were accumulated in the same document hierarchy.
  3. Historical candidate wording sometimes remained visually active after later decisions.
  4. The workflow encouraged current-effective-state resolution but did not clearly say that unresolved ambiguity must remain UNKNOWN and return to the human.
- Lesson: **Ambiguous source state is itself unknown information.** If explicit markers and current user instruction do not make the current state unique, the AI must not infer a winner. It should explain the ambiguity, ask the human to confirm the correct state, and then normalize the Markdown so the same ambiguity does not recur.
- Suggested Change:
  1. Add a Source-State Ambiguity Gate after Source retrieval.
  2. Resolve automatically only when explicit Current / Final / Frozen / Superseded evidence is unambiguous.
  3. Otherwise mark HUMAN CONFIRMATION REQUIRED and ask the user.
  4. After human resolution, strike misleading old text and mark it SUPERSEDED / HISTORICAL with a replacement reference.
  5. Prefer a Markdown structure separating Current Effective Specification, Current Open Items, and Decision History where practical.
- Related Files: core/RULES.md, core/WORKFLOW.md, evaluation/TEST_CASES.md, projects/UIAPduino/UIAP_BASE.md
- Priority: High
- Promotion Target: core/RULES.md / core/WORKFLOW.md / evaluation/*
- Promotion Evidence: explicit human review + Source-State Ambiguity Gate + TEST-007 expansion
- Status: Promoted

---

## LESSON-012 Explicit Delegation Must Be Distinguished from Uncertainty / 明示的委任と不確定を分離する

- Date: 2026-09-20
- Context: Product design work mixed confirmed specifications, undecided choices, AI-discretion choices, and accuracy-blocking unknowns. This created two opposite risks: asking the human to repeat settled choices, or silently filling undecided details during image generation / design / GitHub writes.
- What Happened: Existing rules distinguished LOCKED and UNKNOWN, and later added ambiguous-source handling, but they did not clearly encode whether an undecided item had actually been delegated to the AI.
- Root Cause: `Unknown` and `AI may decide` are different states, but the Harness did not have an explicit delegation state or a pre-output gate tied to it.
- Lesson: For source-dependent design work, distinguish at least:
  1. CONFIRMED / LOCKED
  2. DELEGATED / PROVISIONAL
  3. UNRESOLVED / CONFIRMATION REQUIRED
  Explicit phrases such as `任せる`, `一任する`, or `好きにして` authorize AI judgment only for the current clearly scoped subject. Without such delegation, unresolved choices that affect output correctness should return to the human before final output or Source-of-Truth update.
- Suggested Change:
  1. Add a three-way Design Decision Classification Gate.
  2. Make delegation scope-bound and non-transitive.
  3. Apply the gate before product image generation, design freeze, and GitHub writes.
  4. Preserve AI-selected / Provisional separately from human-confirmed / Frozen.
  5. Delegated choices remain Provisional until explicit human confirmation; delegation alone never freezes them.
  6. When later unresolved facts are decided or changed, re-evaluate all affected Provisional choices and ask whether to keep or change them before promotion.
  7. Avoid duplicate confirmation when the user has already explicitly delegated that exact scope.
- Related Files: core/RULES.md, core/WORKFLOW.md, evaluation/TEST_CASES.md
- Priority: High
- Promotion Target: core/RULES.md / core/WORKFLOW.md / evaluation/*
- Promotion Evidence: explicit human instruction + Design Decision Classification Gate + regression test
- Status: Promoted


---

## LESSON-013 Declarative Rules Need Runtime Enforcement Review / 宣言的ルールと実行強制を分離する

- Date: 2026-09-22
- Context: Two operational failures exposed a common pattern. In source-locked image generation, important project attributes existed in the Source of Truth but could be lost during abstraction/handoff before generation. In continuity handling, Feather Trigger and Context Freshness rules existed, yet the Harness still depended on the AI actually noticing and operating those rules in the correct order. Subsequent review confirmed that Harness files are declarative context and are not self-executing runtime control.
- What Happened:
  1. The necessary instruction or mechanism existed on paper.
  2. The AI could understand it when explicitly tested.
  3. Real work still allowed an execution path where the instruction was not activated, preserved, or checked at the right stage.
  4. Adding more prose risked repeating the same failure mode: a stronger instruction that still depended on AI memory/attention.
- Root Cause: The architecture did not always distinguish **declarative policy** from **enforced execution control**. Important ordering, state freshness, constraint preservation, and gate behavior could remain dependent on model attention, conversation context, or handoff fidelity. A rule being present in a repository was therefore weaker evidence than the rule being activated and verified in the current run.
- Lesson: **Do not treat the existence of a Rule, Workflow, START path, or Source-of-Truth constraint as proof that it will govern execution.** When an important failure occurs despite the relevant instruction already existing, the next review must ask whether the responsibility belongs in runtime orchestration, durable state, deterministic gates/checks, checkpoints, or another enforceable mechanism rather than in more prompt text.
- Research Direction: Public agent/workflow patterns reviewed after the incident converged on separating model reasoning from orchestration/state where predictability matters. Candidate techniques include code-driven orchestration, graph/state-machine execution, lifecycle/preflight hooks, blocking gates/guardrails, durable checkpoints/state, and machine-readable current-state/constraint records. These are investigation directions, not preselected mandatory architecture.
- Suggested Change:
  1. Add a Harness Runtime Enforcement Review Trigger to Core Workflow.
  2. Trigger it when Harness/automation/Context/TRINITY changes touch rule activation, sequencing, state, handoff, or constraint preservation.
  3. Require explicit review of declarative-vs-enforced behavior, bypass paths, execution ownership, durable state, must-preserve constraints, and evidence of actual activation.
  4. For high-impact Harness changes, favor deeper reasoning and independent verification before fixing a concrete architecture.
  5. Add regression coverage that fails when a rule merely exists in text but the execution path can bypass or omit it.
  6. Keep the concrete runtime solution open until current evidence and implementation constraints are reviewed.
- Related Files: HARNESS.md, core/WORKFLOW.md, evaluation/TEST_CASES.md, experiments/feather-trigger/*
- Priority: High
- Promotion Target: HARNESS.md / core/WORKFLOW.md / evaluation/*
- Promotion Evidence: Human-approved trigger insertion + TEST-020 definition; concrete runtime architecture remains intentionally undecided pending deeper design/review.
- Status: Proposed
