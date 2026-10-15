---
status: research_candidate
created: 2026-10-15
origin: Human-shared ten GitHub UI-design repositories
decision: PREPARE_FOR_LATER_COMPARISON
implementation: HOLD
installation: NONE
branch: development
tags:
  - ui
  - ux
  - codex
  - design-skills
  - mcp
  - component-library
  - animations
  - comparative-evaluation
  - human-approval
trigger_topics:
  - UI design skill comparison
  - Design Taste
  - Better Design
  - Superdesign
  - Motion Primitives
  - Canvas UI
  - Paper Shaders
  - UI Layouts
  - Hyperiux
  - Cursify
  - Trickle UI Kit
---

# UI design GitHub 10-repository survey — Comparison readiness checkpoint

**Date:** 2026-10-15 (JST; this is the checkpoint date, not a measured event timestamp)  
**Repo:** `KuraMasajapan/AI-Harness`, branch `development`  
**Human decision:** 「後で比較に進めるように準備と記録だけしておいて」  
**Scope of authorization:** Save research and a reusable, non-executing comparison plan. **Do not install Skills/MCP, copy component source, update live UI, run packages/scripts, deploy, alter Core policies, or choose a winner on Human's behalf.**

## 1. Premise and evidence boundary

Social-media framing: "github repos that turn claude code and codex into elite ui designers". That is a promotional claim, **not an experimentally demonstrated outcome**. The ten named repositories were identified and their README files reviewed during the preceding investigation. Repository availability and documented purpose were verified; no installed behavior, reproducible benchmark, accessibility audit, malware audit, or independent improvement claim has been verified.

**Do not treat all ten as agent Skills.** Group (A) design judgment/workflow, (B) UI component implementations, (C) focused effects. Skills/MCP and component libraries have different acceptance tests; evaluate separately.

Ranking below is **provisional AI-Harness fit / research priority**, not an empirical quality score.

## 2. Full catalog — exact repositories and triage

| # | Candidate and official source | Category | Reported/verified focus from README | Priority and caveat |
| --- | --- | --- | --- | --- |
| 1 | **Superdesign Skill** — https://github.com/superdesigndev/superdesign-skill | A: design workflow / tool-backed agent Skill | CLI-driven UI, slides and graphics on external design canvas; Codex/Claude support advertised | **A / HOLD** — external CLI and service dependency; compare to existing MagicPath/other design paths; terms/account/cost/data exposure need recheck |
| 2 | **Better Design** — https://github.com/marvkr/better-design | A: remote MCP design system / review | Design tokens, curated design systems, component docs, accessibility/UI principles, review methods; MCP + Skill | **A+ / PRIORITY TEST** — overlaps existing DESIGN.md references and frontend Skills; remote service permissions, availability and costs require confirmation |
| 3 | **Design Taste** — https://github.com/madebymustafa/design-taste | A: static agent Skills | 24 Skills spanning design identity, craft, reviews and code guidance; Codex and others described | **A+ / PRIORITY TEST** — full install script copies Skills into multiple agent directories; **do not run global/all-at-once installer**, isolate smallest relevant Skill |
| 4 | **Canvas UI** — https://github.com/DavidHDev/canvas-ui | B/C: React advanced component/effects library | Interactive UI and WebGL/WebGPU effects | **A / CONDITIONAL** — likely expensive rendering on mobile; **MIT + Commons Clause restrictions**, not plain MIT; test consent, performance and redistribution limitations |
| 5 | **Paper Shaders** — https://github.com/paper-design/shaders | C: Canvas shader library | Animatable/customizable graphical textures and backgrounds for web/React | **A / CONDITIONAL** — Apache-2.0 per README; evaluate motion, CPU/GPU, mobile, contrast; avoid purely decorative weight |
| 6 | **UI Layouts** — https://github.com/ui-layouts/uilayouts | B: React layouts/components | Tailwind, Motion and utility packages; UI composition | **A / ON-DEMAND** — library-level dependencies; MIT in root LICENSE; check actual app framework |
| 7 | **Hyperiux Components** — https://github.com/Hyperiux-Immersion-Labs/hyperiux-components | B/C: animation registry/MCP/CLI | 50+ free and 100+ Pro effects per README; Next.js/React oriented | **B / HOLD** — CLI/MCP MIT does **not** cover Effects; separate Hyperiux Effects License, Pro subscription and redistribution limits; assess individual effect before reuse |
| 8 | **Motion Primitives** — https://github.com/ibelick/motion-primitives | B: React motion components | Lightweight composable motion/transition patterns | **A+ / PRIORITY TEST (separate component track)** — MIT per README; test controlled use, reduced-motion, interaction/performance; not a competing design-reasoning Skill |
| 9 | **Cursify** — https://github.com/ui-layouts/cursify | C: cursor-focused UI effects | React cursor interactions with Tailwind/Motion | **C / PASS FOR NOW** — not useful for touch-first/mobile; license not verified in this assessment, do not assume MIT |
| 10 | **Trickle UI Kit** — https://github.com/akaieuan/trickle-UI-kit | C: CSS text animations for React | CSS-centric text motion via shadcn registry; README claims 47 effects/components | **A / CONDITIONAL** — MIT for core components and CC0 demo examples as stated in README; verify particular asset and test motion preference and accessibility |

