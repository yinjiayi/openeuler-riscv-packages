#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Select one existing package from an exact checkout or trusted overlay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
from typing import Sequence


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
OVERLAY_KEYS = {
    "schema_version",
    "kind",
    "status",
    "package_id",
    "package_commit_sha",
    "package_tree_sha",
    "tooling_commit_sha",
}


def git(root: Path, arguments: Sequence[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def validate_overlay(
    root: Path,
    package_id: str,
    package_head: str,
    tooling_head: str,
    evidence_path: Path,
) -> list[str]:
    errors: list[str] = []
    if not COMMIT_SHA.fullmatch(tooling_head):
        return ["tooling head must be a full lowercase commit SHA"]
    if evidence_path.is_symlink() or not evidence_path.is_file():
        return ["overlay evidence must be an existing regular file"]
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return [f"overlay evidence is not valid JSON: {error}"]
    if not isinstance(evidence, dict) or set(evidence) != OVERLAY_KEYS:
        errors.append("overlay evidence fields do not match the protected overlay schema")
        evidence = evidence if isinstance(evidence, dict) else {}
    expected_fields: tuple[tuple[str, object], ...] = (
        ("schema_version", 1),
        ("kind", "protected-main-package-overlay"),
        ("status", "passed"),
        ("package_id", package_id),
        ("package_commit_sha", package_head),
        ("tooling_commit_sha", tooling_head),
    )
    for name, expected in expected_fields:
        if evidence.get(name) != expected or type(evidence.get(name)) is not type(expected):
            errors.append(f"overlay evidence {name} does not match the explicit input")
    package_tree = evidence.get("package_tree_sha")
    if not isinstance(package_tree, str) or not COMMIT_SHA.fullmatch(package_tree):
        errors.append("overlay evidence package_tree_sha is invalid")

    status, actual_head, detail = git(root, ["rev-parse", "HEAD"])
    if status != 0:
        errors.append(f"cannot resolve checkout HEAD: {detail or actual_head or 'git failed'}")
    elif actual_head != tooling_head:
        errors.append("checkout HEAD does not match the explicit protected tooling head")

    package_path = f"packages/{package_id}"
    status, resolved_head, _ = git(root, ["rev-parse", "--verify", f"{package_head}^{{commit}}"])
    if status != 0 or resolved_head != package_head:
        errors.append("explicit package head does not resolve to the exact commit")
        return errors
    status, tree_type, _ = git(root, ["cat-file", "-t", f"{package_head}:{package_path}"])
    if status != 0 or tree_type != "tree":
        errors.append("selected package is not a Git tree at the explicit package head")
        return errors
    status, commit_tree, _ = git(root, ["rev-parse", f"{package_head}:{package_path}"])
    if status != 0 or commit_tree != package_tree:
        errors.append("overlay evidence tree does not match the explicit package head")
    status, index_tree, _ = git(root, ["write-tree", f"--prefix={package_path}/"])
    if status != 0 or index_tree != package_tree:
        errors.append("materialized package index tree does not match overlay evidence")
    status, _, _ = git(root, ["diff", "--quiet", "--", package_path])
    if status != 0:
        errors.append("materialized package worktree differs from its staged tree")
    status, untracked, detail = git(root, ["ls-files", "--others", "--", package_path])
    if status != 0:
        errors.append(f"cannot inspect untracked package files: {detail or 'git failed'}")
    elif untracked:
        errors.append("materialized package contains untracked files")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--tooling-head")
    parser.add_argument("--overlay-evidence", type=Path)
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    errors: list[str] = []
    if not PACKAGE_ID.fullmatch(args.package_id):
        errors.append("package id is not canonical")
    if not COMMIT_SHA.fullmatch(args.head):
        errors.append("head must be a full lowercase commit SHA")
    overlay_arguments = (args.tooling_head is not None, args.overlay_evidence is not None)
    if overlay_arguments.count(True) == 1:
        errors.append("tooling head and overlay evidence must be supplied together")
    elif all(overlay_arguments) and not errors:
        evidence_path = args.overlay_evidence
        if not evidence_path.is_absolute():
            evidence_path = root / evidence_path
        errors.extend(
            validate_overlay(root, args.package_id, args.head, args.tooling_head, evidence_path)
        )
    elif not errors:
        status, actual, detail = git(root, ["rev-parse", "HEAD"])
        if status != 0:
            errors.append(f"cannot resolve checkout HEAD: {detail or actual or 'git failed'}")
        elif actual != args.head:
            errors.append("checkout HEAD does not match the explicit immutable head")
    package_dir = (
        root / "packages" / args.package_id
        if PACKAGE_ID.fullmatch(args.package_id)
        else root / "packages" / "__invalid__"
    )
    if not package_dir.is_dir() or not (package_dir / "package.yaml").is_file():
        errors.append("selected package directory or package.yaml is missing")
    changed_files = (
        sorted(path.relative_to(root).as_posix() for path in package_dir.rglob("*") if path.is_file())
        if not errors
        else []
    )
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
    if not output.is_absolute():
        output = root / output
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
