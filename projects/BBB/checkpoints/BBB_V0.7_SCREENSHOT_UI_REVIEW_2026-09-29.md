# BBB v0.7 Screenshot UI Review — 2026-09-29

Source: Human-provided screenshots of Dashboard / Training Lab / History / Risk & System.

## Overall
- First usable desktop run succeeded on Windows after v0.7.1 startup fix.
- Visual direction is successful: dark financial terminal / research cockpit.
- Navigation is understandable and PAPER / LIVE LOCKED separation is visible.
- Layout is already usable as a daily monitoring console.

## Screenshot findings

### Dashboard
Strengths:
- Market chart is dominant and easy to identify.
- Paper Equity, Research Champion, Safety, Paper operation are visible on one screen.
- LIVE LOCKED is clearly visible.
- Kill Switch is prominent.

Improvements:
- Explain Start / 1 Candle / Stop with hover help.
- Show current bot state more explicitly: stopped / polling / waiting next candle / error.
- Add last market-data timestamp and data freshness indicator near chart.
- Add BUY / SELL markers on chart once decisions exist.
- Paper equity curve empty-state explanation is appropriate, but can include “Start Paper to populate”.

### Training Lab
Strengths:
- Research controls and strategy families are logically grouped.
- Current candidates and future experiment ideas are visually separated.

Improvements:
- Add concise help text for days / candidates / folds / interval.
- Add estimated runtime before starting.
- Add progress bar and current candidate/fold while training.
- Clarify the difference between “今すぐ戦略大会” and “継続学習 ON”.
- Show Champion vs Challenger result immediately after a run.
- Strategy cards should show latest score, drawdown, win rate, and last tested date.

### History
Strengths:
- BUY / SELL / HOLD filters are clear.

Improvements:
- Empty screen feels too sparse before first Paper decision.
- Add a first-use explanation and a direct “Paperを開始” shortcut.
- Add strategy filter, date filter, P/L filter, and export.
- A row click should open decision details: indicators, reason, price, equity, risk gate result.

### Risk & System
Strengths:
- MAX ORDER / MAX POSITION / DAILY LOSS STOP are immediately visible.
- Operational readiness is useful for future Live Gate.
- Private API / Private Stream / Live Trading Gate being locked is clear.

Improvements:
- Add tooltips for each readiness item explaining what is required to pass.
- Add current public API connectivity / last successful fetch / latency.
- Add disk/log health and dataset freshness.
- System JSON is useful for audit but not ideal for normal users; keep raw JSON collapsible and add human-readable cards.
- Add a dedicated “Live is impossible right now” explanation until prerequisites are complete.

## Consistency issue noticed
- Screens show sidebar/footer as v0.7 while System JSON reports version 0.7.1.
- Next build should unify all visible version labels.

## Recommended next UI work
1. Onboarding / first-run help.
2. Contextual tooltips.
3. Training progress and estimated runtime.
4. Decision detail drawer.
5. Chart BUY/SELL markers.
6. Human-readable system health cards.
7. Champion vs Challenger comparison panel.
8. Replay Theater.
9. Layout presets: Compact / Focus / Lab.
10. Consistent version display.

## Safety note
Convenience features may be added aggressively, but PAPER / LIVE distinction, Kill Switch visibility, credential non-display, and Live Gate separation remain fixed safety boundaries.
