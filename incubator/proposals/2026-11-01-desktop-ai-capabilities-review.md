---
document_type: research_evaluation
title: "Desktop AI capabilities — Orkas / Codex / Handy / OpenMontage / Vorssaint / Hex"
date: 2026-11-01
timezone: Asia/Tokyo
repository: KuraMasajapan/AI-Harness
branch: development
origin: Human-provided social-media roundup (five repositories) plus OpenCode Hex 3.0 announcement
scope: feature-centered comparative index; not six independent adoption proposals
status: KNOWLEDGE / FUTURE_VALIDATION_CANDIDATES
decision: MIXED_CANDIDATE_HOLD_REFERENCE
implementation: NOT_APPROVED / NOT_IMPLEMENTED
evidence: upstream repository metadata, README, specific code/release documentation checked; no local reproducibility/security test
human_authority: preserve research only; no promotion to Core, sealed TRINITY or existing project specs
tags: [desktop-ai, agent-orchestration, codex, hermes, local-voice, stt, hex, handy, video, opencode, macos, human-approval, cost]
trigger_topics: [Orkas, Commander, OpenMontage, Handy, Hex 3.0, Vorssaint, local voice dictation, desktop agent teams, multi-agent routing, video pipeline, Codex quota]
---

# Desktop AI機能横断評価 — 2026-11-01

## Purpose / Human decision

Human requested a **single, feature-centered research record**, instead of automatically creating one proposal per advertised OSS. Important individual proposals should be created only if a concrete independent validation project becomes necessary. Save research, **not** installation, product adoption, automation, authority expansion, or modification of working systems.

Scope: Orkas, OpenAI Codex, Handy, OpenMontage, Vorssaint, and the immediately preceding Hex 3.0 research. This is an **index and comparison of reusable functions**, not a new Agent runtime design. The user-provided social post is an intake signal; GitHub star increases and superlatives are not proof of performance or safety.

## Executive decision

- **Priority 1 / CANDIDATE / implementation HOLD:** Orkas's single desktop operator view, goal→task decomposition, cross-agent handoff, To-do/Auto-advance and scheduled work. **Compare to the existing ChatGPT→Codex→Human loop, TRINITY and Hermes; do not insert another orchestration layer without a measured gap.**
- **Priority 2 / CANDIDATE / implementation HOLD:** Handy and Hex are **competing desktop voice-dictation applications**. Compare Japanese accuracy, resource consumption, privacy and reliability on Windows. They are not direct replacements for Soul's full STT+VAD+TTS conversation stack.
- **Conditional CANDIDATE / implementation HOLD:** OpenMontage's video-production pipeline, approval gates, cost estimates and post-render checks. Compare with existing HyperFrames and Remotion references when there is an actual production request.
- **REFERENCE:** Codex is already a principal tool; avoid duplicating its repository study or treating it as a new proposal because of social popularity.
- **REFERENCE / low priority:** Vorssaint can inform Codex quota/status visualization, but is a macOS utility rather than a cross-platform agent runtime; official requirements are Apple Silicon + macOS 14+.

No runtime, dependency, connector, agent, skill, automation, OS setting, permission or model is being added by this entry.

## Functional feature map

