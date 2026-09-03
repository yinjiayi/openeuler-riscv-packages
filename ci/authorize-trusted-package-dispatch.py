#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Authorize one exact internal PR head for a protected-main dispatch.

This program is intentionally run from the ``main`` revision of Package CI
before any job checks out ``inputs.commit_sha``.  A workflow-dispatch caller
cannot turn an arbitrary repository commit into self-hosted runner work by
supplying it as an input: it must identify the current head of one open,
trusted, same-repository package PR, or one of the two exact bot-created
infrastructure PR shapes that exercise no package build.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPOSITORY = "yinjiayi/openeuler-riscv-packages"
PROTECTED_REF = "refs/heads/main"
PACKAGE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
TRUSTED_LOGINS = {"yinjiayi", "github-actions[bot]", "dependabot[bot]"}
TRUSTED_PREFIXES = ("onboard/", "update/", "repair/", "golden/")
IMAGE_LOCK_BRANCH_RE = re.compile(r"^infra/ci-image-[0-9a-f]{12}$")
CATALOG_BRANCH_RE = re.compile(r"^catalog/(discovery-[0-9]{8}T[0-9]{6}Z-[1-9][0-9]*)$")


class AuthorizationError(RuntimeError):
    """A dispatch input or GitHub response is outside the trusted boundary."""


def exact_sha(value: Any, field: str) -> str:
    text = str(value or "")
    if not SHA_RE.fullmatch(text):
        raise AuthorizationError("%s must be a full lowercase commit SHA" % field)
    return text


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def github_json(path: str) -> Any:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise AuthorizationError("GitHub token is unavailable for trusted dispatch authorization")
    request = Request(
        "https://api.github.com/%s" % path.lstrip("/"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer %s" % token,
            "User-Agent": "openeuler-riscv-package-ci-authorizer",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuthorizationError("unable to retrieve trusted PR metadata from GitHub") from exc


def fetch_pr(repo: str, number: int) -> tuple[Mapping[str, Any], list[Mapping[str, Any]]]:
    pr = github_json("repos/%s/pulls/%d" % (repo, number))
    if not isinstance(pr, Mapping):
        raise AuthorizationError("GitHub PR response is not an object")
    files = github_json("repos/%s/pulls/%d/files?per_page=100&page=1" % (repo, number))
    if not isinstance(files, list) or not all(isinstance(item, Mapping) for item in files):
        raise AuthorizationError("GitHub PR file response is not a list")
    return pr, list(files)


def authorize(
    pr: Mapping[str, Any],
    files: Sequence[Mapping[str, Any]],
    *,
    repo: str,
    package_id: str,
    base_sha: str,
    head_sha: str,
    publish_to_repo: str,
    event_ref: str,
) -> None:
    if repo != REPOSITORY:
        raise AuthorizationError("unexpected repository")
    if event_ref != PROTECTED_REF:
        raise AuthorizationError("trusted dispatch must originate from protected main")
    if package_id and not PACKAGE_RE.fullmatch(package_id):
        raise AuthorizationError("package id is invalid")
    expected_base = exact_sha(base_sha, "dispatch base")
    expected_head = exact_sha(head_sha, "dispatch head")
    if publish_to_repo != "false":
        raise AuthorizationError("trusted PR dispatch must disable repository publication")
    if str(pr.get("state") or "").lower() != "open":
        raise AuthorizationError("PR is not open")

    head = pr.get("head") if isinstance(pr.get("head"), Mapping) else {}
    base = pr.get("base") if isinstance(pr.get("base"), Mapping) else {}
    user = pr.get("user") if isinstance(pr.get("user"), Mapping) else {}
    head_repository = head.get("repo") if isinstance(head.get("repo"), Mapping) else {}
    actual_head = exact_sha(head.get("sha"), "PR head")
    actual_base = exact_sha(base.get("sha"), "PR base")
    if str(head_repository.get("full_name") or "").lower() != repo.lower():
        raise AuthorizationError("PR head is not in the trusted repository")
    if str(base.get("ref") or "") != "main":
        raise AuthorizationError("PR base must be protected main")
    head_ref = str(head.get("ref") or "")
    association = str(pr.get("author_association") or "")
    login = str(user.get("login") or "")
    if association not in TRUSTED_ASSOCIATIONS and login not in TRUSTED_LOGINS:
        raise AuthorizationError("PR author is not trusted for persistent runner execution")
    if actual_head != expected_head or actual_base != expected_base:
        raise AuthorizationError("dispatch base or head does not match the current PR")

    changed_files = pr.get("changed_files")
    if not isinstance(changed_files, int) or changed_files < 1 or changed_files > 100:
        raise AuthorizationError("PR changed-file count is outside the trusted one-page boundary")
    if len(files) != changed_files:
        raise AuthorizationError("PR file listing is incomplete")
    paths = [str(item.get("filename") or "") for item in files]
    if package_id:
        if head_ref.startswith(TRUSTED_PREFIXES) is False:
            raise AuthorizationError("PR head ref is outside the trusted package prefixes")
        package_prefix = "packages/%s/" % package_id
        if not paths or any(not path.startswith(package_prefix) for path in paths):
            raise AuthorizationError("PR changes are not confined to packages/%s" % package_id)
        return

    exact_file = len(files) == 1 and not files[0].get("previous_filename")
    if (
        login == "github-actions[bot]"
        and exact_file
        and IMAGE_LOCK_BRANCH_RE.fullmatch(head_ref)
        and paths == ["ci/image.lock"]
        and files[0].get("status") == "modified"
    ):
        return
    catalog = CATALOG_BRANCH_RE.fullmatch(head_ref)
    if (
        login == "github-actions[bot]"
        and exact_file
        and catalog
        and paths == ["catalog/snapshots/%s.json.gz" % catalog.group(1)]
        and files[0].get("status") == "added"
    ):
        return
    raise AuthorizationError("PR is not an allowed bot infrastructure shape")


def write_authorized(path_value: str) -> None:
    path = Path(path_value)
    with path.open("a", encoding="utf-8") as stream:
        stream.write("authorized=true\n")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--repo", required=True)
    result.add_argument("--pr-number", required=True, type=positive_int)
    result.add_argument("--package-id", required=True)
    result.add_argument("--base-sha", required=True)
    result.add_argument("--commit-sha", required=True)
    result.add_argument("--publish-to-repo", required=True)
    result.add_argument("--event-ref", required=True)
    result.add_argument("--github-output", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        pr, files = fetch_pr(args.repo, args.pr_number)
        authorize(
            pr,
            files,
            repo=args.repo,
            package_id=args.package_id,
            base_sha=args.base_sha,
            head_sha=args.commit_sha,
            publish_to_repo=args.publish_to_repo,
            event_ref=args.event_ref,
        )
        write_authorized(args.github_output)
    except AuthorizationError as exc:
        print("authorize-trusted-package-dispatch: %s" % exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
