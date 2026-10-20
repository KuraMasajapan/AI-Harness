---
document_type: research_evaluation
date: 2026-10-21
timezone: Asia/Tokyo
subject: Six open-source research and media tools
stage_1_rank: MIXED
stage_2_rank: PENDING
decision: CANDIDATE / HOLD
implementation: NOT APPROVED
origin: Human-provided social-media post; preliminary chat review
branch: development
tags: [research, local-ai, retrieval, tts, media, oss, ground-station, candidates]
---

# Six OSS candidates — local search, research, speech and media production

## Scope and evidence
Human supplied a promotional post listing six GitHub projects, claiming a free end-to-end AI content factory and anecdotal earnings. This note preserves **interesting or potentially useful research leads**, not the post's claims as established facts. URLs below are research entry points; no repository installation, source audit, benchmark, integration test or commercial-use clearance was completed as part of this save. Prior chat gave a preliminary ranking. Any earlier mention of source verification should not be interpreted as a reproducible code/security audit.

## Candidate register

| Project | Upstream | Status | Why preserve | Critical questions |
| --- | --- | --- | --- | --- |
| DigUp | https://github.com/ARahim3/DigUp | CANDIDATE | Multimodal local file search could inform future Ground Station retrieval over PDFs/images/audio/video. | Mac-specific support vs Windows/Linux; indexing cost; local-only/privacy claims; search accuracy and hardware requirements. |
| Local Deep Research | https://github.com/LearningCircuit/local-deep-research | CANDIDATE / PRIORITY | Research workflow and citation generation may support a local research specialist. Compare with existing Grok collection, ChatGPT Work and AI-Harness evaluation. | Search source provenance; hallucinations; Ollama/local configuration; API/cloud cost; licensing; unattended operation and reproducibility. |
| Kokoro | https://github.com/hexgrad/kokoro | CANDIDATE / PRIORITY | Small-footprint TTS may serve family local AI voice output, even before a large local LLM is affordable. | Japanese voice quality; CPU-only latency; exact model/voice licenses; offline behavior; streaming integration. |
| Short Video Factory | https://github.com/YILS-LIN/short-video-factory | HOLD | Script/voice/subtitles/video pipeline may later help publish research or local community content. | Actual maintenance, dependencies, external APIs, output quality, rights, deployment cost. |
| AI YouTube Shorts Generator | https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator | HOLD | Long-form to short-form clipping may be useful for future outreach. | Highlight quality, subtitles, portrait reframing, rights and platform rules, compute cost. |
| Podcastfy | https://github.com/souzatharsis/podcastfy | CANDIDATE / LOW PRIORITY | Document-to-dialogue audio could provide accessible research briefings and learning material. | Japanese support, voice generation backends, cost, attribution, copyright, fidelity to source documents. |

## Proposed evaluation order
1. Local Deep Research: compare same bounded question against existing Grok + ChatGPT workflow. Measure factual accuracy, primary-source citations, cost, time and Human corrections.
2. Kokoro: short Japanese TTS samples on CPU-first hardware; measure latency, intelligibility, memory and licenses.
3. DigUp: examine indexing/search architecture, then judge portability to the intended Windows/Linux environment; avoid committing to a Mac-only stack.
4. Podcastfy: small offline-or-low-cost document-to-audio trial if an actual use case emerges.
5. Video tools: HOLD until a concrete video publishing workflow is requested.

## Claims not established
- “Free OSS” does not imply zero API/GPU/electricity/hosting cost, or unrestricted commercial use.
- Six independently useful projects do not constitute a proven interoperable production pipeline.
- The post's claimed earnings (JPY 10,000 anecdote) are unverified and not evidence of monetization.
- Automated clipping or republishing may require permissions and platform compliance.
- GitHub project presence alone does not establish security, maintenance or reliable output.

## Harness boundaries
- Research and implementation are separate; this is an incubator record only.
- No new dependencies, downloads, services, permissions or automation are authorized.
- Any integration touching local files, browser/network, shell or personal data requires least-privilege testing and Human approval.
- Revisit overlaps with existing research/agent/tool candidates before promoting any candidate.
- Do not update Core, Hermes Phase 0, Trinity or sealed boundaries on the strength of this note.

## Human decision
2026-10-21: Human requested preserving interesting projects and those with even modest positive research value. This note records all six, retaining HOLD status for lower-priority items rather than discarding them. Approval to **record** does not constitute approval to **implement**.
