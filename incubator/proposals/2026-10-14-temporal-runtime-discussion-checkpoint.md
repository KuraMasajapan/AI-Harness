---
document_type: checkpoint
title: Temporal Runtime / Shared Time Axis — Discussion Checkpoint
created: 2026-10-14
branch: development
status: RESEARCH_ACTIVE
implementation: NOT APPROVED
adoption_decision: HOLD
origin: Human-AI dialogue about Runtime, time-oriented MCP/plugins and low-cost event-driven infrastructure
related_proposal: incubator/proposals/2026-09-20-temporal-context-layer.md
tags: [checkpoint, temporal, runtime, human-ai-time-axis, feather-trigger, context-freshness, event-log, deadline, calendar, source-of-truth]
---

# CHECKPOINT — Temporal Runtime / Human–AI Shared Time Axis
**Recorded:** 2026-10-14 (JST; date only, not a verified chat message timestamp)  
**Repository:** `KuraMasajapan/AI-Harness` / `development`  
**State:** Research and brainstorming continue. No platform or architecture selected. No Runtime deployment, new plugin installation, calendar event, database, webhook, or automated task created by this checkpoint.

## 1. Human's actual objective — PRESERVE

> AIが発言・回答した時刻とHumanが返答・送信した時刻を記録することで、時間の流れをChatGPTの会話とAI-Harnessの判断へ入れ込みたい。

This is more than a decorative timestamp or a clock tool:

1. Human and assistant message/event timestamps should form a shared, recoverable chronological timeline.
2. Time should help detect potentially stale context and resume boundaries, without blindly forcing reloads.
3. When new and old information coexist, the system should help identify the **currently effective** statement, specification, or decision.
4. Natural-language commitments such as `来月の中頃には完了させたい` should be recognized as **provisional deadline windows** relative to the *original utterance date*, surfaced for Human confirmation, then optionally reflected in a calendar.
5. Prefer **one conceptual time axis and event schema**. A single application is desirable but **not required**; multiple small apps/triggers may cooperate using the same schema.
6. Use what already exists where practical, keep costs/setup low, and continue gathering evidence and brainstorming until a clear implementation advantage emerges.

**Do not silently reinterpret** this objective as an instruction to build a 24/7 autonomous agent or a large new database.

## 2. Grounded existing work and boundaries

### Feather Trigger V0.1 — historically tested, currently needs diagnosis
- Existing code and frozen specification: `experiments/feather-trigger/feather-trigger-v0.1.user.js` and `experiments/feather-trigger/V0.1.md`.
- At the 2026-09-20 experiment, Chrome/Violentmonkey injected `[activity_gap: ...]` into outgoing Human messages; both Enter and button routes previously passed live tests.
- This mechanism records **timestamps of detected Human send attempts**, not confirmed server delivery, and computes intervals between Human sends. It **does not** observe assistant response completion.
- In later Human tests the badge returned to `READY` but no timestamp/gap was appended with either Enter or send button, including concerns about Chrome split view. **Do not call today's functionality PASS.**
- Preserve V0.1 feature-freeze evidence. Diagnose and validate a separate repair/V0.2 path, rather than rewriting history.

### Temporal Context Layer — prior proposal, not a product
- `incubator/proposals/2026-09-20-temporal-context-layer.md` identifies `activity_gap`, `current_time`, `timezone`, `scheduled_trigger` and `source_freshness`.
- This checkpoint **extends the question** to include **assistant reply timestamp and shared event history**, rather than replacing the existing proposal.

### HARNESS / Workflow — already contains related policy
- `HARNESS.md`: Runtime Activation & Revalidation separates declarative Markdown from actual execution and says timestamps can be signals, not universal guarantees.
- `core/WORKFLOW.md`: Context Freshness / Resume Boundary, Source-State Ambiguity Gate, Human decision authority, Runtime Enforcement Review Trigger.
- Existing **Current / Superseded / Historical / Human-approved** semantics must not be replaced with “latest timestamp wins”.
- `incubator/proposals/2026-10-09-pidurablekit-iphone-durable-runtime.md`: durable task state / mobile controller candidate, **not adopted or installed**.
- `incubator/proposals/2026-10-14-github-work-pr-event-triggered-review.md`: PR-triggered Work review **candidate only**, not the same as universal chat event capture.

## 3. Key conceptual distinction — two or three clocks

For every meaningful event distinguish, where available:
- **occurred_at:** when the action actually happened, if verified by its source;
- **observed_at:** when browser/Runtime/connector observed it (always identify observer);
- **recorded_at:** when a ledger stored it; and, for decisions/specs,
- **effective_at / valid_from:** when the decision is considered operative, if explicitly known.

A browser-observed assistant completion timestamp is **not** a certified OpenAI server message timestamp. A timestamp acquired from Time MCP Server inside an assistant answer is a **tool-query time**, not necessarily a response-completion time.

**Information reconciliation rule:** chronological recency alone cannot establish authority or truth. Preserve Source of Truth precedence, status (CURRENT / SUPERSEDED / HISTORICAL / PROVISIONAL), human approval, provenance and replacement links; report ambiguities rather than guessing.

**Date interpretation rule:** `来月中旬` should be treated as a **range or approximate target anchored to the utterance date**, never automatically transformed to an exact arbitrary date, hard deadline, or unapproved calendar event.

## 4. Minimum candidate design (provisional, NOT chosen architecture)

```text
ChatGPT Web human-send / assistant-finish observations
                     ↓
        Small event capture layer
                     ↓
          Temporal Ledger schema
           (local-first at pilot)
                     ↓
AI-Harness context freshness / resume / history interpretation
                     ↓
Optional explicit Human-reviewed deadline → Calendar
Optional version-aware decisions → GitHub Source of Truth
Optional remote ingest when needed → Vercel/API + persistent store
```