| Capability to remember | Upstream | Potential use in AI-Harness | Existing overlap | Disposition |
| --- | --- | --- | --- | --- |
| Commander-style task decomposition, handoffs across Codex/Claude Code/OpenCode/Hermes | Orkas | One view for multiple existing executors; bounded handoffs | Dynamic Team Composition, TRINITY, Hermes, OpenRig, Codex CLI | CANDIDATE / HOLD |
| Durable project tasks, rules, per-agent memory, scheduled work | Orkas | Resume and operator overview; possibly reduce repeated briefing | GitHub checkpoints, workflow, Memory proposals, scheduling | CANDIDATE / HOLD; preserve Human authority |
| In-app model/provider choice and local endpoint support | Orkas | Evaluate policy-driven provider routing and budget awareness | Existing Codex model selection, Harness candidates | Compare only; not automatic savings |
| Push-to-talk/offline transcription into arbitrary app | Handy; Hex | Enter longer Codex/ChatGPT instructions without cloud STT fees | speech.cpp / Soul / OS dictation | CANDIDATE / HOLD |
| Vocabulary, term correction, per-app output rules | Hex; Handy's dictation customization | Better recognition of AI-Harness, UIAPduino and project terminology | Speech candidates and app-specific profiles | CANDIDATE / HOLD |
| Voice→text SDK/host integration | Hex (TypeScript SDK); Handy CLI controls | Evaluate *component* integration with Local AI Soul, if feasible | speech.cpp, Soul frozen V0.1 | HOLD; not a ready Windows Soul adapter |
| Video brief→research→script→assets→edit→QA | OpenMontage | GROWGLE, Soul or educational video production | HyperFrames, Remotion, short-video candidates | Conditional CANDIDATE / HOLD |
| Video cost preview, human storyboard approvals, final ffprobe/quality review | OpenMontage | Reusable approval/acceptance-check pattern | Human gates, evaluation, sealed TRINITY | Reference design only |
| Codex agent usage/limit status in a desktop UI | Vorssaint | Quota reset visibility and operator awareness | Codex status / usage page | REFERENCE; Mac-specific |
| Established local coding agent | OpenAI Codex | Current implementation executor | Already active | Existing solution; no duplicate proposal |

## Sources and detailed evaluations

### 1. Orkas — integrated desktop agent teams

- Source: https://github.com/Orkas-AI/Orkas
- Official description/README confirms: open-source MIT local-first desktop software; a Commander coordinating **16 built-in specialists**; external CLI sessions for Claude Code, Codex, OpenCode, OpenClaw and Hermes-Agent; projects with goal/rules/memory/files; manual and auto-advanced To-dos; schedules; connectors; Mac/Windows packaged app, Linux source route.
- Cost/edition boundary: packaged app advertises **500 starter credits** for its built-in model. Model execution is not unlimited free; supplied API keys/providers can incur separate charges. Packaged-app sharing, cloud sync and web publishing are not included in the open-source build according to README. Stored project data being local does not mean chosen model inference or integrations are offline.
- Differentiator: unified human operator UI over a heterogeneous team and ongoing deliverables, not raw code-generation strength.
- Risk: multiple agents can consume **more** context, tokens and subscriptions; self-improvement, auto-advance, schedules, external credentials and connectors require permission/authority containment. GitHub's sealed artifacts, writer-lock/fail-closed and Human release decision are **not** implicitly equivalent to Orkas's review model.
- **Stage 1 A++ → Stage 2 A+; CANDIDATE / HOLD.**
- Minimum experiment, only if separately approved: one bounded, non-sensitive read-only issue triage; single Codex baseline versus Orkas-supervised flow; compare total context/model use, retries, evidence integrity, step-by-step permissions, handoff loss and Human review burden. Do not use production tokens/credentials silently or run multi-agent schedules.

### 2. Codex — incumbent, not a novel discovery

- Source: https://github.com/openai/codex (Apache-2.0).
- Code agent available locally; already used in the user's development workflow. Social post's daily stars do not imply a newly launched Codex or any improvement in the user's usage quotas.
- Existing work on Codex Harness v1.5 is higher priority than adding a parallel management layer.
- **Stage 1 A → Stage 2 A; REFERENCE / no new proposal.**
- Reusable lesson: prefer well-scoped tasks and empirical token/quality comparison over assuming High thinking mode always produces better results.

### 3. Handy — offline desktop dictation

