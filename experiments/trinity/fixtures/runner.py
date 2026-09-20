"""Preseal ground truth, execute all required cases, and persist test provenance."""
import json
from pathlib import Path
from controller.artifact_store import ProtocolError, digest, write_json
from controller.run_manager import RunManager
from fixtures.support import TASK, CONTRACT, FixtureValidator, prepared
from protocol.schema_validation import validate_named

def execute(manager, case):
    condition = case["condition"]
    if condition in {"divergent", "old_transcript"}:
        run = manager.create(TASK)
        inputs = manager.input_manifest(run)
        wrong = dict(inputs)
        if condition == "divergent":
            wrong["task_package_hash"] = "f" * 64
        else:
            old = prepared(manager)
            wrong["transcript_artifact_ids"] = [manager.load(old)["analyst_a_artifact_id"]]
        rejected = False
        try:
            manager.start_analysts(run, inputs, wrong)
        except ProtocolError:
            rejected = True
        return run, dict(binding="NOT_APPLICABLE", semantic="NOT_APPLICABLE",
                         release=manager.release(run)["decision"], conformance_failure=rejected,
                         state=manager.load(run)["state"])
    run = prepared(manager, case["candidate"])
    if condition == "amend":
        updated = dict(TASK, objective="Identify the required region for a replacement deployment")
        new = manager.amend(run, dict(type="TASK_AMENDMENT", reason="Human changes objective",
                                     changes_task_conditions=True), updated)
        return run, dict(binding="NOT_APPLICABLE", semantic="NOT_APPLICABLE",
                         release=manager.release(run)["decision"], state=manager.load(run)["state"],
                         replacement_created=manager.load(new)["previous_run_id"] == run,
                         clean_inputs=manager.input_manifest(new)["transcript_artifact_ids"] == [])
    candidate_id = None
    if condition == "old_candidate":
        old = prepared(manager)
        manager.terminate(old, "Superseded fixture run")
        candidate_id = manager.load(old)["final_candidate_artifact_id"]
    if condition in {"wrong_run", "wrong_hash"}:
        m = manager.load(run)
        original = manager.store.get(m["final_candidate_artifact_id"])
        record = manager.store.seal("FINAL_RESPONSE_CANDIDATE",
                                   "foreign-run" if condition == "wrong_run" else run,
                                   original["content"], m["event_seq"] + 1, original["source_artifact_ids"],
                                   task_package_hash="f" * 64 if condition == "wrong_hash" else m["task_package_hash"],
                                   producer_id=original["producer_id"])
        m["final_candidate_artifact_id"] = record["artifact_id"]
        manager._event(m, "FINAL_CANDIDATE_FROZEN", artifacts=[record["artifact_id"]],
                       metadata={"fixture_fault_injection": condition})
    binding, semantic = manager.checks(run, FixtureValidator(), CONTRACT, candidate_id)
    return run, dict(binding=binding["result"], semantic=semantic["result"] if semantic else "UNRESOLVED",
                     release=manager.release(run)["decision"])

def run_suite(root):
    manager = RunManager(root)
    manifest = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
    validate_named(manifest, "test_manifest")
    cases = {f["fixture_id"]: json.loads((Path(__file__).parent / f["input_artifact_refs"][0]).read_text(encoding="utf-8"))
             for f in manifest["fixtures"]}
    audit_run = manager.create(TASK)
    m = manager.load(audit_run)
    sealed = manager._artifact(m, "TEST_MANIFEST", manifest)
    manager._event(m, "TEST_MANIFEST_SEALED", artifacts=[sealed["artifact_id"]],
                   metadata={"input_hashes": {key: digest(value) for key, value in cases.items()}})
    results = []
    for fixture in manifest["fixtures"]:
        run, actual = execute(manager, cases[fixture["fixture_id"]])
        expected = dict(binding=fixture["expected_binding_result"], semantic=fixture["expected_semantic_result"],
                        release=fixture["expected_release_result"])
        expected.update(cases[fixture["fixture_id"]].get("expected_control", {}))
        passed = all(actual.get(key) == value for key, value in expected.items())
        result = dict(fixture_id=fixture["fixture_id"], test_manifest_artifact_id=sealed["artifact_id"],
                      test_manifest_hash=sealed["content_hash"], result="PASS" if passed else "FAIL", actual=actual)
        m = manager.load(audit_run)
        record = manager._artifact(m, "TEST_RESULT", result, [sealed["artifact_id"]])
        manager._event(m, "TEST_RESULT_RECORDED", artifacts=[record["artifact_id"]], metadata={"fixture_run_id": run})
        write_json(Path(root) / (fixture["fixture_id"] + "-audit.json"), manager.audit(run))
        print(result["result"] + " " + fixture["fixture_id"])
        results.append(result)
    manager.terminate(audit_run, "Fixture suite completed")
    write_json(Path(root) / "test-audit.json", manager.audit(audit_run))
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raise SystemExit(0 if all(r["result"] == "PASS" for r in run_suite(args.output)) else 1)
