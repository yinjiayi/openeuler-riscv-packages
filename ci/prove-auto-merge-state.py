#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prove one live pull request still matches an Auto-merge lease."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any, Mapping


COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
PR_NUMBER = re.compile(r"^[1-9][0-9]*$")
REF_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


class StateProofError(RuntimeError):
    """The live API state does not prove the requested lease."""


def mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise StateProofError(f"{label} must be a JSON object")
    return value


def nested(document: Mapping[str, Any], *keys: str) -> Any:
    value: Any = document
    for index, key in enumerate(keys):
        current = mapping(value, ".".join(keys[:index]) or "pull request")
        if key not in current:
            raise StateProofError(f"pull request is missing {'.'.join(keys[: index + 1])}")
        value = current[key]
    return value


def read_pull_request(repository: str, pr_number: str) -> Mapping[str, Any]:
    try:
        completed = subprocess.run(
            ["gh", "api", f"repos/{repository}/pulls/{pr_number}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise StateProofError("cannot execute the GitHub CLI") from error
    if completed.returncode != 0:
        raise StateProofError("GitHub pull-request API request failed")
    try:
        return mapping(json.loads(completed.stdout), "GitHub pull-request API response")
    except json.JSONDecodeError as error:
        raise StateProofError("GitHub pull-request API response is not valid JSON") from error


def prove(
    pull_request: Mapping[str, Any],
    *,
    repository: str,
    event_head: str,
    event_base: str,
    event_base_ref: str,
    expected_auto_merge: str,
) -> None:
    for field in ("state", "merged", "merged_at", "head", "base", "auto_merge"):
        if field not in pull_request:
            raise StateProofError(f"pull request is missing {field}")

    if pull_request.get("state") != "open":
        raise StateProofError("pull request is not open")
    if pull_request.get("merged") is not False:
        raise StateProofError("pull request is not proven unmerged")
    if pull_request.get("merged_at") is not None:
        raise StateProofError("pull request has a merge timestamp")

    if nested(pull_request, "head", "repo", "full_name") != repository:
        raise StateProofError("pull request head repository changed")
    if nested(pull_request, "base", "repo", "full_name") != repository:
        raise StateProofError("pull request base repository changed")
    if nested(pull_request, "head", "sha") != event_head:
        raise StateProofError("pull request head changed after the workflow event")
    if nested(pull_request, "base", "sha") != event_base:
        raise StateProofError("pull request base changed after the workflow event")
    if nested(pull_request, "base", "ref") != event_base_ref:
        raise StateProofError("pull request base ref changed after the workflow event")

    auto_merge = pull_request["auto_merge"]
    if expected_auto_merge == "disabled" and auto_merge is not None:
        raise StateProofError("Auto-merge is not disabled")
    if expected_auto_merge == "enabled":
        enabled = mapping(auto_merge, "pull request auto_merge")
        if enabled.get("merge_method") != "squash":
            raise StateProofError("Auto-merge is not enabled with the squash method")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr-number", required=True)
    parser.add_argument("--event-head", required=True)
    parser.add_argument("--event-base", required=True)
    parser.add_argument("--event-base-ref", required=True)
    parser.add_argument(
        "--expected-auto-merge", required=True, choices=("disabled", "enabled")
    )
    args = parser.parse_args()

    try:
        if REPOSITORY.fullmatch(args.repo) is None:
            raise StateProofError("repository must be an owner/name pair")
        if PR_NUMBER.fullmatch(args.pr_number) is None:
            raise StateProofError("pull request number must be a positive decimal integer")
        if COMMIT_SHA.fullmatch(args.event_head) is None:
            raise StateProofError("event head must be a full lowercase commit SHA")
        if COMMIT_SHA.fullmatch(args.event_base) is None:
            raise StateProofError("event base must be a full lowercase commit SHA")
        if REF_NAME.fullmatch(args.event_base_ref) is None:
            raise StateProofError("event base ref must be a safe branch name")
        pull_request = read_pull_request(args.repo, args.pr_number)
        prove(
            pull_request,
            repository=args.repo,
            event_head=args.event_head,
            event_base=args.event_base,
            event_base_ref=args.event_base_ref,
            expected_auto_merge=args.expected_auto_merge,
        )
    except StateProofError as error:
        print(f"auto-merge state proof failed: {error}", file=sys.stderr)
        return 2

    print(
        "auto-merge state proof passed: "
        f"PR #{args.pr_number} is open, unmerged, lease-bound, and "
        f"Auto-merge is {args.expected_auto_merge}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