- Source: https://github.com/cjpais/Handy (MIT); https://handy.computer
- Confirms push-to-talk/toggle, local Silero VAD + speech transcription, pasted text, Windows/macOS/Linux. Model options and command-line remote controls are documented.
- **Important Japanese caveat:** upstream catalog lists **Parakeet TDT 0.6B v3** in 25 languages, **not Japanese**. For Japanese use, test a supported multilingual Whisper model rather than interpreting generic 'Parakeet v3 supported' as Japanese support.
- Its offline transcription claim is about its local ASR workflow; any optional enhancement or integrations need their own privacy review.
- Limits: Linux/Wayland may need additional paste tooling; clipboard restoration race is documented. No implication that local speech recognition automatically provides TTS or a full voice-agent API.
- **Stage 1 A+ → Stage 2 A; CANDIDATE / HOLD.**
- Compare *against Hex*, rather than evaluating as a new independent Soul specification.

### 4. Hex 3.0 — adjacent earlier research, kept in the same voice capability cluster

- Sources: https://github.com/anomalyco/hex ; https://github.com/anomalyco/hex/releases/tag/v3.0.0 ; original post https://x.com/opencode/status/2116555630236577819
- The **2026-10-31 v3.0.0** release supplies local-first dictation for Mac/Windows/Linux; Rust/MIT. Shortcuts, vocabulary, per-app text modes, optional OpenCode rewriting, CLI and model selection. Normal ASR does not require OpenCode or cloud voice transcription.
- The **fixed v3.0.0** source recommends **Whisper large-v3-turbo for Japanese** and SenseVoice Small as its faster choice; Japanese also appears in Qwen3-ASR 0.6B's model coverage. This is an upstream recommendation, not an independent Japanese accuracy benchmark.
- Privacy: dictated audio is not retained by default, but **transcript History defaults to 7 days**, whereas Soul V0.1 forbids persisting conversation history. Optional OpenCode text rewriting sends transcript/context to the configured model provider.
- Integration limit: the TypeScript SDK does **not** yet bundle a turnkey native helper, and the **Windows v3.0.0 build lacks the local transcription service**. It cannot be assumed drop-in for a browser-based Soul V0.1.
- User previously requested this research be saved; its standalone chat attachment is titled **2026-11-01-hex-3-local-dictation-ai-soul-review.md**. This cross-project index also retains the essential facts, so no second new GitHub proposal is necessary.
- **Stage 1 A+ → Stage 2 A+; CANDIDATE / HOLD.**

#### Voice comparison decision

- **Desktop assistant dictation**: Handy versus Hex; same Windows machine, Japanese adult/child speech and proper names; record character error rate, end-of-speech latency, offline behavior, RAM/CPU/GPU use, paste reliability and retained records.
- **Local AI Soul runtime**: existing human-preferred **speech.cpp** remains first evaluation candidate for **STT + VAD + TTS**. This preference is *not* displaced by a desktop dictation application.
- **Soul V0.1** remains frozen: Windows 10/11 browser+Node architecture, child-friendly dialogue, output safety before TTS, and **no persisted conversation history**. No wake-word, free-running agent or new dependency is authorized by this research.

### 5. OpenMontage — agent-led video production pipeline

- Source: https://github.com/calesthio/OpenMontage (AGPL-3.0).
- README claims a multi-stage research→proposal→script→scene/asset plan→production→render workflow with multiple pipeline definitions, tools, providers and skills; human creative gates, cost estimation/budgets, FFmpeg/Remotion/HyperFrames and post-render checks. Source availability supports the existence of these designs but **not** blanket claims of professional output, exact production cost or success in one prompt.
- Free/offline subset uses available footage, local TTS, editing/renders; some stock sources require accounts/keys and some assets have license constraints. Premium generation/stock/music/cloud services can incur usage costs.
- Existing overlap: HyperFrames/Remotion motion-design research and several short-video candidates already saved.
- Additional value: **budget- and acceptance-gated multi-step production**, reference-video decomposition, asset QA and reproducibility records. Human approval is relevant but the video application should not modify sealed TRINITY.
- **Stage 1 A+ → Stage 2 A; conditional CANDIDATE / HOLD.**
- Revisit only on a bounded, licensed, short video task. Compare using the simplest existing rendering stack, including total API spend, review steps, output quality and copyright clearance.

### 6. Vorssaint — macOS productivity toolkit / Codex quota visibility

