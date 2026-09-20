# Historical PASS provenance notes — additive audit, 2026-09-20

Original PASS/COMPLETE records are unchanged. These are Test 03 audit findings,
not retrospective execution receipts. Hashes identify the audited raw files;
if current hashes differ, this note applies only to the recorded audit snapshot.
No current-snapshot PASS or invalidity of past PASS is inferred.

| Record | Repository path / audited SHA-256 | Preserved result |
| --- | --- | --- |
| H01 initial TEST-000..010 aggregate | evaluation/RESULTS.md / 116802bd71c12cf0864781c66e7e00c9973d8b848a7764509a1183ddf5406235 | 11/11 PASS; Initial Evaluation COMPLETE |
| H02 controlled Test A/B | experiments/latent-risk-scan/RESULTS.md / c34f8f7349f2928260378aacabbbc05f998190e755e4232592cfc476673e9f59 | initial controlled PASS; solution complexity PARTIAL |

| Provenance field | H01 | H02 |
| --- | --- | --- |
| Result | PRESENT | PRESENT |
| Test/fixture identity | PARTIAL | PARTIAL |
| Source paths | PARTIAL | PRESENT (instructed list, not read log) |
| Execution input hashes | MISSING | MISSING |
| Execution commit/tree/dirty binding | PARTIAL (storage history only) | PARTIAL (branch and storage history only) |
| Executor/model | MISSING | PARTIAL (chat roles only) |
| Context/input | PARTIAL | PARTIAL |
| Runtime/configuration | MISSING | PARTIAL |
| Execution log | PARTIAL (summary only) | PARTIAL (summary only) |
| Reviewer/Human authority | MISSING | PARTIAL (role only) |
| Artifact hashes | PARTIAL (storage blobs recoverable) | PARTIAL (storage blobs recoverable) |
| Relation to current execution snapshot | UNRESOLVED | UNRESOLVED |

H01's current TEST-001 name in TEST_CASES differs from RESULTS; do not silently
join by number. H02 is relatively more detailed but not fully reconstructable.
The audited working-file/HEAD differences for both RESULTS were CRLF/LF only.
The hashes above are raw-byte hashes, not normalized-content hashes.

Storage references, NOT proven execution commits:
H01 3b19105449e060203b0271ff004366ba2821e2b2;
H02 3efc21626c769b7ea7a8e8579e0ee9bb0c812055.
Git authors and dates do not establish executor or reviewer identity.

Evidence origin: Pilot #001 Risk Validation Test 03, fixed H01/H02 sample.
Its saved report and source_manifest.json remain in the operator's outputs.
Missing means not found within the audited sources, not universal nonexistence.
External chat evidence and permitted future reliance remain UNRESOLVED.