Very small initial **event envelope** candidate:

```json
{
  "event_id": "opaque-id",
  "event_type": "human_send_observed | assistant_finish_observed",
  "conversation_ref": "opaque-local-ref",
  "observed_at": "ISO-8601-with-timezone",
  "observer": "browser",
  "capture_status": "observed_not_server_confirmed"
}
```

Do not archive full chat content, secrets or unnecessary personal identifiers by default. For future semantic events (decision, deadline, supersession), use separate references/fields rather than inflating every low-level timestamp entry. Evaluate local storage retention, deduplication and privacy.

## 5. Alternatives discussed, NOT adopted

| Tool/path | Possible responsibility | Evidence/limitation |
| --- | --- | --- |
| **Time MCP Server** | On-demand current time / time zone conversion | Does not log chat replies or control scheduling; not connected to this chat |
| **Feather Trigger / Violentmonkey** | Browser-level chat send / response observation | Existing V0.1 implementation only attempts Human sends; now reportedly fails; UI dependence |
| **Airtable (connected)** | Structured event/decision ledger | Feasible candidate, but no automatic ingestion or schema implemented |
| **GitHub (connected)** | Approved specification/decision truth and history | Not a high-frequency chat event store by default |
| **Google Calendar (not connected)** | Visualize confirmed goals/deadlines | No silent events; requires relevant connection/approval |
| **Vercel (available, not installed)** | Future on-demand API / webhook / serverless receive endpoint | Not a continuously running chat observer; durable storage external; verify free-tier limits/terms before selecting |
| **PiDurableKit** | Long-term iPhone durable Runtime / interruption-safe execution | Research candidate; iOS background constraints; implementation not approved |
| **TimePeace / Nightshift / Agent Calendars and other 'time' plugins** | Selective event/diary, coding-state, plan/deadline workflows | Feature claims need direct compatibility, cost, trust, export/API and permission testing; none proven to be the shared chat-time spine |
| **ChatGPT Work / GitHub Actions** | Supported event-driven analysis / CI triggers | Specific events; not an all-chat timestamp pipeline |

Do not equate a ChatGPT plugin/MCP connector with a permanent background daemon or an automatic observer of every chat message. Avoid paid services or custom MCP development until a concrete unsolved need is demonstrated.

## 6. Current Human direction

- **Decision / CONFIRMED:** move incrementally from existing components; keep public information research and ideation/wall-bouncing ongoing; prefer one logical axis; do not choose Vercel, a plug-in, an iPhone runtime, or a universal architecture prematurely.
- **Research status / ACTIVE:** seek concrete low-cost components; compare with existing tools, verify primary sources and test actual behavior.
- **Implementation status / NOT APPROVED:** no new Runtime, plugin, cloud project, event schema standard, Core/Workflow rule, or production schedule has been promoted.
- **Task continuity:** checkpoint creation is **not** equivalent to project completion or approval for Phase 1 implementation.

## 7. Next actions on resume

1. **Reproduce and diagnose Feather Trigger V0.1 failure** (READY but missing injection for both Enter/button). Capture page/DOM selector behavior, Violentmonkey activation, split-view differences, chat-ID detection, console results and sent message evidence. Do not modify the frozen baseline until the failure is understood.
2. Make a **read-only browser-observation spike** for assistant response completion timestamp. Determine what observable event is reliable, what happens during streaming, failed responses, regeneration, multiple tabs, split view, reload and mobile usage.
3. After both event sources are measured, trial a **minimal local-only timestamp ledger** across ~10 Human–AI exchanges and a reload. Compare count, order, duplicates, missing timestamps, and exact-vs-observed time meaning.
4. Separately test a **stale vs current** scenario with two conflicting assertions and explicit supersession/approval metadata; prove no “latest written = current” shortcut.
5. Separately test **relative due-date capture** as suggestion only; reference utterance date/time zone, record fuzziness, and require Human approval before any Calendar write.
6. Only then compare **Airtable vs local store vs Vercel API vs other plugin** by reliability, exportability, cost, scope, privacy, maintenance and how much actual complexity they remove.
7. Keep collecting OSS/plugin ideas and alternative designs; store only proven new insights or high-value candidates, preserving existing proposals and Human-controlled adoption.

### Minimal acceptance checks before architecture choice

- Human-send and assistant-finish are differentiated and observed without covert content collection.
- Event timestamps survive reload locally and are independently inspectable.
- Missing/unknown timestamps are explicit, not fabricated.
- Duplicated sends/regenerations do not silently corrupt the ordering.
- Effective latest specification respects source authority, approval and supersession—not clock order alone.
- No data leave the device without explicit authorization.
- Full stop/recovery is possible without an always-on home PC.

## 8. Resume handoff prompt

> AI-Harness Temporal Runtime discussion resume. Read this checkpoint, then `incubator/proposals/2026-09-20-temporal-context-layer.md`, `experiments/feather-trigger/V0.1.md`, and relevant `HARNESS.md` / `core/WORKFLOW.md`. Preserve Human's shared time-axis objective. Status: **RESEARCH_ACTIVE, implementation NOT APPROVED**. Next step is diagnosing the Feather Trigger READY/no-injection regression; do not assume that Time MCP Server, TimePeace, Nightshift, Vercel, or PiDurableKit has been selected. Separate event observation from source-of-truth validity and natural-language deadline confirmation. Continue ideation and small, evidence-based experiments.

## Change boundary / evidence

This checkpoint creates one research-continuity file only. No existing proposal, V0.1 userscript, Core, policy, credentials, plugin settings, calendars or production code is changed.
