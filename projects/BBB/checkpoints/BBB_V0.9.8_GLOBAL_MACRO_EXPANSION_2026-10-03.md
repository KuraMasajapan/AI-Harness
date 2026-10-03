# BBB v0.9.8 Global Macro Expansion — Checkpoint
Date: 2026-10-03

## Goal
Expand the Global / U.S. macro case-study cohort before moving to Crypto Native.

## Sources
Baseline retained:
- Federal Reserve FOMC Statement
- BLS CPI
- BLS Employment Situation

Added:
- BEA Personal Income and Outlays / PCE
- BLS Producer Price Index / PPI
- BEA national Gross Domestic Product / GDP

## Classification
- FOMC -> rates_liquidity
- CPI -> inflation
- Employment -> employment
- PCE -> inflation
- PPI -> inflation
- GDP -> growth

Taxonomy version:
- bbb-global-macro-v2

## Relevance gate
All six source families are Tier A.
GDP initial cohort excludes:
- state GDP
- county GDP
- Puerto Rico GDP
- other regional GDP derivatives

## Pipeline reuse
New source events automatically enter:
- official-time impact replay
- Matched Control
- Robustness Check
- Global BTC / JPY decomposition
- FX Evidence Gate

## UI
- PCE / PPI / GDP source checkboxes
- six-source count display
- default Global Macro max items raised to 200

## Validation
- pytest: 113 passed
- compileall: PASS
- UI JavaScript syntax: PASS
- BAT static check: PASS
- flat ZIP root: PASS
- extracted ZIP pytest: 113 passed
- package: BBB_v0.9.8_Global_Macro_Expansion.zip
- SHA-256: b675324597f807d7b036bac6a361044a73f214619b7f3960021e7cfb93c16fa8

## Safety
Public read-only / Research only.
No Paper / Risk / Champion / Live behavior change.
