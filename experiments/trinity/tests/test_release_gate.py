from tests.support import *
from controller.artifact_store import ProtocolError

class ReleaseGate(Base):
    def test_missing_checks_and_human_deny(self):
        run = self.ready()
        self.assertEqual(self.manager.release(run)["decision"], "DENY")
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        self.inject(run, human_disposition_id=None)
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_missing_candidate_denies(self):
        run = self.manager.create(TASK)
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_unresolved_denies(self):
        run = self.ready()
        _, s = self.manager.checks(run)
        self.assertEqual(s["result"], "UNRESOLVED")
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_misaligned_denies(self):
        run = self.ready("The required deployment region is Osaka.")
        _, s = self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        self.assertEqual(s["result"], "MISALIGNED")
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_new_candidate_clears_checks(self):
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        old = self.manager.load(run)
        self.manager.freeze(run, "The required deployment region is Osaka.", "response-producer")
        current = self.manager.load(run)
        self.assertNotEqual(old["final_candidate_artifact_id"], current["final_candidate_artifact_id"])
        self.assertIsNone(current["binding_result_artifact_id"])
        self.assertIsNone(current["semantic_alignment_result_artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_stale_results_cannot_be_reused(self):
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        old = self.manager.load(run)
        self.manager.freeze(run, "The required deployment region is Osaka.", "response-producer")
        self.inject(run, binding_result_artifact_id=old["binding_result_artifact_id"],
                    semantic_alignment_result_artifact_id=old["semantic_alignment_result_artifact_id"])
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_no_silent_semantic_retry(self):
        run = self.ready()
        self.manager.checks(run)
        with self.assertRaises(ProtocolError):
            self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))

    def test_tamper_after_checks_denies(self):
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        aid = self.manager.load(run)["final_candidate_artifact_id"]
        record = self.manager.store.get(aid)
        record["content"]["text"] = "Substituted output"
        write_json(self.manager.store.path(aid), record)
        self.assertEqual(self.manager.release(run)["decision"], "DENY")

    def test_invalidated_run_denies(self):
        run = self.ready()
        self.manager.checks(run, FixtureValidator(), CONTRACT, reviewer=FixtureValidator("fixture-confirmation"))
        self.manager.invalidate(run, "Explicit protocol failure")
        self.assertEqual(self.manager.release(run)["decision"], "DENY")


    def test_release_decision_is_immutable(self):
        run = self.ready()
        self.manager.release(run)
        decision_id = self.manager.load(run)["release_decision_artifact_id"]
        with self.assertRaises(ProtocolError):
            self.manager.release(run)
        self.assertEqual(self.manager.load(run)["release_decision_artifact_id"], decision_id)
