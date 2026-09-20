"""Read-only operator receipt structure/hash check; never a protocol gate."""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from protocol.schema_validation import validate


def check(path):
    path = Path(path)
    receipt = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(Path(__file__).with_name("receipt.schema.json").read_text(encoding="utf-8"))
    validate(receipt, schema)
    errors, limitations = [], list(receipt["limitations"])
    entries = list(receipt["evidence"].items()) + [(f"input[{i}]", e) for i, e in enumerate(receipt["ordered_inputs"])]
    for name, entry in entries:
        if entry["status"] != "PRESENT":
            limitations.append(name + ": " + entry["status"] + ": " + entry["reason"])
            continue
        target = Path(entry["path"])
        if not target.is_absolute():
            target = path.parent / target
        try:
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != entry["sha256"]:
                errors.append(name + ": hash mismatch")
        except OSError as exc:
            errors.append(name + ": " + type(exc).__name__)
    if receipt["expected_timing"] != "BEFORE_EXECUTION":
        limitations.append("expected timing: " + receipt["expected_timing"])
    if not receipt["ordered_inputs"]:
        limitations.append("ordered input list empty")
    return dict(check="ERROR" if errors else "OK", errors=errors,
                limitations=limitations, functional_result=receipt["functional_result"],
                meaning="Structure/hash check only; completeness and authenticity not certified")


if __name__ == "__main__":
    try:
        result = check(sys.argv[1])
    except Exception as exc:
        result = dict(check="ERROR", errors=[str(exc)])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["check"] == "OK" else 1)
