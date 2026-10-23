---
document_type: design_principle_candidate
date: 2026-10-23
title: "UI Anti-Slop Principle — Let Structure Explain Before Copy"
source_post: "https://x.com/luinlee/status/2113085361836744764"
decision: CANDIDATE
implementation: HOLD
stage_1_rank: A+
stage_2_rank: A
evidence_status: "SOURCE POST CONFIRMED; PRINCIPLE PLAUSIBLE; LOCAL EFFECT NOT YET BENCHMARKED"
tags:
  - ui
  - ux
  - anti-slop
  - minimalism
  - information-hierarchy
  - copy
  - design-principle
  - agent-instructions
---

# UI Anti-Slop Principle — Let Structure Explain Before Copy

## Status

**Stage 1: A+**  
**Stage 2: A**  
**Decision: CANDIDATE**  
**Implementation: HOLD**

This principle is a strong candidate for future integration into AI-Harness UI guidance.

It should not be interpreted as "labels and descriptions are bad."

The intended rule is:

> **Use layout, hierarchy, grouping, spacing, position and visual structure to communicate meaning first. Add labels or explanatory copy only where they materially improve comprehension, safety, accessibility or task completion.**

## 1. Source signal

Human-shared X post:

- https://x.com/luinlee/status/2113085361836744764

The source author reported better AI-generated UI results by adding the following guidance to `AGENTS.md`:

> "Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining."

The source frames this as a way to reduce "AI slop" in generated interfaces.

This is an anecdotal practitioner observation, not an independent benchmark.

## 2. Why the idea matters

AI models are strong at generating explanatory language.

When uncertain about UI hierarchy, they may compensate by adding:

- secondary labels,
- subtitles,
- helper text,
- badges,
- repetitive descriptions,
- duplicated metadata,
- explanatory cards,
- repeated headings.

That can create interfaces that contain more words without becoming easier to understand.

Common failure pattern:

```text
weak hierarchy
    ↓
add explanatory copy
    ↓
more visual noise
    ↓
harder scanning
    ↓
add even more labels
```

Preferred pattern:

```text
weak hierarchy
    ↓
fix grouping / spacing / position / scale
    ↓
meaning becomes visible
    ↓
retain only copy that adds real value
```

## 3. Core principle

### Short form

```text
Structure before explanation.
```

### Practical form

Before adding secondary text, ask:

1. Can grouping communicate this?
2. Can hierarchy communicate this?
3. Can spacing communicate this?
4. Can position communicate this?
5. Can typography communicate this?
6. Can an established icon/pattern communicate this?
7. If the text is removed, does comprehension materially decrease?

If not, the extra copy may be unnecessary.

## 4. Important exceptions

The principle must **not** suppress labels or explanations where they are genuinely needed.

Keep or add explicit copy when it improves:

- accessibility,
- form comprehension,
- error recovery,
- destructive-action warnings,
- permission / privacy decisions,
- financial or security-sensitive actions,
- unfamiliar icons,
- domain-specific terminology,
- onboarding,
- child-facing interfaces,
- legal/compliance requirements,
- system status,
- empty/error states,
- irreversible actions.

Do not rely on visual layout alone when meaning must be available to:

- screen readers,
- keyboard-only users,
- low-vision users,
- users with cognitive accessibility needs,
- users encountering an interface for the first time.

## 5. Better formulation for AI-Harness

Recommended future wording:

> **Avoid unnecessary secondary labels and explanatory copy. Prefer clear hierarchy, grouping, spacing, position and established interaction patterns to communicate meaning. Keep explicit labels and descriptions wherever they improve accessibility, safety, comprehension or decision quality.**

This wording preserves the source insight without turning it into an absolute minimal-text rule.

## 6. Relationship to Harness Minimalism

Relevant saved research:

- `incubator/proposals/2026-10-16-harness-minimalism-counterhypothesis.md`
- `incubator/proposals/2026-10-23-ponytail-v5-coding-efficiency.md`

The same structural idea appears across layers:

```text
Harness:
Do not add process when structure already works.

Code:
Do not add implementation when existing primitives already work.

UI:
Do not add explanation when layout already communicates the meaning.
```

Shared principle:

> **Do not compensate for weak structure by adding more surface area. Improve the structure first.**

This is the deeper reason this UI rule is relevant to AI-Harness.

## 7. Relationship to UI UX Pro Max and existing design Skills

Relevant saved research:

- `incubator/proposals/2026-10-23-ui-ux-pro-max-skill-reassessment.md`
- `incubator/proposals/2026-10-15-ui-design-skill-component-comparison-prep.md`

This principle is intentionally much smaller than a large design Skill.

Potential value:

```text
large design system / Skill
= broad design knowledge

anti-slop principle
= small high-leverage constraint
```

A future experiment should test whether one small instruction produces a meaningful improvement before adding larger UI-specific toolchains.

## 8. Suggested future evaluation

Use the same UI task under two conditions:

```text
A: current UI instructions
B: current UI instructions + Anti-Slop Principle
```

Measure:

- number of secondary labels,
- total explanatory copy,
- scanability,
- information hierarchy,
- accessibility,
- task completion,
- Human preference,
- regressions,
- need for follow-up correction,
- token / iteration cost.

Important:

A result with less text is **not automatically better**.

The success condition is:

> fewer unnecessary words **without** loss of comprehension, safety or accessibility.

## 9. Candidate integration points

If future testing is positive, candidate locations include:

- UI-related Skills
- project-local `AGENTS.md`
- UI design review checklist
- frontend implementation instructions
- design-generation prompt templates

Do **not** automatically promote this into global Core rules unless evidence shows it has broad cross-project value.

## 10. Decision

**A+ / CANDIDATE / IMPLEMENTATION HOLD**

Preserve now.

This is considered a potentially high-leverage design principle because it may reduce AI-generated UI clutter with a very small instruction.

No Core, Skill, AGENTS.md, project UI, or shipped product is modified by this record.
