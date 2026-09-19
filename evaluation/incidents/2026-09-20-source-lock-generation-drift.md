# Incident — Source-Lock Generation Drift

- Date: 2026-09-20
- Severity: High
- Outcome: Major near miss; no Source of Truth or GitHub state was corrupted
- Scope: Creation / image-generation execution and verification
- Status: Recorded for regression and workflow hardening

## Summary

During UIAP BASE PCB rough-placement exploration, the AI had already loaded the relevant project Source of Truth, but generated image artifacts that materially diverged from fixed project constraints.

The problem was not primarily missing context.

The critical failure was that correct source information did not retain operational force through the creation pipeline.

Observed deviations included:

- UIAPduino CH32V003 V1.4 being visually replaced by an ESP32-like board
- incorrect or invented GPIO / LED counts and placement
- incorrect UIAPduino socket geometry
- Qwiic / Grove hardware being represented incorrectly or multiplied
- terminal / connector structures being invented or simplified without authority
- unapproved power / USB / other PCB features being introduced
- multiple "alternative" layouts remaining structurally too similar instead of exploring only the intended variable dimensions

After the first poor result, a later retry also used the flawed artifact as an editing base rather than resetting to the authoritative project constraints.

## Why this is a Harness incident

The Harness already had relevant protections:

- Project Source of Truth loading
- Physical Grounding Check
- Creation Task
- Verify / Correct loop

Those protections were present, but they did not jointly prevent the artifact from drifting.

The failure chain was:

```text
Correct Source of Truth available
        ↓
current-effective constraints not compiled explicitly
        ↓
creation tool allowed uncontrolled visual completion
        ↓
artifact drift
        ↓
no locked-constraint verification gate
        ↓
artifact delivered
        ↓
retry edited the bad artifact instead of resetting to source
```

This is an operationalization failure:

> Available constraints were not reliably converted into enforced constraints.

## Contributing factors

### 1. Constraint compilation was missing

The source was read, but fixed facts were not converted into an explicit execution contract.

The creation step should have received at least:

- LOCKED — must remain unchanged
- VARIABLE — intentionally open to exploration
- UNKNOWN — not yet decided; must not be fabricated as final
- FORBIDDEN — must not be introduced

### 2. Tool-fit mismatch

The task required constrained technical layout exploration, while free-form image generation naturally tends to fill visual gaps with plausible-looking electronic detail.

For exact layout comparison, a deterministic diagram / SVG / CAD-like method may be more suitable than unconstrained photorealistic generation.

Image generation may still be useful for later visual concept work if the fixed geometry has already been established.

### 3. Verification was too weak

The generated artifact was not checked against the locked constraints before delivery.

A creation artifact should not pass merely because it looks plausible.

### 4. Failure recovery was wrong

After a specification-drift failure, the flawed artifact should not remain the default base for iterative editing.

The correct recovery path is:

```text
Constraint violation detected
        ↓
reject artifact
        ↓
return to Source of Truth
        ↓
rebuild constraints
        ↓
choose appropriate tool
        ↓
regenerate from clean state
```

### 5. Source contains historical states

`projects/UIAPduino/UIAP_BASE.md` intentionally preserves design history. It therefore contains earlier candidates that are later superseded.

Example:

- an earlier V0.2 candidate describes Grove 5V default + optional 3.3V and no BASE-side Qwiic
- the later 2026-09-19 final direction describes Grove 3.3V fixed and BASE-side Qwiic as a prototype candidate

This did not explain the most extreme generated deviations, but it exposes another requirement:

> Before source-locked creation, determine which statements are currently effective rather than treating all historical sections as equally authoritative.

## Corrective action

Adopt the following minimal creation gate when an artifact depends on an existing Source of Truth:

```text
Current effective Source of Truth
        ↓
Constraint Compile
LOCKED / VARIABLE / UNKNOWN / FORBIDDEN
        ↓
Tool Fit Check
        ↓
Create
        ↓
Artifact Gate
compare against LOCKED + FORBIDDEN
        ↓
PASS → Deliver
FAIL → Reject → Source Reset
```

This gate should remain lightweight and should not be imposed on simple standalone creative work with no authoritative source constraints.

## Regression requirements

At minimum, regression evaluation should verify:

1. fixed project facts remain unchanged during creative variation
2. only explicitly variable dimensions are explored
3. unknowns are not presented as confirmed design facts
4. forbidden / unapproved elements are not introduced
5. tool choice matches the level of precision required
6. a failed artifact is rejected before delivery
7. recovery returns to source constraints rather than recursively editing the invalid artifact

## Relation to existing Harness work

This incident strengthens:

- LESSON-010 Source-Locked Creation
- LESSON-009 Runtime Activation Is Distinct from Rule Existence
- Operationalization Gap candidate

It does not prove that all three share one root cause, but it is consistent with the broader pattern:

> Existence or availability does not guarantee operational effect.
