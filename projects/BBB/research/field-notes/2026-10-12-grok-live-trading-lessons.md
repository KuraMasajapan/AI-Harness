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


## 17. Execution Semantics Parity

### Source claim

A field report described production evaluating exits from a short-interval live ticker while validation evaluated exits only from candle closes.

The author reported that changing only the measurement semantics caused several deployed strategies to move from pass to fail, with trailing-stop strategies particularly affected.

### BBB relevance

A strategy name and parameter set are not sufficient to prove that Production and Replay are testing the same strategy.

Candidate strategy identity should include:

- entry rule
- exit rule
- observed price field
- observation frequency
- candle / ticker timing
- intrabar handling
- stop-loss semantics
- take-profit semantics
- trailing-stop update semantics
- tie-breaking when exact event order is unknown

Candidate principle:

> Production and Replay should be considered semantically equivalent only when they observe and react to market state under equivalent execution semantics.

### Evidence status

**External field report / high relevance to Replay validity.**

---

## 18. When Simulation and Production disagree, either side may be wrong

### Source claim

In the same report, candle-close validation initially appeared to be the defective side because production checked prices more frequently.

Further analysis reframed the result: the candle-close validator had measured a different but internally coherent strategy. The production implementation was then changed to behave like the better-performing validated semantics.

### BBB relevance

Do not automatically assume that validation must always be modified to imitate production.

When Simulation and Production diverge, explicitly compare three possibilities:

```text
A. Change Simulation to match Production
B. Change Production to match Simulation
C. Treat them as separate strategies and compare both
```

### Candidate principle

> A mismatch is evidence of semantic divergence, not proof of which side is correct.

The choice should be driven by explicit objectives, risk, and reproducible validation rather than convenience.

### Evidence status

**External field report / strong methodological candidate.**

---

## 19. Strategy Exit vs Emergency Hard Stop

### Source claim

After moving normal TP/SL evaluation to candle-close timing, the external implementation retained a separate high-severity hard stop that continued to monitor more frequently.

### BBB relevance

This supports a layered exit model:

```text
Strategy Exit
= part of the trading strategy's expected behavior

Emergency Hard Stop
= catastrophic-loss containment outside normal strategy semantics
```

The two controls should not be conflated.

### Candidate direction

Future BBB live-mode design should evaluate whether:

- normal exits belong to strategy semantics,
- emergency exits belong to risk containment,
- each layer has different observation frequency and evidence requirements,
- emergency actions are independently logged and explainable.

### Boundary

The external hard-stop percentage is not adopted.

### Evidence status

**External field report / reinforces Risk Reject vs Emergency Stop separation.**

---

## 20. New validation gates may need retrospective application

### Source claim

The external project had developed stronger validation methods over time, including random control comparisons, but previously deployed strategies had been accepted before those checks existed.

When the newer controls were finally applied retrospectively, several live strategies failed.

### BBB relevance

A validation framework can become asymmetric:

```text
New strategy
→ latest strict gates

Existing strategy
→ older weaker gates
→ continues operating by historical privilege
```

Candidate principle:

> When a materially stronger validation gate is introduced, explicitly decide whether existing strategies must be re-qualified under the new gate.

### Candidate direction

A future BBB strategy registry may need to record:

- validation version
- gates passed
- date last re-qualified
- unresolved legacy exemptions

### Evidence status

**External field report / strong lifecycle governance candidate.**

---

## 21. Control baseline should apply to adopted strategies, not only rejected ideas

### Source claim

The report found that random-control testing had been used mainly on rejected hypotheses, while already-adopted production strategies had never been subjected to the same control.

After applying the control to surviving strategies, the author used those results as additional evidence.

### BBB relevance

A control group is most valuable where it can challenge a strategy that is actually being trusted.

Potential comparison baselines:

- random entry / exit baseline
- buy-and-hold
- simple fixed-allocation baseline
- no-signal baseline
- other deliberately simple benchmark appropriate to the strategy

### Candidate principle

> A validation method should not be considered operationally useful if it is applied only to candidates that are already unlikely to be adopted.

### Evidence status

**External field report / method candidate.**

---

## 22. Predeclare falsification / acceptance criteria

### Source claim

The external report described opposing subagents declaring in advance what result would cause them to concede their position before running the next test.

### BBB relevance

This reduces post-result reinterpretation.

Possible use:

```text
Before test:
- expected claim
- pass condition
- fail condition
- decision if ambiguous

Then run test.
```

### Candidate principle

> For high-impact strategy changes, define the result that would falsify the proposal before observing the outcome.

This is more useful than allowing an evaluator to move the threshold after seeing results.

### Evidence status

**Methodological candidate; not a trading-specific rule.**

---

