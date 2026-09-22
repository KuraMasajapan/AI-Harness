"""External validator boundary; no model, heuristic, retry or semantic controller."""
import json
from dataclasses import dataclass
from typing import Protocol
from controller.artifact_store import canonical, digest, identifier
from validation import accepted_coverage


@dataclass(frozen=True)
class ValidationRequest:
    task_json: str
    candidate_json: str
    contract_json: str
    disposition_json: str
    accepted_items_json: str


class Validator(Protocol):
    provenance: dict

    def evaluate(self, request: ValidationRequest) -> dict:
        """Return requirements plus versioned accepted_item_coverage in one call."""
        ...


def _evaluate(task, candidate, validator, contract, disposition):
    provenance = dict(checker_id="unconfigured", checker_type="unconfigured", model_name=None,
                      model_version=None, checker_version="unconfigured", config_hash=digest({}), prompt_hash=digest(contract), execution_id=identifier())
    requirements = task["content"]["requirements"]
    mapping = [dict(requirement_id=r["requirement_id"], status="UNRESOLVED", response_evidence=None,
                    notes="Validator unavailable") for r in requirements]
    error = None
    coverage = accepted_coverage.unresolved(disposition, provenance["checker_version"])
    try:
        if validator is None:
            raise ValueError("No semantic validator configured")
        supplied = dict(validator.provenance)
        for key in ("checker_id", "checker_type", "checker_version", "model_name", "model_version", "config_hash", "prompt_hash"):
            if key not in supplied:
                raise ValueError("Incomplete validator provenance")
        if not isinstance(supplied["checker_version"], str) or not supplied["checker_version"].strip():
            raise ValueError("Coverage checker version required")
        if supplied["checker_type"] in {"human-local-review", "human-review"}:
            raise ValueError("Human review cannot substitute for Semantic coverage")
        if supplied["checker_id"] == candidate["producer_id"] or supplied["checker_id"] == "C":
            raise ValueError("Self-validation / unresolved Comparator lifecycle is forbidden")
        if supplied["prompt_hash"] != digest(contract):
            raise ValueError("Checker contract hash mismatch")
        for key in ("config_hash", "prompt_hash"):
            if len(supplied[key]) != 64 or any(c not in "0123456789abcdef" for c in supplied[key]):
                raise ValueError("Invalid provenance hash")
        provenance.update({k: supplied[k] for k in supplied if k in provenance and k != "execution_id"})
        request = ValidationRequest(canonical(task), canonical(candidate), canonical(contract),
                                    canonical(disposition), canonical(accepted_coverage.items(disposition)))
        output = json.loads(canonical(validator.evaluate(request)))
        if not isinstance(output, dict) or set(output) != {"requirements", "accepted_item_coverage"}:
            raise ValueError("Legacy or malformed validator result; versioned coverage required")
        coverage = accepted_coverage.check(output["accepted_item_coverage"], disposition, candidate,
                                           provenance["checker_version"])
        rows = output["requirements"]
        expected = {r["requirement_id"] for r in requirements}
        if len(rows) != len(expected) or {r["requirement_id"] for r in rows} != expected:
            raise ValueError("Incomplete or duplicate requirement mapping")
        text = candidate["content"]["text"]
        for row in rows:
            if set(row) != {"requirement_id", "status", "response_evidence", "notes"}:
                raise ValueError("Malformed requirement mapping")
            if row["status"] not in {"COVERED", "CONTRADICTED", "MISSING", "UNRESOLVED"}:
                raise ValueError("Invalid requirement status")
            if not isinstance(row.get("notes"), (str, type(None))):
                raise ValueError("Invalid requirement notes")
            evidence = row.get("response_evidence")
            if evidence is not None and (not isinstance(evidence, str) or evidence not in text):
                raise ValueError("Evidence is not in exact candidate")
            if row["status"] in {"COVERED", "CONTRADICTED"} and not evidence:
                raise ValueError("Evidence required")
        mapping = rows
        material = {r["requirement_id"]: r["material"] for r in requirements}
        if any(r["status"] == "CONTRADICTED" or (r["status"] == "MISSING" and material[r["requirement_id"]]) for r in rows):
            result = "MISALIGNED"
        elif any(r["status"] == "UNRESOLVED" and material[r["requirement_id"]] for r in rows):
            result = "UNRESOLVED"
        else:
            result = "ALIGNED"
        if any(r["status"] in {"MISSING", "CONTRADICTED"} for r in coverage["items"]):
            result = "MISALIGNED"
        elif not coverage["coverage_satisfied"] and result == "ALIGNED":
            result = "UNRESOLVED"
    except Exception as exc:
        result, error = "UNRESOLVED", f"{type(exc).__name__}: {exc}"
        coverage = accepted_coverage.unresolved(disposition, provenance["checker_version"])
    return dict(candidate_artifact_id=candidate["artifact_id"], candidate_content_hash=candidate["content_hash"],
                task_package_hash=task["content"]["task_package_hash"], result=result,
                requirements=mapping, accepted_item_coverage=coverage,
                provenance=provenance, infrastructure_error=error)


