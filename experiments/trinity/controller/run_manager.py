"""Deterministic controller. Only detached role inputs may cross the trust boundary."""
import copy
import json
from pathlib import Path
from controller.artifact_store import ArtifactStore, ProtocolError, canonical, digest, identifier, write_json
from controller.binding_gate import check
from controller.release_gate import decide
from validation.semantic_alignment import validate
from protocol.schema_validation import validate_named

TERMINAL = {"RELEASED", "TERMINATED", "INVALIDATED"}
VERSION = "TRINITY-V0.1"


class RunManager:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.store = ArtifactStore(self.root / "artifacts")

    def _dir(self, run_id):
        self.store.path(run_id)
        return self.root / run_id

    def load(self, run_id):
        try:
            folder = self._dir(run_id)
            manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            events = self.events(run_id)
            previous = None
            for seq, event in enumerate(events, 1):
                body = {k: v for k, v in event.items() if k != "event_hash"}
                if (event["run_id"] != run_id or event["event_seq"] != seq
                        or event["previous_event_hash"] != previous or digest(body) != event["event_hash"]
                        or event["manifest"]["event_seq"] != seq):
                    raise ProtocolError("Journal integrity failure; manual recovery required")
                previous = event["event_hash"]
            if not events or manifest != events[-1]["manifest"]:
                raise ProtocolError("Manifest/journal mismatch; manual recovery required")
            return manifest
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            raise ProtocolError("Incomplete run; manual recovery required") from exc

    def _event(self, m, kind, actor="O", artifacts=(), metadata=None):
        folder = self._dir(m["run_id"])
        path = folder / "events.jsonl"
        previous = None
        if path.exists():
            current = self.load(m["run_id"])
            if current["event_seq"] != m["event_seq"]:
                raise ProtocolError("Non-monotonic event attempt")
            previous = self.events(m["run_id"])[-1]["event_hash"]
        m["event_seq"] += 1
        event = dict(run_id=m["run_id"], event_seq=m["event_seq"], event_type=kind,
                     actor=actor, artifact_ids=list(artifacts), metadata=metadata or {},
                     previous_event_hash=previous, manifest=copy.deepcopy(m))
        event["event_hash"] = digest(event)
        validate_named(event, "event")
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(canonical(event) + "\n")
        write_json(folder / "manifest.json", m)

    def _require(self, run_id, *states):
        m = self.load(run_id)
        if m["state"] not in states:
            raise ProtocolError("Invalid transition from " + m["state"])
        return m

    def _artifact(self, m, kind, body, sources=(), **metadata):
        names = {"TASK_PACKAGE": "task_package", "HUMAN_DISPOSITION": "human_disposition",
                 "BINDING_RESULT": "binding_result", "SEMANTIC_ALIGNMENT_RESULT": "semantic_result",
                 "RELEASE_DECISION": "release_decision", "TEST_MANIFEST": "test_manifest", "TEST_RESULT": "test_result"}
        if kind in names:
            validate_named(body, names[kind])
        return self.store.seal(kind, m["run_id"], body, m["event_seq"] + 1, sources, **metadata)

    def create(self, task, previous_run_id=None):
        if previous_run_id is not None:
            old = self.load(previous_run_id)
            if (old["state"] != "TERMINATED" or old["termination_reason"] != "TASK_AMENDMENT"
                    or old["replacement_run_id"] is not None):
                raise ProtocolError("Replacement must follow an explicit task amendment")
        required = {"title", "objective", "instructions", "required_output", "constraints", "requirements"}
        if set(task) != required:
            raise ProtocolError("Task requires explicit instruction and material requirement declarations")
        if any(not isinstance(task[k], str) or not task[k] for k in ("title", "objective", "instructions", "required_output")):
            raise ProtocolError("Task text must be nonempty")
        if not isinstance(task["constraints"], list) or any(not isinstance(x, str) for x in task["constraints"]):
            raise ProtocolError("Constraints must be strings")
        req = task["requirements"]
        if (not isinstance(req, list) or not req
                or any(set(r) != {"requirement_id", "text", "material"} or type(r["material"]) is not bool
                       or not isinstance(r["requirement_id"], str) or not r["requirement_id"]
                       or not isinstance(r["text"], str) or not r["text"] for r in req)
                or len({r["requirement_id"] for r in req}) != len(req)):
            raise ProtocolError("Invalid explicit requirement declarations")
        run_id = identifier()
        self._dir(run_id).mkdir()
        m = dict(protocol_version=VERSION, run_id=run_id, previous_run_id=previous_run_id,
                 replacement_run_id=None, state="CREATED", event_seq=0, task_package_id=identifier(),
                 task_package_hash="", source_artifact_ids=[], source_artifact_hashes=[],
                 termination_reason=None, invalidation_reason=None, created_at=None, updated_at=None)
        for key in ("analyst_a_artifact_id", "analyst_b_artifact_id", "comparator_artifact_id",
                    "human_disposition_id", "final_candidate_artifact_id", "binding_result_artifact_id",
                    "semantic_alignment_result_artifact_id", "release_decision_artifact_id"):
            m[key] = None
        log = self._artifact(m, "OPERATOR_INTERVENTION_LOG", {"storage": "events.jsonl", "entries": []})
        m["operator_intervention_log_id"] = log["artifact_id"]
        self._event(m, "RUN_CREATED", artifacts=[log["artifact_id"]])
        content = dict(copy.deepcopy(task), task_package_id=m["task_package_id"], run_id=run_id,
                       protocol_version=VERSION, source_artifact_ids=[], source_artifact_hashes=[],
                       created_event_seq=m["event_seq"] + 1, sealed=True)
        content["task_package_hash"] = digest(content)
        record = self._artifact(m, "TASK_PACKAGE", content)
        m.update(task_package_hash=content["task_package_hash"], task_artifact_id=record["artifact_id"])
        self._event(m, "TASK_PACKAGE_SEALED", artifacts=[record["artifact_id"]])
        return run_id

    def invalidate(self, run_id, reason):
        m = self.load(run_id)
        if m["state"] in TERMINAL:
            raise ProtocolError("Terminal run")
        m.update(state="INVALIDATED", invalidation_reason=reason)
        self._event(m, "RUN_INVALIDATED", metadata={"protocol_error": reason})

    def input_manifest(self, run_id):
        m = self.load(run_id)
        return dict(task_package_hash=m["task_package_hash"], task_artifact_id=m["task_artifact_id"],
                    source_artifact_ids=[], transcript_artifact_ids=[])

    def start_analysts(self, run_id, a_input, b_input):
        m = self._require(run_id, "CREATED")
        expected = self.input_manifest(run_id)
        if a_input != expected or b_input != expected:
            self.invalidate(run_id, "A/B identity or clean-input violation")
            raise ProtocolError("A/B must receive identical clean canonical inputs")
        self.store.get(m["task_artifact_id"])
        m["state"] = "ANALYST_RUNNING"
        self._event(m, "ANALYST_A_STARTED", actor="A", metadata={"input_manifest": a_input})
        self._event(m, "ANALYST_B_STARTED", actor="B", metadata={"input_manifest": b_input})

    def role_inputs(self, run_id, role):
        m = self.load(run_id)
        if role in {"A", "B"}:
            self._require(run_id, "ANALYST_RUNNING")
            ids = [m["task_artifact_id"]]
        elif role == "C":
            self._require(run_id, "COMPARATOR_RUNNING")
            ids = [m[k] for k in ("task_artifact_id", "analyst_a_artifact_id", "analyst_b_artifact_id", "operator_intervention_log_id")]
        else:
            raise ProtocolError("Unknown reasoning role")
        return {"role": role, "artifacts": [self.store.get(aid) for aid in ids],
                "instructions": ("Compare evidence, convergence, divergence and unresolved items; no winner, vote, truth certification or feedback."
                                 if role == "C" else "Use only this canonical task in a fresh isolated context."),
                "interventions": self.interventions(run_id) if role == "C" else []}

    def register_analyst(self, run_id, role, text):
        m = self._require(run_id, "ANALYST_RUNNING")
        if role not in {"A", "B"} or not isinstance(text, str) or not text:
            raise ProtocolError("Invalid analyst output")
        key = "analyst_" + role.lower() + "_artifact_id"
        if m[key]:
            raise ProtocolError("Analyst already sealed")
        record = self._artifact(m, "ANALYST_OUTPUT_" + role, {"text": text}, [m["task_artifact_id"]])
        m[key] = record["artifact_id"]
        if m["analyst_a_artifact_id"] and m["analyst_b_artifact_id"]:
            m["state"] = "ANALYST_SEALED"
        self._event(m, "ANALYST_" + role + "_SEALED", actor=role, artifacts=[record["artifact_id"]])

    def start_comparator(self, run_id):
        m = self._require(run_id, "ANALYST_SEALED")
        self.store.get(m["analyst_a_artifact_id"]); self.store.get(m["analyst_b_artifact_id"])
        m["state"] = "COMPARATOR_RUNNING"
        self._event(m, "COMPARATOR_STARTED", actor="C")
        return self.role_inputs(run_id, "C")

    def register_comparator(self, run_id, text):
        m = self._require(run_id, "COMPARATOR_RUNNING")
        if not isinstance(text, str) or not text:
            raise ProtocolError("Invalid comparator output")
        sources = [m[k] for k in ("task_artifact_id", "analyst_a_artifact_id", "analyst_b_artifact_id", "operator_intervention_log_id")]
        record = self._artifact(m, "COMPARATOR_OUTPUT", {"text": text}, sources)
        m.update(comparator_artifact_id=record["artifact_id"], state="COMPARATOR_SEALED")
        self._event(m, "COMPARATOR_SEALED", actor="C", artifacts=[record["artifact_id"]])

    def interventions(self, run_id):
        return [e["metadata"] for e in self.events(run_id) if e["event_type"] == "OPERATOR_INTERVENTION_RECORDED"]

    def intervention(self, run_id, kind, content, source="HUMAN", targets=("A", "B", "C"), changes_task_conditions=False):
        m = self.load(run_id)
        if m["state"] in TERMINAL or source not in {"HUMAN", "OPERATOR"}:
            raise ProtocolError("Terminal run")
        semantic_types = {"TASK_AMENDMENT", "HUMAN_DECISION"}
        informational_types = {"SOURCE_CLARIFICATION", "PROTOCOL_REPAIR", "AUDIT_CORRECTION"}
        if kind not in semantic_types | informational_types or not isinstance(content, str) or (not content and kind != "HUMAN_DECISION"):
            raise ProtocolError("Invalid intervention")
        target_roles = list(targets)
        if changes_task_conditions or kind == "TASK_AMENDMENT":
            raise ProtocolError("Use amend() so task-changing intervention restarts the run")
        if kind == "HUMAN_DECISION" and target_roles != ["H"]:
            raise ProtocolError("Human decisions stay at H boundary")
        if kind in informational_types and set(target_roles) != {"A", "B", "C"}:
            raise ProtocolError("Informational intervention must be symmetric")
        entry = dict(run_id=run_id, event_seq=m["event_seq"] + 1, intervention_id=identifier(), phase=m["state"],
                     target_roles=target_roles, type=kind, content=content, changes_task_conditions=False,
                     shared_symmetrically=kind in informational_types, source=source)
        self._event(m, "OPERATOR_INTERVENTION_RECORDED", actor=source, metadata=entry)

    def disposition(self, run_id, decision, accepted_items=(), rejected_items=(), deferred_items=(), notes=""):
        m = self._require(run_id, "COMPARATOR_SEALED")
        if decision not in {"ACCEPT", "ACCEPT_WITH_EXPLICIT_SELECTION", "DEFER", "NO_DECISION"}:
            raise ProtocolError("Invalid human disposition")
        if any(not isinstance(x, str) for seq in (accepted_items, rejected_items, deferred_items) for x in seq):
            raise ProtocolError("Disposition items must be strings")
        self.intervention(run_id, "HUMAN_DECISION", notes, targets=["H"])
        m = self.load(run_id)
        record = self._artifact(m, "HUMAN_DISPOSITION",
                                dict(decision=decision, accepted_items=list(accepted_items), rejected_items=list(rejected_items),
                                     deferred_items=list(deferred_items), notes=notes), [m["comparator_artifact_id"]])
        m.update(human_disposition_id=record["artifact_id"], state="HUMAN_DISPOSITION")
        self._event(m, "HUMAN_DISPOSITION_RECORDED", actor="H", artifacts=[record["artifact_id"]])

    def freeze(self, run_id, text, producer_id):
        m = self._require(run_id, "HUMAN_DISPOSITION", "FINAL_CANDIDATE_FROZEN", "RELEASE_CHECK")
        if not isinstance(text, str) or not text or not isinstance(producer_id, str) or not producer_id:
            raise ProtocolError("Exact response and producer required")
        sources = [m[k] for k in ("task_artifact_id", "analyst_a_artifact_id", "analyst_b_artifact_id", "comparator_artifact_id", "human_disposition_id")]
        record = self._artifact(m, "FINAL_RESPONSE_CANDIDATE", {"text": text}, sources,
                                task_package_hash=m["task_package_hash"], producer_id=producer_id)
        m.update(final_candidate_artifact_id=record["artifact_id"], binding_result_artifact_id=None,
                 semantic_alignment_result_artifact_id=None, release_decision_artifact_id=None, state="FINAL_CANDIDATE_FROZEN")
        self._event(m, "FINAL_CANDIDATE_FROZEN", actor=producer_id, artifacts=[record["artifact_id"]])
        return record["artifact_id"]

    def checks(self, run_id, validator=None, contract=None, candidate_id=None, reviewer=None):
        m = self._require(run_id, "FINAL_CANDIDATE_FROZEN")
        candidate_id = candidate_id or m["final_candidate_artifact_id"]
        binding = check(m, self.store, candidate_id)
        m["state"] = "RELEASE_CHECK"
        record = self._artifact(m, "BINDING_RESULT", binding, [candidate_id])
        m["binding_result_artifact_id"] = record["artifact_id"]
        self._event(m, "BINDING_CHECK_COMPLETED", artifacts=[record["artifact_id"]])
        try:
            semantic = validate(self.store.get(m["task_artifact_id"]), self.store.get(candidate_id),
                                validator, contract or {}, self.store.get(m["human_disposition_id"]), reviewer=reviewer)
        except ProtocolError as exc:
            self.invalidate(run_id, str(exc))
            return binding, None
        record = self._artifact(m, "SEMANTIC_ALIGNMENT_RESULT", semantic,
                                [m["task_artifact_id"], candidate_id, m["human_disposition_id"]])
        m["semantic_alignment_result_artifact_id"] = record["artifact_id"]
        self._event(m, "SEMANTIC_ALIGNMENT_COMPLETED", artifacts=[record["artifact_id"]],
                    metadata={"infrastructure_error": semantic["infrastructure_error"]})
        return binding, semantic

    def release(self, run_id):
        m = self.load(run_id)
        if m["state"] in TERMINAL:
            return dict(decision="DENY", reasons=["Terminal run; no further protocol events"])
        if m["release_decision_artifact_id"]:
            raise ProtocolError("Decision already recorded; freeze a new candidate for new checks")
        result = decide(m, self.store)
        sources = [m[k] for k in ("final_candidate_artifact_id", "binding_result_artifact_id", "semantic_alignment_result_artifact_id", "human_disposition_id") if m[k]]
        record = self._artifact(m, "RELEASE_DECISION", result, sources)
        m["release_decision_artifact_id"] = record["artifact_id"]
        self._event(m, "RELEASE_DECISION_RECORDED", artifacts=[record["artifact_id"]])
        if result["decision"] == "RELEASE":
            m["state"] = "RELEASED"
            self._event(m, "RUN_RELEASED", artifacts=[m["final_candidate_artifact_id"], record["artifact_id"]])
            result["text"] = self.store.get(m["final_candidate_artifact_id"])["content"]["text"]
        return result

    def terminate(self, run_id, reason):
        m = self.load(run_id)
        if m["state"] in TERMINAL:
            raise ProtocolError("Terminal run")
        m.update(state="TERMINATED", termination_reason=reason)
        self._event(m, "RUN_TERMINATED", metadata={"reason": reason})

    def amend(self, run_id, declaration, task):
        m = self.load(run_id)
        if m["state"] in TERMINAL or set(declaration) != {"type", "reason", "changes_task_conditions"}:
            raise ProtocolError("Invalid amendment")
        if declaration["type"] != "TASK_AMENDMENT" or declaration["changes_task_conditions"] is not True or not declaration["reason"]:
            raise ProtocolError("Explicit human declaration required")
        entry = dict(run_id=run_id, event_seq=m["event_seq"] + 1, intervention_id=identifier(), phase=m["state"],
                     target_roles=["A", "B", "C", "H"], type="TASK_AMENDMENT", content=declaration["reason"],
                     changes_task_conditions=True, shared_symmetrically=True, source="HUMAN")
        self._event(m, "OPERATOR_INTERVENTION_RECORDED", actor="H", metadata=entry)
        self.terminate(run_id, "TASK_AMENDMENT")
        new_id = self.create(task, previous_run_id=run_id)
        m = self.load(run_id)
        m["replacement_run_id"] = new_id
        self._event(m, "REPLACEMENT_RUN_CREATED", metadata={"replacement_run_id": new_id})
        inputs = self.input_manifest(new_id)
        self.start_analysts(new_id, inputs, inputs)
        return new_id

    def audit_repair(self, run_id, analyst_id, material, reason):
        record = self.store.get(analyst_id)
        if record["run_id"] != run_id or record["artifact_type"] not in {"ANALYST_OUTPUT_A", "ANALYST_OUTPUT_B"}:
            raise ProtocolError("Audit repair requires this run's analyst artifact")
        m = self.load(run_id)
        entry = dict(run_id=run_id, event_seq=m["event_seq"] + 1, intervention_id=identifier(), phase=m["state"],
                     target_roles=[], type="AUDIT_CORRECTION",
                     content=canonical(dict(original_artifact_id=analyst_id, original_sealed_hash=record["content_hash"],
                                            added_transcript_material=material, reason=reason)),
                     changes_task_conditions=False, shared_symmetrically=True, source="OPERATOR")
        self._event(m, "OPERATOR_INTERVENTION_RECORDED", actor="OPERATOR", metadata=entry)

    def events(self, run_id):
        return [json.loads(s) for s in (self._dir(run_id) / "events.jsonl").read_text(encoding="utf-8").splitlines()]

    def audit(self, run_id):
        m = self.load(run_id)
        events = self.events(run_id)
        records = {}
        validity_records = {}
        def visit(aid):
            if aid in validity_records:
                return
            try:
                records[aid] = self.store.get(aid)
                validity_records[aid] = {"valid": True}
            except ProtocolError as exc:
                validity_records[aid] = {"valid": False, "reason": str(exc)}
                return
            for source in records[aid]["source_artifact_ids"]:
                visit(source)
        for event in events:
            for aid in event["artifact_ids"]:
                visit(aid)
        return dict(manifest=m, events=events, artifacts=records, interventions=self.interventions(run_id), validity_records=validity_records)



