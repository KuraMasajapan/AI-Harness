# Feather Trigger — Phase 0 Validation Record

- Date: 2026-09-19
- Branch: development
- Status: PASS
- Scope: Minimal hypothesis validation only

## Hypothesis

A minimal external `activity_gap` signal can influence Context Freshness judgment when the receiver understands its semantics, without making elapsed time itself the decision maker.

Receiver Contract used in the controlled tests:

- `activity_gap` represents elapsed time since the last user activity.
- It is one signal that Context may be stale.
- It must not force reacquisition by itself.
- Reacquisition should also consider the current task and its dependency on fresh external state.

## Test Source

Primary mutable Source of Truth:

`experiments/feather-trigger/TEST_STATE.md`

Distractor/reference source:

`experiments/feather-trigger/REFERENCE_STATE.md`

The test chat was intentionally allowed to hold an older state while the primary source was changed externally.

## Results

| Test | Condition | Observed result | Result |
|---|---|---|---|
| Baseline | No Feather-specific receiver activation | Correct project continuation was possible, but no visible source reacquisition | Baseline |
| Stale / 18h | Mutable external source | FT-001 / ALPHA -> reacquired FT-002 / BRAVO | PASS |
| Stale / 5m | Mutable external source | Kept FT-002 / BRAVO; explicitly did not reacquire | PASS |
| Stale / 4h | Mutable external source | Reacquired FT-003 / CHARLIE | PASS |
| Stale / 45m | Mutable external source | Reacquired FT-004 / DELTA | PASS |
| Negative Control / 18h | Fixed chat-only context | Returned ORANGE without unnecessary reacquisition | PASS |
| Source Selection / 18h | Stale state + distractor source; source not named in prompt | Selected current work source and reached FT-005 / ECHO, not REF-001 / FOXTROT | PASS |

## Auxiliary Observation

Immediately before the Source Selection result, the UI briefly displayed wording including:

`可変の状態に直面しています`

This is retained only as auxiliary observational data. It is not treated as a reliable or complete trace of internal reasoning.

## Phase 0 Conclusion

PASS for the minimal hypothesis:

`activity_gap` can act as a lightweight external attention signal for Context Freshness when paired with a minimal Receiver Contract.

The observed behavior was not consistent with a simple rule of "long gap = always reacquire":

- 18h + mutable external state -> reacquisition
- 18h + fixed chat-only context -> no unnecessary reacquisition
- 5m + mutable but recently used context -> no reacquisition
- 45m / 4h / 18h + mutable external state -> reacquisition in these trials

No fixed time threshold is inferred from these results.

## What Phase 0 Does NOT Prove

Phase 0 does not prove that:

- Feather Trigger is a finished product.
- `activity_gap` is automatically captured or injected.
- a new chat automatically knows the Receiver Contract from Harness/Core.
- 5m, 45m, 4h, or 18h are universal thresholds.
- the same behavior will reproduce across all models, sessions, tools, or future platform versions.
- source selection is universally reliable.
- the brief UI status text exposes the model's true internal reasoning.

## Phase Boundary

Phase 0 ends here.

The next implementation target remains V0.1:

1. save `last_user_message_at`
2. calculate elapsed time on the next user send
3. inject minimal metadata such as `[activity_gap: ...]`
4. keep the external mechanism lightweight
5. do not add conversation storage, vector databases, project IDs, or a large session-management layer unless later evidence requires them

## Experiment Integrity Notes

During Phase 0, several Harness-level observations emerged but were not promoted into Core as part of the experiment:

- Receiver Contract requirement
- Cross-chat continuity/leakage as a confound
- Decision Integrity / constructive dissent
- Prospective Memory and Capture Guarantee
- Delegated Capture with human gates for important changes
- Tool Availability awareness
- Source Selection and distractor-source handling
- Human Error Tolerance
- Action Handoff: when the human is acting as the browser/test actuator, provide the next concrete operation in the same response
- External Permission Gate behavior was not consistent across all GitHub writes and therefore remains an observation requiring review

These should be evaluated through the LESSON process rather than silently becoming Core rules.
