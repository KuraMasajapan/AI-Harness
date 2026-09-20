# Incident — Source-Lock Generation Drift

- Date: 2026-09-20
- Severity: High
- Outcome: Major near miss; no Source of Truth or GitHub state was corrupted
- Scope: Creation / image-generation execution and verification
- Status: Recorded for regression and workflow hardening

## Summary

During UIAP BASE PCB rough-placement exploration, the AI had already loaded the relevant project Source of Truth, but generated image artifacts that materially diverged from fixed project constraints.

The problem was not primarily missing information in the project Source of Truth.

A re-check of `projects/UIAPduino/UIAP_BASE.md` confirmed that several of the omitted or distorted elements were explicitly documented before generation, including:

- two 2×12 female sockets for the UIAPduino
- the requirement that 15 status LEDs follow the actual UIAPduino pin arrangement rather than becoming a single inline bar
- no status LED for GND
- right-side terminal blocks with corresponding socket access
- the educational requirement that connection points remain visually understandable

Therefore, the leading hypothesis is not "the design intent was absent from the Harness."

The critical failure is more specifically that correct source information appears not to have retained sufficient fidelity and priority across the handoff into the creation tool / image-generation execution context.

This remains a hypothesis until the handoff path is experimentally tested.

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

The revised failure chain is:

```text
Correct Source of Truth available
        ↓
ChatGPT retrieval / reading substantially succeeds
        ↓
important source constraints must cross the creation-tool boundary
        ↓
possible Constraint Handoff Loss
(relations / prohibitions / layout constraints lose fidelity or priority)
        ↓
image generator fills gaps with plausible visual completion
        ↓
artifact drift
        ↓
no locked-constraint verification gate
        ↓
artifact delivered
        ↓
retry edited the bad artifact instead of resetting to source
```

This is still an operationalization failure, but the most important unresolved point is now the **handoff boundary**:

> Available in the reasoning context does not prove that the same constraint reached the creation tool with sufficient fidelity and priority.

## Contributing factors

### 1. Constraint handoff loss is the leading root-cause hypothesis

The source itself contained several critical constraints that disappeared from or were weakened in the generated artifact.

The pattern was not purely random. In several cases, simple component nouns survived while relational or negative constraints did not.

Examples:

- "15 LEDs" survived, while "do not make a 15-inline LED bar; follow corresponding UIAPduino pin positions" did not.
- "terminal block" survived, while "terminal block with corresponding socket access" did not.
- "UIAPduino" survived, while the specified 2×12 socket relationship and exact board-grounding requirements were weakened or lost.

This suggests a possible transformation such as:

```text
Source:
component + relationship + prohibition + spatial intent
        ↓
creation handoff
        ↓
component noun survives
relationship / prohibition / spatial constraint weakens
```

This hypothesis must be tested directly. It should not yet be treated as a proven implementation fact.

### 2. Constraint compilation was missing

Even if the creation tool can preserve source constraints, the Harness did not create an explicit execution contract before the tool call.

The creation step should receive at least:

- LOCKED — must remain unchanged
- VARIABLE — intentionally open to exploration
- UNKNOWN — not yet decided; must not be fabricated as final
- FORBIDDEN — must not be introduced

The key requirement is not only to create these categories internally, but to verify that the relevant contents are actually carried across the tool boundary.

### 3. Tool-fit mismatch

The task required constrained technical layout exploration, while free-form image generation naturally tends to fill visual gaps with plausible-looking electronic detail.

For exact layout comparison, a deterministic diagram / SVG / CAD-like method may be more suitable than unconstrained photorealistic generation.

Image generation may still be useful for later visual concept work if the fixed geometry has already been established.

### 4. Verification was too weak

The generated artifact was not checked against the locked constraints before delivery.

A creation artifact should not pass merely because it looks plausible.

### 5. Failure recovery was wrong

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

### 6. Source contains historical states

`projects/UIAPduino/UIAP_BASE.md` intentionally preserves design history. It therefore contains earlier candidates that are later superseded.

Example:

- an earlier V0.2 candidate describes Grove 5V default + optional 3.3V and no BASE-side Qwiic
- the later 2026-09-19 final direction describes Grove 3.3V fixed and BASE-side Qwiic as a prototype candidate

This did not explain the most extreme generated deviations, because several violated requirements were already explicit in current project text.

It still exposes a secondary requirement:

> Before source-locked creation, determine which statements are currently effective rather than treating all historical sections as equally authoritative.

However, historical-state ambiguity should not be used as the primary explanation for this incident.

## Corrective action

The previously added creation gate remains necessary, but it is not sufficient until the handoff boundary is verified.

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

### Handoff verification experiment

