#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run the repo-native audit command across explicitly selected fleet stages."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


FIRST = 201
LAST = 250
CANARY = {201, 202, 203, 204, 205}
CONDITIONAL = {211, 220, 224, 231}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=("canary", "clean", "conditional", "all"))
    parser.add_argument("--jobs", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def octets(stage: str) -> list[int]:
    all_hosts = set(range(FIRST, LAST + 1))
    clean = all_hosts - CONDITIONAL
    if stage == "canary":
        selected = CANARY
    elif stage == "clean":
        selected = clean
    elif stage == "conditional":
        selected = CONDITIONAL
    else:
        selected = all_hosts
    return sorted(selected)


def audit(last: int, conditional: bool) -> dict[str, Any]:
    host = f"10.230.50.{last}"
    name = f"oe-rva23-qemu-{last}"
    remote = [
        "/usr/local/libexec/openeuler-actions-runner/audit.sh",
        "--host",
        host,
        "--name",
        name,
    ]
    if conditional:
        remote.append("--allow-degraded")
    command = [
        "ssh", "-T", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=yes",
        "-o", "ConnectTimeout=6", "-o", "ConnectionAttempts=1", f"root@{host}", *remote,
    ]
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False)
    payload: dict[str, Any] | None = None
    if completed.returncode == 0:
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            pass
    return {
        "host": host,
        "name": name,
        "returncode": completed.returncode,
        "audit": payload,
        "stderr": completed.stderr[-4000:],
    }


def main() -> int:
    args = parse_args()
    if not 1 <= args.jobs <= 10:
        raise SystemExit("--jobs must be between 1 and 10")
    selected = octets(args.stage)
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(audit, last, last in CONDITIONAL): last for last in selected}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: int(item["host"].rsplit(".", 1)[1]))
    document = {
        "schema_version": 1,
        "stage": args.stage,
        "requested": len(results),
        "passed": sum(item["returncode"] == 0 and item["audit"] is not None for item in results),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: document[key] for key in ("stage", "requested", "passed")}, sort_keys=True))
    return 0 if document["passed"] == document["requested"] else 1


if __name__ == "__main__":
    sys.exit(main())
