# LOCAL AI SOUL × Local Speaker Identification (2026-10-25)

Status: **CANDIDATE / concept only; NOT IMPLEMENTED**  
Origin: user discussion following CompreFace review, 2026-10-25  
Scope: family local AI / LOCAL AI SOUL concept; exact existing LOCAL AI SOUL specification **not yet reviewed**.

## Hypothesis (not an existing verified feature)
Speech could provide both transcription (STT: what was said) and speaker identification (who likely spoke). LOCAL AI SOUL could use the speaker hint to select an appropriate conversation profile or memory scope, without sending biometric speaker embeddings to a cloud LLM.

Proposed flow (conceptual):
microphone -> local speech processing -> STT + speaker identification -> low-trust person ID with confidence -> access policy / user confirmation -> LOCAL AI SOUL context selection -> response / TTS.

## Why relevant
- Natural hands-free family interaction; may reduce repeated manual profile switching.
- Fits local-first architecture and the AI-Harness Shared / AI-Specific / Private separation.
- Can complement or substitute face recognition, avoiding a camera.

## Security and uncertainty
- Speaker embeddings/voiceprints are biometric-like personal data; retain only if necessary, with consent and clear deletion paths.
- Recording replay, synthetic voice cloning, TV audio, background speakers, children’s changing voices, illness and noise can cause misidentification.
- Speaker recognition is **not authentication**. For private memories, secrets, purchases or permissions, require separate confirmation and enforced access controls.
- Keep raw audio and voice embeddings local; cloud LLM receives at most a minimal authorized context identifier, and only after authorization.
- Check whether LOCAL AI SOUL actually exists as a defined project and its current architecture before creating files or dependencies around it.

## Minimum future evaluation
Compare manual selection vs speaker ID for latency, false identity matches, child/adult variation, opt-in/opt-out, privacy and hardware load. Begin with an offline, consented toy dataset only if approved.

## Decision
**CANDIDATE / HOLD implementation**. Preserve as an idea; do not install speech recognition, collect voiceprints, change ACCESS, or declare LOCAL AI SOUL specifications.