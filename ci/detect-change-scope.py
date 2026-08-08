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


def changed_files(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB", "-z", base, head, "--"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [item.decode("utf-8", "strict") for item in result.stdout.split(b"\0") if item]


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

    result = classify(changed_files(args.base, args.head))
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
