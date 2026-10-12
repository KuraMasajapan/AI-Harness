---
status: research-notes
created: 2026-10-12
scope: BBB
evidence: mixed
promotion: human-gated
---

# Grok Live-Trading Lessons — Initial Field Notes

## Status

**Research notes only.**

These items were extracted from Grok-curated external reports and user-supplied article text.

They are not yet BBB requirements.

Article-specific claims and numeric thresholds remain unverified unless independently checked against primary sources or reproduced in BBB.

---

## 1. Production / Replay / Forward parity

### Source claim

One field report described a live system with a spread guard that rejected trades above a threshold, while its validation script assumed every asset could trade with one fixed round-trip cost.

The author reported that a meaningful fraction of backtest trades would never have been accepted in production and that correcting the mismatch materially reduced expected performance.

### BBB relevance

Candidate principle:

> A backtest or replay should not assume a trade is executable when production would reject the same trade.

Potential production constraints that may need parity:

- spread guard
- minimum order size
- available balance
- pending-order state
- risk limits
- price / amount precision
- exchange capability
- liquidity / depth constraints
- fees and expected execution cost

### Candidate direction

Prefer a shared or centrally defined set of **Trading Constraints** rather than independently reimplementing the same assumptions across Production, Replay, and Forward paths.

### Evidence status

**External field report / not independently reproduced in BBB.**

---

## 2. Shared constraints instead of duplicated validation logic

### Source claim

The same report described fixing one validation script while other strategy-specific validation scripts retained the old assumptions.

### BBB relevance

Duplicated execution assumptions can drift independently.

Candidate architecture:

```text
Trading Constraints / Execution Rules
             ↓
      shared definition
       ↙     ↓      ↘
Production  Replay  Forward
```

### Candidate direction

Where practical, deterministic execution constraints should have one authoritative implementation or one machine-readable configuration consumed by all relevant execution and validation paths.

### Evidence status

**Design candidate derived from external failure report.**

---

## 3. Independent calculation cross-check

### Source claim

An external implementation reported a large discrepancy between two implementations of the same portfolio calculation. Investigating the mismatch exposed a missing buy-side cost. After correction, the two calculations converged.

### BBB relevance

Important deterministic calculations may benefit from an independent checker.

Potential targets:

- PnL
- fee calculation
- portfolio value
- position quantity
- replay return calculation
- execution cost
- drawdown

Candidate rule:

```text
Primary calculation = A
Independent checker = B

A != B
→ do not trust result
→ investigate before promotion
```

### Boundary

Do not duplicate the entire BBB system. Use independent cross-checks only for high-impact deterministic calculations where divergence would invalidate conclusions.

### Evidence status

**External field report / strong design relevance.**

---

## 4. NO TRADE / SKIP reason logging

### Source claim

A live system appeared inactive for several days. Counting skip reasons showed that the system was generating signals but rejecting them because of execution constraints.

### BBB relevance

```text
NO TRADE != NO OPPORTUNITY
```

A no-trade state should ideally be attributable.

Possible reason codes:

- NO_SIGNAL
- SPREAD_REJECT
- RISK_REJECT
- BALANCE_SHORTAGE
- PENDING_ORDER
- DATA_MISSING
- API_ERROR
- CONFIDENCE_LOW
- EXCHANGE_CONSTRAINT

### Candidate direction

Aggregate skip/no-trade reason counts so the Human can distinguish market inactivity from execution or system constraints.

### Evidence status

**External field report / directly testable in BBB.**

---

## 5. Capture execution context on the decision path

### Source claim

One report noted that spread data was already fetched during entry evaluation, making it possible to record additional execution context at the same point without adding a separate collector.

### BBB relevance

When a decision path already has current market context, preserve useful observations at that moment where practical.

Potential fields:

- bid / ask
- spread
- depth / liquidity snapshot
- expected fee
- estimated slippage
- available balance
- pending-order state
- relevant market regime

### Candidate principle

> Prefer observing critical execution context on a path that already runs at the moment of decision, rather than creating an expensive always-on collector without clear need.

### Evidence status

**External implementation idea / requires cost-benefit validation.**

---

## 6. Execution Reality Gap

