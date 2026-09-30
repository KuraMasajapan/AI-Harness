# BBB v0.8.2 Local AI Setup Robustness Fix

Date: 2026-09-30
Status: IMPLEMENTED IN DISTRIBUTABLE PACKAGE

## Trigger

On target Windows PC, v0.8.1 setup reported:

- BBB Python 3.14.0
- compatible launcher found: py -3.13
- dedicated Local AI environment created
- immediately after creation, setup incorrectly stopped with an unsupported-Python message

This showed that the v0.8.1 setup validation path was too brittle even though a compatible Python 3.13 launcher was present.

## v0.8.2 fix

- Resolve `py -3.13 / 3.12 / 3.11` to the actual `sys.executable` path first.
- Create `.venv_local_ai` from that concrete executable path.
- Remove any existing `.venv_local_ai` before recreation.
- Print the actual Local AI Python version after venv creation.
- Use a simple major/minor check for 3.11 / 3.12 / 3.13.
- Improve error text so a newly-created environment is not mislabeled as merely an "existing" unsupported environment.
- Document the correct first-time order:
  1. close BBB
  2. run `BBB_LOCAL_AI_SETUP.bat`
  3. after successful setup, run `BBB_START.bat`

## Validation

- pytest: 33 passed
- Python compileall: PASS
- UI JavaScript syntax check: PASS
- BAT label/goto static check: PASS

## Safety boundary

Unchanged:
- Local AI is SANDBOX ONLY
- trade influence OFF
- no Live authority
- BBB continues without Local AI
- no private API credentials are passed to Local AI
