---
status: proposal
created: 2026-10-26
decision: CANDIDATE
priority: A+
implementation: NOT IMPLEMENTED
---

# addyosmani/agent-skills — AI-Harness Evaluation

Source: https://github.com/addyosmani/agent-skills

## Why it matters
Portable skill workflows for Codex, Claude Code, Gemini CLI, OpenCode, Copilot and others.

Especially relevant:
- context-engineering
- source-driven-development
- doubt-driven-development
- constraint-driven-development
- debugging-and-error-recovery
- code-review-and-quality
- security-and-hardening
- observability-and-instrumentation

Skills are process-oriented, with checkpoints, verification gates and anti-rationalization guidance.

## AI-Harness relation
Strong overlap with RULES / WORKFLOW / Definition of Done / evidence requirements.

Do not import the whole pack automatically.

Use as an external reference implementation to compare:
- instruction loading
- verification discipline
- progressive disclosure
- failure recovery
- constraint preservation
- skill portability across agents

## Decision
**CANDIDATE — A+ / COMPARE**

No install, no Core change, no Codex configuration change.
