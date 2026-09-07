#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Overlay one exact package tree onto protected-main CI tooling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Sequence


PACKAGE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class MaterializeError(RuntimeError):
    """The requested package tree cannot be materialized safely."""


def run(root: Path, arguments: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git failed"
        raise MaterializeError(detail[-1000:])
    return completed.stdout.strip()


def require_sha(value: str, label: str) -> str:
    if SHA_RE.fullmatch(value) is None:
        raise MaterializeError(f"{label} must be a full lowercase commit SHA")
    return value


def remove_package_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def materialize(
    root: Path,
    package_id: str,
    commit_sha: str,
    tooling_sha: str,
    output: Path,
) -> dict[str, object]:
    if PACKAGE_RE.fullmatch(package_id) is None:
        raise MaterializeError("package id is invalid")
    commit_sha = require_sha(commit_sha, "package commit")
    tooling_sha = require_sha(tooling_sha, "tooling commit")
    if root.is_symlink() or not root.is_dir():
        raise MaterializeError("repository root must be a regular directory")
    observed_tooling = run(root, ["rev-parse", "HEAD"])
    if observed_tooling != tooling_sha:
        raise MaterializeError(
            f"checked-out tooling commit {observed_tooling} does not match {tooling_sha}"
        )

    commit_probe = subprocess.run(
        ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if commit_probe.returncode != 0:
        run(root, ["fetch", "--no-tags", "--depth=1", "origin", commit_sha])
    resolved_commit = run(root, ["rev-parse", f"{commit_sha}^{{commit}}"])
    if resolved_commit != commit_sha:
        raise MaterializeError("package commit did not resolve exactly")

    package_path = Path("packages") / package_id
    tree_type = run(root, ["cat-file", "-t", f"{commit_sha}:{package_path.as_posix()}"])
    if tree_type != "tree":
        raise MaterializeError("package path is not a Git tree at the requested commit")
    tree_sha = run(root, ["rev-parse", f"{commit_sha}:{package_path.as_posix()}"])

    remove_package_path(root / package_path)
    run(
        root,
        [
            "restore",
            f"--source={commit_sha}",
            "--staged",
            "--worktree",
            "--",
            package_path.as_posix(),
        ],
    )
    completed = subprocess.run(
        ["git", "diff", "--cached", "--quiet", commit_sha, "--", package_path.as_posix()],
        cwd=root,
        check=False,
    )
    if completed.returncode != 0:
        raise MaterializeError("materialized package tree differs from the requested commit")

    document: dict[str, object] = {
        "schema_version": 1,
        "kind": "protected-main-package-overlay",
        "status": "passed",
        "package_id": package_id,
        "package_commit_sha": commit_sha,
        "package_tree_sha": tree_sha,
        "tooling_commit_sha": tooling_sha,
    }
    destination = output if output.is_absolute() else root / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return document


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--tooling-sha", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        document = materialize(
            args.repo_root.resolve(),
            args.package_id,
            args.commit_sha,
            args.tooling_sha,
            args.output,
        )
    except (MaterializeError, OSError, subprocess.SubprocessError) as error:
        print(f"materialize-package-head: {error}", file=sys.stderr)
        return 1
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
