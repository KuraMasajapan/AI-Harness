---
status: proposal
created: 2026-09-20
origin: TRINITY multi-agent operating discussion
---

# Dynamic Agent Team Composition

## Signal

TRINITY demonstrated that useful work does not require one persistent AI identity or one visible window per role.

Fresh executors can be created for bounded roles, given only the required inputs, and discarded after producing artifacts.

## Proposal

Treat TRINITY as an early pattern for a broader **dynamic team composer**.

Instead of always using a fixed A/B/C structure, choose the smallest useful team for the current task.

Possible roles include:

- Planner
- Independent Analyst
- Designer
- Reviewer
- Adversarial Tester / Breaker
- Evidence Collector
- Specialist
- Auditor
- Synthesizer
- Implementation Engineer
- Coordinator

Possible patterns:

```text
small task
→ single agent

implementation task
→ planner + reviewer + implementation engineer

high-risk design
→ independent A/B + comparator + human

large research task
→ parallel researchers + synthesizer
```

## Bias as a controllable variable

Fresh context can reduce prior-conversation contamination.

Roles can also intentionally introduce a viewpoint such as:

- conservative
- adversarial
- minimal-change
- cost-first
- safety-first

The goal is not to eliminate all bias.

The goal is to make important viewpoints explicit and controllable.

## Memory model

Role executors should not require persistent personal memory.

Prefer:

```text
agent working memory = temporary
HARNESS artifacts / Source of Truth = persistent
```

A later executor should be able to reconstruct its task from durable artifacts.

## Important limits

More agents are not automatically better.

Additional agents add coordination, comparison, token, and latency costs.

Dynamic composition should optimize for the smallest team that provides meaningful risk reduction or parallelism.

## Why preserve this proposal

If validated, dynamic team composition could turn TRINITY from a fixed three-role protocol into a reusable orchestration primitive for many Harness workflows.
