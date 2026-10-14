# BBB Checkpoint — v0.9.35 / Hoheto Research Handoff

Date: 2026-10-14 (JST)
Repository: `KuraMasajapan/AI-Harness`
Branch: `main`
Status: **Checkpoint / resumable handoff**, not a strategy promotion or live approval.

## 1. Why this checkpoint exists

Human request: checkpoint the current BBB development and external-research progress after reviewing Hoheto's note account.

Preserve separately:
- what was implemented and observed in BBB,
- what research was actually conducted or only indexed,
- promising hypotheses awaiting BBB reproduction,
- explicit safety boundaries,
- exact next action for a future chat.

Human policy (2026-10-14): use information when evidence supports it; when a plausible idea still requires verification, do controlled tests and preserve results, including failures. Design and ordinary research implementation may be delegated, but Source-of-Truth changes and live trading remain gated by user approval. This file itself was explicitly requested.

## 2. Latest known BBB release — v0.9.35

Release: **Public Trading Constraints & Parity**
Package filename supplied by release session:
`BBB_v0.9.35_PUBLIC_TRADING_CONSTRAINTS_PARITY_FULL.zip`

Build-session report (not rerun by this checkpoint action):
- 265 / 265 tests PASS
- packaged ZIP re-extracted tests PASS
- Python/JavaScript syntax checks PASS
- reported package SHA-256: `a0443718c5334bc63db84920fd51a60e559e7e587b1b3f64dea4bda919ae7539`

Features added after v0.9.34:
- Public bitbank spot pair trading-constraint reference, including public maker/taker fee and precision/order rules where available.
- Reference execution-cost scenarios using public fee information plus modeled slippage.
- Same-semantics trade-count parity diagnostic and explicit `DATA_MISMATCH` status when Forward/replayed baseline count cannot be reconciled.
- Public data retrieval failure must not stop the frozen Forward lane.
- No assumption that a public taker rate equals an account's eventual realized all-in trading cost.

Previous checkpoint (v0.9.34):
`projects/Bitbank_bot/CHECKPOINT_2026-10-14_v0.9.34.md` on `main`.

## 3. Local observed v0.9.35 snapshot

User screenshot discussed in chat on 2026-10-14. Values below were described from that UI; they are not direct exchange-fill evidence.

| Metric | Observed |
| --- | ---: |
| Existing Active Forward return | **+0.38%** |
| Next-open / no-cost return | **+0.39%** |
| Next-open / earlier assumed-cost scenario | **-0.65%** |
| Next-open / public bitbank Taker reference + assumed slippage | **-0.53%** |
| Harsher modeled-cost scenario | **-1.27%** |
| Public BTC/JPY Taker reference shown | **0.1000% per side** |
| Forward trade count in same-semantics comparison | **72** |
| Audit trade count in same-semantics comparison | **72** |
| Same-semantics trade-count delta | **0** |
| Audit economic status | **REVIEW** |

Interpretation:
- The parity/count reconciliation improved in this snapshot: 72 vs 72 is consistent under matched semantics, not proof that all individual trades are identical.
- Apparent gross profit flips to modeled net loss with public fee reference + assumed slippage.
- This is evidence of significant **cost sensitivity**, NOT proof of negative actual live PnL.
- Distinguish reference maker/taker fees, actual account schedule, order-book spread/depth, fill probability, slippage and timing.
- A risk-efficiency benchmark label does not demonstrate executable profitability.

## 4. Frozen strategy and operational boundaries

- Venue / pair / scope: bitbank, BTC/JPY spot-only; no short / leverage.
- Research Champion: Mean Reversion.
- Frozen parameters: lookback 79, entry_z 2.0, exit_z 0.0.
- Active Forward Freeze: **2026-10-08 17:20 JST**.
- Active Forward is immutable research comparator; update market observations only.
- Shadow Training is isolated from Active; previous Shadow Economic Viability Gate prevents unsuitable champion promotion. Do not treat Shadow research success as live eligibility.
- `Shadow継続研究` is OFF unless deliberately turned on after adequate new data.
- v0.9.33 graceful desktop close exists; close after running jobs are DONE.
- No private API order placement, live trades, automatic capital promotion or risk-gate relaxation is authorized.

## 5. External-research status: Hoheto / note

Public profile: https://note.com/hht
Author index: https://note.com/hht/all

**Important coverage limitation:** the audit is NOT confirmed complete. The accessible public author listing only exposed a short first page (~18 items) reliably, and dynamic older-page pagination could not be enumerated reliably. Search-index / magazine archives added older titles. Do not say all posts were read.

Research audit on `development`:
- `projects/BBB/research/field-notes/2026-10-14-hoheto-account-audit.md`
  - **30 independently linked article URLs**.
  - **14 additional indexed titles** with unresolved article URLs/read status.
  - Those counts are **catalog entries**, not a proven total count of articles on the account.
  - Distinguishes `BODY` / `INDEX` / `RECHECK` and `CANDIDATE` / `HOLD` / `REJECT_FOR_BBB_NOW`.
- `projects/BBB/research/field-notes/2026-10-14-hoheto-execution-cost-research.md`
  - Focused fee/horizon experiments, Shadow test design, and staged evidence policy.
- Earlier multi-source incident catalog:
  - `projects/BBB/research/field-notes/2026-10-12-grok-live-trading-lessons.md`.