## 23. Intrabar ordering uncertainty

### Derived BBB concern

If historical Replay has only OHLC candles, the exact order of events inside the candle may be unknown.

Example:

```text
same candle:
High reaches TP
Low reaches SL
```

OHLC alone may not reveal which occurred first.

### BBB relevance

Replay must not silently invent an event order.

Possible explicit policies:

- pessimistic ordering
- optimistic ordering
- mark result unresolved
- retrieve finer-grained data when available
- exclude ambiguous events from selected evaluation metrics

### Candidate principle

> Unknown intrabar order should remain an explicit uncertainty unless finer-grained evidence resolves it.

### Evidence status

**BBB inference derived from the external timing-granularity failure; requires design review before adoption.**

---


## 24. Executable Edge / Dynamic Fee Model

### Source

`https://note.com/like_hyssop8403/n/n844e66b033e6`

External article describing a triangular-arbitrage bot operated in live markets.

### Two-stage evaluation

- **Stage 1 Rank:** A+
- **Stage 2 Final Rank:** **A++**

The detailed article was materially more valuable than the initial summary because it exposed several distinct sources of live execution error and quantified how small assumption errors accumulated over high turnover.

### Source claims

The author reported:

- 81 days of operation
- 35,997 orders
- final PnL of approximately -156,844 JPY
- notional turnover of approximately 236 million JPY
- a configured fee assumption of 0.0225% during a period where the actual applicable fee was 0.0300%
- the fee-underestimation interval contributing approximately -40,357 JPY, roughly 26% of the reported total loss
- many trades that would not have passed the entry threshold under the correct fee
- observed market-price discrepancy shrinking materially when executable order-book conditions were checked
- some fee/campaign conditions being overestimated while others were underestimated
- realized slippage not being the dominant loss source the author initially expected
- historical profit attribution requiring reconstruction from exchange execution records

These numbers are **author-reported field results**, not independently reproduced by BBB.

### ChatGPT evaluation

**Final importance: A++**

The strongest lesson is not "fees matter."

It is:

> **Observed Edge != Executable Edge != Actual Filled Edge**

A profitable-looking signal is not actionable until expected execution cost and actual market mechanics are included.

Candidate chain:

```text
Observed Edge
    ↓
Executable Edge
    ↓
Actual Filled Edge
```

BBB should eventually distinguish these states explicitly.

### BBB relevance — Dynamic Fee Model

A fixed fee constant can become stale or incorrect because actual cost may depend on:

- exchange
- symbol
- maker / taker status
- current account fee tier
- campaign / temporary discount
- rebate conditions
- account state
- order type

Candidate model:

```text
Expected Edge
- current fee
- spread
- estimated slippage
- rounding / precision effects
- execution uncertainty
= Executable Edge
```

If Executable Edge is not positive after conservative assumptions, **NO TRADE is a valid optimal result**.

### BBB relevance — Fee-tier economics

Lower fees are not automatically beneficial if obtaining or maintaining the lower tier requires additional turnover whose cost exceeds the fee saving.

Candidate principle:

> Evaluate the economic value of a fee tier net of the cost required to obtain or maintain it.

Do not optimize for fee percentage in isolation.

### BBB relevance — Order size / capital allocation

Execution cost may change with order size, liquidity, and market depth.

Therefore future Position Sizing should not assume:

```text
higher confidence
→ proportionally larger order
```

without checking whether a larger order materially worsens executable price or slippage.

This reinforces the separation between:

```text
Signal / Confidence
      ↓
Capital Allocation
      ↓
Position Sizing
      ↓
Execution Feasibility
      ↓
Order
```

### BBB relevance — Logging granularity

Post-mortem diagnosis becomes difficult if only aggregate trade-level PnL is retained.

Candidate execution record should preserve enough information to reconstruct:

- decision timestamp
- signal / expected edge
- expected price
- expected fee
- expected spread / slippage
- submitted order
- order identity
- fill(s)
- actual fill price
- actual fee
- realized slippage
- final reconciliation state
- resulting PnL

The aim is not maximum logging volume.

The aim is to retain the minimum evidence needed to explain why Expected and Actual diverged.

### BBB relevance — Hypothesis vs measured cause

The author initially suspected other causes such as slippage or inventory effects, but later reconstruction pointed to fee assumptions and opportunity quality as more important contributors.

Candidate principle:

> Record the initial causal hypothesis, but attribute loss only after reconstructing the actual execution evidence.

This helps prevent post-hoc storytelling.

### BBB relevance — NO TRADE as a successful decision

A bot that rejects a trade because executable edge is negative has not "failed to trade."

It has potentially avoided a negative-expectation execution.

This reinforces the need for explicit reason codes such as:

