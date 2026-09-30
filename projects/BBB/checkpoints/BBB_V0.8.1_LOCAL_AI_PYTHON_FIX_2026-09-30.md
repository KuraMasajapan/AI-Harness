# BBB v0.8.1 Local AI Python Compatibility Fix

Date: 2026-09-30
Status: IMPLEMENTED IN DISTRIBUTABLE PACKAGE

## Trigger

The first v0.8 Local AI setup failed on the target Windows PC while BBB itself installed successfully.

Observed pip result:
- Sokudan 0.3.0 requires Python >=3.11,<3.14.
- The BBB environment rejected the Sokudan package as Python-incompatible.
- No BBB core failure was observed.

## Root cause

v0.8 installed Sokudan directly into BBB's main `.venv`.
This unnecessarily coupled BBB's Python version to Sokudan's narrower supported range.

## v0.8.1 fix

Separate the runtimes:

```text
BBB/
  .venv/            -> BBB application
  .venv_local_ai/   -> Sokudan only
```

The Local AI setup now:
1. searches for Python 3.13, then 3.12, then 3.11;
2. uses BBB Python only if it is inside Sokudan's supported range;
3. creates `.venv_local_ai`;
4. installs `sokudan[serve]>=0.3,<0.4` there;
5. if no supported interpreter exists and Windows winget is available, asks before installing Python 3.13;
6. leaves BBB's existing `.venv` untouched.

BBB auto-start now detects the dedicated Local AI environment.
The Local AI manager launches Sokudan with `.venv_local_ai` rather than the BBB interpreter.

## Safety

Unchanged:
- Sandbox only
- trade influence OFF
- no Live authority
- Local AI failure does not stop BBB
- no API credentials passed to Local AI

## Validation

Package validation:
- pytest: 33 passed
- Python compileall: PASS
- UI JavaScript syntax check: PASS
- BAT label/goto static check: PASS

## Human action

Run the updated `BBB_LOCAL_AI_SETUP.bat`.

If Python 3.11-3.13 is already installed, setup uses it automatically.
If not, setup can offer Python 3.13 installation through winget with explicit confirmation.
