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

---

## 11. Follow-up — Unslop: a procedural anti-slop UI finishing skill (2026-11-01)

### Intake and primary sources

- Human-shared post (Codex 研究所, 2026-10-31 JST): https://x.com/codex_lab_/status/2116581624939004137
- Original author (Damir Sokolovsky): https://x.com/heydamir/status/2115063463063998736
- Official repository: https://github.com/heydamir/unslop
- README: https://github.com/heydamir/unslop/blob/main/README.md
- Actual skill definition: https://github.com/heydamir/unslop/blob/main/skills/unslop/SKILL.md
- Verified in upstream repository at review time (2026-11-01): **CC BY 4.0**, attribution required when copying/adapting; a *Claude Code / Codex UI-refinement Skill*, **not** an autonomous desktop agent, backend controller, or orchestration system.
- Status: **CANDIDATE / HOLD**. The post's claim that it turns any page "professional quality in one shot" is **unverified marketing**, not an independently reproduced result. No local run, visual A/B, security check, or quality benchmark was performed.

### What is novel relative to the existing short principle?

The original Anti-Slop Principle is **a small, high-leverage instruction**: let structure and hierarchy explain before adding copy. **Unslop** packages a *repeatable workflow* for an existing screen:

1. Inspect real rendered UI and its source files (or an authorized copy of a publicly accessible page), identify concrete defects first.
2. Determine whether the screen needs a heavy redesign, a limited polish pass, or **no changes**. Keep a good existing design.
3. Set a product-specific direction: **Product / Character / World / Moments / Signature**. Unless the owner already delegated that choice, propose and obtain agreement **before editing**.
4. Apply ordered passes: **spacing → color → icons → copy → typography → layout → details → visuals → motion**.
5. Render and inspect the changed screen; report the edits, unresolved issues and any generated-asset prompts. Optional short transformation-story video is a separate output, not the core function.

The skill discourages generic gradients, indiscriminate glow, filler icons, overlong labels, noisy cards and animations without meaning. It emphasizes plausible data, controlled accent colors, legible contrast, real product imagery and restrained motion. It says to preserve features, content and section order, but **its own instructions permit copy changes and visual/layout revisions**; verify behavior and labels rather than assuming zero regression.

### Supported workflow and true tool boundaries

- Upstream documents React, Next.js, Tailwind, Vue, Svelte and plain HTML/CSS. These are **codebases it can guide the agent to edit**, not dedicated independently tested integrations.
- Claude Code invocation: `/unslop`. **Codex invocation: `$unslop`**, typically after an installation such as `$skill-installer install https://github.com/heydamir/unslop/tree/main/skills/unslop` or isolated project-level Skill placement. Do not repeat the social post's `/unslop` syntax as if it were the Codex invocation.
- Optional snapshotting of a live URL uses Playwright/Chromium and writes a **local captured copy** for redesign; without authorization and deployment access, this does **not** modify the actual live website.
- Optional story video requires Playwright and FFmpeg. Optional image generation may use external providers (fal / Replicate / OpenAI / etc.) and **can incur costs**; upstream guidance calls for showing the prompt and obtaining approval before paid generation.
- A CC BY 4.0 Skill does not make third-party screenshots, fonts, images, websites, generated assets or dependencies automatically free of their own rights/terms.

### AI-Harness relevance — the important conceptual distinction

The Human reaction to the UI demo: a mature operator interface makes it **feel possible to get work done purely through the UI**. This is an **operator UX hypothesis** for the future AI-Harness control surface, not evidence that Unslop delivers task execution or agent coordination. Relevant examples: current job, delegated agent/owner, progress, evidence, Human-review-required status, quality/regression alerts, and Codex quota visibility. **Live metrics and action buttons must be grounded in actual backend state; a polished mock dashboard does not constitute a functioning orchestration system.**

This complements but does **not** replace:
- This existing **UI Anti-Slop Principle** (simple rules on visual structure over extra copy).
- `incubator/proposals/2026-10-23-ui-ux-pro-max-skill-reassessment.md` (broader searchable design knowledge and design-system generation).
- `incubator/proposals/2026-10-15-ui-design-skill-component-comparison-prep.md` (different design Skills/components, independent comparisons and acceptance rules).
- `incubator/proposals/2026-09-20-harness-launcher-ui.md` (operator UI idea).
- `incubator/proposals/2026-11-01-desktop-ai-capabilities-review.md` (Orkas commander and unified desktop operator workflows).
- `projects/JARVIS_Soul_UI/V0.1_SPEC.md` (Local AI Soul **frozen** V0.1 design and child-friendly functionality; deliberate Orb glow/motion is product identity, not automatically "slop" to remove).

### Testing proposal — only when separately approved

Use a **real, non-frozen** candidate screen in its isolated branch or copy, with no credentials or private production data. Keep the same starting commit, model, brief and functionality requirements:

- **A:** existing frontend workflow, no additional design Skill.
- **B:** existing workflow + Unslop *alone*.
- Optional later **C:** UI UX Pro Max *alone*; do not stack Skills in the first benchmark.
- Compare before/after screenshots, keyboard/navigation semantics, screen-reader labels, contrast, responsive/mobile behavior, loading/performance, functional regression tests, Human visual preference, iteration time and Codex token/usage cost.
- Guardrails: retain brand-specific aesthetics; preserve Human-approved screen states/alerts; require explanation before changing copy or introducing new controls; no paid image calls, unreviewed scripts, global Skill install or third-party MCP without approval.

### Decision

**A / CANDIDATE / IMPLEMENTATION HOLD** — Strong match as a *finishing/review* process for dashboards and operational interfaces, **not** evidence of a standalone UI-driven AI company or of immediate quality gains. Store in this existing anti-slop research file rather than opening a duplicate independent Proposal. **No Core, Skill, AGENTS.md, Soul, TRINITY, UI implementation or automated workflow changed.**
