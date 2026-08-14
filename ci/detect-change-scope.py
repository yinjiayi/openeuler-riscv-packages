#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Classify a PR diff as a single-package change, infrastructure change, or invalid."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import PurePosixPath

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{40}$")


class ScopeError(ValueError):
    """A fail-closed error in immutable-ref or ancestry validation."""


def verified_commit(value: str, label: str) -> str:
    if not COMMIT_SHA.fullmatch(value):
        raise ScopeError(f"{label} must be a full 40-character commit SHA")
    normalized = value.lower()
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{normalized}^{{commit}}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise ScopeError(f"{label} is not an available commit")
    resolved = result.stdout.strip().lower()
    if resolved != normalized:
        raise ScopeError(f"{label} must identify a commit object directly")
    return normalized


def stable_pr_base(base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "merge-base", "--all", base, head],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode not in {0, 1}:
        raise ScopeError("unable to resolve the base/head merge base")
    candidates = [line.strip().lower() for line in result.stdout.splitlines() if line.strip()]
    if not candidates:
        raise ScopeError("base and head do not share a common ancestor")
    if len(candidates) != 1 or not COMMIT_SHA.fullmatch(candidates[0]):
        raise ScopeError("base and head do not have exactly one unambiguous merge base")
    merge_base = candidates[0]
    for label, tip in (("base", base), ("head", head)):
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", merge_base, tip],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        if ancestry.returncode != 0:
            raise ScopeError(f"resolved merge base is not an ancestor of {label}")
    if merge_base == head:
        raise ScopeError("head is already an ancestor of base; no stable PR delta exists")
    return merge_base


def changed_files(base: str, head: str) -> tuple[list[str], str]:
    merge_base = stable_pr_base(base, head)
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB", "-z", merge_base, head, "--"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ScopeError("unable to compute the stable PR delta")
    paths = [item.decode("utf-8", "strict") for item in result.stdout.split(b"\0") if item]
    return paths, merge_base


def allowed_generated(path: str, package_id: str) -> bool:
    return path in {
        "catalog/package-index.json",
        "dashboard/data/index.json",
        f"dashboard/data/packages/{package_id}.json",
    }


def classify(paths: list[str]) -> dict[str, object]:
    invalid_paths: list[str] = []
    package_ids: set[str] = set()
    for raw in paths:
        path = PurePosixPath(raw)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            invalid_paths.append(raw)
            continue
        if path.parts[0] == "packages":
            if len(path.parts) < 3 or not PACKAGE_ID.fullmatch(path.parts[1]):
                invalid_paths.append(raw)
            else:
                package_ids.add(path.parts[1])

    errors: list[str] = []
    if invalid_paths:
        errors.append("invalid package path(s): " + ", ".join(invalid_paths))
    if len(package_ids) > 1:
        errors.append("a package PR may change exactly one package directory")

    package_id = next(iter(package_ids), "") if len(package_ids) == 1 else ""
    if package_id:
        mixed = [
            path
            for path in paths
            if not path.startswith(f"packages/{package_id}/")
            and not allowed_generated(path, package_id)
        ]
        if mixed:
            errors.append("package PR contains shared or unrelated files: " + ", ".join(mixed))

    if errors:
        mode = "invalid"
    elif package_id:
        mode = "package"
    else:
        mode = "infrastructure"
    return {
        "schema_version": 1,
        "mode": mode,
        "package_id": package_id,
        "changed_files": paths,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()

    base_sha = args.base.lower() if COMMIT_SHA.fullmatch(args.base) else None
    head_sha = args.head.lower() if COMMIT_SHA.fullmatch(args.head) else None
    merge_base_sha = None
    try:
        base_sha = verified_commit(args.base, "base")
        head_sha = verified_commit(args.head, "head")
        paths, merge_base_sha = changed_files(base_sha, head_sha)
        result = classify(paths)
    except (ScopeError, UnicodeDecodeError) as error:
        result = {
            "schema_version": 1,
            "mode": "invalid",
            "package_id": "",
            "changed_files": [],
            "errors": [str(error)],
        }
    result.update(
        {
            "base_sha": base_sha,
            "head_sha": head_sha,
            "merge_base_sha": merge_base_sha,
        }
    )
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as handle:
            handle.write(f"mode={result['mode']}\n")
            handle.write(f"package_id={result['package_id']}\n")
    if result["errors"]:
        for error in result["errors"]:
            print(f"scope error: {error}", file=sys.stderr)
        return 2
    print(f"change scope: {result['mode']} {result['package_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
