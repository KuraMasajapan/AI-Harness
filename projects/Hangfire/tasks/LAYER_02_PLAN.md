# Layer 2 plan / pre-flight — 2026-09-27

READ CURRENT STATE: GitHub PR #2 merged by explicit Human request; development
4d03e065c3c1deebceebb0bf864dbadb5bd94974 fetched. PROJECT confirms Layer 1 complete.
Clean checkout on hangfire/layer-02-turn-resource; no AGENTS.md.
Read current ASTRA_START/PROJECT/README/SERVER_ARCHITECTURE/GEAR_COLLISION/
TUNING_POLICY, Layer 1 checkpoint/code/tests, and attached task (saved alongside).
Harness/core context retained, no relevant changes. Reference not required.
Baseline Layer 1 tests 7/7 PASS. PRE-FLIGHT PASS.

LOCKED: Layer 2 only, two fixed players, all game results Server-owned; preserve
Layer 1 formula/tuning/Canvas/standard-library architecture. No Layer 3 systems.
PROVISIONAL: A/B initial X=0/60; 100 resource; FIRE uses 20 resource/30 logical
delay; MOVE uses 2 per unit/10 logical delay, integer distance 1..20, default 5.
Tie: numeric nextActionTime ascending, then ID A before B. No wall-clock timer.
No refill/pass/elimination/winner invented. Resource exhaustion can stop progress;
restart resets prototype. No account or trusted identity: selector is hotseat test
input, never a claim of multiplayer authentication.

PLAN:
1. Central Layer 2 tuning; private game state/reducer; validate then commit once.
2. Reuse simulate with optional server-only launch X; no formula rewrite.
3. Gate BOTH /api/fire and /api/move on explicit actor + observed revision;
   revision rejects stale/duplicate requests, not a client-set game state.
4. Minimal current/resource/time/position table, actor selector, move controls.
5. Layer 1 pure tests unchanged; adapt two HTTP tests to actor/revision and state
   response, retaining ballistic/authority assertions. Add Layer 2 transition,
   insufficient-resource, malformed/state-injection, duplicate-request coverage.
6. Build/test/runtime, acceptance/omission, checkpoint, PROJECT, final close, STOP.

DEPENDENCY: none. Existing Node HTTP/tests/Canvas suffice.
SERVER_COST_IMPACT: one process, two-player in-memory state; event-driven actions;
no polling/timer/DB/queue/framework. Changes confined to projects/Hangfire.