**Source/evidence limitations:** Count, pricing, services and licenses may change. Reopen **each exact GitHub URL and its license file** at execution time; do not install based on stale catalog metadata. For links 2, 3 and 8, the above A+ refers only to *investigation priority*. The actual improvement hypothesis remains **UNVERIFIED**.

## 3. Existing Harness assets / non-duplication

Read before comparing:
- `skills/README.md` — minimal/specific/verifiable Skills, no unconditional loading or Core duplication.
- `incubator/proposals/2026-10-14-voltagent-awesome-design-md-ui-reference.md` — candidate static DESIGN.md design tokens/reference; **not adopted**, overlaps Better Design at the reference layer but lacks live MCP/review.
- `incubator/proposals/2026-09-20-generative-ui-component-library.md` — approved concept? **proposal only** for a curated, manifest-driven, verified component registry; not an implemented package. Motion Primitives etc. are candidate sources, not automatically trusted components.
- `incubator/proposals/2026-10-12-mattpocock-skills-engineering.md` — coding Skill candidate; installation HOLD.
- Relevant project Source of Truth, design rules and accepted screen layout, particularly BBB (data-rich dashboard), growgle (children/mobile/catalog), and any launcher UI; choose **one actual target screen later**.
- Historic Human report: external `hueyexe/frontend-agent-skills` set installed earlier with Project scope. **Confirm what is actually available in the test environment**, do not infer that all nine are now in this repo or always active.
- Available external app/tooling such as MagicPath may already cover design workflows. Compare before adding Superdesign.

Avoid duplicate Skills and blanket repo imports. Never override Human-approved project aesthetics, accessibility constraints or functional requirements.

## 4. Proposed comparison protocol — NO RUN YET

### Track A: Does AI design judgment improve?

**Pilot candidates:** baseline (existing agent/workflow), baseline + *one* isolated Design Taste Skill, baseline + Better Design MCP guidance, optionally baseline + selected project-local DESIGN.md from existing reference concept as fourth comparator **only if materially distinct and feasible**.

**Preflight before trial**:
1. Human chooses a single **actual UI improvement task** and approved screen, e.g. a BBB dashboard panel or growgle catalog view. Do not invent a new product/brand just for the benchmark.
2. Record framework, package versions, codebase commit, source-of-truth design requirements, fonts/assets legally available, target screen size, device constraints, touch targets, contrast/legibility and navigation semantics.
3. Confirm actual agent + model + context, existing Skills (including installed external frontend set), Better Design MCP access/terms, and whether the tool requires shell/network/account permissions. Ask Human before connecting services or installing code.
4. Fix identical input data, copy, layout acceptance criteria, source version and time budget for each run. Use a fresh equivalent baseline per condition to reduce prompt-history contamination; randomize condition order when practical.
5. Run **only one additional treatment at a time**. Do not use Design Taste + Better Design simultaneously in initial causal comparison.
6. Capture side-by-side desktop/mobile screenshots *and* a runnable build, design rationale, code diff, dependencies, network endpoints, runtime performance, edit/iteration count, time, token/tool consumption where measurable.
7. Human blind-comparison of visuals where feasible; independent functional/accessibility checks instead of treating an AI's self-critique as proof.