### Source claims

Multiple reports described differences between simulated assumptions and live execution, including:

- actual fee schedules differing from configured estimates
- maker/taker mix differing from assumptions
- slippage changing with volatility and size
- rounding affecting recorded amounts
- order/fill state differing from local assumptions
- timing granularity changing stop / take-profit outcomes

### BBB relevance

Candidate metric family:

```text
Virtual / Expected
        ↓ compare
Actual Execution
```

Potential measures:

- expected vs actual fee
- expected vs actual fill price
- maker/taker ratio
- slippage
- fill ratio
- rounding delta
- expected vs actual PnL
- rejection / fallback count

### Candidate direction

Treat execution quality as an independent evaluation dimension, not as a hidden implementation detail.

### Evidence status

**Multiple external reports; individual numeric claims not yet independently verified.**

---

## 7. Reconciliation after order submission

### Source claims

External failure reports described cases where exchange responses, local position state, order status, fills, and balances could diverge.

### BBB relevance

Candidate reconciliation chain:

```text
Order submitted
      ↓
Exchange order identity
      ↓
Order state
      ↓
Trades / fills
      ↓
Balance / holdings
      ↓
BBB Position Ledger
```

The principle is more important than any one exchange-specific workaround:

> An order request being accepted is not sufficient proof that BBB's internal position state is correct.

### Candidate direction

Before future live trading, define authoritative evidence for:

- order accepted
- partially filled
- fully filled
- canceled
- rejected
- unknown / unresolved

Unknown should not silently become success.

### Evidence status

**High-value operational candidate; exchange-specific behavior must be verified against bitbank primary documentation and live/paper observations.**

---

## 8. Pending order / duplicate-order protection

### Source claim

External systems have produced duplicate orders when a new cycle began while a prior limit order was still pending.

### BBB relevance

A new order cycle should consider unresolved orders first.

Potential flow:

```text
Pending order detected
      ↓
Reconcile with exchange
      ↓
OPEN / FILLED / CANCELED / UNKNOWN
      ↓
Only then decide whether a new order is allowed
```

### Boundary

A stale local "pending" flag should not permanently block the bot without reconciliation.

### Evidence status

**Operationally plausible and testable; exact implementation TBD.**

---

## 9. Risk Reject vs Emergency Stop

### Source claim

One implementation distinguished between rejecting the current order and stopping the bot itself after severe or repeated risk violations.

### BBB relevance

Candidate separation:

```text
Risk Reject
= do not execute this order

Emergency Stop
= suspend further trading until recovery / review
```

These are different controls and should not be conflated.

### Candidate direction

Future live mode may need explicit escalation from ordinary risk rejection to system-level halt.

### Evidence status

**Strong design candidate; thresholds not adopted.**

---

## 10. Safety mechanism verification

### Source claim

A reported kill switch falsely triggered because of a data-quality bug rather than a real portfolio loss.

### BBB relevance

A safety mechanism can itself fail.

Candidate chain:

```text
Market / account data
      ↓
Data validation
      ↓
Risk calculation
      ↓
Kill switch decision
      ↓
Reason / evidence log
```

Candidate principle:

> A safety action should be explainable from observable input and state.

### Boundary

Do not assume that "more safety rules" automatically means greater safety if the rules depend on unreliable data.

### Evidence status

**External field report / architecture relevance high.**

---

## 11. Central capital / position authority

### Source claim

One multi-bot failure example showed several bots independently attempting to sell the same asset and interfering with each other's assumed holdings.

### BBB relevance

If BBB later supports multiple strategies, each strategy should not independently assume ownership of the full exchange balance.

Candidate structure:

```text
Exchange Balance
       ↓
Capital / Position Authority
       ↓
Strategy A
Strategy B
Strategy C
```

Potential responsibilities:

- available capital
- reserved capital
- open positions
- pending-order reservations
- per-strategy allocation
- maximum exposure
- portfolio-level risk

### Evidence status

**Design candidate; future-facing for BBB.**

---

## 12. Position sizing as a first-class decision

### Source claim

A live strategy report used continuous position sizing rather than a binary all-in / all-out signal and described lower drawdown during a declining market, with reduced upside capture during a rising market.

