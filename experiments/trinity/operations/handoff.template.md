# Pilot handoff — operator record, not a protocol artifact

Run ID: <exact run ID>
Candidate artifact ID / content hash: <copy exact sealed values>
Human Disposition artifact ID / content hash: <copy exact sealed values>

| Outcome | Recorded result | Meaning / limitation |
| --- | --- | --- |
| Binding | <copy PASS/FAIL, artifact ID> | Identity/seal/lineage only. PASS does not establish accepted-item semantic coverage. |
| Accepted-item coverage | UNRESOLVED until separately evidenced | Operator observations below are not a Semantic result. |
| Semantic | <copy result, artifact ID, validator identity> | validator=None means UNRESOLVED; never replace it with Human Disposition. |
| Release | <copy actual decision and artifact ID> | Copy the recorded decision. Do not infer release from Binding PASS. |

| Exact accepted item | Candidate excerpt/location or absent | Operator observation | Evidence / limitation |
| --- | --- | --- | --- |
| <verbatim item> | <literal excerpt or none> | UNRESOLVED | Presence of a phrase is not proof of semantic coverage. |

Keep source outputs unchanged. If no accepted items exist, explicitly record the
empty set; do not infer meaningful coverage. This table cannot mark ALIGNED or
authorize release. R1-B remains UNRESOLVED.

Test 01 saved examples (not reruns): Negative Binding PASS / coverage UNRESOLVED
(item absent) / Semantic UNRESOLVED / Release DENY; Positive Binding PASS /
coverage UNRESOLVED (item text present) / Semantic UNRESOLVED / Release DENY.
