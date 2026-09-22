from tests.support import *
from controller.artifact_store import ProtocolError
from pathlib import Path

class StateMachine(Base):
    def test_lifecycle_reload_and_exact_release(self):
        run = self.ready()
        self.manager = RunManager(self.temp.name)
        b, s = self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        result = self.manager.release(run)
        self.assertEqual((b["result"], s["result"], result["decision"]), ("PASS", "ALIGNED", "RELEASE"))
        self.assertEqual(result["text"], "The required deployment region is Tokyo.")
        events = self.manager.events(run)
        self.assertEqual([e["event_seq"] for e in events], list(range(1, len(events) + 1)))
        self.assertEqual(self.manager.load(run)["state"], "RELEASED")
        audit = self.manager.audit(run)
        for aid, record in audit["artifacts"].items():
            self.assertTrue(set(record["source_artifact_ids"]) <= set(audit["artifacts"]))
            self.assertEqual(record["created_event_seq"], next(e["event_seq"] for e in events if aid in e["artifact_ids"]))

    def test_out_of_order_comparator_rejected(self):
        run = self.manager.create(TASK)
        with self.assertRaises(ProtocolError):
            self.manager.start_comparator(run)
        self.assertEqual(self.manager.load(run)["state"], "CREATED")

    def test_duplicate_analyst_rejected(self):
        run = self.manager.create(TASK)
        i = self.manager.input_manifest(run)
        self.manager.start_analysts(run, i, i)
        self.manager.register_analyst(run, "A", "Sealed")
        with self.assertRaises(ProtocolError):
            self.manager.register_analyst(run, "A", "Replacement")

    def test_peer_and_comparator_access_boundaries(self):
        run = self.manager.create(TASK)
        i = self.manager.input_manifest(run)
        self.manager.start_analysts(run, i, i)
        a = self.manager.register_analyst(run, "A", "Private A")
        b_input = self.manager.role_inputs(run, "B")
        self.assertNotIn(a, [r["artifact_id"] for r in b_input["artifacts"]])
        with self.assertRaises(ProtocolError):
            self.manager.role_inputs(run, "C")
        b_input["artifacts"][0]["content"]["instructions"] = "tampered local copy"
        self.assertNotEqual(self.manager.role_inputs(run, "A")["artifacts"][0]["content"]["instructions"], "tampered local copy")
        self.manager.register_analyst(run, "B", "Private B")
        self.assertEqual(len(self.manager.start_comparator(run)["artifacts"]), 4)
        with self.assertRaises(ProtocolError):
            self.manager.role_inputs(run, "A")
        with self.assertRaises(ProtocolError):
            self.manager.intervention(run, "SHARED_CLARIFICATION", "feedback", source="OPERATOR", targets=["A", "B"])
        with self.assertRaises(ProtocolError):
            self.manager.intervention(run, "PROCEDURAL_NOTICE", "feedback", source="C")

    def test_clean_restart_and_terminal_old_run(self):
        run = self.ready()
        new = self.manager.amend(run, dict(type="TASK_AMENDMENT", reason="New objective", changes_task_conditions=True),
                                 dict(TASK, objective="Updated objective"))
        old = self.manager.load(run)
        self.assertEqual((old["state"], old["replacement_run_id"]), ("TERMINATED", new))
        self.assertEqual(self.manager.load(new)["previous_run_id"], run)
        self.assertNotEqual(old["task_package_hash"], self.manager.load(new)["task_package_hash"])
        with self.assertRaises(ProtocolError):
            self.manager.freeze(run, "Old", "producer")
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_task_changing_intervention_cannot_bypass_restart(self):
        run = self.ready()
        with self.assertRaises(ProtocolError):
            self.manager.intervention(run, "SHARED_CLARIFICATION", "change objective", changes_task_conditions=True)
        with self.assertRaises(ProtocolError):
            self.manager.amend(run, dict(type="TASK_AMENDMENT", reason="change", changes_task_conditions=False), TASK)

    def test_audit_repair_retains_original(self):
        run = self.ready()
        aid = self.manager.load(run)["analyst_a_artifact_id"]
        before = self.manager.store.get(aid)
        self.manager.audit_repair(run, aid, "Omitted visible text", "Recording repair")
        self.assertEqual(before, self.manager.store.get(aid))
        log = self.manager.interventions(run)[-1]
        self.assertIn(before["content_hash"], log["content"])
        self.assertIn("Omitted visible text", log["content"])

    def test_event_or_manifest_corruption_fail_closed(self):
        for target in ("events.jsonl", "manifest.json"):
            with self.subTest(target=target):
                run = self.ready()
                path = self.manager._dir(run) / target
                if target == "events.jsonl":
                    with path.open("a", encoding="utf-8") as stream:
                        stream.write(path.read_text(encoding="utf-8").splitlines()[0] + "\n")
                else:
                    m = self.manager.load(run)
                    m["state"] = "RELEASED"
                    write_json(path, m)
                with self.assertRaises(ProtocolError):
                    self.manager.release(run)

    def test_writer_overlap_and_crash_marker_rejected(self):
        (Path(self.temp.name) / ".writer.lock").write_text("incomplete", encoding="utf-8")
        with self.assertRaises(ProtocolError):
            self.manager.create(TASK)

    def test_noncompletion_has_no_synthetic_output(self):
        run = self.manager.create(TASK)
        self.manager.terminate(run, "Analyst unavailable")
        self.assertIsNone(self.manager.load(run)["analyst_a_artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")


    def test_post_release_audit_repair_does_not_reopen_run(self):
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        self.manager.release(run)
        m = self.manager.load(run)
        original = self.manager.store.get(m["analyst_a_artifact_id"])
        self.manager.audit_repair(run, original["artifact_id"], "Late visible transcript", "Audit completeness")
        self.assertEqual(self.manager.load(run)["state"], "RELEASED")
        self.assertEqual(original, self.manager.store.get(original["artifact_id"]))

    def test_direct_replacement_cannot_bypass_termination(self):
        run = self.ready()
        with self.assertRaises(ProtocolError):
            self.manager.create(TASK, previous_run_id=run)

    def test_audit_preserves_corruption_diagnostics(self):
        run = self.ready()
        aid = self.manager.load(run)["analyst_a_artifact_id"]
        self.manager.store.path(aid).unlink()
        self.manager.release(run)
        audit = self.manager.audit(run)
        self.assertFalse(audit["validity_records"][aid]["valid"])
