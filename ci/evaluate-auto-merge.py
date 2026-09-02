#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Fail closed unless a current pull request changes exactly one package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
TRUSTED_LOGINS = {"yinjiayi", "github-actions[bot]"}
BLOCKING_LABELS = {
    "repair-queued",
    "needs-native-riscv",
    "qemu-limitation",
    "needs-human",
    "source-blocked",
    "license-blocked",
    "checksum-blocked",
    "security-blocked",
    "tests-disabled",
}
FILE_STATUSES = {"added", "changed", "copied", "modified", "removed", "renamed"}


class PolicyInputError(ValueError):
    """The policy input cannot be interpreted safely."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PolicyInputError(f"cannot read valid JSON from {path}") from error


def mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PolicyInputError(f"{label} must be a JSON object")
    return value


def nested(document: Mapping[str, Any], *keys: str) -> Any:
    value: Any = document
    for key in keys:
        current = mapping(value, ".".join(keys))
        value = current.get(key)
    return value


def file_entries(document: Any) -> list[Mapping[str, Any]]:
    if not isinstance(document, list):
        raise PolicyInputError("files JSON must be an array or an array of page arrays")
    if all(isinstance(item, Mapping) for item in document):
        raw_entries = document
    elif all(isinstance(page, list) for page in document):
        raw_entries = [item for page in document for item in page]
    else:
        raise PolicyInputError("files JSON mixes page arrays with file objects")
    return [mapping(item, "file entry") for item in raw_entries]


def package_path(raw: Any) -> tuple[str | None, str | None]:
    if not isinstance(raw, str) or not raw or "\\" in raw or "\0" in raw:
        return None, "changed file has an invalid path"
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != raw:
        return None, f"changed file path is not canonical: {raw}"
    if len(path.parts) < 3 or path.parts[0] != "packages":
        return None, f"changed file is outside a package directory: {raw}"
    package_id = path.parts[1]
    if not PACKAGE_ID.fullmatch(package_id):
        return None, f"changed file has an invalid package directory: {raw}"
    return package_id, None


def evaluate(
    pr: Mapping[str, Any],
    files: Sequence[Mapping[str, Any]],
    *,
    repository: str,
    event_head: str,
    event_base: str,
) -> dict[str, Any]:
    reasons: list[str] = []
    package_ids: set[str] = set()
    changed_paths: list[str] = []

    if pr.get("state") != "open":
        reasons.append("pull request is not open")
    if pr.get("draft") is not False:
        reasons.append("pull request is a draft")

    login = nested(pr, "user", "login")
    association = pr.get("author_association")
    if association not in TRUSTED_ASSOCIATIONS and login not in TRUSTED_LOGINS:
        reasons.append("pull request author is not trusted for automatic merge")

    current_head = nested(pr, "head", "sha")
    current_base = nested(pr, "base", "sha")
    head_repository = nested(pr, "head", "repo", "full_name")
    base_repository = nested(pr, "base", "repo", "full_name")
    if head_repository != repository or base_repository != repository:
        reasons.append("pull request head and base must belong to the current repository")
    if not isinstance(current_head, str) or not COMMIT_SHA.fullmatch(current_head):
        reasons.append("pull request head is not a full lowercase commit SHA")
    elif current_head != event_head:
        reasons.append("pull request head changed after the workflow event")
    if not isinstance(current_base, str) or not COMMIT_SHA.fullmatch(current_base):
        reasons.append("pull request base is not a full lowercase commit SHA")
    elif current_base != event_base:
        reasons.append("pull request base changed after the workflow event")

    labels = pr.get("labels")
    if not isinstance(labels, list):
        reasons.append("pull request labels are unavailable")
    else:
        names = {
            item.get("name")
            for item in labels
            if isinstance(item, Mapping) and isinstance(item.get("name"), str)
        }
        blockers = sorted(names & BLOCKING_LABELS)
        if blockers:
            reasons.append("blocking label(s) present: " + ", ".join(blockers))

    declared_count = pr.get("changed_files")
    if not isinstance(declared_count, int) or isinstance(declared_count, bool) or declared_count < 1:
        reasons.append("pull request changed_files must be a positive integer")
    elif declared_count != len(files):
        reasons.append(
            f"pull request file list is incomplete: API declares {declared_count}, received {len(files)}"
        )

    seen_filenames: set[str] = set()
    for entry in files:
        status = entry.get("status")
        filename = entry.get("filename")
        if status not in FILE_STATUSES:
            reasons.append(f"changed file has unsupported status: {status!r}")
        if isinstance(filename, str):
            if filename in seen_filenames:
                reasons.append(f"changed file appears more than once: {filename}")
            seen_filenames.add(filename)
            changed_paths.append(filename)
        package_id, error = package_path(filename)
        if error:
            reasons.append(error)
        elif package_id:
            package_ids.add(package_id)

        previous = entry.get("previous_filename")
        if status == "renamed" and not isinstance(previous, str):
            reasons.append(f"renamed file is missing previous_filename: {filename}")
        if previous is not None:
            previous_package, previous_error = package_path(previous)
            if previous_error:
                reasons.append(previous_error.replace("changed file", "renamed source"))
            elif previous_package:
                package_ids.add(previous_package)

    if len(package_ids) != 1:
        reasons.append("automatic merge requires exactly one package directory")

    reasons = list(dict.fromkeys(reasons))
    eligible = not reasons
    return {
        "schema_version": 1,
        "status": "eligible" if eligible else "blocked",
        "eligible": eligible,
        "package_id": next(iter(package_ids)) if eligible else "",
        "head_sha": current_head if isinstance(current_head, str) else None,
        "base_sha": current_base if isinstance(current_base, str) else None,
        "changed_files": changed_paths,
        "reasons": reasons,
    }


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-json", type=Path, required=True)
    parser.add_argument("--files-json", type=Path, required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--event-head", required=True)
    parser.add_argument("--event-base", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    try:
        if not COMMIT_SHA.fullmatch(args.event_head) or not COMMIT_SHA.fullmatch(args.event_base):
            raise PolicyInputError("event head and base must be full lowercase commit SHAs")
        pr = mapping(load_json(args.pr_json), "pull request")
        files = file_entries(load_json(args.files_json))
        result = evaluate(
            pr,
            files,
            repository=args.repo,
            event_head=args.event_head,
            event_base=args.event_base,
        )
    except PolicyInputError as error:
        result = {
            "schema_version": 1,
            "status": "blocked",
            "eligible": False,
            "package_id": "",
            "head_sha": None,
            "base_sha": None,
            "changed_files": [],
            "reasons": [str(error)],
        }
        write_result(args.output, result)
        print(f"auto-merge policy input error: {error}", file=sys.stderr)
        return 2

    write_result(args.output, result)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"eligible={'true' if result['eligible'] else 'false'}\n")
            handle.write(f"package_id={result['package_id']}\n")
    print(f"auto-merge policy: {result['status']} {result['package_id']}")
    for reason in result["reasons"]:
        print(f"auto-merge blocked: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