**Proposed rubric** (0–5 each, weights decided before the test):
- Functional compliance and no regression — pass/fail gate.
- Mobile readability / accessibility (contrast, visible focus, touch targets, responsive behavior, reduced motion) — pass/fail safety gate + quality score.
- Information hierarchy and task completion efficiency.
- Visual coherence with current project-specific design standards.
- Human preference (ask Human to rank independent variants, no leading descriptions).
- Engineering cost (iterations, build size, dependencies, tokens/time/maintenance).
- Privacy, third-party rights, provenance and reproducibility.

Document counterexamples; do not infer statistical superiority from one sample. If testing only one screen, mark result `SINGLE-PILOT / UNGENERALIZED`.

### Track B: Can a component improve a specific interaction without regressions?

**Pilot candidate:** Motion Primitives (first), with UI Layouts/Trickle/Paper Shaders/Canvas UI only when the approved app has an actual need.

Do **not** score component effects as if they were design-judgment Skills. Compare **plain functional control** vs the same control with a *single* effect. Judge usability, performance, screen reader/keyboard/touch behavior, `prefers-reduced-motion`, mobile power/GPU burden, build size, SSR/browser support, licensing and safe fallback. Keep animations subordinate to data legibility (especially BBB trading UI and child-oriented growgle).

### Baseline experiment worksheet (duplicate when starting)

```text
Experiment ID:
Human-approved task/screen:
Agent/model/tool version:
Source commit/framework:
Existing Skills actively loaded:
Treatment: baseline | Design Taste one Skill | Better Design MCP | ...
Prompt/spec version:
External accounts/cost/privacy approvals:
Run start/end (source + timezone):
Build/tests/interaction evidence:
Desktop/mobile screenshots:
Accessibility/reduced-motion:
UI quality scores and Human preference:
Time/tokens/dependencies/change scope:
Functional regressions:
Verdict: IMPROVED | SAME | WORSE | INCONCLUSIVE
Next action: ADOPT CANDIDATE | REPEAT | REJECT
Human decision:
```

## 5. Decision gates and stop conditions

- No install, update, MCP connection, global install script, CLI `npx`, file-copy, paid account or build command without a **separate implementation-stage Human approval**.
- Never run scripts embedded in an untrusted README/SKILL.md automatically; code-review and pin versions before executing; consider prompt injection and exfiltration risks.
- If an external MCP/tool requires transmitting code/screenshots/project data, make it explicit and constrain/redact to minimum.
- If a selected React/Next component mismatches the project's actual stack, reject rather than rebuild the whole app around it.
- Stop before replacing functional or accessibility requirements with appearance-first layouts.
- "Works on my machine" is insufficient for adoption. Require reproducible build, usability checks, rights/license review and Human preference evidence.
- A+ shortlist ≠ permission to install or claim elite quality.
- When confidence is insufficient, retain `CANDIDATE` / `HOLD` and record why.

## 6. Next resume instruction

> Continue the UI design GitHub 10-repository survey. First read this file plus `incubator/proposals/2026-10-14-voltagent-awesome-design-md-ui-reference.md`, `incubator/proposals/2026-09-20-generative-ui-component-library.md` and `skills/README.md`. Human authorized **preparation and record only**, not installation. At the next explicit comparison request, first revalidate the repo/license/tool state and ask/select one real Human-approved UI screen; compare baseline against one isolated Design Taste Skill and Better Design MCP with stable input spec, then test Motion Primitives independently as a component. Report evidence, costs, safety and overlap. Preserve approved project design constraints, Human final decision and implementation HOLD until separately authorized.

## 7. Checkpoint closure

- [x] All 10 source repository identities and research status recorded
- [x] Comparison tracks separated, avoiding category confusion
- [x] Existing Harness proposals / overlap mapped
- [x] Minimum reproducible test protocol and worksheet prepared
- [x] No change to Core, Workflow, shipped product, Skills installation or dependencies
- [ ] Tool compatibility and package/license currentness validated at future trial
- [ ] Human-approved test screen and reference commit selected
- [ ] Experiments executed (NOT YET)
- [ ] Adoption decision (NOT YET)
