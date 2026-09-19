# Latent Risk Scan — Exploratory Observations

- Date: 2026-09-20
- Branch: development
- Status: Observation only
- Scope: Exploratory probe after V0.1 controlled PASS
- Not a Core promotion
- Not a formal PASS/FAIL test

## Purpose

After the initial controlled Test A / Test B passed, an additional fresh-chat probe was used to see whether Latent Risk Scan could find important missing layers without being given a predetermined expected finding.

The probe was intentionally exploratory.

The tested AI was asked to review Latent Risk Scan V0.1 for important omissions before real operation, with emphasis on practicality, robustness, and simplicity.

It was **not** prompted with the expected terms:

- observability
- activation receipt
- trigger visibility
- Confirmation Firewall

## Observed Findings

The tested AI independently identified three missing or ambiguous areas:

### 1. Runtime activation path

The experiment exists in the repository, but normal runs do not yet have a guaranteed path that activates it.

Observation:

```text
rule exists
≠
rule is loaded
≠
rule is triggered
```

This is consistent with the broader Harness distinction between declarative files and runtime activation.

### 2. Trigger ambiguity

The V0.1 phrase:

```text
external write/action capability
```

may be broader than intended.

A normal low-risk write, such as a typo correction, could match the wording even though Test B demonstrated that this class of edit should not escalate.

Candidate clarification observed:

```text
new or materially expanded external write/action capability
```

This is an observation, not an approved wording change.

### 3. Post-detection behavior

V0.1 defines how to look for a missing layer, but does not yet define what happens after one is found.

Observed minimal distinction:

```text
material missing layer found
→ pause only the affected high-risk action and present the finding

no material missing layer
→ continue normal work
```

This is also an observation, not yet a Core rule.

## Expected Finding That Was NOT Found

Before the exploratory probe, the evaluator chat had considered another possible missing layer:

```text
The system may trigger internally,
but a human may not be able to tell that it triggered.
```

In other words, activation observability / an activation receipt may be missing.

The tested AI did **not** identify this.

This miss is important and must not be rewritten as a successful self-discovery.

The expected finding originated from the human's question about whether activation could be detected.

Therefore:

```text
activation observability
= externally prompted concern
≠ autonomous discovery in this probe
```

## Additional Error Exposed by the Probe

The tested AI stated that the controlled Test A / Test B results had not yet been stored in a durable source.

That statement was incorrect.

The results had already been committed to:

```text
experiments/latent-risk-scan/RESULTS.md
```

This happened because the tested AI had not loaded that file.

This exposes another possible failure mode:

```text
missing-layer scan
→ limited context
→ assumes an artifact or protection does not exist
→ false missing-layer finding
```

A future refinement may need to distinguish:

```text
not observed in current context
```

from:

```text
verified absent from the relevant Source of Truth
```

Do not turn this into a permanent rule yet.

## Interpretation

The exploratory probe produced mixed but useful evidence.

Positive:

- It did not merely reproduce the evaluator's expected answer.
- It independently found several plausible missing layers.
- It remained aligned with simplicity and did not require a large external framework.

Negative / unresolved:

- It missed activation observability.
- It made one false absence claim because its context was incomplete.
- It suggested Core promotion earlier than the current experiment process intended.

These outcomes are useful because they reveal limitations instead of only confirming the hypothesis.

## Real-World Observation #1 — Context Present, Self-Trigger Absent

A later observation occurred during ordinary Harness improvement work in another project chat.

The relevant Latent Risk Scan V0.1 context and recent validation information were already available to that run.

The task itself was strongly related to Harness improvement and therefore relevant to Latent Risk Scan.

However, the AI did not independently recall or invoke Latent Risk Scan during the work.

Only after the human explicitly asked whether the hidden-risk work had been considered did the AI connect the current task to Latent Risk Scan.

Observed sequence:

```text
relevant Latent Risk Scan context already available
        ↓
strongly related Harness-improvement task
        ↓
AI does not independently recall / trigger Latent Risk Scan
        ↓
human points to the hidden-risk topic
        ↓
AI makes the connection
```

Interpretation:

```text
knowledge was present
≠
capability was activated at the needed moment
```

This is best treated as a real-world observation of an **Activation / Recall / Routing Gap**, not a knowledge gap.

It is not a formal failure of V0.1 because the runtime activation path has not yet been promoted into Core, but it provides practical evidence that the earlier Runtime Activation Path finding is real rather than merely hypothetical.

Important distinction:

```text
rule exists
≠
rule is available in context
≠
rule is recalled
≠
rule is triggered
≠
rule affects action
```

The value of this observation is that it arose during normal project work rather than from a synthetic test.

## Current Decision

Do not modify Core yet.

Do not add more synthetic test cases immediately.

Return to normal AI-Harness / Proposal Incubator work and observe whether Latent Risk Scan:

- triggers spontaneously during real work
- finds genuinely useful missing layers
- remains quiet on low-risk work
- distinguishes unknown from verified absence
- avoids disproportionate mitigation
- exposes its own activation state when that becomes necessary

Future changes should be driven by repeated practical evidence rather than by expanding the experiment indefinitely.
