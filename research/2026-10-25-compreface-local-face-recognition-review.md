# CompreFace — Local Face Recognition Research (2026-10-25)

Status: **CANDIDATE / future research; NOT IMPLEMENTED**  
Scope: AI-Harness / family local AI / possible visual identity input  
Source: https://x.com/aiexplorertim/status/2114168322959024128  
Primary source: https://github.com/exadel-inc/CompreFace

## Verified facts
- Exadel CompreFace is an Apache-2.0 self-hostable face recognition service with Docker Compose and REST APIs.
- Supports face detection, recognition, verification and optional landmark, mask and head-pose plugins; CPU/GPU model options.
- README lists Docker and modern x86/AVX as baseline requirements. Performance on the intended low-cost family PC is **not measured**.
- Self-hosting can avoid sending face data to an external recognition service if deployment and network paths are configured accordingly; it does **not** by itself prove an air-gapped or secure setup.

## AI-Harness value
Potential opt-in visual identification for choosing per-person conversation settings in a future family local AI. This is not needed for the initial voice-first design. Evaluate against lower-complexity alternatives: explicit profile selection, voice-based speaker identification, and device pairing.

## Risks / controls to test
- Biometric images/templates are sensitive and hard to replace if compromised. Local malware, theft, backups, unauthorized LAN exposure and misconfiguration remain risks.
- Face recognition is probabilistic. False matches, demographic/performance variation, photographs/replay spoofing and lack of liveness detection must be considered.
- Use recognition output as a low-trust identity hint, **never as sole authorization** for private memory, purchases or administrative functions.
- Require family consent, retention/deletion policy, access restrictions, encrypted storage where practical, and network egress review. Do not forward images/templates to cloud LLMs.
- Measure CPU load, latency, false accepts/rejects, Docker resource cost, and maintainability before any adoption.

## Secondary judgment
**CANDIDATE / low urgency**: useful future module, but privacy and operational burden outweigh near-term benefit. No installation, camera activation, collection of face data, or change to Core/ACCESS.