- Source: https://github.com/vorssaint/vorssaint-utils (GPL-3.0-or-later).
- Mac utilities: per-app sound, system monitoring, window management, clipboard, screen tools and a developer section that advertises AI-agent quota/token/activity visibility including Codex. A utility, **not** a desktop AI team.
- Requirement: **Apple Silicon; macOS 14+**. Intel Mac users should not treat this as compatible.
- Caution: privacy/permission scopes differ by enabled utility; displays of token spend or quotas may be estimates or arrive after session updates.
- **Stage 1 B → Stage 2 B; REFERENCE.** Keep the **feature idea**, not a desktop app adoption requirement.

## Duplicate-control pointers — source-of-truth files that remain unchanged

1. Dynamic team composition: incubator/proposals/2026-09-20-dynamic-agent-team-composition.md
2. Agent OS comparison and existing ChatGPT→Codex→Human preference: incubator/proposals/2026-10-02-agent-os-oss-landscape.md
3. OpenRig orchestration precedent: incubator/proposals/2026-10-12-openrig-agent-team-orchestration.md
4. Local voice runtime baseline and Human's first-choice evaluation: incubator/proposals/2026-10-14-speech-cpp-local-voice-preferred-candidate.md
5. Local AI Soul frozen specification: projects/JARVIS_Soul_UI/V0.1_SPEC.md
6. HyperFrames/Remotion prior study: incubator/proposals/2026-10-12-hyperframes-html-video.md
7. Earlier short-video/media candidates: incubator/proposals/2026-10-21-open-source-research-media-tool-candidates.md
8. Hermes local agent phase and limits: projects/Hermes_Local_Agent/PROJECT.md

**No duplicate candidate files are created here.** If an individual experiment is approved later, link back to this index and the corresponding canonical proposal rather than copying them.

## Evidence limits and validation gates

- **Confirmed:** repository existence; publicly documented feature scope; metadata licenses at check time; v3.0.0 release contents; the existing AI-Harness files referenced above.
- **Not independently confirmed:** social-media “+N stars in one day” for every repository; the assertion that any one tool is the first, best or an overnight business success; end-to-end reliability, security, Japanese speech accuracy on the user's hardware, real cost savings, and cross-agent approval correctness.
- **Security/authority:** treat downloaded agents, skills, MCP servers, video-generating scripts, shell installers and connectors as untrusted until inspected. Use least privilege; review the exact action, workspace, output and network access before testing. Do not expose credentials, data, unpublished proposals or sealed artifacts.
- **Cost:** separate open-source licensing, hosted-model credits, API charges, Codex subscription quota, local compute and human review effort. More agents and more skills need not improve quality.
- **Licensing:** Orkas MIT, Codex Apache-2.0, Handy MIT, Hex MIT, OpenMontage AGPL-3.0, Vorssaint GPL-3.0-or-later; each bundled model, asset and content source may carry independent terms.
- **No operations performed:** no install, sample audio recording, outgoing API test, cost benchmark, workflow execution or automatic production.

## Revisit conditions / small tests

1. **Orkas:** only if the current workflow exhibits repeated, demonstrable cross-agent handoff friction and the claimed integration can retain Human decision and fail-closed controls.
2. **Voice:** only when a concrete dictation workflow or the Soul voice implementation is ready; test Handy versus Hex for desktop text input and speech.cpp separately for full-duplex conversation.
3. **Video:** only when an actual short-video deliverable is requested; start with a single, rights-cleared, low/no-cost example.
4. **Vorssaint:** optional if a compatible Apple Silicon Mac is in use and Codex usage visibility is genuinely missing.
5. **Codex:** optimize current work first and collect actual performance data rather than adding layers.

## Recall triggers

Orkas / 16 specialists / Commander / multi-agent desktop / auto-advance / Codex Hermes orchestration / GitHub stars not quality / Handy / Hex / Japanese Whisper / offline dictation / Local AI Soul / speech.cpp / video pipeline / OpenMontage / Backlot / HyperFrames / human approval / no autonomous integration / Vorssaint / Codex usage limits.
