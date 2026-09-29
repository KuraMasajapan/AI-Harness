# BBB v0.7.1 Startup Fix Checkpoint — 2026-09-29

Status: RESEARCH / PAPER
Version: v0.7.1

## Trigger
Human reported that double-clicking `BBB_START.bat` opened a command window briefly and then closed with no visible error.

## Root issue in v0.7 launcher
The launcher had a failure path where browser fallback/runtime errors could exit immediately without pausing, which made first-start diagnosis difficult.

## Fixes
- Startup failure now keeps the console open.
- `BBB_STARTUP.log` is always created.
- Python detection expanded to:
  - `py -3`
  - `python`
  - common Python 3.12 / 3.11 LocalAppData paths
- Existing virtual environment is checked and repaired if BBB dependencies are missing.
- Native pywebview failure automatically falls back to localhost browser UI.
- Added `BBB_OPEN_BROWSER.bat` for explicit safe browser mode.
- Added `BBB_DIAGNOSTIC.bat` which writes `BBB_DIAGNOSTIC.txt`.
- No API key or secret is collected by diagnostics.

## Verification
- pytest: 29 passed
- Python compileall: PASS
- live order path: NOT IMPLEMENTED
