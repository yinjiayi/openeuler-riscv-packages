#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Derive an evidence-preserving rpmbuild deadline from package policy."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

MIN_TIMEOUT_MINUTES = 5
MAX_TIMEOUT_MINUTES = 360
MAX_RESERVE_SECONDS = 3600
POSITIVE_INTEGER = re.compile(r"^[1-9][0-9]*$")


def parse_positive_integer(name: str, value: str) -> int:
    if not POSITIVE_INTEGER.fullmatch(value):
        raise ValueError(f"{name} must be a positive base-10 integer")
    return int(value)


def start_budget(timeout_minutes: int, requested_reserve_seconds: int, now_epoch: int) -> dict[str, int | str]:
    if not MIN_TIMEOUT_MINUTES <= timeout_minutes <= MAX_TIMEOUT_MINUTES:
        raise ValueError("timeout minutes are outside the schema-validated range")
    if not 1 <= requested_reserve_seconds <= MAX_RESERVE_SECONDS:
        raise ValueError("evidence reserve is outside the allowed range")
    if now_epoch <= 0:
        raise ValueError("current epoch must be positive")
    total_seconds = timeout_minutes * 60
    effective_reserve_seconds = min(requested_reserve_seconds, total_seconds // 2)
    return {
        "schema_version": 1,
        "phase": "rpmbuild-timeout-budget",
        "status": "started",
        "timeout_minutes": timeout_minutes,
        "requested_reserve_seconds": requested_reserve_seconds,
        "effective_reserve_seconds": effective_reserve_seconds,
        "started_at_epoch": now_epoch,
        "deadline_epoch": now_epoch + total_seconds - effective_reserve_seconds,
    }


def remaining_budget(deadline_epoch: int, now_epoch: int) -> tuple[dict[str, int | str], int]:
    if deadline_epoch <= 0 or now_epoch <= 0:
        raise ValueError("deadline and current epoch must be positive")
    remaining_seconds = deadline_epoch - now_epoch
    if remaining_seconds <= 0:
        return ({
            "schema_version": 1,
            "phase": "rpmbuild-timeout-budget",
            "status": "failed",
            "classification": "failure:infrastructure",
            "exit_code": 124,
            "deadline_epoch": deadline_epoch,
            "observed_at_epoch": now_epoch,
            "remaining_seconds": remaining_seconds,
            "message": "The validated package job budget expired before rpmbuild began.",
        }, 124)
    if remaining_seconds > MAX_TIMEOUT_MINUTES * 60:
        raise ValueError("remaining rpmbuild budget exceeds the schema maximum")
    return ({
        "schema_version": 1,
        "phase": "rpmbuild-timeout-budget",
        "status": "ready",
        "deadline_epoch": deadline_epoch,
        "observed_at_epoch": now_epoch,
        "remaining_seconds": remaining_seconds,
    }, 0)


def write_json(path: str, document: dict[str, int | str]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--timeout-minutes", required=True)
    start.add_argument("--reserve-seconds", default="300")
    start.add_argument("--output", required=True)
    start.add_argument("--github-output", required=True)
    start.add_argument("--now-epoch")

    remaining = subparsers.add_parser("remaining")
    remaining.add_argument("--deadline-epoch", required=True)
    remaining.add_argument("--output", required=True)
    remaining.add_argument("--failure-output")
    remaining.add_argument("--now-epoch")

    args = parser.parse_args()
    try:
        now_epoch = (
            parse_positive_integer("now epoch", args.now_epoch)
            if args.now_epoch
            else int(time.time())
        )
        if args.command == "start":
            document = start_budget(
                parse_positive_integer("timeout minutes", args.timeout_minutes),
                parse_positive_integer("reserve seconds", args.reserve_seconds),
                now_epoch,
            )
            write_json(args.output, document)
            with open(args.github_output, "a", encoding="utf-8") as handle:
                handle.write(f"deadline_epoch={document['deadline_epoch']}\n")
            return 0

        document, status = remaining_budget(
            parse_positive_integer("deadline epoch", args.deadline_epoch),
            now_epoch,
        )
        write_json(args.output, document)
        if status != 0:
            if args.failure_output:
                write_json(args.failure_output, document)
            return status
        print(document["remaining_seconds"])
        return 0
    except ValueError as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