- EDGE_BELOW_COST
- FEE_TOO_HIGH
- SPREAD_TOO_WIDE
- LIQUIDITY_INSUFFICIENT
- SLIPPAGE_RISK
- EXECUTION_UNCERTAIN

### Parts not to import directly

Do not directly copy into BBB:

- the author's fee percentages
- the author's edge threshold
- Binance-specific fee-tier assumptions
- triangular-arbitrage-specific order sequencing
- the author's reported slippage distribution
- the author's turnover target
- campaign-specific behavior
- any claim that the same loss decomposition applies to bitbank

bitbank-specific execution cost must be derived from current official documentation and BBB's own observations.

### Evidence status

**Detailed external field report reviewed.**

- operational lessons: strong
- reported numeric results: source claim only
- BBB applicability: design-level inference
- bitbank-specific applicability: requires separate verification

### Candidate follow-up

Before BBB live trading, evaluate whether the execution layer can provide:

1. current applicable fee assumptions,
2. expected vs actual execution cost,
3. executable-edge calculation,
4. per-order reconciliation,
5. reason-coded NO TRADE decisions,
6. sufficient evidence to reconstruct PnL differences after the fact.

---

## 25. Live Reconciliation / Rounding Gap

### Source

https://zenn.dev/codecraft/articles/live-trade-reconciliation-rounding-gap

External field report describing a small live-trading pilot where the bot's internally recorded position cost differed from the actual cash decrease at the exchange.

### Two-stage evaluation

- **Stage 1 Rank:** A
- **Stage 2 Final Rank:** **A**

The detailed article reinforces BBB's reconciliation requirements, but does not justify promotion above A because part of the article's claimed "only discoverable in live trading" behavior is documented in official exchange materials and should be separated from genuinely undocumented execution behavior.

### Source claims

The author reported a small live pilot in which:

- the bot recorded a position cost of approximately 3,952.904 JPY,
- the actual cash decrease was approximately 3,956 JPY,
- the difference was approximately 3.096 JPY,
- order identity, quantity, price, and timestamp matched,
- the remaining discrepancy was attributed to exchange-side fee and rounding behavior.

The exact reported numbers are source claims and have not been reproduced by BBB.

### ChatGPT evaluation

**Final importance: A**

The important lesson is not the size of the discrepancy.

It is:

> **Order success does not prove ledger correctness.**

A trading system should reconcile the complete accounting path:

```text
Order
  ↓
Fill
  ↓
Fee
  ↓
Cash / Asset Balance
  ↓
Internal Position Ledger
```

If the final internal state differs from the exchange-observed state, the difference should remain visible until explained.

### BBB relevance — Reconciliation Delta

Candidate model:

```text
Expected Cash Delta
vs
Actual Cash Delta

difference:
├─ FEE
├─ ROUNDING
├─ SLIPPAGE
├─ PARTIAL_FILL
├─ EXTERNAL_BALANCE_CHANGE
└─ UNKNOWN
```

The important rule is:

> **UNKNOWN must not be silently absorbed as harmless rounding.**

Small unexplained differences can accumulate or mask a more serious state-consistency failure.

### BBB relevance — Source hierarchy

The article also exposes a useful research discipline.

Some exchange behaviors that may appear to be "live-only surprises" can already be described in official exchange documentation.

Candidate principle:

```text
Official specification
      ↓
Expected exchange behavior
      ↓
Small live pilot
      ↓
Observed behavior
      ↓
Reconciliation
```

Use the small live pilot to confirm and calibrate real behavior, not as a substitute for reading primary documentation.

### BBB relevance — Small Live Pilot as Execution Calibration

A small-capital pilot should not primarily be judged by profitability.

Its more valuable role can be:

- confirm fee behavior,
- confirm rounding / precision behavior,
- observe fill-state transitions,
- compare expected and actual balances,
- validate reconciliation,
- detect undocumented or misunderstood exchange behavior,
- measure execution reality before scaling.

Candidate progression:

```text
Paper / Replay
      ↓
Small Live Pilot
      ↓
Execution Calibration
      ↓
Reconciliation health
      ↓
Capital promotion decision
```

### Parts not to import directly

Do not directly import:

- GMO-specific rounding assumptions,
- GMO-specific fee rules,
- the article's exact JPY discrepancy,
- any assumption that all exchange-side differences are harmless,
- the claim that every observed behavior could only have been discovered with live funds.

bitbank-specific behavior must be checked against bitbank primary documentation and BBB observations.

### Evidence status

**Detailed external field report reviewed.**

- reconciliation lesson: strong
- exact numeric discrepancy: source claim
- GMO-specific mechanics: exchange-specific
- BBB applicability: design-level
- bitbank behavior: requires separate verification

