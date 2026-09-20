# Deterministic lifecycle

| Current state | Operation / condition | Next state |
| --- | --- | --- |
| CREATED | sealed task and identical clean A/B descriptors | ANALYST_RUNNING |
| ANALYST_RUNNING | first analyst seal | ANALYST_RUNNING |
| ANALYST_RUNNING | both analyst seals | ANALYST_SEALED |
| ANALYST_SEALED | comparator receives sealed inputs | COMPARATOR_RUNNING |
| COMPARATOR_RUNNING | comparator seal | COMPARATOR_SEALED |
| COMPARATOR_SEALED | logged human disposition | HUMAN_DISPOSITION |
| HUMAN_DISPOSITION | freeze exact response | FINAL_CANDIDATE_FROZEN |
| FINAL_CANDIDATE_FROZEN | binding check starts/completes | RELEASE_CHECK |
| RELEASE_CHECK | semantic result and RELEASE decision | RELEASED |
| FINAL_CANDIDATE_FROZEN / RELEASE_CHECK | explicitly freeze new candidate | FINAL_CANDIDATE_FROZEN |
| any nonterminal | explicit TASK_AMENDMENT | TERMINATED, then linked new run |
| any nonterminal | explicit termination / non-completion | TERMINATED |
| any nonterminal | invariant violation / recoverable integrity report | INVALIDATED |

Wrong-state calls are rejected. A/B descriptor divergence records RUN_INVALIDATED
before either start event. A/B never wait on peer negotiation. C starts once.
DENY leaves the run unreleased; a fresh candidate is required before new checks.

RELEASED, TERMINATED and INVALIDATED never transition back. A replacement-link
event or audit-only transcript repair can append without changing terminal state.
A terminal release attempt returns DENY without overwriting the recorded decision.

Every event increments event_seq exactly once; state-only transitions have no
independent mutable control channel. The first creation event initializes the
manifest; the second seals the task. Informational timestamps do not order events.
An inconsistent journal cannot accept a trustworthy recovery event and is refused
pending manual review.
