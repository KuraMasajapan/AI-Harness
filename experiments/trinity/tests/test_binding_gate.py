from tests.support import *
from controller.binding_gate import check
from controller.artifact_store import ProtocolError

class BindingGate(Base):
    def test_positive(self):
        run = self.ready()
        m = self.manager.load(run)
        self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "PASS")

    def test_missing_unsealed_invalidated_and_tampered_sources(self):
        for fault in ("missing", "unsealed", "invalidated", "content", "metadata"):
            with self.subTest(fault=fault):
                run = self.ready()
                m = self.manager.load(run)
                aid = m["analyst_a_artifact_id"]
                path = self.manager.store.path(aid)
                record = self.manager.store.get(aid)
                if fault == "missing":
                    path.unlink()
                else:
                    if fault == "unsealed": record["sealed"] = False
                    if fault == "invalidated": record["invalidated"] = True
                    if fault == "content": record["content"]["text"] = "changed"
                    if fault == "metadata": record["run_id"] = "foreign"
                    write_json(path, record)
                self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "FAIL")
                self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_missing_candidate_lineage(self):
        run = self.ready()
        self.reseal_candidate(run, sources=[])
        m = self.manager.load(run)
        self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "FAIL")

    def test_wrong_task_and_run(self):
        for change in (dict(run_id="another-run"), dict(task_package_hash="0" * 64)):
            run = self.ready()
            self.reseal_candidate(run, **change)
            m = self.manager.load(run)
            self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "FAIL")

    def test_wrong_artifact_type(self):
        run = self.ready()
        self.reseal_candidate(run, kind="ANALYST_OUTPUT_A")
        m = self.manager.load(run)
        self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "FAIL")

    def test_path_traversal_rejected(self):
        for aid in ("../manifest", "", None, "a/b"):
            with self.assertRaises(ProtocolError):
                self.manager.store.get(aid)

    def test_integrity_failure_before_comparator_invalidates(self):
        run = self.manager.create(TASK)
        i = self.manager.input_manifest(run)
        self.manager.start_analysts(run, i, i)
        aid = self.manager.register_analyst(run, "A", "A")
        self.manager.register_analyst(run, "B", "B")
        self.manager.store.path(aid).write_text("{}", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            self.manager.start_comparator(run)
        self.assertEqual(self.manager.load(run)["state"], "INVALIDATED")


    def test_manifest_source_mismatch_fails(self):
        run = self.ready()
        m = self.manager.load(run)
        m["source_artifact_ids"] = ["unexpected"]
        self.assertEqual(check(m, self.manager.store, m["final_candidate_artifact_id"])["result"], "FAIL")
