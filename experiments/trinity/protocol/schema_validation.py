"""Offline validator for the explicit JSON Schema vocabulary used in this prototype.
Not a general JSON Schema engine. Unsupported keywords fail rather than being ignored.
Schemas themselves are ordinary draft 2020-12 documents usable by full validators.
"""
import json
import re
from pathlib import Path
from controller.artifact_store import ProtocolError

ROOT = Path(__file__).parent / "schemas"
KEYWORDS = {"$schema", "$id", "title", "description", "type", "properties", "required",
            "additionalProperties", "items", "enum", "const", "minimum", "minLength",
            "pattern", "minItems", "uniqueItems", "anyOf"}

def validate(value, schema, path="$"):
    unknown = set(schema) - KEYWORDS
    if unknown:
        raise ProtocolError("Unsupported schema keyword: " + str(unknown))
    if "anyOf" in schema:
        for choice in schema["anyOf"]:
            try:
                validate(value, choice, path)
                break
            except ProtocolError:
                pass
        else:
            raise ProtocolError(path + ": no schema alternative")
    types = schema.get("type")
    if types:
        types = [types] if isinstance(types, str) else types
        matches = {"object": isinstance(value, dict), "array": isinstance(value, list),
                   "string": isinstance(value, str), "integer": type(value) is int,
                   "boolean": type(value) is bool, "null": value is None}
        if not any(matches.get(t, False) for t in types):
            raise ProtocolError(path + ": wrong type")
    if "const" in schema and (value != schema["const"] or type(value) is not type(schema["const"])):
        raise ProtocolError(path + ": wrong constant")
    if "enum" in schema and value not in schema["enum"]:
        raise ProtocolError(path + ": wrong enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or ("pattern" in schema and not re.search(schema["pattern"], value)):
            raise ProtocolError(path + ": invalid string")
    if type(value) is int and value < schema.get("minimum", value):
        raise ProtocolError(path + ": below minimum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        if set(schema.get("required", [])) - set(value):
            raise ProtocolError(path + ": missing required fields")
        if schema.get("additionalProperties") is False and set(value) - set(props):
            raise ProtocolError(path + ": unexpected fields")
        for key, child in value.items():
            if key in props:
                validate(child, props[key], path + "." + key)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ProtocolError(path + ": too few items")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise ProtocolError(path + ": duplicate items")
        if "items" in schema:
            for index, child in enumerate(value):
                validate(child, schema["items"], path + "[" + str(index) + "]")

def validate_named(value, name):
    validate(value, json.loads((ROOT / (name + ".schema.json")).read_text(encoding="utf-8")))
