#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Download retained Dashboard-safe build and publication JSON artifacts."""

from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import os
import pathlib
import re
import stat
import subprocess
import tempfile
import time
import zipfile
from typing import Any, Dict, List


ARTIFACT_NAME = re.compile(
    r"^(?P<kind>package-ci-smoke|rpm-repository-publish)-(?P<package>.+)-(?P<run_id>[1-9][0-9]*)$"
)
MAX_JSON_BYTES = 8 * 1024 * 1024
ARTIFACT_PAGE_SIZE = 25
MAX_ARTIFACT_PAGES = 1000
ARTIFACT_PAGE_ATTEMPTS = 6
MAX_ARTIFACT_PAGE_BYTES = 2 * 1024 * 1024


def gh(*arguments: str, binary: bool = False, timeout_seconds: int = 180) -> bytes | str:
    completed = subprocess.run(
        ["gh", *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_seconds,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError("gh api failed: %s" % message[:1000])
    return completed.stdout if binary else completed.stdout.decode("utf-8")


def safe_basename(value: str) -> str:
    name = pathlib.PurePosixPath(value).name
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name)[:120] or "evidence.json"


def extract_json(archive: bytes, output: pathlib.Path, artifact_id: int) -> List[str]:
    extracted: List[str] = []
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        members = sorted(bundle.infolist(), key=lambda item: item.filename)
        for index, member in enumerate(members):
            if member.is_dir() or not member.filename.lower().endswith(".json"):
                continue
            mode = member.external_attr >> 16
            file_type = stat.S_IFMT(mode)
            if file_type and file_type != stat.S_IFREG:
                continue
            if member.file_size > MAX_JSON_BYTES:
                continue
            payload = bundle.read(member)
            try:
                document = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(document, dict):
                continue
            destination = output / str(artifact_id) / ("%03d-%s" % (index, safe_basename(member.filename)))
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = tempfile.NamedTemporaryFile(prefix=".%s." % destination.name, dir=str(destination.parent), delete=False)
            try:
                with temporary:
                    temporary.write((json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8"))
                    temporary.flush()
                    os.fsync(temporary.fileno())
                os.chmod(temporary.name, 0o644)
                os.replace(temporary.name, destination)
            finally:
                try:
                    os.unlink(temporary.name)
                except FileNotFoundError:
                    pass
            extracted.append(str(destination))
    return extracted


def select_artifacts(artifacts: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], int]:
    """Keep the newest artifact per package/kind and fetch publications first."""
    newest: Dict[tuple[str, str], Dict[str, Any]] = {}
    eligible_count = 0
    for artifact in artifacts:
        name = artifact.get("name")
        artifact_id = artifact.get("id")
        if artifact.get("expired") or not isinstance(name, str) or not isinstance(artifact_id, int):
            continue
        match = ARTIFACT_NAME.fullmatch(name)
        if not match:
            continue
        eligible_count += 1
        key = (match.group("kind"), match.group("package"))
        prior = newest.get(key)
        ordering = (str(artifact.get("created_at") or ""), artifact_id)
        prior_ordering = (
            (str(prior.get("created_at") or ""), int(prior["id"]))
            if prior
            else ("", -1)
        )
        if prior is None or ordering > prior_ordering:
            newest[key] = artifact
    selected = sorted(
        newest.values(),
        key=lambda artifact: (
            str(artifact["name"]).startswith("rpm-repository-publish-"),
            str(artifact.get("created_at") or ""),
            int(artifact["id"]),
        ),
        reverse=True,
    )
    return selected, eligible_count


def list_artifacts(repository: str) -> tuple[List[Dict[str, Any]], int, int]:
    """Fetch bounded JSON pages independently so a truncated page can be retried.

    The Actions API lists newest artifacts first. Fetch through the first short
    page rather than trusting a changing total_count during concurrent CI runs.
    A repeated malformed or incomplete page fails the Dashboard build closed.
    """
    artifacts: List[Dict[str, Any]] = []
    seen_ids: set[int] = set()
    retries = 0
    for page_number in range(1, MAX_ARTIFACT_PAGES + 1):
        endpoint = (
            "repos/%s/actions/artifacts?per_page=%d&page=%d"
            % (repository, ARTIFACT_PAGE_SIZE, page_number)
        )
        for attempt in range(ARTIFACT_PAGE_ATTEMPTS):
            try:
                payload = str(gh("api", endpoint, timeout_seconds=30))
                if len(payload.encode("utf-8")) > MAX_ARTIFACT_PAGE_BYTES:
                    raise ValueError("artifact page exceeds the response bound")
                document = json.loads(payload)
                if not isinstance(document, dict) or not isinstance(document.get("artifacts"), list):
                    raise ValueError("artifact page has an invalid shape")
                page = document["artifacts"]
                if len(page) > ARTIFACT_PAGE_SIZE or not all(isinstance(item, dict) for item in page):
                    raise ValueError("artifact page has invalid entries")
                break
            except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
                if attempt + 1 == ARTIFACT_PAGE_ATTEMPTS:
                    raise RuntimeError("artifact page %d failed after %d attempts: %s" % (
                        page_number, ARTIFACT_PAGE_ATTEMPTS, error
                    )) from error
                retries += 1
                time.sleep(attempt + 1)
        for artifact in page:
            artifact_id = artifact.get("id")
            if not isinstance(artifact_id, int) or artifact_id <= 0:
                raise ValueError("artifact page has an invalid artifact id")
            if artifact_id not in seen_ids:
                seen_ids.add(artifact_id)
                artifacts.append(artifact)
        if len(page) < ARTIFACT_PAGE_SIZE:
            return artifacts, page_number, retries
    raise RuntimeError("artifact listing exceeded the %d-page safety bound" % MAX_ARTIFACT_PAGES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    repository = os.environ.get("GITHUB_REPOSITORY") or os.environ.get("GH_REPOSITORY")
    if not repository or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        parser.error("GITHUB_REPOSITORY or GH_REPOSITORY must name owner/repository")
    artifacts, page_count, listing_retries = list_artifacts(repository)
    selected, eligible_count = select_artifacts(artifacts)
    output = pathlib.Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    failures: List[Dict[str, Any]] = []
    extracted: List[str] = []
    def download(artifact: Dict[str, Any]) -> tuple[List[str], Dict[str, Any] | None]:
        artifact_id = int(artifact["id"])
        try:
            archive = gh("api", "repos/%s/actions/artifacts/%d/zip" % (repository, artifact_id), binary=True)
            return extract_json(archive, output, artifact_id), None  # type: ignore[arg-type]
        except (RuntimeError, zipfile.BadZipFile) as exc:
            return [], {"artifact_id": artifact_id, "name": artifact["name"], "error": str(exc)[:1000]}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for paths, failure in executor.map(download, selected):
            extracted.extend(paths)
            if failure:
                failures.append(failure)
    result = {
        "schema_version": 1,
        "kind": "dashboard-evidence-collection",
        "repository": repository,
        "eligible_artifact_count": eligible_count,
        "listing_page_count": page_count,
        "listing_retries": listing_retries,
        "selected_artifact_count": len(selected),
        "selection_strategy": "latest-per-package-kind-publication-first",
        "extracted_json_count": len(extracted),
        "failures": failures,
    }
    result_path = pathlib.Path(args.result)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