### Candidate follow-up

For BBB, later evaluate whether live-mode accounting can expose:

1. expected fee,
2. actual fee,
3. expected cash / asset delta,
4. actual cash / asset delta,
5. reconciliation delta,
6. categorized cause,
7. unresolved UNKNOWN state.

---

## 26. Monitoring Latency / Execution Policy / Validation-System Risk

### Source

`https://zenn.dev/milkypeco/articles/3c813dd9d4648f`

External field report describing a bot whose live results degraded relative to paper / validation expectations because of execution slippage, client-side monitoring latency, regime-detection lag, and weaknesses in the validation process itself.

### Two-stage evaluation

- **Stage 1 Rank:** B+
- **Stage 2 Final Rank:** **A+**

The detailed article was more valuable than the intake summary because it connected multiple live-production failure modes rather than only describing slippage.

### Source claims

The author reported:

- live market-order slippage exceeding the backtest assumption during volatile periods,
- thin altcoin entries becoming negative expectancy after real execution cost,
- a client-side stop check running every 60 seconds and missing fast adverse moves,
- shortening monitoring to 15 seconds as one mitigation,
- switching from market orders to limit-oriented execution,
- adding a minimum stop width tied to ATR,
- a fixed walk-forward-analysis training window that may have overfit recent noise,
- a long moving-average regime detector reacting too slowly to a fast market transition,
- Forward validation being strengthened before further capital scaling.

These are author-reported operational findings and should not be treated as independently proven causal attribution.

### ChatGPT evaluation

**Final importance: A+**

The strongest lesson is broader than "slippage was too high."

It is:

> **Execution controls are defined not only by their threshold, but also by where and how quickly they are enforced.**

A stop rule that exists in configuration can still be ineffective if the observation / enforcement path is too slow for the market behavior it is supposed to contain.

### BBB relevance — Monitoring latency is part of the risk rule

Candidate model:

```text
Risk rule
    ↓
Where is it enforced?
    ↓
Exchange-side order
or
Client-side monitoring
    ↓
What is the worst detection / reaction latency?
```

BBB should eventually describe risk controls with both:

- threshold / trigger semantics, and
- enforcement location + maximum expected reaction latency.

A nominal stop percentage alone is not a complete safety specification.

### BBB relevance — Exchange-side vs client-side protection

When the exchange supports native stop / trigger order types, BBB should compare them against client-side polling rather than assuming all protection must be implemented in the local loop.

Potential dimensions:

- exchange-side survivability if BBB disconnects,
- trigger semantics,
- order-type availability,
- partial-fill behavior,
- cancellation / replacement behavior,
- latency,
- recoverability and reconciliation.

This should be verified specifically against current bitbank primary documentation before any live implementation.

### BBB relevance — Execution Policy, not Market-vs-Limit ideology

The article moved away from market-style execution, but BBB should not generalize this as:

```text
Market = bad
Limit  = good
```

Each shifts risk:

```text
Market
→ slippage / price uncertainty

Limit
→ non-fill / partial-fill / opportunity-loss / adverse-selection risk
```

Candidate principle:

> Choose order type through an explicit Execution Policy that measures the trade-off among fill certainty, latency, price quality, and missed opportunity.

Relevant metrics may include:

- fill ratio,
- partial-fill ratio,
- time-to-fill,
- realized slippage,
- cancellation count,
- fallback count,
- missed-opportunity estimate.

### BBB relevance — Validation systems also require validation

The article used WFA as an anti-overfitting control, but the WFA configuration itself became a source of questionable behavior.

Candidate principle:

> **A validation tool is not trustworthy merely because it is named WFA, Forward Test, Replay, or Risk Gate. Its own assumptions must be tested.**

Candidate chain:

```text
Strategy
  ↓
Backtest / Replay
  ↓
WFA / Forward / Validation Gate
  ↓
Validate the validator assumptions
```

Potential validator assumptions to expose:

- training-window length,
- test-window length,
- sample count,
- regime diversity,
- parameter-search breadth,
- data leakage boundaries,
- execution-cost assumptions,
- minimum evidence before pass / fail.

### BBB relevance — Regime detection has latency

A regime classifier should not be evaluated only by whether its labels look reasonable in hindsight.

Candidate additional metric:

- **Detection Lag** — how long after a material market-state change the classifier changes state.

This is relevant not only to technical regime detection, but potentially to future BBB fundamental / local-AI classification if such classifications ever influence live decisions.

### BBB relevance — Forward evidence before capital promotion

The article reinforces the idea that a change which improves historical validation should still gather forward evidence before capital is increased.

Candidate progression:

```text
Historical validation
      ↓
Forward / dry_run
      ↓
Execution-quality observation
      ↓
Small live pilot
      ↓
Capital promotion decision
```

