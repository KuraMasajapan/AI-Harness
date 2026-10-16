# GitHub AI repositories TOP10 — research intake (2026-10-16)

## Status and provenance
- **Status:** RESEARCH ONLY / NOT IMPLEMENTED
- **Decision:** CANDIDATE (selected items), HOLD (others). No automatic adoption or changes to Core, Hermes, Trinity, or other projects.
- **Source:** User-provided Japanese social-media roundup describing "this week's trending AI repositories" (2026-10-16). Trending rank, time window, stars, and growth rate **not independently verified**.
- **Evidence:** Repository URLs and descriptions supplied by the user; initial review in conversation. This is an **intake / provisional evaluation**, not a code audit, reproduction test, security review, or complete upstream documentation verification.
- **Governance:** Read-only research allowed; further GitHub edits, installation, execution, permissions, and integration require separate Human approval.

## Intake: 10 projects

| # | Repository | Proposed function | Stage 1 | Stage 2 / current status | AI-Harness relationship / key uncertainty |
|---|---|---|---|---|---|
| 1 | [morluto/rea](https://github.com/morluto/rea) | Agent-assisted reverse engineering | A | HOLD | Security, analysis authorization, licensing, operational need |
| 2 | [mattpocock/skills](https://github.com/mattpocock/skills) | Engineering workflow skills | A+ | CANDIDATE / REINFORCE | Compare with existing Skills, RULES, WORKFLOW, handoff and test practices; avoid duplication |
| 3 | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | Diagram generation patterns | A+ | CANDIDATE | Visual specification fidelity and reproducibility; verify output format and dependencies |
| 4 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | AI-assisted video production | B | HOLD | Lower current priority; verify maturity and costs if use case emerges |
| 5 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Persistent context capture and recall | A++ | CANDIDATE / REINFORCE | Memory, Checkpoint, Hermes; verify integrations, data retention, privacy, retrieval quality |
| 6 | [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) | Free-tier access workflows for coding agents | B | HOLD | Terms, credential handling, stability, actual free limits |
| 7 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Knowledge-work plugins and patterns | A+ | CANDIDATE / REINFORCE | Skills and connectors reference; compare against existing ChatGPT workflows and permissions |
| 8 | [lyogavin/airllm](https://github.com/lyogavin/airllm) | Layer-wise inference for large models on limited GPU | A++ | CANDIDATE | CPU/GPU/RAM/SSD tradeoffs, actual latency, model support; not proof of practical realtime use |
| 9 | [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | Natural-language CAD generation | A | HOLD | Potential UIAPduino/mechanical prototyping use; verify precision, exports, licenses |
| 10 | [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) | AI-based SRE / incident operations | A | HOLD | Future agent monitoring; high permissions, production risks, excessive complexity for Phase 0 |

## Prioritized follow-up

### P1 — claude-mem × Hermes × Vercel Drives
Investigate **distinct layers** rather than assuming integration:
- claude-mem: recording, summarizing, searching, and recalling context;
- Hermes: agent runtime / tool orchestration;
- Vercel Drives: persistence of mounted work files across Vercel Sandbox instances.

**Hypothesis, not established fact:** these may complement one another for recovery and continuity. Verify actual adapters, supported versions, session isolation, sensitive data handling, failure recovery, deletion behavior, storage and runtime fees, and whether a simpler local-first arrangement works. Preserve Hermes Phase 0 / NOT IMPLEMENTED.

### P2 — mattpocock/skills × existing AI-Harness Skills
Compare individual practices such as specification clarification, TDD, diagnosis and handoff with existing skills and core rules. Select only demonstrated gaps; do not bulk install.

### P3 — airllm × local inference economics
Benchmark model loading, tokens/sec, peak RAM/VRAM, SSD footprint, model compatibility, power, and startup latency on representative hardware before purchasing a GPU. Running a model on low VRAM does **not** establish usable interactive performance.

## Other useful candidates
- diagram-design: candidate for visual checks on specifications and generated diagrams.
- knowledge-work-plugins: reference implementation for knowledge-work Skills and connector permission boundaries.
- rea, free-claude-code, OpenMontage, text-to-cad, opensre: HOLD pending concrete use case and security/cost justification.

## Required secondary verification
1. Confirm exact repository identity, maintainer, license, last commit, release history, and active maintenance.
2. Read upstream README, documentation, source, issues, PRs, and security notices; separate verified claims from social-media descriptions.
3. Reproduce a small **read-only or sandboxed** task, document environment and results.
4. Compare overlap with existing AI-Harness Core / Memory / Skills / Evaluation / Hermes / Trinity / LCU / Vercel research.
5. Review installation scripts, credentials, external API calls, persistence, network permissions, costs, and rollback.
6. Only then decide CANDIDATE / HOLD / REJECT with Human approval for any write or implementation.

## Decision boundary
This record is a research intake, not a specification change or adoption authorization. No code installation, integration, repository-wide edits, or production automation is authorized by saving this note.
