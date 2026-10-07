# Bitbank_bot Checkpoint v0.9.25

Date: 2026-10-07
Status: important observation checkpoint

## Version
- BBB v0.9.25
- Package SHA-256: b35240cece90e31e48101105dbac100c4125a6480871225a374a37c5f473de9
- Update method: Full ZIP. Delta/Patch method is paused.

## Forward validation baseline
- Freeze: 2026/10/05 21:36:40 JST
- UTC: 2026-10-05T12:36:40.316Z
- Latest baseline event: 2026/10/02 01:16:07 JST
- Baseline n: 8
- Forward events: 2
- Effective independent episodes: 1
- Overlap suppressed: 1
- Status: EARLY

## First forward episode
Two CFTC events occurred 1h20m apart, so their 24h observation windows substantially overlap.
- 2026/10/06 00:40 JST: anchor event
- 2026/10/06 02:00 JST: overlap event
- Event IDs remain separately auditable, but the pair counts as one effective market episode.

## Small-N guard
While Effective Episodes < 5:
- 24h Excess is reference/descriptive only.
- Ratio is marked REF / n<5.
- 95% CI is shown as N/A / n<5.
- Current descriptive 24h Excess: +0.90 pp.
- Current descriptive Median Excess: +0.90 pp.

## UI/runtime
- Replay completion preserves STATE = DONE.
- Forward OOS Event Audit shows Event time, Source, Event ID, Title, Control, Lane, Episode role, and dedupe state.
- Integrity check passed for the audited Regulation/ETF set.

## Latest observed data state
- Stored: 149
- Replay coverage: 148/149
- Standard: 122
- Extended: 26
- Waiting: 1

## Operating procedure
Start BBB when needed, run Import once, and only run Matched Replay when new cases are added. Then review Forward OOS Gate and Event Audit. Continuous runtime is not required.

## Next phase
Keep v0.9.25 as the observation baseline unless a correctness issue appears. Focus on accumulating genuinely independent Forward OOS episodes before drawing stronger conclusions.