The exact number of required forward trades should not be copied from the article.

### Parts not to import directly

Do not directly import:

- 15-second polling as a universal optimum,
- the author's ATR stop-width parameter,
- the author's WFA window lengths,
- the author's minimum number of forward trades,
- "market to limit" as a universal fix,
- the author's macro explanation for a specific market transition,
- any assumption that the same slippage profile applies to bitbank or BTC/JPY.

### Evidence status

**Detailed external field report reviewed.**

- execution-latency lesson: strong
- order-type trade-off: strong design relevance
- WFA critique: useful, but author-specific implementation
- regime-change causal narrative: partially inferential / retrospective
- BBB applicability: design-level
- bitbank-specific implementation: requires primary-source verification

### Candidate follow-up

For BBB, later evaluate whether the execution / validation stack can expose:

1. enforcement location for each risk control,
2. worst-case detection / reaction latency,
3. exchange-side vs client-side protection choice,
4. execution-policy metrics by order type,
5. validator configuration and assumptions,
6. regime detection lag,
7. forward evidence required before capital promotion.

---

## 27. Batch II — Order State Truth / Recovery / Reconciliation

This batch was selected from Grok-discovered live-operation incidents, then reviewed against the original public sources.

Common theme:

> **Events are evidence, not final truth. Reconstruct authoritative trading state before retrying, replacing, resuming, or escalating.**

### 27.1 Hummingbot #7294 — Failure Event followed by actual fill

Source: `https://github.com/hummingbot/hummingbot/issues/7294`

- **Stage 1 Rank:** A++
- **Stage 2 Final Rank:** **A++**

Observed log sequence:

- a market close order emitted `MarketOrderFailureEvent`,
- the client tracker marked the same order `FAILED`,
- milliseconds later the same client order ID received an actual fill,
- the executor then retried and another close order also filled.

The issue therefore provides strong direct evidence for:

> **Failure Event != Confirmed Failure**

Candidate order-state flow:

```text
SUBMITTED
   ↓
timeout / failure event / ambiguous response
   ↓
UNKNOWN
   ↓
exchange reconciliation
   ↓
FILLED / OPEN / CANCELED / REJECTED
   ↓
retry only if still required
```

This complements the existing rule that UNKNOWN must not silently become success:

> **UNKNOWN must not silently become failure either.**

Later issue investigation also exposed a second concern: strategy/controller semantics did not align cleanly with Hyperliquid's ONEWAY position mode. A later Hummingbot release note/comment suggested an ONEWAY close-order update may address the original issue, but the thread did not establish a clean reproduced closure of every failure path.

Candidate BBB principle:

```text
Strategy Requirements
        ↓
Exchange Capability Contract
        ↓
Connector Implementation
```

Before live execution, semantics such as order type, close behavior, precision, partial-fill handling, and exchange capabilities should be explicitly compatible.

Do not import Hyperliquid-specific ONEWAY handling or Hummingbot implementation code directly.

---

### 27.2 Hummingbot #7230 — Connection restored but trading state not recovered

Source: `https://github.com/hummingbot/hummingbot/issues/7230`

- **Stage 1 Rank:** A++
- **Stage 2 Final Rank:** **A++**

The issue reported that after a short network interruption:

- the transport connection returned,
- existing orders could be lost from local tracking and new orders could be submitted,
- the controller later stopped executing,
- `market_data_provider.ready` remained false,
- investigation traced this through `user_stream_initialized=false` to a `ws_assistant` that failed to recover.

The initial reporter believed the issue was Docker-only. Later maintainer investigation explicitly stated it was **not Docker-only**. The deeper root cause of why the user-stream assistant failed to recover was still under investigation in the thread.

Candidate principle:

> **Connection Restored != Trading State Recovered**

Candidate recovery barrier:

```text
DISCONNECTED
     ↓
RECONNECTING
     ↓
RECOVERING_STATE
     ↓
RECONCILING
     ↓
TRADING_READY
```

New orders should remain blocked until the required state is reconciled.

Candidate readiness dimensions:

- NETWORK_READY
- MARKET_DATA_READY
- PRIVATE_STREAM_READY
- ORDERS_RECONCILED
- BALANCE_RECONCILED
- POSITION_RECONCILED
- TRADING_ALLOWED

A single `ready=true/false` can hide both permanent freeze and premature resume.

Also separate:

```text
Liveness
= control loop is still progressing

Safety
= orders are allowed only from trustworthy state
```

Candidate watchdog signals include `last_market_data_at`, `last_private_event_at`, `last_control_loop_at`, and `last_reconcile_at` so a live process with a dead trading loop can be detected.

