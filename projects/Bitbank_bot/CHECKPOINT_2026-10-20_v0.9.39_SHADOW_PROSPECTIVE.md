# BBB Checkpoint — v0.9.39 Shadow Prospective Forward

Date: 2026-10-20 (JST). Stage: ZIP packaged; Windows UI acceptance pending.

## Release
- Full ZIP: `BBB_v0.9.39_SHADOW_PROSPECTIVE_FORWARD_FULL.zip`
- SHA-256: `991fe831f42929b893f49314c3fc0407c741a083ff4eae79c98d632a2e47581b`
- Tests: 288/288 PASS in source and clean ZIP extraction; Python and JS syntax PASS.
- ZIP resides in ChatGPT artifact storage, not GitHub.
- No API secrets or local trading data uploaded.

## Background
As of 2026-10-20, Active Forward (Mean Reversion) was VALIDATING with 3,482 5m candles, gross +1.37%, modeled public taker+slippage -0.99%; Execution Parity REVIEW. v0.9.38 Evidence Readiness UI was visually accepted by Human: Research OBSERVING, Economic NET NEGATIVE, Execution NOT IMPLEMENTED, overall LIVE BLOCKED.

Historical Shadow Buffer Lab selected a stricter entry buffer using development data, but its old historical Holdout was already observed. Repeatedly tuning the same holdout is not independent prospective evidence.

## What v0.9.39 does
New isolated Shadow Prospective Forward in Training Lab:
- Human presses `Shadow候補を今からFreeze` exactly once after installation.
- Wall-clock UTC Freeze timestamp, candidate chosen by existing development-only historical comparison, original Mean Reversion reference, hypothetical cost scenarios, and historical research fingerprint are retained as immutable `data/strategy_lab/shadow/prospective/freeze.json`.
- The old exposed historical Holdout is explicitly flagged. No historical trades are counted as prospective returns.
- Subsequent `Shadow Forward更新` downloads public BTC/JPY candles and evaluates only complete candles whose opening timestamp is newer than freeze; historical candles serve solely as indicator warmup.
- Paired next-open baseline/challenger results with cost-free, assumed-cost and stress-cost assumptions, net returns, DD, PF and closed trades saved in `data/strategy_lab/shadow/prospective/last_report.json`.
- The 30-day state remains REVIEW, not auto-qualified.
- No changes to Active Champion, Active Forward Freeze/history, Paper, Risk, Private API or Live eligibility. Live remains blocked.

## Deployment and next step
1. Preserve local `data`, `config.json`, local virtual environments. Overlay v0.9.39 Full ZIP while app is stopped, then launch.
2. Human opens Training Lab, presses Shadow freeze once, confirms new freeze timestamp.
3. On subsequent days refresh Shadow Forward once as desired; keep existing Active Forward observation daily.
4. Continue accumulating evidence without re-optimizing from the displayed forward samples.
5. Actual bitbank fees, order book, fill probability and production order-state recovery remain unverified.

## Notes
Study is model-only, not demonstrated profitable trading. Upstream research notes remain on development branch and are not automatically promoted to canonical strategy rules.
