#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create the missing ``configure`` CheckRun for one trusted image-lock PR.

This helper runs only from the protected default branch.  It never checks out or
executes candidate content.  Every write is surrounded by API readbacks bound to
the source workflow run, pull-request head, and current default-branch head.
"""

from __future__ import annotations

import argparse
import base64
import binascii
from datetime import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping


SHA = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
IMAGE_BRANCH = re.compile(r"^infra/ci-image-[0-9a-f]{12}$")
SOURCE_NAME = "Auto Merge Policy"
SOURCE_PATH = ".github/workflows/auto-merge.yml"
BRIDGE_NAME = "Configure Context Bridge"
BRIDGE_PATH = ".github/workflows/configure-context-bridge.yml"
CHECK_NAME = "configure"
CHECK_APP_ID = 15368
CHECK_APP_SLUG = "github-actions"
LOCK_FIELDS = {
    "schema_version",
    "image",
    "tag",
    "digest",
    "status",
    "source_repository",
    "repomd_sha256",
    "rpm_manifest_sha256",
    "containerfile_sha256",
    "built_at",
    "qemu_version",
    "self_test",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
BUILT_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LOCK_KEY = re.compile(r"^([a-z][a-z0-9_]*):[ \t]*(.*)$")


class BridgeError(RuntimeError):
    """The attestation is unavailable, malformed, or changed."""


def mapping(value: Any, description: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BridgeError(f"{description} is not an object")
    return value


def api_json(arguments: list[str], payload: Mapping[str, Any] | None = None) -> Any:
    command = [
        "gh", "api", "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28", *arguments,
    ]
    stdin = None
    if payload is not None:
        command.extend(["--input", "-"])
        stdin = json.dumps(payload, sort_keys=True)
    try:
        completed = subprocess.run(
            command,
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise BridgeError("cannot execute the GitHub CLI") from error
    if completed.returncode != 0:
        raise BridgeError(f"GitHub API request failed with exit status {completed.returncode}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise BridgeError("GitHub API response is not valid JSON") from error


def write_atomic(path: Path, document: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(document, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def source_attestation(repository: str, run_id: int) -> tuple[Mapping[str, Any], bool]:
    run = mapping(api_json([f"repos/{repository}/actions/runs/{run_id}"]), "source workflow run")
    if run.get("id") != run_id:
        raise BridgeError("source workflow-run id changed")
    if run.get("name") != SOURCE_NAME or run.get("path") != SOURCE_PATH:
        raise BridgeError("source workflow provenance is not Auto Merge Policy")
    if run.get("event") != "pull_request" or run.get("status") != "completed":
        raise BridgeError("source workflow event or status is invalid")
    if mapping(run.get("repository"), "source repository").get("full_name") != repository:
        raise BridgeError("source workflow repository changed")
    if mapping(run.get("head_repository"), "source head repository").get("full_name") != repository:
        raise BridgeError("source workflow head repository is not trusted")
    conclusion = run.get("conclusion")
    if conclusion != "action_required":
        return run, False
    actor = mapping(run.get("actor"), "source actor").get("login")
    triggering = mapping(run.get("triggering_actor"), "source triggering actor").get("login")
    if actor != "github-actions[bot]" or triggering != "github-actions[bot]":
        raise BridgeError("action-required source was not initiated by github-actions[bot]")
    pulls = run.get("pull_requests")
    if not isinstance(pulls, list) or len(pulls) != 1:
        raise BridgeError("action-required source does not identify exactly one pull request")
    return run, True


def current_main(repository: str, trusted_main_sha: str) -> str:
    repo = mapping(api_json([f"repos/{repository}"]), "repository")
    if repo.get("full_name") != repository or repo.get("default_branch") != "main":
        raise BridgeError("repository identity or default branch changed")
    ref = mapping(api_json([f"repos/{repository}/git/ref/heads/main"]), "default branch ref")
    obj = mapping(ref.get("object"), "default branch object")
    head = obj.get("sha")
    if ref.get("ref") != "refs/heads/main" or obj.get("type") != "commit" or not isinstance(head, str) or not SHA.fullmatch(head):
        raise BridgeError("default branch ref is malformed")
    if head != trusted_main_sha:
        raise BridgeError("bridge policy checkout is not the current default-branch head")
    return head


def bridge_attestation(repository: str, run_id: int, trusted_main_sha: str) -> None:
    run = mapping(api_json([f"repos/{repository}/actions/runs/{run_id}"]), "bridge workflow run")
    if run.get("id") != run_id or run.get("name") != BRIDGE_NAME or run.get("path") != BRIDGE_PATH:
        raise BridgeError("bridge workflow provenance is invalid")
    if run.get("event") not in ("workflow_run", "workflow_dispatch"):
        raise BridgeError("bridge workflow event is invalid")
    if run.get("head_sha") != trusted_main_sha or run.get("head_branch") != "main":
        raise BridgeError("bridge workflow is not executing the trusted main commit")
    if mapping(run.get("repository"), "bridge repository").get("full_name") != repository:
        raise BridgeError("bridge workflow repository changed")


def source_pull(run: Mapping[str, Any]) -> tuple[int, str, str]:
    pull = mapping(run["pull_requests"][0], "source pull request")
    number = pull.get("number")
    head = mapping(pull.get("head"), "source pull head").get("sha")
    base = mapping(pull.get("base"), "source pull base").get("sha")
    if not isinstance(number, int) or number <= 0:
        raise BridgeError("source pull-request number is invalid")
    if not isinstance(head, str) or not SHA.fullmatch(head):
        raise BridgeError("source pull-request head is invalid")
    if not isinstance(base, str) or not SHA.fullmatch(base):
        raise BridgeError("source pull-request base is invalid")
    if run.get("head_sha") != head:
        raise BridgeError("source workflow head differs from its pull request")
    return number, head, base


def pull_attestation(repository: str, number: int, head: str, base: str) -> Mapping[str, Any]:
    pull = mapping(api_json([f"repos/{repository}/pulls/{number}"]), "pull request")
    pull_head = mapping(pull.get("head"), "pull-request head")
    pull_base = mapping(pull.get("base"), "pull-request base")
    if pull.get("number") != number or pull.get("state") != "open" or pull.get("merged") is not False or pull.get("merged_at") is not None:
        raise BridgeError("pull request is no longer open and unmerged")
    if pull.get("auto_merge") is not None:
        raise BridgeError("pull request auto-merge is armed")
    if pull.get("draft") is not False:
        raise BridgeError("image-lock pull request is draft")
    if mapping(pull.get("user"), "pull-request author").get("login") != "github-actions[bot]":
        raise BridgeError("image-lock pull request author is not github-actions[bot]")
    if pull_head.get("sha") != head or pull_base.get("sha") != base:
        raise BridgeError("pull-request head or base changed")
    if pull_head.get("ref") is None or not isinstance(pull_head.get("ref"), str) or not IMAGE_BRANCH.fullmatch(str(pull_head.get("ref"))):
        raise BridgeError("image-lock pull-request branch is invalid")
    for side, value in (("head", pull_head), ("base", pull_base)):
        if mapping(value.get("repo"), f"pull-request {side} repository").get("full_name") != repository:
            raise BridgeError(f"pull-request {side} repository is not trusted")
    if pull_base.get("ref") != "main" or base != current_main(repository, base):
        raise BridgeError("pull request is not based on the current default-branch head")
    if pull.get("changed_files") != 1:
        raise BridgeError("image-lock pull request does not contain exactly one changed file")
    pages = api_json(["--paginate", "--slurp", f"repos/{repository}/pulls/{number}/files?per_page=100"])
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise BridgeError("pull-request file listing is not a paginated array")
    files = [item for page in pages for item in page]
    if len(files) != 1 or not isinstance(files[0], Mapping) or files[0].get("filename") != "ci/image.lock":
        raise BridgeError("image-lock pull request changed an unexpected path")
    if files[0].get("status") != "modified" or files[0].get("previous_filename") is not None:
        raise BridgeError("image-lock file change shape is invalid")
    return pull


def contents_file(repository: str, commit: str) -> str:
    document = mapping(
        api_json([f"repos/{repository}/contents/ci/image.lock?ref={commit}"]),
        "image-lock contents response",
    )
    if (
        document.get("type") != "file"
        or document.get("path") != "ci/image.lock"
        or document.get("name") != "image.lock"
        or document.get("encoding") != "base64"
    ):
        raise BridgeError("image-lock contents identity is invalid")
    blob_sha = document.get("sha")
    size = document.get("size")
    content = document.get("content")
    if not isinstance(blob_sha, str) or not SHA.fullmatch(blob_sha):
        raise BridgeError("image-lock blob SHA is invalid")
    if type(size) is not int or size <= 0 or size > 16384 or not isinstance(content, str):
        raise BridgeError("image-lock contents size is invalid")
    try:
        if re.fullmatch(r"[A-Za-z0-9+/=\n]+", content) is None:
            raise binascii.Error("unexpected base64 character")
        raw = base64.b64decode(content.replace("\n", ""), validate=True)
        text = raw.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as error:
        raise BridgeError("image-lock contents are not canonical base64 UTF-8") from error
    if len(raw) != size or "\x00" in text:
        raise BridgeError("image-lock decoded size or encoding is invalid")
    return text


def parse_lock(text: str, description: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = LOCK_KEY.fullmatch(raw_line)
        if match is None:
            raise BridgeError(f"{description} contains unsupported YAML syntax")
        key, raw_value = match.groups()
        if key in values:
            raise BridgeError(f"{description} contains duplicate field {key}")
        if raw_value.startswith('"'):
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError as error:
                raise BridgeError(f"{description} contains an invalid quoted value") from error
            if not isinstance(value, str):
                raise BridgeError(f"{description} quoted value is not a string")
        elif re.fullmatch(r"[0-9]+", raw_value):
            value = int(raw_value)
        elif re.fullmatch(r"[A-Za-z0-9./:+_-]+", raw_value):
            value = raw_value
        else:
            raise BridgeError(f"{description} contains an unsafe scalar")
        values[key] = value
    if set(values) != LOCK_FIELDS:
        raise BridgeError(f"{description} fields do not match schema version 1")
    if values["schema_version"] != 1:
        raise BridgeError(f"{description} schema version is not 1")
    if values["image"] != "ghcr.io/yinjiayi/openeuler-riscv64-rpmbuild":
        raise BridgeError(f"{description} image identity changed")
    if values["tag"] != "24.03-lts-sp3-rva23":
        raise BridgeError(f"{description} target tag changed")
    digest = values["digest"]
    if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise BridgeError(f"{description} digest is not immutable sha256")
    if values["status"] != "published-public-anonymous-verified":
        raise BridgeError(f"{description} publication status is not verified")
    if values["self_test"] != "passed":
        raise BridgeError(f"{description} self-test did not pass")
    if values["source_repository"] != "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/":
        raise BridgeError(f"{description} source repository changed")
    for key in ("repomd_sha256", "rpm_manifest_sha256", "containerfile_sha256"):
        if not isinstance(values[key], str) or not HEX64.fullmatch(values[key]):
            raise BridgeError(f"{description} {key} is invalid")
    built_at = values["built_at"]
    if not isinstance(built_at, str) or not BUILT_AT.fullmatch(built_at):
        raise BridgeError(f"{description} built_at is invalid")
    try:
        datetime.fromisoformat(built_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise BridgeError(f"{description} built_at is not a real timestamp") from error
    qemu = values["qemu_version"]
    if not isinstance(qemu, str) or not re.fullmatch(r"tonistiigi/binfmt:qemu-v[0-9]+\.[0-9]+\.[0-9]+", qemu):
        raise BridgeError(f"{description} qemu version is invalid")
    return values


def lock_attestation(repository: str, head: str, base: str, branch: str) -> dict[str, Any]:
    candidate = parse_lock(contents_file(repository, head), "candidate image lock")
    previous = parse_lock(contents_file(repository, base), "base image lock")
    prefix = branch.removeprefix("infra/ci-image-")
    digest_hex = str(candidate["digest"]).removeprefix("sha256:")
    if len(prefix) != 12 or not re.fullmatch(r"[0-9a-f]{12}", prefix) or not digest_hex.startswith(prefix):
        raise BridgeError("image-lock branch does not match the candidate digest prefix")
    if candidate["digest"] == previous["digest"]:
        raise BridgeError("candidate image lock did not update digest")
    if candidate["built_at"] <= previous["built_at"]:
        raise BridgeError("candidate image lock did not advance built_at")
    for key in ("schema_version", "image", "tag", "source_repository"):
        if candidate[key] != previous[key]:
            raise BridgeError(f"candidate image lock unexpectedly changed {key}")
    return candidate


def disarm(repository: str, number: int, head: str, base: str) -> None:
    try:
        completed = subprocess.run(
            ["gh", "pr", "merge", str(number), "--repo", repository, "--disable-auto"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise BridgeError("cannot execute the GitHub CLI to disarm auto-merge") from error
    # GitHub returns non-zero when auto-merge is already off.  Exact API
    # readback, rather than the command's exit status, is the security proof.
    pull_attestation(repository, number, head, base)
    if completed.returncode != 0:
        print("disable-auto returned non-zero; exact API readback proves it is off", file=sys.stderr)


def prove_context_absent(repository: str, head: str) -> None:
    status_pages = api_json([
        "--paginate", "--slurp", f"repos/{repository}/commits/{head}/statuses?per_page=100"
    ])
    if not isinstance(status_pages, list) or any(not isinstance(page, list) for page in status_pages):
        raise BridgeError("commit status listing is not a paginated array")
    statuses = [item for page in status_pages for item in page]
    if any(isinstance(item, Mapping) and item.get("context") == CHECK_NAME for item in statuses):
        raise BridgeError("a forbidden configure StatusContext already exists")
    check_pages = api_json([
        "--paginate", "--slurp",
        f"repos/{repository}/commits/{head}/check-runs?check_name={CHECK_NAME}&per_page=100",
    ])
    if not isinstance(check_pages, list) or any(not isinstance(page, Mapping) for page in check_pages):
        raise BridgeError("configure CheckRun listing is not a paginated object array")
    checks: list[Any] = []
    for page in check_pages:
        page_checks = page.get("check_runs")
        if not isinstance(page_checks, list):
            raise BridgeError("configure CheckRun page is malformed")
        checks.extend(page_checks)
    if checks:
        raise BridgeError("a configure CheckRun already exists on the exact head")


def external_id(repository: str, number: int, head: str, base: str, source_run: int, bridge_run: int) -> str:
    return ":".join(("configure-bridge-v1", repository, str(number), head, base, str(source_run), str(bridge_run)))


def patch_check(repository: str, check_id: int, conclusion: str, title: str, summary: str) -> Mapping[str, Any]:
    return mapping(api_json(
        ["-X", "PATCH", f"repos/{repository}/check-runs/{check_id}"],
        {
            "status": "completed",
            "conclusion": conclusion,
            "output": {"title": title, "summary": summary},
        },
    ), "updated check run")


def fail_created_check(repository: str, check_id: int, reason: str) -> None:
    try:
        patch_check(repository, check_id, "failure", "Configure bridge attestation failed", reason[:65000])
    except BridgeError:
        pass


def create_check(repository: str, head: str, eid: str, details_url: str) -> tuple[int, Mapping[str, Any]]:
    payload = {
        "name": CHECK_NAME,
        "head_sha": head,
        "status": "in_progress",
        "external_id": eid,
        "details_url": details_url,
        "output": {
            "title": "Configure bridge attestation in progress",
            "summary": "Protected-main policy is validating the exact image-lock pull request.",
        },
    }
    try:
        created = mapping(api_json(["-X", "POST", f"repos/{repository}/check-runs"], payload), "created check run")
    except BridgeError as original:
        # A transport error can hide a successful POST.  Recover only the one
        # exact external-id match and mark it failed; never infer success.
        try:
            listing = mapping(api_json([f"repos/{repository}/commits/{head}/check-runs?check_name={CHECK_NAME}&per_page=100"]), "check-run recovery listing")
            runs = listing.get("check_runs")
            matches = [item for item in runs if isinstance(item, Mapping) and item.get("external_id") == eid] if isinstance(runs, list) else []
            if len(matches) == 1 and isinstance(matches[0].get("id"), int):
                fail_created_check(repository, int(matches[0]["id"]), str(original))
        except BridgeError:
            pass
        raise original
    check_id = created.get("id")
    if not isinstance(check_id, int) or check_id <= 0:
        raise BridgeError("created check-run id is invalid")
    if created.get("name") != CHECK_NAME or created.get("head_sha") != head or created.get("external_id") != eid:
        fail_created_check(repository, check_id, "created CheckRun identity did not match the request")
        raise BridgeError("created check-run identity is invalid")
    return check_id, created


def prove_check(
    repository: str,
    check_id: int,
    head: str,
    eid: str,
    details_url: str,
    status: str,
    conclusion: str | None,
) -> Mapping[str, Any]:
    check = mapping(api_json([f"repos/{repository}/check-runs/{check_id}"]), "check-run readback")
    app = mapping(check.get("app"), "check-run app")
    expected = {
        "id": check_id,
        "name": CHECK_NAME,
        "head_sha": head,
        "status": status,
        "conclusion": conclusion,
        "external_id": eid,
        "details_url": details_url,
    }
    if any(check.get(key) != value for key, value in expected.items()):
        raise BridgeError("check-run readback identity is invalid")
    if app.get("id") != CHECK_APP_ID or app.get("slug") != CHECK_APP_SLUG:
        raise BridgeError("configure was not created by the GitHub Actions Checks app")
    return check


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-run-id", required=True, type=int)
    parser.add_argument("--bridge-run-id", required=True, type=int)
    parser.add_argument("--trusted-main-sha", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    result: dict[str, Any] = {
        "schema_version": 1,
        "status": "failed",
        "repository": args.repository,
        "source_run_id": args.source_run_id,
        "bridge_run_id": args.bridge_run_id,
        "trusted_main_sha": args.trusted_main_sha,
        "check_run_id": None,
        "pull_request": None,
        "head_sha": None,
        "base_sha": None,
        "image_digest": None,
        "image_built_at": None,
        "errors": [],
    }
    check_id: int | None = None
    try:
        if not REPOSITORY.fullmatch(args.repository):
            raise BridgeError("repository must be in owner/name form")
        if args.source_run_id <= 0 or args.bridge_run_id <= 0:
            raise BridgeError("workflow-run ids must be positive integers")
        if not SHA.fullmatch(args.trusted_main_sha):
            raise BridgeError("trusted main SHA must be a lowercase 40-character SHA")
        source, candidate = source_attestation(args.repository, args.source_run_id)
        if not candidate:
            result["status"] = "not-applicable"
            write_atomic(args.output, result)
            print(json.dumps(result, sort_keys=True))
            return 0
        current_main(args.repository, args.trusted_main_sha)
        bridge_attestation(args.repository, args.bridge_run_id, args.trusted_main_sha)
        number, head, base = source_pull(source)
        result.update({"pull_request": number, "head_sha": head, "base_sha": base})
        if base != args.trusted_main_sha:
            raise BridgeError("source pull request is stale relative to trusted main")
        pull = pull_attestation(args.repository, number, head, base)
        lock = lock_attestation(args.repository, head, base, str(mapping(pull.get("head"), "pull-request head")["ref"]))
        result.update({"image_digest": lock["digest"], "image_built_at": lock["built_at"]})
        prove_context_absent(args.repository, head)
        disarm(args.repository, number, head, base)
        # The complete second pass immediately precedes the CheckRun write.
        current_main(args.repository, args.trusted_main_sha)
        bridge_attestation(args.repository, args.bridge_run_id, args.trusted_main_sha)
        source_again, candidate_again = source_attestation(args.repository, args.source_run_id)
        if not candidate_again or source_pull(source_again) != (number, head, base):
            raise BridgeError("source workflow binding changed before CheckRun creation")
        pull = pull_attestation(args.repository, number, head, base)
        if lock_attestation(args.repository, head, base, str(mapping(pull.get("head"), "pull-request head")["ref"])) != lock:
            raise BridgeError("image-lock contents changed between exact-head attestations")
        prove_context_absent(args.repository, head)
        details = f"https://github.com/{args.repository}/actions/runs/{args.bridge_run_id}"
        eid = external_id(args.repository, number, head, base, args.source_run_id, args.bridge_run_id)
        check_id, _ = create_check(args.repository, head, eid, details)
        result["check_run_id"] = check_id
        # Prove the Checks App provenance while the context is still pending;
        # an unexpected creator must never receive a transient success.
        prove_check(args.repository, check_id, head, eid, details, "in_progress", None)
        # A third exact lease protects completion from a post-create race.
        current_main(args.repository, args.trusted_main_sha)
        source_final, candidate_final = source_attestation(args.repository, args.source_run_id)
        if not candidate_final or source_pull(source_final) != (number, head, base):
            raise BridgeError("source workflow binding changed after CheckRun creation")
        pull = pull_attestation(args.repository, number, head, base)
        if lock_attestation(args.repository, head, base, str(mapping(pull.get("head"), "pull-request head")["ref"])) != lock:
            raise BridgeError("image-lock contents changed after CheckRun creation")
        patch_check(
            args.repository,
            check_id,
            "success",
            "Configure bridge attestation passed",
            f"Trusted protected-main bridge validated PR #{number} at exact head {head} and base {base}.",
        )
        prove_check(args.repository, check_id, head, eid, details, "completed", "success")
        # Final lease: a success is invalidated if the candidate changed during
        # the successful-check readback window.
        current_main(args.repository, args.trusted_main_sha)
        pull = pull_attestation(args.repository, number, head, base)
        if lock_attestation(args.repository, head, base, str(mapping(pull.get("head"), "pull-request head")["ref"])) != lock:
            raise BridgeError("image-lock contents changed after CheckRun completion")
        result["status"] = "passed"
        write_atomic(args.output, result)
        print(json.dumps(result, sort_keys=True))
        return 0
    except BridgeError as error:
        if check_id is not None:
            fail_created_check(args.repository, check_id, str(error))
        result["errors"].append(str(error))
        write_atomic(args.output, result)
        print(json.dumps(result, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
