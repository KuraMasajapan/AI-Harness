"""Fail-closed deterministic release decision."""
from controller.binding_gate import check
from controller.artifact_store import ProtocolError
from validation.accepted_coverage import result_is_bound


def decide(manifest, store):
    candidate_id = manifest["final_candidate_artifact_id"]
    reasons = []
    if check(manifest, store, candidate_id)["result"] != "PASS":
        reasons.append("Current binding or required artifact integrity failed")
    for key, kind, expected in (("binding_result_artifact_id", "BINDING_RESULT", "PASS"),
                                 ("semantic_alignment_result_artifact_id", "SEMANTIC_ALIGNMENT_RESULT", "ALIGNED")):
        try:
            record = store.get(manifest.get(key) or "missing")
            body = record["content"]
            if (record["artifact_type"] != kind or record["run_id"] != manifest["run_id"]
                    or body["candidate_artifact_id"] != candidate_id or body["result"] != expected
                    or candidate_id not in record["source_artifact_ids"]):
                reasons.append(f"{kind} failed or does not bind this candidate")
            if kind == "SEMANTIC_ALIGNMENT_RESULT":
                candidate = store.get(candidate_id)
                if body["candidate_content_hash"] != candidate["content_hash"] or body["task_package_hash"] != manifest["task_package_hash"]:
                    reasons.append("Stale semantic result")
                disposition = store.get(manifest["human_disposition_id"])
                if (disposition["artifact_id"] not in record["source_artifact_ids"]
                        or not result_is_bound(body, disposition, candidate)):
                    reasons.append("Missing, legacy or stale accepted-item Semantic receipt")
        except (ProtocolError, KeyError):
            reasons.append(f"{kind} missing or corrupt")
    return dict(candidate_artifact_id=candidate_id,
                binding_result_artifact_id=manifest["binding_result_artifact_id"],
                semantic_alignment_result_artifact_id=manifest["semantic_alignment_result_artifact_id"],
                human_disposition_id=manifest["human_disposition_id"],
                decision="DENY" if reasons else "RELEASE", reasons=reasons)
