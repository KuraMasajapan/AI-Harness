---
document_type: research_evaluation
date: 2026-10-26
project: Hermes Local Agent
decision: CANDIDATE
priority: A+
implementation: HOLD
---

# VoxCPM2 — Local TTS Candidate

Source: https://github.com/OpenBMB/VoxCPM

## Confirmed
VoxCPM2 is an open-source 2B-parameter TTS model supporting:
- Japanese and 29 other languages
- voice design
- controllable voice cloning
- streaming synthesis
- 48 kHz output
- Apache-2.0 code/weights
- CUDA inference
- vLLM-Omni serving
- llama.cpp-omni / GGUF ecosystem for CPU, Metal, CUDA and Vulkan paths

## AI-Harness relevance
Direct candidate for the future family local-AI voice layer:

text / agent response
→ local TTS
→ spoken output

Potentially reduces dependence on paid cloud TTS.

## Important limits
- GPU-free real-time performance on target hardware is UNVERIFIED.
- Voice cloning introduces consent / misuse concerns and should be bounded to authorized voices.
- Quality, latency, RAM/VRAM usage and Japanese naturalness must be measured locally.

## Decision
**CANDIDATE — A+**

Research only. Hermes Local Agent remains Phase 0 / NOT IMPLEMENTED.
