import json
from controller.artifact_store import digest
from validation.accepted_coverage import header

TASK = dict(title="Current deployment", objective="Identify the required deployment region",
            instructions="State the required region Tokyo. Osaka is the previous deployment.",
            required_output="One sentence naming the required region", constraints=["Use the current deployment"],
            requirements=[dict(requirement_id="region", text="Required deployment region is Tokyo", material=True)])
CONTRACT = {"id": "fixture-semantic-contract-v1", "requirement_mapping": True}

def prepared(manager, text="The required deployment region is Tokyo."):
    run = manager.create(TASK)
    inputs = manager.input_manifest(run)
    manager.start_analysts(run, inputs, inputs)
    manager.register_analyst(run, "A", "Tokyo; task instructions are the evidence.")
    manager.register_analyst(run, "B", "Tokyo; agreement alone is not proof.")
    manager.start_comparator(run)
    manager.register_comparator(run, "Converges on Tokyo, grounded in the current task. No vote or winner.")
    manager.disposition(run, "ACCEPT", accepted_items=["region"])
    manager.freeze(run, text, "response-producer")
    return run

class FixtureValidator:
    """Test double only. Reads a fixed response corpus, never the expected-results manifest."""
    def __init__(self, checker_id="offline-fixture-adapter"):
        from pathlib import Path
        self.corpus = json.loads((Path(__file__).parent / "validator_corpus.json").read_text(encoding="utf-8"))
        self.provenance = dict(checker_id=checker_id, checker_type="test-double",
                               checker_version="fixture-corpus-v2",
                               model_name=None, model_version=None, config_hash=digest(self.corpus),
                               prompt_hash=digest(CONTRACT))
    def evaluate(self, request):
        task = json.loads(request.task_json)["content"]
        text = json.loads(request.candidate_json)["content"]["text"]
        status = self.corpus.get(text, "UNRESOLVED")
        rows = [dict(requirement_id=r["requirement_id"], status=status,
                     response_evidence=text if status in {"COVERED", "CONTRADICTED"} else None,
                     notes="Fixed adapter corpus; no claim of semantic capability") for r in task["requirements"]]
        coverage = dict(**header(json.loads(request.disposition_json), self.provenance["checker_version"]),
                        items=[dict(item_id=i["item_id"], item_index=i["item_index"], required=True,
                                    status=status, response_evidence=text if status in {"COVERED", "CONTRADICTED"} else None,
                                    notes="Fixed test double verdict, not production semantic judgment")
                               for i in json.loads(request.accepted_items_json)])
        return dict(requirements=rows, accepted_item_coverage=coverage)
