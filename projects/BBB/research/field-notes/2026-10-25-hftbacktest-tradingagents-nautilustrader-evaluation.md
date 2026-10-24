# BBB Research Field Note — HFT execution realism and AI trading stack

Date: 2026-10-25
Status: CANDIDATE / IMPLEMENTATION HOLD
Scope: Research only. No strategy, execution, or production changes.

## Source
- X post: https://x.com/carm1nee/status/2114057300365218005
- hftbacktest: https://github.com/nkaz001/hftbacktest
- TradingAgents: https://github.com/TauricResearch/TradingAgents
- NautilusTrader: https://github.com/nautechsystems/nautilus_trader

## Claim vs verification
The X post advocates combining three open-source tools into a free HFT trading stack. The repositories exist and document the claimed broad functionality, but this does **not** demonstrate profitability, parity on bitbank, or a viable low-cost HFT strategy. Low-latency competitive advantages, market data acquisition, integration and running costs remain unresolved.

## BBB-specific assessment
1. **hftbacktest — A+ research priority**: replay order book/trade tick data with feed/order latency and order-queue position. Strongest methodological fit for improving realistic fill simulation and extending Execution Parity Audit. However, BBB's existing 5-minute candles alone are insufficient. Must first verify bitbank BTC/JPY order-book/tick data availability, collection fidelity, history, timestamp alignment and costs. Do not add HFT execution or assume this will increase return.
2. **TradingAgents — A conditional**: multi-agent bull/bear debate, analysis, risk review; could be tested for news interpretation or decision explanations. Not evidence that multi-agent voting improves risk-adjusted return. May duplicate Sokudan, Macro Replay, current decision journal and existing LLM research; incurs complexity and API cost. Research only.
3. **NautilusTrader — B+ future candidate**: shared strategy semantics between backtest and live, event-driven Rust engine. Significant replacement/integration costs and no verified ready-to-use bitbank adapter. No immediate need to replace BBB engine.

## Existing BBB work to preserve
- Mean Reversion Champion frozen for forward out-of-sample evaluation.
- Forward Gate (WAITING/EARLY/VALIDATING/QUALIFIED or REVIEW) must remain intact.
- Execution Parity Audit and Paper execution logs remain primary evidence.
- Do not mix pre-freeze or optimization data into forward evaluation.
- Historical +1.77% strategy return was reported in an earlier research run, **not** a guarantee or evidence of live profit.

## Proposed staged experiment (not authorized implementation)
1. Audit existing spread, fees, slippage, latency and fill assumptions in BBB.
2. Check whether bitbank order-book/tick data can be collected and retained legally and affordably.
3. Independently compare baseline 5-minute bar assumptions vs realistic execution models on the same frozen signals.
4. Assess fills, net return after costs, drawdown, latency sensitivity and parity with paper fills; avoid look-ahead.
5. Only if material benefit is reproducible, propose a scoped change for Human approval.

## Decision
A / CANDIDATE; implementation HOLD. Prefer learning the execution-realism methodology to importing the full three-tool stack. Complexity and integration cost likely outweigh immediate value of a full rebuild. No installation, new strategy, live trading or Core/Trinity modification.
