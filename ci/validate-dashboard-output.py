#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail closed on every generated Pages JSON schema before upload/deployment."""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import runpy

ROOT = pathlib.Path(__file__).resolve().parents[1]
HISTORY = runpy.run_path(str(ROOT / "ci/collect-build-history.py"))


def format_checker(schema: dict):
    checker = HISTORY["required_format_checker"](schema)
    controls = {"uri": ("https://example.org/a%20b", "https://example.org/a b"),
                "date-time": ("2026-10-09T00:00:00Z", "not a timestamp")}
    for kind, (valid, invalid) in controls.items():
        if kind in checker.checkers and (not checker.conforms(valid, kind) or checker.conforms(invalid, kind)):
            raise ValueError("required format control failed: " + kind)
    return checker


def validate(output: pathlib.Path, published: pathlib.Path) -> dict:
    import jsonschema
    expected = {"data.json", "inventory.json", "build-history.json", "build-history-ledger.json"}
    json_paths = {str(path.relative_to(output)) for path in output.rglob("*.json")}
    if json_paths != expected:
        raise ValueError("unexpected or missing generated JSON asset")
    if any((output / name).is_symlink() or not (output / name).is_file() for name in expected) or published.is_symlink() or not published.is_file():
        raise ValueError("generated JSON and publication input must be regular files")
    records = []
    documents = {}
    for name, schema_name in (("data.json", "dashboard.schema.json"),
                              ("inventory.json", "dashboard-inventory.schema.json"),
                              ("build-history-ledger.json", "build-history.schema.json")):
        raw = (output / name).read_bytes()
        document = json.loads(raw)
        schema = json.loads((ROOT / "schemas" / schema_name).read_bytes())
        checker = format_checker(schema)
        jsonschema.Draft202012Validator(schema, format_checker=checker).validate(document)
        documents[name] = document
        records.append({"name": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    HISTORY["validate_seed"](documents["build-history-ledger.json"], "yinjiayi/openeuler-riscv-packages")
    history_raw = (output / "build-history.json").read_bytes()
    if json.loads(history_raw) != documents["data.json"]["build_history"]:
        raise ValueError("browser history differs from validated dashboard history")
    records.append({"name": "build-history.json", "bytes": len(history_raw), "sha256": hashlib.sha256(history_raw).hexdigest()})
    pub_raw = published.read_bytes()
    pub_schema = json.loads((ROOT / "schemas/dashboard-published-state.schema.json").read_bytes())
    jsonschema.Draft202012Validator(pub_schema, format_checker=format_checker(pub_schema)).validate(json.loads(pub_raw))
    records.append({"name": "published-state.json", "bytes": len(pub_raw), "sha256": hashlib.sha256(pub_raw).hexdigest()})
    return {"status": "passed", "scope": "Generated JSON schemas, required format handlers, history seed semantics and browser equality; not RPM rebuild/install or deployment acceptance", "files": records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=pathlib.Path)
    parser.add_argument("--published-state", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    result = validate(args.output_dir, args.published_state)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
