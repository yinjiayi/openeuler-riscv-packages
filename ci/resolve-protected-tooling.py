#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bind Package CI to one immutable protected-main tooling commit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Sequence


REPOSITORY = "yinjiayi/openeuler-riscv-packages"
PROTECTED_REF = "refs/heads/main"
PROTECTED_BRANCH = "main"
PACKAGE_WORKFLOW = ".github/workflows/package-ci.yml"
BACKFILL_WORKFLOW = ".github/workflows/rpm-repo-backfill.yml"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVENT_SHA_EVENTS = {"push", "workflow_dispatch", "workflow_call"}


class ToolingError(RuntimeError):
    """The event cannot be bound to trusted immutable tooling."""


def require_sha(value: str, label: str) -> str:
    if SHA_RE.fullmatch(value) is None:
        raise ToolingError(f"{label} must be a full lowercase commit SHA")
    return value


def require_pr_number(value: str) -> str:
    if re.fullmatch(r"[1-9][0-9]*", value) is None:
        raise ToolingError("pull request number must be a positive decimal integer")
    return value


def git(root: Path, arguments: Sequence[str]) -> str:
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
        raise ToolingError(detail[-1000:])
    return completed.stdout.strip()


def require_checked_head(root: Path, expected_sha: str) -> None:
    observed_head = git(root, ["rev-parse", "HEAD"])
    if observed_head != expected_sha:
        raise ToolingError(
            f"checked-out workflow commit {observed_head} does not match {expected_sha}"
        )
    resolved_head = git(root, ["rev-parse", f"{expected_sha}^{{commit}}"])
    if resolved_head != expected_sha:
        raise ToolingError("workflow SHA did not resolve exactly to a commit")


def require_ancestor(root: Path, ancestor: str, descendant: str) -> None:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode == 1:
        raise ToolingError("merge-group base SHA is not an ancestor of the workflow commit")
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git failed"
        raise ToolingError(detail[-1000:])