CONFIRMATION_VERSION = "independent-semantic-confirmation-v1"


def validate(task, candidate, validator, contract, disposition, reviewer=None):
    """Two one-shot evaluations; neither request contains the other's verdict.

    Host must isolate sessions. Distinct declared IDs prevent accidental reuse,
    not forged identities or correlated model errors. This is not a truth oracle.
    """
    primary = _evaluate(task, candidate, validator, contract, disposition)
    separation_error = None
    try:
        if (reviewer is None or reviewer is validator
                or reviewer.provenance["checker_id"] == primary["provenance"]["checker_id"]):
            raise ValueError("Separate Semantic reviewer required")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        reviewer = None
        separation_error = str(exc)
    review = _evaluate(task, candidate, reviewer, contract, disposition)
    if separation_error:
        review["infrastructure_error"] = separation_error
    results = [primary["result"], review["result"]]
    result = ("UNRESOLVED" if primary["infrastructure_error"] is not None else
              "MISALIGNED" if "MISALIGNED" in results else
              "ALIGNED" if results == ["ALIGNED", "ALIGNED"] else "UNRESOLVED")
    return dict(primary, result=result,
                infrastructure_error=primary["infrastructure_error"] or review["infrastructure_error"],
                semantic_confirmation=dict(version=CONFIRMATION_VERSION,
                                           primary_result=primary["result"], review=review))


def confirmation_is_bound(body, task, disposition, candidate):
    """Receipt identity and aggregation only; never infer meaning at Release."""
    from protocol.schema_validation import validate_named
    try:
        validate_named(body, "semantic_result")
        confirmation = body["semantic_confirmation"]
        review = confirmation["review"]
        if (confirmation["version"] != CONFIRMATION_VERSION
                or confirmation["primary_result"] != "ALIGNED"
                or body["result"] != "ALIGNED" or review["result"] != "ALIGNED"
                or body["infrastructure_error"] is not None
                or review["infrastructure_error"] is not None
                or body["provenance"]["checker_id"] == review["provenance"]["checker_id"]
                or body["provenance"]["prompt_hash"] != review["provenance"]["prompt_hash"]):
            return False
        required = {r["requirement_id"]: r["material"] for r in task["content"]["requirements"]}
        for receipt in (body, review):
            if (receipt["candidate_artifact_id"] != candidate["artifact_id"]
                    or receipt["candidate_content_hash"] != candidate["content_hash"]
                    or receipt["task_package_hash"] != task["content"]["task_package_hash"]
                    or not accepted_coverage.result_is_bound(receipt, disposition, candidate)
                    or receipt["provenance"]["checker_id"] in {"C", candidate["producer_id"]}
                    or receipt["provenance"]["checker_type"] in {"human-review", "human-local-review"}):
                return False
            rows = receipt["requirements"]
            if len(rows) != len(required) or {r["requirement_id"] for r in rows} != set(required):
                return False
            for row in rows:
                if row["status"] == "CONTRADICTED" or (required[row["requirement_id"]] and row["status"] != "COVERED"):
                    return False
                quote = row["response_evidence"]
                if quote is not None and quote not in candidate["content"]["text"]:
                    return False
                if row["status"] == "COVERED" and not quote:
                    return False
        return True
    except (KeyError, TypeError, ValueError):
        return False