Do not copy workaround code that simply bypasses readiness checks. Avoiding a freeze is not sufficient if state integrity is unknown.

---

### 27.3 Freqtrade #11461 — Position adjustment semantics and cancel/replace

Source: `https://github.com/freqtrade/freqtrade/issues/11461`

- **Stage 1 Rank:** A++
- **Stage 2 Final Rank:** **A+**

Grok initially framed this as a confirmed duplicate-order race-condition bug. Detailed review changed that interpretation.

The exchange history showed both replacement-related orders fully filled, but the Freqtrade maintainer explained the behavior as consistent with the documented `adjust_trade_position()` semantics: if the callback returns a new adjustment while an order is open and its amount/price/direction differs, the framework may cancel the existing order and place a new one.

The key lesson is therefore not simply "Freqtrade duplicated an order."

It is the semantic difference between:

```text
Action command
BUY +X

vs

Target state
Desired position = Y
```

Repeated action callbacks can legitimately create repeated orders unless the strategy itself accounts for what has already filled or remains pending.

Candidate accounting dimensions:

- requested_qty
- filled_qty
- remaining_qty
- pending_qty
- target_position

Important rule:

> **requested_qty != remaining_qty**

Also:

> **Cancel requested != Canceled**

Candidate cancel flow:

```text
CANCEL_REQUESTED
       ↓
exchange reconciliation
       ↓
CANCELED / PARTIALLY_FILLED / FILLED / UNKNOWN
```

The issue also followed a framework behavior change introduced in the 2025.1 line, reinforcing:

> **Dependency updates can change execution semantics even when strategy code is unchanged.**

Future BBB preflight should consider strategy version, execution-engine version, CCXT version, and exchange/API assumptions together.

---

### 27.4 Staking reward false positive — safety gate halted entries for about 10 days

Source: `https://zenn.dev/codecraft/articles/staking-reward-false-positive-10day-halt`

- **Stage 1 Rank:** A++
- **Stage 2 Final Rank:** **A++**

The external report described an internal ETH record of approximately `0.0054` versus an exchange balance of approximately `0.00540325`, a positive delta of `0.00000325 ETH` (about 1.2 JPY in the report). The mismatch was attributed to automatic staking rewards and caused the bot's reconciliation guard to block new entries for roughly 10 days while exits continued.

The main lesson is not to relax reconciliation because the difference is small.

It is to preserve both **direction** and **provenance** of the delta:

```text
Reconciliation Delta
├─ NEGATIVE
│   ├─ fee
│   ├─ fill / ledger mismatch
│   ├─ manual / external withdrawal
│   └─ UNKNOWN
└─ POSITIVE
    ├─ reward
    ├─ deposit / manual change
    ├─ missing fill record
    └─ UNKNOWN
```

Candidate principle:

> **Known external mutation and unexplained delta are not the same state. UNKNOWN should remain visible even when the amount is tiny.**

The incident also demonstrates that a safety mechanism has a false-positive cost:

```text
missed real danger
→ loss risk

false positive
→ unnecessary halt / opportunity loss
```

The same article reported a separate data-coverage problem: an API provided deeper order-book data, while the bot retained only the top subset and then calculated a wider-depth liquidity metric from insufficient retained data. This supports:

> **Data available != Data retained != Data required by the metric**

Candidate Data Coverage Contract should make required depth, sampling interval, and observation coverage explicit.

The report also described repeated warnings every short interval that failed to attract attention. Candidate alert rule:

```text
state transition → notify
persistent state → update counter / dashboard
recovery → notify
reoccurrence → notify again
```

Do not import the article's specific tolerance rule as a universal safety threshold.

---

### 27.5 Gainium — partial fill during limit-order repositioning

Source: `https://community.gainium.io/t/limit-order-bot-behaviour/5328`

- **Stage 1 Rank:** A+
- **Stage 2 Final Rank:** **A+**

The report described a target entry of roughly 1000 LIT where a small partial fill occurred during dynamic limit-order repositioning. The bot treated the partial execution as if the entry had completed and failed to restore the remaining intended quantity. The provider identified the behavior and deployed a fix, though the thread still depended on later reproduction under the same timing condition.

Candidate principle:

> **PARTIALLY_FILLED must not be promoted to FILLED merely because the original order lifecycle ended.**

Target quantity should survive order replacement:

```text
Target Qty
   ↓
Placed Qty
   ↓
Filled Qty
   ↓
Remaining Qty
   ↓
Cancel / Reposition / Replace
   ↓
Remaining target intent survives
```

This complements Freqtrade #11461 from the opposite direction:

- Freqtrade case: repeated action intent can over-add.
- Gainium case: target intent can be lost after a partial fill.

Together they support target-state accounting rather than treating each order object as the trading intent itself.

