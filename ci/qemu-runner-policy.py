#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Record the fail-closed QEMU runner routing decision.

This evidence helper is not the scheduling authority: the job-level GitHub
expression independently repeats the same protected-main predicate.  Keeping
the decision in a structured artifact makes a misroute visible and testable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TRUSTED_EVENTS = {"push", "workflow_dispatch"}
PROTECTED_REF = "refs/heads/main"
SELF_HOSTED_LABELS = ["self-hosted", "linux", "x64", "oe-rva23-qemu"]
HOSTED_LABELS = ["ubuntu-24.04"]


def decide(mode: str, needs_native: bool, event_name: str, ref: str) -> dict[str, object]:
    eligible = (
        mode == "package"
        and not needs_native
        and event_name in TRUSTED_EVENTS
        and ref == PROTECTED_REF
    )
    if eligible:
        runner_kind = "self-hosted-qemu"
        labels = SELF_HOSTED_LABELS
        reason = "protected-main QEMU package build"
    else:
        runner_kind = "github-hosted"
        labels = HOSTED_LABELS
        reason = "pull requests, merge queue, infrastructure, and native policy fail closed"
    return {
        "schema_version": 1,
        "kind": "qemu-runner-policy",
        "status": "passed",
        "mode": mode,
        "needs_native": needs_native,
        "event_name": event_name,
        "ref": ref,
        "runner_kind": runner_kind,
        "labels": labels,
        "reason": reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("package", "infrastructure", "invalid"), required=True)
    parser.add_argument("--needs-native", choices=("true", "false"), required=True)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    document = decide(
        args.mode,
        args.needs_native == "true",
        args.event_name,
        args.ref,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
