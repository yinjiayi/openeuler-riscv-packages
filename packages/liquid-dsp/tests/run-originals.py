#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
"""Repeat unchanged original programs; no benchmark timing/performance claim."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--programs", type=Path, required=True)
p.add_argument("--data", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
programs = a.programs.resolve(strict=True)
data = a.data.resolve(strict=True)
a.output.mkdir(parents=True, exist_ok=False)
out = a.output.resolve(strict=True)
examples = (data / "examples.list").read_text().splitlines()
names = (data / "registry-names.list").read_text().splitlines()
assert len(examples) == len(set(examples)) == 191
assert len(names) == len(set(names)) == 1349
assert all(re.fullmatch(r"[A-Za-z0-9_]+", s) for s in examples + names)
records = []
def emit_log(name, path, returncode):
    raw = path.read_bytes()
    record = dict(name=name, returncode=returncode,
                  log_sha256=hashlib.sha256(raw).hexdigest(), log_bytes=len(raw))
    print("BEGIN ORIGINAL PROGRAM " + json.dumps(record, sort_keys=True), flush=True)
    print(raw.decode("utf-8", errors="replace"), end="", flush=True)
    print("\nEND ORIGINAL PROGRAM " + name, flush=True)
    return record

for name in examples:
    cwd = out / name
    cwd.mkdir()
    binary = programs / "examples" / name
    assert binary.is_file() and os.access(binary, os.X_OK)
    with (cwd / "output.log").open("xb") as log:
        result = subprocess.run([str(binary)], cwd=cwd, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    records.append(emit_log(name, cwd / "output.log", result.returncode))
    if result.returncode:
        raise SystemExit(f"Original example {name} failed: {result.returncode}")
cwd = out / "autotest"
cwd.mkdir()
with (cwd / "output.log").open("xb") as log:
    result = subprocess.run([str(programs / "xautotest"), "-o", "results.json"],
                            cwd=cwd, stdout=log, stderr=subprocess.STDOUT,
                            check=False)
autotest_record = emit_log("autotest", cwd / "output.log", result.returncode)
if result.returncode:
    raise SystemExit(f"Original full autotest failed: {result.returncode}")
r = json.loads((cwd / "results.json").read_text())
assert r["pass"] is True and r["num_failed"] == 0 and r["num_checks"] > 0
assert r["stop-on-fail"] is False
rows = r["tests"]
assert len(rows) == 1349 and [x["id"] for x in rows] == list(range(1349))
assert [x["name"] for x in rows] == names
assert all(x["pass"] is True and x["num_checks"] == x["num_passed"] for x in rows)
assert sum(x["num_checks"] for x in rows) == r["num_checks"]
log = re.sub(r"\x1b\[[0-9;]*m", "", (cwd / "output.log").read_text())
assert len(re.findall(r"\bskip\s*:\s*0\b", log)) == 1
summary = dict(original_examples=records, original_autotests=1349,
               autotest_program=autotest_record,
               original_checks=r["num_checks"], warnings=r["num_warnings"],
               skipped=0, benchmark_built_but_not_timed=True,
               downstream_consumer_is_separate=True)
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print("ORIGINAL TEST RECEIPT " + json.dumps(summary, sort_keys=True), flush=True)
print(json.dumps({k: v for k, v in summary.items() if k != "original_examples"},
                 sort_keys=True))