---

### 27.6 Cross-case synthesis

These five incidents converge on a common architecture candidate:

```text
Intent / Target State
        ↓
Order Request
        ↓
Exchange / Connector Events
        ↓
Authoritative Reconciliation
        ↓
Confirmed Trading State
        ↓
Retry / Replace / Resume decision
```

Candidate rules:

1. **Event != Truth** — failure, cancel, reconnect, and completion events require state confirmation when ambiguous.
2. **Order != Intent** — target position or target quantity should survive individual order replacement.
3. **UNKNOWN is a first-class state** — do not silently coerce it to success or failure.
4. **Retry must be reconciliation-aware** — blind retry can duplicate exposure.
5. **Recovery needs a barrier** — reconnect is not sufficient to resume trading.
6. **Readiness is multidimensional** — transport, market data, private stream, orders, balances, and positions may recover independently.
7. **Safety and liveness are separate** — a running process can have a dead control loop; a live control loop can still be unsafe.
8. **Execution semantics are versioned** — framework, connector, and exchange capability changes can alter behavior without strategy-code changes.
9. **Reconciliation deltas need provenance** — positive/negative and known/unknown causes should remain distinguishable.
10. **Data coverage is part of metric validity** — a correct formula over insufficient retained data is still wrong.

### Batch evidence boundary

- Hummingbot #7294: strong log evidence for failure-event/fill divergence; later ONEWAY interpretation adds a second semantic issue.
- Hummingbot #7230: strong evidence for recovery/readiness failure; deepest root cause was not fully closed in the thread.
- Freqtrade #11461: exchange fills confirmed; duplicate behavior should not be recorded as a proven Freqtrade bug because the maintainer described it as expected callback semantics.
- Staking false-positive article: detailed external field report; article-specific exchange behavior and numbers remain external evidence.
- Gainium report: provider acknowledged and fixed the behavior, but exact timing reproduction remained part of follow-up.

These remain **research candidates**, not CURRENT_SPEC requirements.

---


## 28. Reported Performance Strategies — Stage 2 Research Batch

**Status:** Research only. These are external author-reported live or historical results, not BBB-verified profitability or approved trading logic. Ranks measure BBB research utility, not expected return.

### 28.1 DXY + Funding regime-based position sizing

Source: https://zenn.dev/koheikameyama/articles/e2ee191412e486

- **Stage 1:** A+; **Stage 2:** **A+**
- **Reported live period:** 2026-05-20 to 2026-07-28, approximately JPY 100,000 capital.
- **Reported comparison:** BTC/JPY -15.0% vs strategy total assets -3.0% in a selected decline period; in a reported rising month, buy-and-hold +9.18% vs strategy +2.98%. The strategy sacrificed upside participation.
- **Described logic:** DXY score weighted 0.6 and funding-rate score weighted 0.4 to choose continuous BTC allocation from 0 to 1, with daily 10:05 JST rebalancing; maker-first limit execution and a 300-second waiting policy.
- **Reported execution measures:** maker fill 78.6%, effective fee +1.46 bps, mean slippage 1.3 bps; the author also disclosed a kill-switch false trigger.
- **Evidence boundary:** author-reported results, not an independently audited track record. Selected periods do not establish general outperformance. The specific feature weights, funding source, rebalance schedule, and execution assumptions are not validated for BBB.
- **BBB candidate:** separate signal confidence, portfolio allocation, target position, and execution feasibility. Compare drawdown, upside capture, turnover, fee drag, and sensitivity to feature weights. Treat DXY/Funding as candidate external features, not proven predictors.
- **Do not import:** 0.6/0.4 weights, timing, 300-second wait, or reported execution statistics as bitbank defaults.

### 28.2 GridForge — bitbank grid trading + HODL+

Source: https://zenn.dev/soushu/articles/gridforge-update-live-trading

- **Stage 1:** A+; **Stage 2:** **A+**
- **Reported live pilot:** JPY 30,000 for seven days; 22 trades; **JPY 219 (+0.73%) realized grid profit**. The author subsequently described scaling to JPY 100,000 and a 100-level grid.
- **Described logic:** buy/sell on grid levels within a price range; liquidate above upper boundary, retain assets below lower boundary (HODL+ without stop-loss), rebuild grids after sustained deviation, and periodically re-read capital limits / reinvest profits.
- **Important distinction:** +0.73% is reported **realized grid profit**, not proof of +0.73% total portfolio return. Unrealized inventory loss, opportunity cost, and capital lockup may dominate.
- **Evidence boundary:** short, author-reported live window; no demonstrated multi-regime profitability. bitbank venue overlap is valuable but does not validate strategy edge.
- **BBB candidate:** benchmark grid realized PnL against mark-to-market total equity, buy-and-hold, fees, inventory exposure, drawdown, and time spent below range. Test range breaks and capital reservation in Replay.
- **Do not import:** the author's grid count, spacing, no-stop HODL+ rule, or capital scaling as BBB defaults.

