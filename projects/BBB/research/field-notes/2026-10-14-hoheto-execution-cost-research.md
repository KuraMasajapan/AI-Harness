---
status: research-candidate
created: 2026-10-14
scope: BBB / Shadow Training / Execution Parity
source: https://note.com/hht
evidence: article-primary-source-read; BBB-reproduction-pending
implementation: not-yet-approved-as-strategy
---

# Hoheto / note — Execution-cost-aware research intake (2026-10-14)

## Intent and boundaries
Human direction (2026-10-14): use demonstrably useful principles, run staged verification for promising but unproven ideas, preserve findings while proceeding.

This is **not** a profitability claim or permission for Live trading.

Current BBB release known from local operation: v0.9.35 (Public Trading Constraints & Parity). Active Mean Reversion and Strategy Forward Freeze are not to be changed by research.

## Sources inspected (article text)
1. Hoheto, 2022-01-16, 予測力と執行戦略について
   - https://note.com/hht/n/nb7fcfe538c59
   - Author's 5-minute toy mean-reversion example shows cost-free profitability can disappear with a small modeled cost; author explains trade-off between forecasting horizon, turnover, expected return and fees/spread/slippage.
   - The example is illustrative, NOT a reproducible measured BBB edge.
2. Hoheto, 2026-02-17, Claude Codeとマーケット分析や投資戦略作成をする際のTips集
   - https://note.com/hht/n/n0a4574636276
   - Author emphasizes more reproducible idea exploration, not AI-guaranteed profits; mentions bitbank Discord's ほへと部屋 / beginner bot workshop (historic description only).
3. Hoheto, ccxtでResponse Headerに含まれるRate Limitなどを取得する方法
   - https://note.com/hht/n/n39030dec880d
   - Developer operations/observability candidate. Exchange-independent snippet must not be copied blindly.
4. Hoheto, 例のbot作るなら板くらい確認しておこう
   - https://note.com/hht/n/naa0c998b854d
   - Order book/market depth is relevant; illustrative venue is not necessarily bitbank.

Primary exchange documentation (for separate BBB rules):
- https://github.com/bitbankinc/bitbank-api-docs/blob/master/public-api.md

Existing related evidence:
- projects/BBB/research/field-notes/2026-10-12-grok-live-trading-lessons.md sections 1, 6, 14, 15, 17, 24 and 28.
This note adds a scoped experiment rather than duplicating generic fee/parity and live reconciliation principles.

## Verified BBB-specific trigger (user-observed UI)
v0.9.35 Execution Parity Audit:
- Next-open, cost-free: +0.39%
- Public bitbank taker reference + modeled slippage: -0.53%
- Original Forward: +0.38%
- Matching same-semantics trade count comparison: delta 0
These are **research/model outputs**, not actual fills, account PnL or evidence of tradable edge.

## Triage and 2-stage evaluation
### A. Use now as test methodology — CANDIDATE (A+)
- Always present gross and net returns together and attribute cost drag explicitly.
- Rank research candidates by net-of-cost results on an untouched chronological Holdout, alongside drawdown, turnover and trade count. Guard against tiny samples.
- Record execution-price assumption, data horizon, assumed fee/spread/slippage, fill model and data-coverage status with each run.
- Shadow-only evaluation; no automatic Active/FWD/Live mutation.

### B. Timeframe × cost sensitivity experiment — CANDIDATE (A+), requires reproduction
- Compare existing 5m reference against 15m, 30m, 1h (4h optional after first results).
- For each, use past-only signals and next-available-bar execution without future candles.
- Hold decision/evaluation horizon definitions explicit; never compare unlike exposure periods without normalization.
- Include fixed relative fee, stress cost and Buy & Hold; report exposure, turnover, net PnL, DD, PF, trade count, bootstrap or regime robustness where sample permits.
- Run on common chronological train/test split. Lock the untouched test period before tuning.
- **Fail/hold** if gains vanish net of costs or appear only in one thin/specific period.

### C. No-trade buffer / entry-threshold search — CANDIDATE (A), requires reproduction
- Do not adopt an externally suggested z threshold or optimized value as truth.
- In Shadow only, compare current z=2, exit_z=0 against a small fixed predeclared entry/exit grid with fees/slippage; penalize turnover and overly sparse trading.
- Limit degrees of freedom; a strong backtest alone is not enough for qualification.
- No implicit use of future price to decide whether a trade to be skipped.

### D. Maker-first / order-book-aware execution — HOLD
- Lower maker fee is not sufficient. Need fill probability, partial fills, non-fill opportunity cost and queue/latency assumptions.
- Verify bitbank current order types and venue-specific mechanics from official materials before using any such model for promotion.
- Current public trading constraints reference is informational, not account-specific executable fee.

### E. AI agents and high-frequency/live implementation borrowed from author — HOLD / REJECT for immediate BBB
- AI can help generate/tests, but no evidence to treat model output as an alpha predictor.
- Do not add autonomous live orders, leveraged/short trades or a new HFT infrastructure solely from anecdotal articles.
- Do not copy sample cost constants, particular strategy's claimed returns or another venue's order behavior.

## Proposed validation ladder
1. **Baseline parity:** reproduce v0.9.35 5m research net/gross accounting and ensure immutable Active state.
2. **Shadow experiment:** limited predeclared timeframe/threshold configurations, cache reusable candles, independent output directory; production-quality test coverage.
3. **Holdout/regime:** compare net returns and volatility regimes, detect small-n and overfitting; include no-trade baseline and B&H.
4. **Audit:** review assumptions, missing candles, execution timing, invalid fills and counterfactual trading constraints.
5. **Decision:** keep only independently repeatable candidate strategies for new frozen Shadow Forward; never silently promote existing Active champion.

## Recording conventions
- Every run should record hypothesis, accepted metric, rejection condition, time range, data coverage, code version and assumptions **before** examining results.
- Record negative outcomes; do not repeatedly re-tune to the same holdout.
- Stop short of CURRENT_SPEC promotion or implementation into Live until separate evidence and human review.

## Current status
Read and assessed. Experimental validation not yet completed. No profitability claim. No Active/Forward/Live changes authorized.
