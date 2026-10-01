#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prove that a pull-request event is based on the current default-branch head."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any, Mapping
from urllib.parse import quote


REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


class FreshnessError(RuntimeError):
    """The repository default-branch state is malformed or unavailable."""


def api_json(endpoint: str) -> Any:
    try:
        completed = subprocess.run(
            ["gh", "api", endpoint],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise FreshnessError("cannot execute the GitHub CLI") from error
    if completed.returncode != 0:
        raise FreshnessError("GitHub default-branch API request failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise FreshnessError("GitHub default-branch API response is not valid JSON") from error


def mapping(value: Any, description: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise FreshnessError(f"{description} is not an object")
    return value


def prove(repository: str, event_base: str, event_base_ref: str) -> dict[str, Any]:
    repository_document = mapping(api_json(f"repos/{repository}"), "repository response")
    default_branch = repository_document.get("default_branch")
    if not isinstance(default_branch, str) or not default_branch:
        raise FreshnessError("repository default branch is missing")
    encoded_branch = quote(default_branch, safe="")
    ref_document = mapping(
        api_json(f"repos/{repository}/git/ref/heads/{encoded_branch}"),
        "default-branch ref response",
    )
    ref_object = mapping(ref_document.get("object"), "default-branch ref object")
    default_head = ref_object.get("sha")
    if ref_object.get("type") != "commit" or not isinstance(default_head, str):
        raise FreshnessError("default-branch ref does not resolve to a commit")
    if COMMIT_SHA.fullmatch(default_head) is None:
        raise FreshnessError("default-branch head is not a full commit SHA")
    if event_base_ref != default_branch:
        return {
            "fresh": False,
            "reason": "pull request does not target the repository default branch",
            "default_branch": default_branch,
            "default_head": default_head,
        }
    if event_base != default_head:
        return {
            "fresh": False,
            "reason": "pull request base is behind the current default-branch head",
            "default_branch": default_branch,
            "default_head": default_head,
            "event_base": event_base,
        }
    return {
        "fresh": True,
        "reason": "pull request event uses the current default-branch head",
        "default_branch": default_branch,
        "default_head": default_head,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--event-base", required=True)
    parser.add_argument("--event-base-ref", required=True)
    args = parser.parse_args()
    if REPOSITORY.fullmatch(args.repository) is None:
        parser.error("--repository must be OWNER/NAME")
    if COMMIT_SHA.fullmatch(args.event_base) is None:
        parser.error("--event-base must be a full lowercase commit SHA")
    if not args.event_base_ref:
        parser.error("--event-base-ref must not be empty")
    try:
        result = prove(args.repository, args.event_base, args.event_base_ref)
    except FreshnessError as error:
        json.dump({"fresh": False, "error": str(error)}, sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
        return 2
    json.dump(result, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0 if result["fresh"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
