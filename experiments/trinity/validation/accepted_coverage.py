"""Accepted-item structure, identity and aggregation only; no semantic inference."""
from controller.artifact_store import digest

VERSION = "accepted-items-v0.1"
STATUSES = {"COVERED", "MISSING", "CONTRADICTED", "UNRESOLVED"}


def items(disposition):
    # Position, not text, identifies an occurrence. Duplicates remain distinct.
    return [dict(item_id=f"{disposition['artifact_id']}:{i}", item_index=i,
                 text=text, required=True)
            for i, text in enumerate(disposition["content"]["accepted_items"])]


def header(disposition, checker_version):
    return dict(coverage_version=VERSION, checker_version=checker_version,
                human_disposition_artifact_id=disposition["artifact_id"],
                human_disposition_content_hash=disposition["content_hash"])


def unresolved(disposition, checker_version):
    rows = [dict(item_id=i["item_id"], item_index=i["item_index"], required=True,
                 status="UNRESOLVED", response_evidence=None, notes="Coverage unavailable")
            for i in items(disposition)]
    return dict(**header(disposition, checker_version), items=rows,
                empty_set=not rows, coverage_satisfied=not rows)


def check(payload, disposition, candidate, checker_version):
    expected_header = header(disposition, checker_version)
    if set(payload) != set(expected_header) | {"items"}:
        raise ValueError("Malformed accepted-item coverage")
    if not isinstance(checker_version, str) or not checker_version.strip():
        raise ValueError("Coverage checker version required")
    if any(payload[k] != v for k, v in expected_header.items()):
        raise ValueError("Coverage version or Disposition ID/hash mismatch")
    if (disposition["artifact_type"] != "HUMAN_DISPOSITION"
            or disposition["run_id"] != candidate["run_id"]
            or disposition["artifact_id"] not in candidate["source_artifact_ids"]
            or digest(disposition["content"]) != disposition["content_hash"]):
        raise ValueError("Coverage Disposition does not bind candidate")
    expected = items(disposition)
    rows = payload["items"]
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError("Missing or duplicate accepted-item mapping")
    for row, item in zip(rows, expected):
        if set(row) != {"item_id", "item_index", "required", "status", "response_evidence", "notes"}:
            raise ValueError("Malformed accepted-item row")
        if (row["item_id"] != item["item_id"] or type(row["item_index"]) is not int
                or row["item_index"] != item["item_index"] or row["required"] is not True):
            raise ValueError("Accepted-item occurrence identity mismatch")
        if row["status"] not in STATUSES:
            raise ValueError("Invalid coverage status")
        if not isinstance(row["notes"], str) or not row["notes"].strip():
            raise ValueError("Validator coverage rationale required")
        evidence = row["response_evidence"]
        # An exact quote is an evidence-integrity check, never a coverage classifier.
        if evidence is not None and (not isinstance(evidence, str) or evidence not in candidate["content"]["text"]):
            raise ValueError("Coverage evidence is not in exact candidate")
        if row["status"] in {"COVERED", "CONTRADICTED"} and (not evidence or not evidence.strip()):
            raise ValueError("Validator coverage evidence required")
    return dict(**payload, empty_set=not rows,
                coverage_satisfied=all(r["status"] == "COVERED" for r in rows))


def result_is_bound(body, disposition, candidate):
    """Validate the versioned Semantic receipt, not the meaning of its text."""
    try:
        coverage = body["accepted_item_coverage"]
        if (not isinstance(coverage, dict) or type(coverage.get("empty_set")) is not bool
                or type(coverage.get("coverage_satisfied")) is not bool):
            return False
        payload = {k: v for k, v in coverage.items() if k not in {"empty_set", "coverage_satisfied"}}
        verified = check(payload, disposition, candidate, body["provenance"]["checker_version"])
        return coverage == verified and verified["coverage_satisfied"]
    except (KeyError, TypeError, ValueError):
        return False
