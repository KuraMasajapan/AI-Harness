"""Identity and lineage checks only. No text interpretation."""
from controller.artifact_store import ProtocolError, digest


REQUIRED = {
    "task_artifact_id": "TASK_PACKAGE",
    "analyst_a_artifact_id": "ANALYST_OUTPUT_A",
    "analyst_b_artifact_id": "ANALYST_OUTPUT_B",
    "comparator_artifact_id": "COMPARATOR_OUTPUT",
    "human_disposition_id": "HUMAN_DISPOSITION",
    "final_candidate_artifact_id": "FINAL_RESPONSE_CANDIDATE",
}


def check(manifest, store, candidate_id):
    checks = []

    def add(name, ok, evidence):
        checks.append(dict(name=name, result="PASS" if ok else "FAIL", evidence=str(evidence)))

    add("active_current_run", manifest["state"] in {"FINAL_CANDIDATE_FROZEN", "RELEASE_CHECK"}
        and not manifest["replacement_run_id"] and not manifest["invalidation_reason"], manifest["state"])
    add("candidate_identity", candidate_id == manifest["final_candidate_artifact_id"], candidate_id)
    visited = set()

    def visit(aid):
        if aid in visited:
            return
        visited.add(aid)
        record = store.get(aid)
        if record["run_id"] != manifest["run_id"]:
            raise ProtocolError("Foreign run in source lineage")
        for source in record["source_artifact_ids"]:
            visit(source)

    for key, kind in REQUIRED.items():
        aid = candidate_id if key == "final_candidate_artifact_id" else manifest.get(key)
        try:
            record = store.get(aid or "missing")
            visit(aid)
            add(key, record["artifact_type"] == kind, aid)
        except ProtocolError as exc:
            add(key, False, exc)
    try:
        candidate = store.get(candidate_id)
        add("candidate_run", candidate["run_id"] == manifest["run_id"], candidate["run_id"])
        add("candidate_task_hash", candidate.get("task_package_hash") == manifest["task_package_hash"], candidate.get("task_package_hash"))
        task = store.get(manifest["task_artifact_id"])["content"]
        task_hash = digest({k: v for k, v in task.items() if k != "task_package_hash"})
        add("canonical_task", task_hash == task["task_package_hash"] == manifest["task_package_hash"]
            and task["task_package_id"] == manifest["task_package_id"], task_hash)
        add("task_source_manifest", task["source_artifact_ids"] == manifest["source_artifact_ids"]
            and task["source_artifact_hashes"] == manifest["source_artifact_hashes"]
            and task["run_id"] == manifest["run_id"], task["source_artifact_ids"])
        expected_edges = {
            "analyst_a_artifact_id": ["task_artifact_id"],
            "analyst_b_artifact_id": ["task_artifact_id"],
            "comparator_artifact_id": ["task_artifact_id", "analyst_a_artifact_id", "analyst_b_artifact_id"],
            "human_disposition_id": ["comparator_artifact_id"],
        }
        for key, parents in expected_edges.items():
            record = store.get(manifest[key])
            add(key + "_lineage", {manifest[p] for p in parents}.issubset(set(record["source_artifact_ids"])),
                record["source_artifact_ids"])
        required_ids = {manifest[k] for k in REQUIRED if k != "final_candidate_artifact_id"}
        add("required_lineage", required_ids.issubset(set(candidate["source_artifact_ids"])), candidate["source_artifact_ids"])
    except (ProtocolError, KeyError) as exc:
        add("canonical_integrity", False, exc)
    return dict(candidate_artifact_id=candidate_id,
                result="PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL", checks=checks)
