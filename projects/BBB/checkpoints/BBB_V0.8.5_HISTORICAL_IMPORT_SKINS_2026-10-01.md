# BBB v0.8.5 Historical Fundamental Import + Skin System — Checkpoint
Date: 2026-10-01
Project: BITBANK-BOT (BBB)
Branch: development

## Human decisions
- Proceed from the successful v0.8.4 Fundamental Replay target run into historical case studies.
- Start with BOJ historical data and target roughly 100 cases.
- Adopt all four proposed UI skins.
- Add English / Japanese side-by-side labels; Human will point out unnatural Japanese where found.

## Implemented
### Historical Fundamental Import
- New module: fundamental_history.py
- BOJ official yearly archive sources:
  - monetary policy decisions
  - Policy Board opinions
  - speeches
  - press conferences
- UI default:
  - 2025-01-01 through 2025-12-31
  - max 100 items
  - all 4 BOJ archive sources selected
- Candidate selection is balanced across archive categories.
- Stable event IDs and de-duplication.
- Stored separately from live Fundamental Feed under data/fundamental_history.
- Sokudan classification stays Sandbox only.

### Historical timestamp policy
- The BOJ archive pages reliably expose a publication date, but not a guaranteed exact intraday release time for every row.
- Do not invent an exact time.
- date-only knowledge boundary: 23:59:59 JST on publication date.
- 5m / 30m / 1h / 4h outcomes are null for date-only events.
- Initial Historical Replay scores BTC/JPY 24h only using 1h public market candles.

### UI Skin System
- Aurora Light / オーロラライト
- Sunrise Gold / サンライズゴールド
- Midnight / ミッドナイト
- Sakura Tech / サクラテック
- right-top selector
- local persistence via localStorage
- first-run default: Aurora Light

### Bilingual UI
Major navigation, cards, replay controls, and table labels show English / Japanese together.
Translations are explicitly open to Human correction.

## Validation
- pytest: 48 passed
- Python compileall: PASS
- UI JavaScript syntax: PASS
- BAT goto/label static check: PASS
- packaged ZIP extracted and 48 tests passed again
- package: BBB_v0.8.5_Historical_Import_Skins.zip
- SHA-256: 8d9a946c5ca8084a169bdb743801f563c1a6464358bdbcc8b5ad7ded5f4aefbf

## Safety
Unchanged:
- no private API
- no real-money order path
- no Local AI direct BUY / SELL authority
- no automatic Risk mutation
- no Historical Replay auto-promotion to Live

## Target PC next steps
1. Overwrite-update BBB while preserving data.
2. Start BBB and confirm Local AI READY.
3. Switch among all four skins and inspect Japanese wording.
4. Risk & System -> Historical Fundamental Import.
5. Keep 2025-01-01 to 2025-12-31 and max 100.
6. Start Historical Import and wait for DONE.
7. Start Historical Replay.
8. Review 24H Bias Alignment by n; do not treat early rates as performance proof.
