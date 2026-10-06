# Hermes Local Agent

Status: PLANNING / NOT IMPLEMENTED
Created: 2026-10-07

## Purpose

Evaluate Nous Research Hermes Agent as a future local-agent / Ground Station candidate.

The project is intentionally created before implementation so that the concept, constraints, and lessons can accumulate without committing to hardware or architecture too early.

## Current Decision

- Do not implement yet.
- GPU is not a prerequisite for starting the project.
- Initial experimentation, when started, should work on the existing PC where possible.
- Prefer gradual capability growth over building a large autonomous-agent system at once.
- Do not duplicate capabilities already provided well by ChatGPT Work or Codex.
- Focus on capabilities that remain useful across cloud models and future local models.

## Working Concept

Hermes is treated as a persistent local execution layer that may eventually connect:

- Memory
- Skills
- Shell / file operations
- AI-Harness
- Cloud LLMs
- Local LLMs such as Ollama

The long-term value to test is not merely "a local AI", but whether Hermes can become a reusable local operating layer whose accumulated skills and state survive model changes.

## Initial Evaluation Questions

1. Can Hermes be useful without a GPU?
2. What can be learned and retained through Memory and Skills?
3. How reliably can it execute local tools and file operations?
4. Can it work safely with a restricted folder / permission boundary?
5. Can it complement ChatGPT Work and Codex rather than duplicate them?
6. Can cloud and local models be switched without losing accumulated operational knowledge?
7. Does it reduce repeated context loading or unnecessary cloud-model usage?

## Safety / Scope Boundary

Until explicitly changed:

- No production automation.
- No autonomous destructive actions.
- No deletion, publishing, purchasing, external sending, or irreversible operation without Human approval.
- Start with read-only or low-risk local tasks.
- AI-Harness integration is a future experiment, not active behavior.

## Future Phases

### Phase 0 — Project Definition
Current phase. Preserve the idea and evaluation criteria only.

### Phase 1 — Minimal Local Trial
Install Hermes and restrict it to a safe test folder. Evaluate basic Memory, Skills, shell, and file handling.

### Phase 2 — AI-Harness Trial
Test whether Hermes can read project state, prepare context, and perform repeatable local support tasks without changing sealed / critical design areas.

### Phase 3 — Hybrid Model Trial
Compare cloud-model use with CPU-only local models. Measure speed, reliability, tool-calling quality, and cloud usage reduction.

### Phase 4 — GPU Decision
Only after real usage data exists, decide whether a GPU or dedicated local-AI PC is justified.

## Success Criterion

The project is successful if Hermes becomes a useful, model-independent local execution layer that reduces repetitive manual work while keeping Human control and clear boundaries.

The project is not considered successful merely because Hermes can run locally.
