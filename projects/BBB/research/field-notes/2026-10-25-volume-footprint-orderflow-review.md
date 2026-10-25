# Volume Footprint / order-flow analysis — BBB research (2026-10-25)

**Decision: CANDIDATE / RESEARCH ONLY**
**X source:** https://x.com/chinpan2512/status/2113913930926194771 (2026-10-24)
**Follow-up:** https://x.com/chinpan2512/status/2113913934386483277
**Indicator lead from reply:** TradingView 'Volume Footprint: Measuring by Math & Geometry' by ata_sabanci.
**Indicator URL (lead, independently verify exact version and methods before use):** https://www.tradingview.com/script/Tm1cGCPD-Volume-Footprint-Measuring-by-Math-Geometry/

## Claim and interpretation
- X author describes a volume footprint visualization that displays buy/sell concentration at price levels.
- Author suggests high traded volume without corresponding price movement can indicate absorption by a large counterparty.
- **Absorption is a hypothesis**, not something a footprint plot proves; low price movement may have other causes.
- Aggressor-side volume imbalance is not synonymous with future price direction or a reliable entry signal.
- The linked TradingView script's methods/limitations must be checked against its current documentation and Pine source; a mathematical estimate derived from candles is not the same as actual tick/price-level trade data.

## BBB relevance
- Existing BBB has bitbank BTC/JPY candle data, Mean Reversion research champion, Training Lab, frozen Forward Gate and execution parity audit.
- Candles (OHLCV) alone cannot uniquely reconstruct individual fills, aggressor side or a true bid/ask footprint. Historical trades and/or order-book data may be required; verify bitbank API history and limits before designing a data collector.
- Candidate hypotheses: price movement conditional on abnormal volume, absorption proxy and imbalance persistence; evaluate as **separate research**, not as a live strategy change.
- Additional costs: high-frequency storage, missing trades, event-time alignment, fees, spread, slippage, websocket disconnects, clock skew, and retention limits.

## Research gates
1. Confirm exact data semantics (trades vs candles vs depth), buy/sell labeling and exchange coverage.
2. Establish reproducible calculations and data-quality audit (timestamps, gaps, duplicate fills, latency).
3. Define null hypotheses and controls; test with historical training data that does **not** overlap frozen Forward OOS.
4. Measure incremental predictive value versus BBB's existing features with fees/slippage and appropriate baselines.
5. Require separate Human approval before adding dependencies, network access, new signals or execution paths.

**Conclusion:** CANDIDATE for a BBB-only, read-only research experiment. No installation, production strategy change, Forward data contamination or live orders authorized.
