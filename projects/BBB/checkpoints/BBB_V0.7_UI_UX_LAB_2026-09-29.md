# BBB v0.7 UI UX Lab Checkpoint — 2026-09-29

Status: RESEARCH / PAPER
Version: v0.7

## Human direction
- 過剰でもよいので便利機能・UI/UXをいろいろ試す。
- 実用性だけでなく、日常的に見たくなるCockpitを目指す。
- Live安全境界は維持する。

## Implemented UI
- Sidebar navigation
- Dashboard
- Training Lab
- History
- Risk & System
- Public OHLCV candlestick chart
- Paper equity curve
- Return / Max DD / decision / fill / error metrics
- Research Champion card
- Strategy Family catalog
- Research Job timeline
- Operational Readiness
- Risk visualization
- Toast notifications
- Ctrl+K command palette
- keyboard navigation
- audit snapshot export
- responsive layout

## Backend additions
- get_analytics
- get_strategy_catalog
- get_readiness
- cached get_market_chart
- export_snapshot
- pure journal analytics helper

## Verification
- pytest: 29 passed
- UI JavaScript syntax check: PASS
- live order path: NOT IMPLEMENTED
- private API credentials: NOT USED

## Planned UI experiments
- Replay Theater
- Champion vs Challenger visual comparison
- Market Regime indicator
- Orderbook heatmap
- Strategy Plugin browser
- Training calendar / history heatmap
- explanation panel for each decision
- selectable compact/focus/lab layouts
