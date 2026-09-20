---
status: proposal
created: 2026-09-20
origin: public agent-method research discussion
---

# Role Pattern Library

## Signal

Public research, vendor guidance, open-source agent frameworks, and community practice contain many reusable role and orchestration techniques.

Reinventing each pattern locally would waste effort.

## Proposal

Treat public multi-agent knowledge as a **parts library**, not as authority.

Research and preserve useful patterns in a structured Role Pattern Library.

Candidate dimensions:

- Role Definition
- Knowledge Boundary
- Authority Boundary
- Handoff Contract
- Evaluation Role
- Bias Mode
- Memory Scope
- Orchestration Pattern
- Stop / escalation condition
- Expected cost and coordination burden

Candidate orchestration families may include:

- single agent
- sequential pipeline
- parallel independent analysis
- manager / worker
- orchestrator / workers
- evaluator / optimizer
- adversarial review
- specialist handoff

## HARNESS integration principle

External patterns should pass through:

```text
discover
→ understand claimed benefit
→ identify assumptions
→ adapt minimally
→ controlled test
→ compare against baseline
→ Human decision
```

Do not promote a method because it is popular or appears in a vendor guide.

## Relationship to dynamic teams

The Role Pattern Library could become the repertoire used by a future Dynamic Team Composer.

The composer would select among tested patterns based on task properties rather than inventing a team structure from scratch each time.

## Why preserve this proposal

The internet provides a large and continually growing source of candidate mechanisms.

A disciplined library can convert that abundance into reusable tested components without turning the Harness into a collection of unverified prompting tricks.
