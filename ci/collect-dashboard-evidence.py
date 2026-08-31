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
import zipfile
from typing import Any, Dict, List


ARTIFACT_PREFIXES = ("package-ci-smoke-", "rpm-repository-publish-")
MAX_JSON_BYTES = 8 * 1024 * 1024


def gh(*arguments: str, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["gh", *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    repository = os.environ.get("GITHUB_REPOSITORY") or os.environ.get("GH_REPOSITORY")
    if not repository or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        parser.error("GITHUB_REPOSITORY or GH_REPOSITORY must name owner/repository")
    pages = json.loads(str(gh("api", "--paginate", "--slurp", "repos/%s/actions/artifacts?per_page=100" % repository)))
    artifacts: List[Dict[str, Any]] = []
    for page in pages if isinstance(pages, list) else []:
        if isinstance(page, dict) and isinstance(page.get("artifacts"), list):
            artifacts.extend(item for item in page["artifacts"] if isinstance(item, dict))
    selected = sorted(
        (
            item
            for item in artifacts
            if not item.get("expired")
            and isinstance(item.get("name"), str)
            and str(item["name"]).startswith(ARTIFACT_PREFIXES)
            and isinstance(item.get("id"), int)
        ),
        key=lambda item: (str(item.get("created_at") or ""), int(item["id"])),
    )
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
        "selected_artifact_count": len(selected),
        "extracted_json_count": len(extracted),
        "failures": failures,
    }
    result_path = pathlib.Path(args.result)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
