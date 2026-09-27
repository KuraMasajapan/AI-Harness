# Layer 3 pre-flight / plan — 2026-09-27
Base: development 56f6e2b (PR #3 merged as 158c3ef; Human added Task).
Branch: hangfire/layer-03-hit-win; clean start.
READ/PRE-FLIGHT PASS: current ASTRA/PROJECT/Task, architecture/collision/tuning,
Layer 1/2 checkpoints/code/tests. Baseline 15/15 tests + syntax PASS; game code
unchanged between tested merge tree and current base. No reference needed.
PROJECT's Layer 2 complete state meets Task Start Gate; current explicit Human GO
selects Layer 3 despite historical stopped/current-layer entries.

PLAN: keep free-flight formula, add pure segment-circle/first-contact resolver;
derive independent visual/contact/hit anchors on Server; distance-based explosion;
apply all damage/HP/elimination then select surviving turn or finish atomically.
Reject eliminated/finished requests and all injected result fields.
Minimal HP/result UI and DEV-only checkbox for circle/blast markers.
Regression + collision/boundary/self/draw/authority tests; Browser; acceptance,
omission, checkpoint, PROJECT, final close, STOP. No Layer 4 systems.

Provisional values: HP100, hit offset(0,4), direct radius2, blast radius18,
direct damage60, blast max40, linear falloff exponent1. Direct victim receives
direct damage instead of double-counting splash; others (including shooter)
receive ceil(max*(1-distance/radius)^exponent) strictly inside blast radius.
Self has no immunity; launch Y8 initially outside own hit circle.
Earliest contact wins; exact terrain/gear tie favors terrain, gear tie ID order.
Both eliminated => finished, winner null (draw). No automatic resource refill.
Dependencies: none. Work on fire only, bounded path * two players, no idle loop.