### 28.3 Volatility breakout — transaction-cost falsification

Source: https://zenn.dev/neetux/articles/3b5fb3cc7f66fd

- **Stage 1:** A++; **Stage 2:** **A++**
- **Described rule:** daily buy trigger = current day open + 0.5 × previous day's high-low range; exit at the following day's open.
- **Reported validation:** bitbank BTC/JPY daily bars, approximately 2024-01 through 2026-09. The author reports about **-62%** with modeled trading costs versus **+35%** in a zero-cost scenario.
- **Cost explanation:** roughly 0.07% gross per-trade average derived from zero-cost cumulative return divided by approximately 424 trades, versus modeled round-trip cost near 0.3%. **The 0.07% is an approximation, not an independently observed mean realized fill return.**
- **Evidence boundary:** backtest, **not live performance**. Results depend on fee/slippage assumptions, OHLC intrabar ambiguity, execution timing, and compounding/accounting conventions.
- **BBB candidate (highest replication priority):** independently reproduce the entry/exit conditions on bitbank BTC/JPY, record bar coverage and ambiguous candles, compare zero-cost, maker/taker, realistic fee/slippage, and spread/depth assumptions; validate execution-semantic parity.
- **Do not import:** -62% as a universal result or assume the reported OHLC execution was executable at the assumed price.

### 28.4 Pump-collapse short with filters

Source: https://note.com/0xbot_jp/n/n253dcba6621f

- **Stage 1:** B; **Stage 2:** **B**
- **Reported live observation:** about 1.5 days, USD 78.22 profit on approximately USD 6,000 deployed (roughly 1.3%), with a claimed win rate above 75%.
- **Described logic:** multiple filters to detect an abnormal price pump and short its collapse; risk-based dynamic sizing and emergency handling for funding risk.
- **Evidence boundary:** extremely short author-reported record; no independently demonstrated edge, robust tail-risk analysis, or full-cycle reproducibility. Promotional framing and paid-bot funnel further limit evidentiary weight.
- **BBB fit:** low. The described short/futures/funding mechanism does not belong in BBB's initial bitbank BTC/JPY spot-only scope.
- **Possible research-only extraction:** study false-positive controls, liquidity checks, and risk-trigger monitoring independently of the short strategy.
- **Do not import:** short execution, leverage, funding assumptions, win-rate claims, or capital-risk fractions.

### 28.5 Cross-case assessment and next verification

| Candidate | Stage 1 | Stage 2 | Evidence type | BBB next action |
|---|---|---|---|---|
| DXY + Funding allocation | A+ | A+ | Author-reported live pilot | Compare regime features and allocation sensitivity |
| GridForge | A+ | A+ | Author-reported short bitbank live pilot | Mark-to-market inventory and range-break Replay |
| Volatility breakout | A++ | A++ | Historical backtest, not live | Independent cost-aware BTC/JPY Replay first |
| Pump-collapse short | B | B | Very short author-reported live log | Do not adopt; extract generic risk checks only |

**Decision:** preserve all four as research evidence; prioritize independent reproduction of the cost-sensitive breakout result, then compare regime-based allocation and grid strategy under common total-equity / execution-cost metrics. No strategy adoption, trading-capital change, CURRENT_SPEC edit, or live deployment is authorized by this note.

---

# Current Priority

Highest-value candidates across the reviewed batches:

1. **Order State Machine / UNKNOWN-state reconciliation**
2. **Production / Replay / Forward parity**
3. **Execution Semantics Parity**
4. **Recovery / Reconciliation Barrier before trading resumes**
5. **Executable Edge / Dynamic Fee Model**
6. **Target-state accounting for partial fill / cancel / replace**
7. **Shared Trading Constraints**
8. **Execution Reality Gap**
9. **Order / Fill / Fee / Balance / Ledger reconciliation**
10. **Exchange Capability / Semantic Contract**
11. **Multidimensional Readiness + Liveness / Safety monitoring**
12. **Monitoring latency / enforcement location**
13. **Validation-System Validation**
14. **Reconciliation delta provenance + safety false-positive cost**
15. **Data Coverage Contract / sampling coverage**
16. **Strategy Exit vs Emergency Hard Stop**
17. **Capital / Position Authority**
18. **Position sizing**
19. **Capital Promotion / Demotion Gate**
20. **Retrospective re-qualification when validation gates improve**
21. **Independent deterministic cross-check**
22. **NO TRADE reason logging**

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