def _serialized(method):
    """Reject overlapping writers; this is a guard, not a production concurrency policy."""
    from functools import wraps
    @wraps(method)
    def call(self, *args, **kwargs):
        nested = getattr(self, "_operation_depth", 0)
        lock = self.root / ".writer.lock"
        if not nested:
            try:
                with lock.open("x", encoding="utf-8") as stream:
                    stream.write("prototype operation in progress")
            except FileExistsError as exc:
                raise ProtocolError("Writer active or incomplete operation; manual recovery required") from exc
        self._operation_depth = nested + 1
        try:
            return method(self, *args, **kwargs)
        except ProtocolError as exc:
            if not nested and args and method.__name__ != "create" and any(
                    word in str(exc).lower() for word in ("integrity", "malformed artifact", "missing or malformed")):
                try:
                    current = self.load(args[0])
                    if current["state"] not in TERMINAL:
                        self.invalidate(args[0], str(exc))
                except ProtocolError:
                    pass
            raise
        finally:
            self._operation_depth = nested
            if not nested:
                lock.unlink()
    return call


for _name in ("create", "invalidate", "start_analysts", "register_analyst", "start_comparator",
              "register_comparator", "intervention", "disposition", "freeze", "checks", "release",
              "terminate", "amend", "audit_repair"):
    setattr(RunManager, _name, _serialized(getattr(RunManager, _name)))
