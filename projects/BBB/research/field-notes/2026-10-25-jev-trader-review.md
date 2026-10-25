# Jev trader — BBB-specific research note (2026-10-25)

**Status:** HOLD / RESEARCH ONLY. No live trading, no strategy adoption, no changes to BBB.

**X source:** https://x.com/GitTrend0x/status/2113986396062925178
**Primary source:** https://github.com/jarrodwatts/jev-trader

## Verified project description
- A prototype for the Monad/Kuru MON-USDC order book; Jev selects a buy/sell direction approximately once per ~300ms block and the system places post-only maker orders.
- With no `PRIVATE_KEY`, the README states it dry-runs on real order-book data with simulated fills. `MODEL=jev` and a TypeSafe API key are required to use Jev; default mock mode uses a heuristic.
- The project's README documents event telemetry including model latency, block decisions, quotes, fills, position, fees/gas and P&L. Live order submission exists; it is not merely a harmless analytics dashboard.
- The ~300ms figure is the underlying block cadence and project target, **not** evidence of consistent latency, execution success or profitability.

## Relevance to Bitbank_bot (BBB)
- Research candidates: separation of model intent from execution, deterministic safety checks, dry-run/live boundary, event logs, latency and late-decision handling.
- Weak direct fit: Monad/Kuru on-chain market-making is different from BBB's bitbank BTC/JPY strategy and existing Training Lab / Forward Gate. Porting the strategy would be unjustified.
- Major risks: private keys, real-order capabilities, fees/gas, latency-dependent market making, inventory exposure, data leakage, false confidence from simulated fills.
- Any performance or risk comparison would require controlled data and independent validation. No claim of profitability.

## Evaluation questions
1. Which telemetry concepts are absent from BBB's current decision journal and execution parity audit?
2. Are 'decision', 'intent', 'order sent', 'acknowledged', 'filled', 'cancelled', and 'rejected' represented separately?
3. Can late decisions, missing quotes and execution drift be detected without modifying frozen strategy/Forward OOS data?
4. Can any useful design be adapted without adding on-chain dependencies, live order permissions, or new paid APIs?

## Decision and boundaries
- **HOLD** as a domain-specific reference implementation. No installation or integration.
- BBB research notes remain separate from general AI-HARNESS Jev research.
- Prior BBB trading OSS review: `projects/BBB/research/field-notes/2026-10-25-trading-oss-review.md`.
- Implementation requires a separate proposal and explicit Human approval.