### BBB relevance

Potential future separation:

```text
Signal / Confidence
      ↓
Capital Allocation
      ↓
Position Sizing
      ↓
Execution
```

The strategy should not necessarily have unrestricted authority to choose order size.

### Candidate direction

If BBB later maps confidence to size, begin with bounded deterministic tiers rather than unrestricted AI-generated sizing.

Illustrative concept only:

```text
LOW confidence    → small / no allocation
MEDIUM confidence → bounded allocation
HIGH confidence   → larger bounded allocation
```

No numeric thresholds are adopted here.

### Evidence status

**External field report + BBB design candidate.**

---

## 13. Capital Promotion / Demotion Gate

### Source claim

An external live-trading report predeclared conditions for increasing capital and paired them with conditions for reducing or stopping exposure.

### BBB relevance

Capital scale should not change only because recent PnL feels encouraging or discouraging.

Candidate promotion dimensions:

- minimum observation period
- execution health
- reconciliation health
- drawdown behavior
- virtual vs actual divergence
- unresolved safety incidents
- Human review

Candidate demotion dimensions:

- persistent execution degradation
- unexplained divergence
- unresolved safety-event triggers
- drawdown or loss beyond predefined tolerance
- state inconsistency

### Boundary

External numeric thresholds are not adopted.

### Evidence status

**Strong process candidate.**

---

## 14. Define what a strategy is trying to beat

### Source claim

A live regime-sizing strategy intentionally sacrificed upside capture to reduce downside and improve risk-adjusted behavior.

### BBB relevance

A strategy can appear to "underperform" while still meeting its intended objective.

Before evaluating a strategy, define its target:

- absolute return
- buy-and-hold excess return
- drawdown reduction
- Sharpe / MAR improvement
- tail-risk reduction
- capital preservation
- other explicit objective

### Candidate principle

> Strategy success criteria should be written before observing favorable or unfavorable results.

### Evidence status

**Generalizable process lesson.**

---

## 15. Timing granularity parity

### Source claim

Another field report described production evaluating prices at shorter intervals while validation evaluated only candle closes, causing strategy pass/fail outcomes to change.

### BBB relevance

A replay using candle-close data may miss events that production would observe intrabar.

Potential examples:

- stop-loss touch
- take-profit touch
- trailing stop update
- spread spike
- transient liquidity loss

### Candidate direction

For each strategy, explicitly document:

- production observation frequency
- replay data granularity
- intrabar assumptions
- pessimistic / optimistic tie-breaking behavior when exact path is unknown

### Evidence status

**External field report / high relevance to replay validity.**

---

## 16. Outcome vs process quality

### Source claim

A separate trading note argued that profitable outcomes do not prove rule compliance or decision quality.

### BBB relevance

Possible evaluation split:

```text
PnL
Process / Rule Compliance
Risk Compliance
Execution Quality
```

A profitable trade may still be a process failure, and a losing trade may still be a correctly executed rule-following trade.

### Candidate direction

Do not let accidental profitable violations become "good" learning examples.

### Evidence status

**General principle; useful but not independently novel.**

---

# Current Priority

Highest-value candidates from this first batch:

1. **Production / Replay / Forward parity**
2. **Shared Trading Constraints**
3. **Execution Reality Gap**
4. **Order / Fill / Balance / Ledger reconciliation**
5. **Capital / Position Authority**
6. **Position sizing**
7. **Capital Promotion / Demotion Gate**
8. **Risk Reject vs Emergency Stop**
9. **Independent deterministic cross-check**
10. **NO TRADE reason logging**

---

# Do Not Import Directly

Do not directly copy:

- another bot's spread threshold
- another bot's loss-limit percentages
- another bot's position-size percentages
- exchange-specific response handling
- article code snippets
- reported return multiples
- author-specific promotion thresholds

All such values require BBB-specific verification.

---

# Next Step

Continue collecting field reports.

For each new report:

1. extract only the operational lesson,
2. separate source claim from BBB inference,
3. avoid importing external thresholds,
4. verify primary exchange/API facts where relevant,
5. compare against BBB's current implementation before promotion,
6. request Human approval before any Source-of-Truth change.
