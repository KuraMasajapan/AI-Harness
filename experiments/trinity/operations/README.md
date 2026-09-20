# Pilot evaluation operations (non-protocol)

These optional operator records do not affect RunManager, Binding, Semantic or
Release. They are not sealed protocol artifacts and do not authenticate humans.

1. Copy receipt.template.json outside this source directory. Assign evaluation
   and test IDs. Before execution, save exact ordered inputs, expected/oracle,
   approval reference, repository snapshot and executor/runtime information.
2. Each evidence entry uses PRESENT with path and SHA-256 of raw bytes, or
   MISSING/PARTIAL/UNRESOLVED with a reason. Do not guess model identity.
   Snapshot evidence should include commit, tree, dirty status and relevant
   working bytes/hashes. A storage commit is not an execution snapshot.
3. Record expected_timing as BEFORE_EXECUTION only when an independent record
   supports that order; otherwise AFTER_EXECUTION or UNRESOLVED. Preserve the
   pre-execution receipt separately and reference it in the final receipt.
4. Save final output and raw execution log, then complete result and reviewer.
   Keep functional result separate from provenance limitations. Unknown model
   identity does not rewrite a functional PASS into FAIL.
5. Run `python check_receipt.py receipt.json`. Relative evidence paths resolve
   from the receipt directory. The read-only check validates structure and
   hashes. OK means supplied references match, not complete reconstruction,
   authentic provenance, semantic alignment, or release approval. Exit 1 means
   malformed structure or broken hash/path; limitations remain explicit on OK.
6. Copy handoff.template.md for human review. Show all three gate outcomes plus
   accepted-item coverage uncertainty together. Never use this table as Semantic.

Do not rewrite historical results or backdate receipts. See historical-notes.md.
No DB, network, automatic execution, model access or new protocol gate is added.
Protected sources and prior sealed runs remain untouched.

Limited tests: from experiments/trinity, run
`python -m unittest discover -s operations -p 'test_*.py' -v`.

Still requires Human design decisions: semantic enforcement boundary, coverage
and materiality rules, checker responsibility, compatibility and the permitted
uses of provenance-incomplete historical evidence. This operations aid does not
resolve R1-B or implement Risk 02/04 production fixes.
