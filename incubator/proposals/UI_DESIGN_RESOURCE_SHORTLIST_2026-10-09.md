# UI Design Resource Shortlist — 2026-10-09

Status: RESEARCH / SELECTED CANDIDATES / NOT IMPLEMENTED  
Recorded: 2026-10-09 (JST)  
Source: Human-shared list of 25 vibe-coding design resources, independently checked against the providers' public sites and selected original project documents.

## Purpose and decision

Keep **only useful UI-reference/design-contract patterns** from this resource list. Do not install 25 tools, ingest arbitrary third-party prompts, or alter the existing local AI architecture.

Priority is AI-Harness UI_dev_Lab and a potential family-facing local AI UI. The main architecture is not changed. A visual interface must reflect real system states, not simulate unsupported AI emotions, comprehension, or presence.

Existing sources consulted:
- `projects/UI_dev_Lab/CURRENT_STATE.md`
- `projects/UI_dev_Lab/UI_SKILLS_GUIDE.md`
- `projects/UI_dev_Lab/UI_TOOLING_OPERATION.md`
- `incubator/proposals/HARNESS_VNEXT_VALIDATION_CANDIDATES.md` (especially Candidate J and Human Interface principles)
- `research/PROMPT_MOTION_REFERENCE_2026-10-07.md`

**Current policy:** UI Skills = interaction/accessibility/design thinking; MagicPath = isolated exploratory prototypes; external catalogs = references and candidate code/design artifacts. No additional mandatory layer, runtime agent or framework.

## Selected short list (five)

