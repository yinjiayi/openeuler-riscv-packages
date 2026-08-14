#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Select one existing package at an exact checkout for trusted backfill runs."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()
    errors: list[str] = []
    if not PACKAGE_ID.fullmatch(args.package_id):
        errors.append("package id is not canonical")
    if not COMMIT_SHA.fullmatch(args.head):
        errors.append("head must be a full lowercase commit SHA")
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.strip()
    if actual != args.head:
        errors.append("checkout HEAD does not match the explicit immutable head")
    package_dir = Path("packages") / args.package_id
    if not package_dir.is_dir() or not (package_dir / "package.yaml").is_file():
        errors.append("selected package directory or package.yaml is missing")
    changed_files = sorted(path.as_posix() for path in package_dir.rglob("*") if path.is_file()) if not errors else []
    result = {
        "schema_version": 1,
        "mode": "package" if not errors else "invalid",
        "package_id": args.package_id if not errors else "",
        "changed_files": changed_files,
        "errors": errors,
        "base_sha": None,
        "head_sha": args.head if COMMIT_SHA.fullmatch(args.head) else None,
        "merge_base_sha": None,
        "selection": "trusted-explicit-package",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as stream:
            stream.write(f"mode={result['mode']}\npackage_id={result['package_id']}\n")
    for error in errors:
        print(f"scope error: {error}")
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
