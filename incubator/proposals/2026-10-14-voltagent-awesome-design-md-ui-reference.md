---
status: proposal
created: 2026-10-14
origin: Human-shared https://github.com/VoltAgent/awesome-design-md
stage_1_rank: A+
stage_2_rank: A+
evidence_status: CONFIRMED (official repo and DESIGN.md content) / UNVERIFIED (UI quality improvement on Harness projects)
decision: CANDIDATE
implementation: HOLD
tags:
  - ui
  - ux
  - design-system
  - markdown
  - design-tokens
  - coding-agent
  - brand-reference
  - accessibility
trigger_topics:
  - awesome-design-md
  - DESIGN.md
  - Google Stitch
  - UI redesign
  - visual consistency
  - BBB UI
  - growgle UI
  - Harness dashboard
  - coding agent design
---

# VoltAgent / awesome-design-md — AI向けDESIGN.md参照ライブラリ

## Human decision
- 2026-10-14「ここまでの優良なものを保存」とのHuman依頼により**検証候補として保存承認**。
- 現行UIのデザイン仕様、Core、Skills、Component Library等を変更する承認ではない。
- Decision **CANDIDATE** / Implementation **HOLD**。

## Verified sources (2026-10-14)
- Repository: https://github.com/VoltAgent/awesome-design-md
- Google Stitch DESIGN.md overview: https://stitch.withgoogle.com/docs/design-md/overview/
- Google Stitch specification: https://stitch.withgoogle.com/docs/design-md/specification/
- Sample: https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md
- Sample: https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/apple/DESIGN.md
- Sample: https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/airtable/DESIGN.md
- MIT license according to repository README. README reports 84 DESIGN.md documents; the 2026-10-14 main-tree listing also contained 84 corresponding files. Count changes with upstream updates.
- The repository describes its content as **third-party analysis of publicly visible design systems**, not official brand design documentation, and disclaims accuracy/warranty.

## What is confirmed and what is not
**CONFIRMED from files**
- Real Markdown design analyses include structured tokens for palette/semantic roles, typography, spacing, radii, buttons/cards/navigation, layout, interaction states, responsive guidance and do/don't rules.
- Agents can be given a selected project's `DESIGN.md` as context. Basic use requires only reading Markdown, not installing a daemon or complex framework.
- The README contrasts `AGENTS.md` (how to build) and `DESIGN.md` (what the output should look and feel like).
- Sample Linear, Apple and Airtable files contain substantial concrete styling detail.

**UNVERIFIED**
- Consistency, UI quality, accessibility or user satisfaction improve for any specific AI model/project.
- Reported GitHub stars/forks indicate performance, originality or benchmark superiority.
- Any copied brand specification is 100% accurate, current or legally reusable. Brand names, images, logos and proprietary fonts can have rights distinct from code/documentation MIT license.
- Using a reference file automatically overrides constraints, approved screen layouts, existing project identity or requirements.

## Why interesting for AI-Harness
- User-facing applications (BBB dashboard, Harness launcher, growgle catalog, local AI user interface) often need consistent, readable and coherent visual systems across generated screens.
- Rather than telling an agent merely 'make it stylish', pass explicit design tokens and rules.
- The particularly useful feature is **making tacit visual preferences explicit as versionable, readable source text**, not copying another company's UI.
- Good fit for a project-local DESIGN.md if/when a real UI work cycle shows a need.

## Overlap / existing assets
- `incubator/proposals/2026-09-20-generative-ui-component-library.md`: reusable verified UI elements and lazy-loaded component registry. DESIGN.md is a **style contract/reference**, not a component implementation or replacement.
- `skills/README.md`: Skills specify reusable procedures; DESIGN.md supplies visual standards for the task. Do not duplicate Core rules or load unnecessary files.
- `incubator/proposals/2026-09-20-harness-launcher-ui.md`: future child-friendly control room UI already has functional, simplicity and reliability requirements. External style rules cannot override those.
- `projects/Hangfire/VISUAL_DIRECTION.md`: existing adopted pixel-art style and source-of-truth constraints. Do **not** overwrite project-specific approved design decisions with borrowed templates.
- Existing external frontend/UI Skills remain separate from this textual design reference approach.

## Suggested small test (NOT STARTED)
1. Choose one real upcoming UI change and a **single** target screen with fixed content, data and interaction requirements.
2. Preserve existing brand restrictions, child-accessibility, responsiveness, touch targets, contrast and accessibility; external inspiration is subordinate to adopted project specs.
3. Prepare A (existing prompts/skills alone) and B (same conditions, plus an **adapted** DESIGN.md rather than wholesale branded imitation).
4. Evaluate using screenshots and working interaction checks: style consistency, readability, smartphone usability, accessibility, completion/correction time, token consumption, runtime performance.
5. If B demonstrably improves outcome, propose a light project-specific DESIGN.md; store only stable, selected tokens and rules. Human approves any actual project edit.
6. Do not import whole 84-design catalog or automatically update every project. Avoid copyright/trademark/font assumptions.

## Assessment / triggers
- Stage 1 **A+** / Stage 2 **A+**.
- Evidence **CONFIRMED** (files/structure) / **UNVERIFIED** (actual benefits).
- Decision **CANDIDATE**, Implementation **HOLD**.
- Recall when: UI redesign, frontend-agent, design drift, unreadable dashboards, visual polish, Markdown styling contract, reusable components, BBB/growgle/Harness interface creation.