| Resource | Source | Decision | Harness value and constraint |
|---|---|---|---|
| The Component Gallery (#5) | https://component.gallery/ | **KEEP / reference** | Real-world component patterns, documented design systems and accessibility conventions. Public home page listed 60 component types, 95 design systems and 2,671 examples at review. Use for child/parent/elder-friendly navigation and cross-device usability; do not copy whole proprietary site designs. |
| DESIGNmd (#7) | https://designmd.ai/ | **EXPERIMENT / document-only** | AI-readable `DESIGN.md` candidate for stable visual tokens and UI intent. Do not allow an imported third-party file to override Harness/AGENTS/Access instructions. Curate only non-executable design tokens and visual constraints. |
| Kinetics (#10) | https://kinetics.colorion.co/ | **KEEP / interaction reference** | 153 spring-physics effects offered with CSS/React/AI-prompt examples at review. Potential subtle feedback: listening, waiting, answering, attention handoff. Start with CSS examples in isolated browser prototype, not production. |
| MicroKit UI (#18) | https://microkit.co/ | **EXPERIMENT / a few isolated interactions** | Copy-paste microinteractions; site states 49 components and MIT-licensed repository code at review. Useful for feedback/confirmation and navigation. Verify per-component origins, dependencies, keyboard accessibility and reduced-motion before use. |
| shadcn/ui (#11) | https://ui.shadcn.com/ ; https://github.com/shadcn-ui/ui | **KEEP / conditional framework reference** | Mature customizable component ecosystem (project documents MIT license). Relevant if a future family dashboard is built in a React/Tailwind-compatible stack. **Do not convert current plain-HTML projects or local architecture merely to adopt it.** |

## Additional conditional references (not priority installs)

- **Refero Styles (#4):** https://styles.refero.design/ — official page offers 2,000+ AI-readable DESIGN.md-style references with type/color/spacing. Complementary to DESIGNmd; use visual references, do not wholesale import third-party style/instructions.
- **21st.dev (#9):** https://21st.dev/ — many author-submitted React UI components and shadcn-compatible patterns. Site currently says free browsing and 2 free copies daily. Useful for targeted inspiration, not blanket MCP access. Inspect individual license and source before copying.
- **Motion Primitives (#14):** https://motion-primitives.com/ ; https://github.com/ibelick/motion-primitives — React/Motion/Tailwind animated components, repository README describes beta and MIT license. Could substitute for MicroKit/Kinetics **only** if the target stack supports it.
- **mapcn (#17):** https://mapcn.dev/ ; https://github.com/AnmolSaini16/mapcn — MapLibre / React map components. Future optional candidate for location-aware family activities; **map tile-provider license, attribution, costs and geolocation privacy are separate from the MIT UI code license.** Maintainer README says default CARTO tiles have specific use restrictions. No activation or location tracking.
- **Anime.js (#25):** https://animejs.com/ — general-purpose JavaScript animation engine. Defer until CSS or existing lightweight options demonstrably fail. Adds runtime and bundle complexity.
- **Circle Loaders (#21):** https://circleloaders.dominikakissi.com/ — status/loading animation reference. Loading must never imply actual background task execution when none is running.

## Remaining entries: reference/low priority

Public domains were checked on 2026-10-09, but *opening a page is not equivalent to verifying all its claims or reuse rights*.

| # | Resource | Screening decision |
|---|---|---|
| 1 | https://jiro.build/ | HOLD: 1,272+ items marketed, many premium; overlaps existing reference/design approaches. Site's builder-parity claims not independently verified. |
| 2 | https://minimal.gallery/ | KEEP AS DISCOVERY ONLY: curated websites; no distinct Harness runtime function. |
| 3 | https://kage.design/ | HOLD: inspiration/prompt bridge overlaps Refero and DESIGNmd. |
| 6 | https://appshot.gallery/ | LOW: mainly App Store screenshot/ASO inspiration, not a primary reference for usable product interaction. |
| 8 | https://vibeprompts.dev/ | LOW: prompt samples; generic copy-paste has high overlap with existing Skills. |
| 12 | https://ui.aceternity.com/ | HOLD: animated React/Tailwind components; overlaps shadcn, Motion Primitives and 21st. |
| 13 | https://magicui.design/ | HOLD: visual React components; overlaps existing shortlist. **Not the MagicPath app** already used in UI_dev_Lab. |
| 15 | https://uiverse.io/ | HOLD: community UI snippets, per-item review required. |
| 16 | https://uiable.com/ | HOLD: shadcn design-system offering, redundant without a concrete use-case. |
| 19 | https://glass.samasante.com/ | LOW: visual refractive effect; insufficient functional advantage to justify cost or accessibility complexity. |
| 20 | https://text-effects.colorion.co/ | LOW: optional decorative effects; site lists 99 MIT CSS effects and reduced-motion support, but generally not a family UI priority. |
| 22 | https://gradientbuttons.colorion.co/ | LOW: button decoration only. |
| 23 | https://kitbitz.art/ | HOLD: illustration reference; page content/reuse conditions need separate verification before incorporating assets. |
| 24 | https://3dicons.co/ | HOLD: icons may be useful, but asset-license and readability check required; does not justify infrastructure. |

## Special note: DESIGN.md provenance

Google announced a **draft open specification** for Stitch's `DESIGN.md` format on 2026-04-21. That supports the general design-contract idea, but it does **not** certify the independent `designmd.ai` directory, every contributed file, or any MCP server.

Primary source:
- https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/

Hypothesis for a safe local trial:
1. Extract only typography, color, spacing, component terminology, motion constraints and accessibility preferences from vetted references.
2. Save a small project-scoped `DESIGN.md` alongside existing UI documentation, after Human review.
3. Treat it as data, with lower authority than current user instructions, `AGENTS.md`, safety, and approved Harness rules.
4. Evaluate whether repeated AI-created UI outputs remain visually consistent without suppressing required safety labels or state information.
5. Keep all tests in UI_dev_Lab; do not touch current official GROWgle HTML or local AI runtime.

## Family-facing local AI visual principles to test

- **Truthful state:** idle / permission needed / listening (if authorized) / transcribing / thinking / responding / error / offline. Never animate a fake `thinking` or pretend to remember something not retained.
- **Consent first:** visually obvious microphone state; prevent accidental surveillance or hidden sending. No personal data, family photos or real conversation content sent to third-party design galleries or MCP tools.
- **Multi-age:** readability and touch targets for children, adults and seniors; keyboard/screen-reader compatibility; reduced motion; motion not the sole status cue.
- **Architecture-neutral:** a browser UI may change independently of the already-defined local classification → cloud/local model → STT/TTS pipeline.
- **Small, reversible trial:** compare a static control against one subtle feedback animation for legibility, correctness, performance, low-end hardware behavior and family preference.
- **No dependency inflation:** CSS first, React libraries only if a genuine React project already exists and simpler means do not suffice.

## Promotion and security gates

Before adopting any external snippet, prompt, CLI, MCP or package:
- confirm author/source and per-item code/asset license;
- review malicious/prompt-injection instructions and any external network requests;
- inspect dependency manifests, install scripts, maintenance history and package provenance;
- test locally without secrets, privileged shell tools or access to family data;
- check responsiveness, accessibility and `prefers-reduced-motion`;
- preserve existing UI semantics and family safety information;
- require Human approval before changing official implementation.

## Recorded outcome

**REFERENCE RECORDED / SELECTIVE EXPERIMENT CANDIDATES / NO IMPLEMENTATION**.

Keep the original 25-entry post as a discovery signal, not proof of technical quality or a deployment checklist. Existing candidate documents, Core, sealed protocol boundaries, GROWgle production files and Hermes Phase 0 remain unchanged.