Before declaring the root cause addressed, run a controlled image-generation test in which the creation contract is explicitly rebuilt immediately before generation.

The contract should include easily auditable constraints such as:

- 2×12 female socket ×2
- 15 GPIO LEDs
- LEDs must follow the corresponding UIAPduino pin positions
- 15 LEDs must not be collapsed into one straight status bar
- right-side terminal blocks must retain their corresponding socket-access structure
- no unapproved power / USB / wireless hardware

The test should distinguish three outcomes:

1. **Constraints are preserved**
   - supports the hypothesis that earlier failures were caused primarily by incomplete handoff / weak constraint packaging.
2. **Constraints still disappear**
   - indicates a deeper limitation in tool-boundary transmission, priority retention, or image-generation constraint adherence.
3. **Some constraint types survive and others do not**
   - identify whether relational, negative, count, spatial, or identity constraints are disproportionately vulnerable.

The experiment must compare the pre-generation contract with the actual artifact, not only with the model's verbal description of what it intended to create.

## Regression requirements

At minimum, regression evaluation should verify:

1. fixed project facts remain unchanged during creative variation
2. only explicitly variable dimensions are explored
3. unknowns are not presented as confirmed design facts
4. forbidden / unapproved elements are not introduced
5. tool choice matches the level of precision required
6. the compiled creation contract is actually represented at the tool boundary
7. relational and negative constraints survive, not only component nouns
8. a failed artifact is rejected before delivery
9. recovery returns to source constraints rather than recursively editing the invalid artifact

## Relation to existing Harness work

This incident strengthens:

- LESSON-010 Source-Locked Creation
- LESSON-009 Runtime Activation Is Distinct from Rule Existence
- Operationalization Gap candidate

It does not prove that all three share one root cause, but it is consistent with the broader pattern:

> Existence or availability does not guarantee operational effect.

A stronger formulation for this incident is:

> **Retrieved ≠ Handed Off ≠ Enforced ≠ Verified**

The missing link between "retrieved" and "handed off" is now an explicit investigation target.


## Controlled Clean-Room Evidence — 2026-09-20

Two clean-room UIAPduino-only generation tests were run in a new chat without supplying the earlier UIAP BASE concept images as direct references.

### Test 1 — Source read, weakly packaged constraints

The model was instructed to use the Harness and project Source of Truth, then generate UIAPduino Pro Micro CH32V003 V1.4.

Observed artifact:

- general identity was partially preserved: white small development board, USB-C, CH32V003-like device, Pro Micro-like form
- MCU changed to CH32V003F4P6 instead of CH32V003F4U6
- through-hole count expanded beyond the source-backed 24
- mounting-hole count became four instead of the source-backed three
- Arduino-like analog pin labels and other generic development-board details were invented

Result: **FAIL** for fixed-attribute preservation.

### Test 2 — Explicit minimal creation contract

A second clean-room prompt repeated the Source-of-Truth procedure but also promoted a small set of auditable attributes to explicit generation anchors:

- MCU = CH32V003F4U6
- through holes = exactly 24
- mounting holes = exactly 3
- board ≈ 17.8 × 33.0 mm
- USB-C
- white PCB
- explicit forbidden substitutions and invented features

Observed artifact:

- MCU text retained CH32V003F4U6
- 24 through holes were substantially preserved as two rows of 12
- three mounting holes were preserved
- USB-C and white PCB were preserved
- overall vertical identity improved markedly
- deeper structural fidelity remained imperfect: the physical MCU package / footprint and detailed component placement were still generic or incorrect

Result: **PARTIAL PASS** for explicit attribute preservation; **FAIL** for deeper physical-structure fidelity.

### Evidence interpretation

These two tests strengthen the Constraint Handoff Loss hypothesis.

The observed contrast is:

```text
Source read
        ↓
weak / implicit handoff
        ↓
F4P6 + too many holes + 4 mounting holes

Source read
        +
explicit generation anchors
        ↓
F4U6 + 24 holes + 3 mounting holes
```

This does not prove the internal implementation of the tool boundary, but it provides behavioral evidence that explicit creation-contract packaging materially improves preservation.

A second distinction is now necessary:

```text
Discrete explicit attributes
(name / count / color / connector type)
        ↓
can often be strengthened by explicit handoff

Deep structural attributes
(actual package geometry / exact component placement / exact board topology)
        ↓
still vulnerable to generic visual completion unless separately grounded
```

### Current incident model

The working model is now:

> **Source exists → retrieved → explicitly packaged for handoff → image model enforces some attributes → artifact gate verifies actual output**

The remaining unresolved question is how to preserve deeper relational and physical structure, not merely discrete labels and counts.