def resolve(
    root: Path,
    *,
    event_name: str,
    repository: str,
    workflow_ref: str,
    workflow_sha: str,
    event_sha: str,
    event_ref: str,
    base_repository: str,
    base_ref: str,
    pr_number: str,
    package_head: str,
    base_sha: str,
) -> dict[str, object]:
    if repository != REPOSITORY:
        raise ToolingError("unexpected repository")
    package_workflow_ref = f"{repository}/{PACKAGE_WORKFLOW}@{PROTECTED_REF}"
    backfill_workflow_ref = f"{repository}/{BACKFILL_WORKFLOW}@{PROTECTED_REF}"

    if root.is_symlink() or not root.is_dir():
        raise ToolingError("repository root must be a regular directory")

    binding_source: str
    if event_name == "pull_request":
        merge_sha = require_sha(workflow_sha, "workflow SHA")
        if require_sha(event_sha, "event SHA") != merge_sha:
            raise ToolingError("pull-request workflow SHA and event SHA must match")
        number = require_pr_number(pr_number)
        expected_workflow_ref = (
            f"{repository}/{PACKAGE_WORKFLOW}@refs/pull/{number}/merge"
        )
        if workflow_ref != expected_workflow_ref:
            raise ToolingError("pull-request workflow ref is not the exact synthetic merge ref")
        if event_ref != f"refs/pull/{number}/merge":
            raise ToolingError("pull-request event ref is not the exact synthetic merge ref")
        if base_repository != repository:
            raise ToolingError("event base repository is not the protected repository")
        if base_ref != PROTECTED_BRANCH:
            raise ToolingError("event base ref is not protected main")
        reported_base_sha = require_sha(base_sha, "reported pull-request base SHA")
        package_sha = require_sha(package_head, "package head SHA")
        require_checked_head(root, merge_sha)
        parents = git(root, ["rev-list", "--parents", "-n", "1", merge_sha]).split()
        if len(parents) != 3 or parents[0] != merge_sha:
            raise ToolingError("pull-request workflow commit must have exactly two parents")
        tooling_sha = require_sha(parents[1], "pull-request merge first parent")
        if parents[2] != package_sha:
            raise ToolingError("pull-request merge second parent is not the package head")
        if git(root, ["rev-parse", f"{tooling_sha}^{{commit}}"]) != tooling_sha:
            raise ToolingError("pull-request tooling parent did not resolve exactly")
        checked_workflow_sha = merge_sha
        binding_source = "pull-request-merge-first-parent"
    elif event_name == "merge_group":
        checked_sha = require_sha(workflow_sha, "workflow SHA")
        if require_sha(event_sha, "event SHA") != checked_sha:
            raise ToolingError("merge-group workflow SHA and event SHA must match")
        tooling_sha = require_sha(base_sha, "merge-group base SHA")
        require_sha(package_head, "merge-group head SHA")
        if workflow_ref != package_workflow_ref:
            raise ToolingError("merge-group workflow is not protected package CI")
        if base_repository != repository:
            raise ToolingError("event base repository is not the protected repository")
        if base_ref != PROTECTED_REF:
            raise ToolingError("event base ref is not protected main")
        require_checked_head(root, checked_sha)
        require_ancestor(root, tooling_sha, checked_sha)
        reported_base_sha = tooling_sha
        package_sha = package_head
        checked_workflow_sha = checked_sha
        binding_source = "merge-group-protected-base"
    elif event_name in EVENT_SHA_EVENTS:
        tooling_sha = require_sha(event_sha, "event SHA")
        expected_workflow_ref = (
            backfill_workflow_ref if event_name == "workflow_call" else package_workflow_ref
        )
        if workflow_ref != expected_workflow_ref:
            raise ToolingError("protected-main event workflow ref is unexpected")
        if event_ref != PROTECTED_REF:
            raise ToolingError("protected-main event ref is unexpected")
        require_checked_head(root, tooling_sha)
        reported_base_sha = ""
        package_sha = ""
        checked_workflow_sha = tooling_sha
        binding_source = "protected-main-event"
    else:
        raise ToolingError("unsupported Package CI event")

    return {
        "schema_version": 2,
        "kind": "protected-main-tooling-binding",
        "status": "passed",
        "event_name": event_name,
        "repository": repository,
        "workflow_ref": workflow_ref,
        "workflow_commit_sha": checked_workflow_sha,
        "binding_source": binding_source,
        "reported_base_sha": reported_base_sha,
        "package_commit_sha": package_sha,
        "tooling_commit_sha": tooling_sha,
    }


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--workflow-ref", required=True)
    parser.add_argument("--workflow-sha", required=True)
    parser.add_argument("--event-sha", required=True)
    parser.add_argument("--event-ref", required=True)
    parser.add_argument("--base-repository", default="")
    parser.add_argument("--base-ref", default="")
    parser.add_argument("--pr-number", default="")
    parser.add_argument("--package-head", default="")
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--github-output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    try:
        document = resolve(
            root,
            event_name=args.event_name,
            repository=args.repository,
            workflow_ref=args.workflow_ref,
            workflow_sha=args.workflow_sha,
            event_sha=args.event_sha,
            event_ref=args.event_ref,
            base_repository=args.base_repository,
            base_ref=args.base_ref,
            pr_number=args.pr_number,
            package_head=args.package_head,
            base_sha=args.base_sha,
        )
        output = args.output if args.output.is_absolute() else root / args.output
        write_json(output, document)
        with args.github_output.open("a", encoding="utf-8") as stream:
            stream.write(f"tooling_sha={document['tooling_commit_sha']}\n")
    except (ToolingError, OSError, subprocess.SubprocessError) as error:
        print(f"resolve-protected-tooling: {error}", file=sys.stderr)
        return 2
    print(json.dumps(document, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
