---
status: proposal
created: 2026-09-20
origin: ASTRA usage-limit / TRINITY optimization discussion
---

# ASTRA Work Compression

## Signal

Implementation-capable ASTRA time is a scarce resource.

During Pilot work, ASTRA was used not only for repository changes and tests, but also for requirement analysis, evidence organization, test design, long-form reporting, and repeated context reconstruction.

Many of those tasks may be performed earlier by cheaper or more available reasoning roles.

## Proposal

Optimize for **ASTRA work compression** rather than merely shorter prompts.

Use other agents and deterministic tools to transform a broad human request into a small implementation packet before ASTRA begins work.

Target flow:

```text
Human request
→ analysis / research / comparison
→ design + constraints + tests
→ Minimal Implementation Packet
→ ASTRA implements and executes
→ external review
→ only required deltas return to ASTRA
```

ASTRA should preferentially receive work that genuinely benefits from repository/tool execution:

- code changes
- integration
- build/test execution
- repository-grounded verification
- environment-specific actions

## Minimal Implementation Packet

A compact packet may include:

```text
TASK
FILES / SCOPE
DO
DO NOT
ACCEPTANCE TESTS
KNOWN UNRESOLVED
RETURN FORMAT
```

The packet should minimize rediscovery without hiding information necessary for correctness.

## Candidate optimization mechanisms

- source hashes and unchanged-file reuse
- context maps
- retrieval filtering
- tool-output truncation
- local deterministic preprocessing
- role-based pre-analysis
- prompt / prefix caching where available
- minimal-diff review
- reuse of prior verified artifacts

## Measurement principle

Do not optimize token count alone.

Measure whether equal or better quality is achieved with lower ASTRA usage, fewer retries, less elapsed time, or less human intervention.

## Important limits

Compression can remove necessary context.

Every optimization should be benchmarked against quality and failure detection.

Do not silently trade reliability for lower usage.

## Why preserve this proposal

If successful, each optimization cycle can increase the amount of future implementation work possible within the same scarce ASTRA budget.
