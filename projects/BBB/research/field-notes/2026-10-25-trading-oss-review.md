# Trading OSS landscape — research note (2026-10-25)

Status: CANDIDATE / RESEARCH ONLY — not approved for implementation or production trading.
Source X post (2026-10-24): https://x.com/bi_9527zx/status/2113888235034386581

## Scope
Initial review of open-source trading software mentioned in the post for AI-HARNESS, especially Bitbank_bot (BBB). This is a research note, not a design decision, endorsement, performance claim, or permission to alter BBB.

## Primary-source checks and prioritization
- **NautilusTrader — CANDIDATE (priority)**: deterministic, event-driven research/backtest/live architecture; investigate parity between historical simulation and real execution, event ordering, and auditability. https://github.com/nautechsystems/nautilus_trader
- **VectorBT — CANDIDATE (priority)**: vectorized backtesting and broad parameter exploration; investigate isolated benchmarking and robustness/walk-forward testing without replacing BBB's current lab. https://github.com/polakowo/vectorbt
- **Freqtrade — CANDIDATE (priority)**: backtesting, dry-run, strategy optimization, FreqAI. Official exchange list does not explicitly name bitbank; do not assume direct bitbank support. https://github.com/freqtrade/freqtrade
- **CCXT — CANDIDATE (compare)**: exchange API abstraction; CCXT lists bitbank. Compare with BBB's existing direct API adapter; do not replace without evidence. https://github.com/ccxt/ccxt
- **Hummingbot — HOLD/COMPARE**: market-making framework, primarily different trading style. https://github.com/hummingbot/hummingbot
- **Condor (Hummingbot) — CANDIDATE (architecture only)**: agent harness separates LLM reasoning from deterministic execution, supports decision tracing and isolated P&L. Research applicability; do not connect live trading. https://condor.hummingbot.org/
- **OctoBot — HOLD/COMPARE**: GUI, AI/Ollama and automation integrations; likely overlap. https://github.com/Drakkar-Software/OctoBot
- **OpenTrader — HOLD/COMPARE**: GRID/DCA, paper trading, backtesting; check actual exchange integration rather than generic '100+' claim. https://github.com/Open-Trader/opentrader
- **OpenBB — CANDIDATE for financial-data research / NISA Scout**, not a BBB engine replacement. https://github.com/OpenBB-finance/OpenBB
- **AI Hedge Fund — HOLD (education only)**: README states it is educational and does not execute real trades. https://github.com/virattt/ai-hedge-fund
- **QuantConnect LEAN — HOLD**: comprehensive multi-asset engine, likely high adoption cost/overlap. https://github.com/QuantConnect/Lean
- **Meme Radar — HOLD / source discrepancy**: post describes AVE discovery, but current README describes GMGN discovery and GoPlus/DexScreener checks. Verify version and history before trusting the post's details. https://github.com/nhovongoc0-max/meme-radar

## Evaluation criteria for a second pass
1. Current BBB capabilities and overlap, particularly Training Lab, Forward Gate, replay, and execution parity.
2. Reproducibility: data alignment, timestamp semantics, fees/slippage, survivorship/lookahead controls, OOS isolation.
3. Security: exchange credentials, network boundaries, order authority, dry-run and human approval.
4. Integration cost: Windows/local operation, runtime dependencies, maintenance, API usage and licensing.
5. Empirical evidence: compare the same historical dataset and assumptions; no claims of improved returns without tests.

## Constraints
- Preserve BBB's ongoing Forward validation and frozen strategy; no retroactive fitting on OOS data.
- Research and implementation are separate. No installation, API key connection, order execution, automatic adoption, or code changes authorized by this note.
- GitHub stars and social claims do not establish profitability or safety.
- Any implementation requires a separate proposal, scope, and human approval.

Research order: NautilusTrader → VectorBT → Freqtrade → Condor; CCXT as a bounded adapter comparison.