- Canonical field-note process:
  - `projects/BBB/research/field-notes/README.md`.

### Most useful conclusions, none yet proven on BBB

**CANDIDATE / highest test priority**
1. **Buy/Hold buffer and hysteresis**: decouple entry, holding and exit rules instead of only tightening entry. Source: https://note.com/hht/n/n7f82d3810278 ; research basis Novy-Marx & Velikov (original empirical setting: equities), https://www.nber.org/papers/w20721 . Need BTC/JPY-specific out-of-sample replication.
2. **Cost × timeframe sensitivity**: compare 5m baseline with carefully predeclared 15m/30m/1h variants; measure cost-adjusted total equity return, DD, exposure, trade count and signal decay. Source: https://note.com/hht/n/nb7fcfe538c59 .
3. **Mean-reversion signal decay vs latency**: a signal can be observable without remaining exploitable by actual execution time. Source: https://note.com/hht/n/neb66fd3c945a (old seconds-level bitFlyer result, not directly transferable).
4. **Trend / volatility NO-ENTRY filter**: Shadow A/B test with past-only market state, noting opportunity cost of skipped winning entries. Source: https://note.com/hht/n/na333099d536f .
5. **A/B evaluation and decision telemetry**: monitor no-trade reasons and paired controls; reuse existing BBB run metadata. Source: https://note.com/hht/n/n5657038dba6c .

**HOLD**
- VPIN complex pipeline until cheap volatility baselines justify it.
- Maker-first execution until fill probability, partial fills, queue, and cancel-replace semantics are modeled.
- AI/HFT alpha claims, liquidation heatmaps and author-specific exchange mechanics pending independent venue verification.

**REJECT for current BBB scope**
- Old leveraged futures rotation strategies, bitFlyer-specific SFD economics, untested short or leverage mechanisms.
- Do not import any external fee rate, z threshold or PnL as a universal bitbank rule.

### Key negative evidence
- Hoheto VPIN paper/article series reports that signal detection did not convert cleanly to attractive executable trading and the author stopped that line of strategy; value may be in risk monitoring, not automatic alpha.
- Author reports severe loss in a historical leveraged/futures rotation project; retain this counterexample when interpreting impressive selective returns.
- External sources are evidence of *reported experience*, not BBB strategy performance.

## 6. Next actionable work: Shadow-only reproducible experiment

**Next project task**: inspect v0.9.35 Shadow simulator source and determine how entry/exit thresholds, candidate scoring, costs and chronology are implemented. Then prepare an isolated `Shadow Cost-Aware Search / Buy-Hold Buffer` mini-batch; **no coding or release of v0.9.36 has been completed as of this checkpoint**.

Suggested sequence:
1. Code audit: verify which simulation assumptions are shared or divergent; match existing baseline return/trade count and identify data source, granularity, fee/slippage, position cash accounting.
2. Predeclare a small fixed experiment matrix: frozen 5m Mean Reversion baseline; entry-only buffer vs entry/hold/exit hysteresis; optional trend/no-entry filter only after baseline.
3. Only use past-known indicators at decision time, execute on next available bar, report missing-candle and intrabar ambiguities.
4. Use a chronological training/validation/untouched holdout split with distinct market regimes; avoid retuning to the held-out data.
5. Compare **net** return (main), cost drag, max DD, PF, total turnover, number of trades, exposure time, vs buy-and-hold and NO TRADE controls, with stress fees and sensitivity.
6. Reject or retain failed/null results visibly; require meaningful trade counts and forward validation before any promotion.
7. Preserve all Active state, frozen Champion and Forward values. Shadow candidates do not change Paper, Risk, Live or capital.
8. After test results, determine whether complexity is justified before adding further indicators or modules.

## 7. Other pending input, not a blocker

- bitbank official Discord has a BOT development community stream / posts according to user; direct read connector unavailable in plugin discovery. No channel archive acquired.
- Access to Discord export requires official platform permissions; do not use normal-user token self-bot or unauthorized scraping. Video/audio stream content is not included automatically in text export.
- Continue Hoheto author inventory without claiming full-account completion until pagination or authorized complete export is verified.

## 8. File / branch policy

- Use `main/projects/Bitbank_bot/CHECKPOINT_*.md` for this durable release/project checkpoint.
- Specialized unverified third-party evidence remains in `development/projects/BBB/research/field-notes/`.
- Do not mistake separate branch paths for a single merged tree.
- Do **not** silently modify `CURRENT_SPEC.md`, `DECISION_LOG.md`, frozen Active fields or connected trade permissions based on external note claims.

## 9. Resume prompt (copy into new chat if needed)

> Resume BBB from checkpoint `main:projects/Bitbank_bot/CHECKPOINT_2026-10-14_v0.9.35_RESEARCH_HANDOFF.md`. Review Hoheto research notes on the `development` branch, especially `2026-10-14-hoheto-account-audit.md`. Current deployed release is v0.9.35; forward Champion and freeze remain locked. First audit the existing Shadow simulator. Then propose/implement a bounded, chronological, cost-aware Buy/Hold Buffer comparison strictly in Shadow, without changing Active, Paper, Risk or Live. Do not claim all note articles have been read. Record both positive and negative evidence and ask before external canonical spec changes or live permissions.
