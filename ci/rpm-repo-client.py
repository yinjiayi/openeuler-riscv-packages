#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resolve and verify immutable snapshots of the supplemental RPM repository."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


PUBLIC_ROOT = "http://2.27.148.101:38080"
STATE_URL = f"{PUBLIC_ROOT}/state.json"
PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
GENERATION = re.compile(
    r"^(?:bootstrap-[0-9]{8}T[0-9]{6}Z|"
    r"[a-z0-9]+(?:-[a-z0-9]+)*-[0-9a-f]{40}-[1-9][0-9]{0,19}-[1-9][0-9]{0,9})$"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MAX_STATE_BYTES = 4 * 1024 * 1024
MAX_REPOMD_BYTES = 16 * 1024 * 1024


class RepositoryUnavailable(ValueError):
    """The fixed supplemental endpoint could not be contacted."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def fetch(url: str, maximum: int) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    expected = urllib.parse.urlsplit(PUBLIC_ROOT)
    if (
        parsed.scheme != expected.scheme
        or parsed.netloc != expected.netloc
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("repository URL is outside the fixed public endpoint")
    request = urllib.request.Request(url, headers={"User-Agent": "openeuler-riscv-rpm-repo-client/1"})
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=20) as response:
            if response.status != 200 or response.geturl() != url:
                raise ValueError("repository response changed URL or did not return HTTP 200")
            length = response.headers.get("Content-Length")
            if length and int(length) > maximum:
                raise ValueError("repository response exceeds the size limit")
            payload = response.read(maximum + 1)
    except urllib.error.HTTPError as error:
        if error.code in {408, 429, 500, 502, 503, 504}:
            raise RepositoryUnavailable(
                f"fixed supplemental repository endpoint returned transient HTTP {error.code}"
            ) from error
        raise ValueError(f"repository returned HTTP {error.code} for {url}") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise RepositoryUnavailable("fixed supplemental repository endpoint is unavailable") from error
    if len(payload) > maximum:
        raise ValueError("repository response exceeds the size limit")
    return payload


def validate_state(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("repository state is not an object")
    expected_keys = {
        "schema_version",
        "generation",
        "published_at",
        "package_id",
        "commit_sha",
        "run_id",
        "run_attempt",
        "repositories",
    }
    if set(value) != expected_keys or value.get("schema_version") != 1:
        raise ValueError("repository state has missing or unexpected fields")
    generation = value.get("generation")
    if not isinstance(generation, str) or not GENERATION.fullmatch(generation):
        raise ValueError("repository generation is invalid")
    package_id = value.get("package_id")
    commit_sha = value.get("commit_sha")
    run_id = value.get("run_id")
    run_attempt = value.get("run_attempt")
    bootstrap = generation.startswith("bootstrap-")
    if bootstrap:
        if any(item is not None for item in (package_id, commit_sha, run_id, run_attempt)):
            raise ValueError("bootstrap state contains package publication claims")
    else:
        if not isinstance(package_id, str) or not PACKAGE_ID.fullmatch(package_id):
            raise ValueError("repository state package_id is invalid")
        if not isinstance(commit_sha, str) or not COMMIT_SHA.fullmatch(commit_sha):
            raise ValueError("repository state commit_sha is invalid")
        if not isinstance(run_id, int) or isinstance(run_id, bool) or run_id < 1:
            raise ValueError("repository state run_id is invalid")
        if not isinstance(run_attempt, int) or isinstance(run_attempt, bool) or run_attempt < 1:
            raise ValueError("repository state run_attempt is invalid")
    repositories = value.get("repositories")
    if not isinstance(repositories, dict) or set(repositories) != {"riscv64", "source"}:
        raise ValueError("repository state must contain exactly riscv64 and source repositories")
    for name, document in repositories.items():
        if not isinstance(document, dict) or set(document) != {"baseurl", "repomd_sha256", "rpm_count"}:
            raise ValueError(f"{name} repository state has missing or unexpected fields")
        expected_base = f"{PUBLIC_ROOT}/generations/{generation}/{name}/"
        if document.get("baseurl") != expected_base:
            raise ValueError(f"{name} baseurl is not the immutable expected generation URL")
        checksum = document.get("repomd_sha256")
        count = document.get("rpm_count")
        if not isinstance(checksum, str) or not SHA256.fullmatch(checksum):
            raise ValueError(f"{name} repomd SHA-256 is invalid")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError(f"{name} RPM count is invalid")
    return value


def load_and_verify_state(state_url: str) -> tuple[dict[str, Any], str, dict[str, str]]:
    state_bytes = fetch(state_url, MAX_STATE_BYTES)
    try:
        state = validate_state(json.loads(state_bytes.decode("utf-8")))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"repository state is not valid UTF-8 JSON: {error}") from error
    repomd_hashes: dict[str, str] = {}
    for name, repository in state["repositories"].items():
        repomd_url = repository["baseurl"] + "repodata/repomd.xml"
        repomd = fetch(repomd_url, MAX_REPOMD_BYTES)
        checksum = sha256_bytes(repomd)
        if checksum != repository["repomd_sha256"]:
            raise ValueError(f"{name} repomd.xml does not match state.json")
        repomd_hashes[name] = checksum
    return state, sha256_bytes(state_bytes), repomd_hashes


def atomic_text(path: Path, value: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def unavailable_repo_text() -> str:
    return "\n".join(
        [
            "# Supplemental repository unavailable; use the official repository only.",
            "[openeuler-riscv-project]",
            "name=openEuler RISC-V project packages (unavailable)",
            f"baseurl={PUBLIC_ROOT}/",
            "enabled=0",
            "gpgcheck=0",
            "repo_gpgcheck=0",
            "metadata_expire=never",
            "skip_if_unavailable=1",
            "module_hotfixes=1",
            "",
        ]
    )


def write_unavailable_resolution(args: argparse.Namespace) -> None:
    atomic_text(Path(args.repo_file), unavailable_repo_text())
    atomic_json(
        Path(args.output),
        {
            "schema_version": 1,
            "kind": "supplemental-repository-resolution",
            "status": "unavailable",
            "resolved_at": utc_now(),
            "state_url": args.state_url,
            "state_sha256": None,
            "generation": None,
            "repositories": {},
            "verified_repomd_sha256": {},
            "reason": "endpoint-unavailable",
            "fallback": {
                "active_repository_ids": ["openeuler-rva23"],
                "supplemental_repository_enabled": False,
            },
            "trust": {
                "transport": "official openEuler HTTPS repository",
                "rpm_gpgcheck": True,
                "controls": [
                    "supplemental repository explicitly disabled",
                    "official repository only",
                    "official repository GPG verification retained",
                ],
            },
        },
    )


def resolve(args: argparse.Namespace) -> int:
    if args.state_url != STATE_URL:
        raise ValueError("resolve requires the fixed global state URL")
    try:
        state, state_sha, repomd_hashes = load_and_verify_state(args.state_url)
    except RepositoryUnavailable:
        if not args.allow_unavailable:
            raise
        write_unavailable_resolution(args)
        print("official-only")
        return 0
    binary = state["repositories"]["riscv64"]
    repo_text = "\n".join(
        [
            "# Generated from a verified immutable repository generation.",
            "[openeuler-riscv-project]",
            "name=openEuler RISC-V project packages (immutable generation)",
            f"baseurl={binary['baseurl']}",
            "enabled=1",
            "gpgcheck=0",
            "repo_gpgcheck=0",
            "metadata_expire=never",
            "skip_if_unavailable=0",
            "module_hotfixes=1",
            "",
        ]
    )
    atomic_text(Path(args.repo_file), repo_text)
    atomic_json(
        Path(args.output),
        {
            "schema_version": 1,
            "kind": "supplemental-repository-resolution",
            "status": "passed",
            "resolved_at": utc_now(),
            "state_url": args.state_url,
            "state_sha256": state_sha,
            "generation": state["generation"],
            "repositories": state["repositories"],
            "verified_repomd_sha256": repomd_hashes,
            "trust": {
                "transport": "operator-provided HTTP endpoint",
                "rpm_gpgcheck": False,
                "controls": [
                    "fixed endpoint",
                    "no redirects",
                    "immutable generation URL",
                    "state-bound repomd SHA-256",
                ],
            },
        },
    )
    print(state["generation"])
    return 0


def verify_generation(args: argparse.Namespace) -> int:
    if not GENERATION.fullmatch(args.expected_generation):
        raise ValueError("expected generation is invalid")
    expected_url = f"{PUBLIC_ROOT}/generations/{args.expected_generation}/state.json"
    if args.state_url != expected_url:
        raise ValueError("generation state URL does not match the expected generation")
    if not PACKAGE_ID.fullmatch(args.expected_package) or not COMMIT_SHA.fullmatch(args.expected_commit):
        raise ValueError("expected package or commit is invalid")
    state, state_sha, repomd_hashes = load_and_verify_state(args.state_url)
    if (
        state["generation"] != args.expected_generation
        or state["package_id"] != args.expected_package
        or state["commit_sha"] != args.expected_commit
    ):
        raise ValueError("published generation does not match the expected package and commit")
    atomic_json(
        Path(args.output),
        {
            "schema_version": 1,
            "kind": "rpm-repository-publication-verification",
            "verified_at": utc_now(),
            "state_url": args.state_url,
            "state_sha256": state_sha,
            "generation": state["generation"],
            "package_id": state["package_id"],
            "commit_sha": state["commit_sha"],
            "run_id": state["run_id"],
            "run_attempt": state["run_attempt"],
            "repositories": state["repositories"],
            "verified_repomd_sha256": repomd_hashes,
            "status": "passed",
        },
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--state-url", default=STATE_URL)
    resolve_parser.add_argument("--repo-file", required=True)
    resolve_parser.add_argument("--output", required=True)
    resolve_parser.add_argument(
        "--allow-unavailable",
        action="store_true",
        help="record an official-repository-only fallback when the fixed endpoint cannot be contacted",
    )
    resolve_parser.set_defaults(function=resolve)
    verify_parser = subparsers.add_parser("verify-generation")
    verify_parser.add_argument("--state-url", required=True)
    verify_parser.add_argument("--expected-generation", required=True)
    verify_parser.add_argument("--expected-package", required=True)
    verify_parser.add_argument("--expected-commit", required=True)
    verify_parser.add_argument("--output", required=True)
    verify_parser.set_defaults(function=verify_generation)
    args = parser.parse_args()
    try:
        return args.function(args)
    except ValueError as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
