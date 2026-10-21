#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit published RPM/SRPM availability without executing packages or changing the server."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = "http://2.27.148.101:38080"
MAX_PRIMARY = 32 * 1024 * 1024
RPM_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.~%-]*\.rpm$")
CLIENT_SPEC = importlib.util.spec_from_file_location("published_rpm_client", ROOT / "ci/rpm-repo-client.py")
CLIENT = importlib.util.module_from_spec(CLIENT_SPEC)
CLIENT_SPEC.loader.exec_module(CLIENT)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative_url(base: str, relative: str, *, rpm: bool = False) -> str:
    parsed = urllib.parse.urlsplit(relative)
    if (parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or
            relative.startswith("/") or ".." in relative.split("/") or "\\" in relative or "%" in relative):
        raise ValueError("unsafe repository metadata location")
    if rpm:
        if not relative.startswith("Packages/") or not RPM_FILENAME.fullmatch(relative[9:]):
            raise ValueError("unsafe RPM filename")
    elif not relative.startswith("repodata/"):
        raise ValueError("metadata location is outside repodata")
    return base + relative


def primary_entries(repository: dict, category: str) -> tuple[list[dict], dict]:
    base = repository["baseurl"]
    repomd_url = base + "repodata/repomd.xml"
    repomd = CLIENT.fetch(repomd_url, CLIENT.MAX_REPOMD_BYTES)
    if digest(repomd) != repository["repomd_sha256"]:
        raise ValueError("repomd checksum does not match immutable state")
    ns = {"r": "http://linux.duke.edu/metadata/repo"}
    documents = [d for d in ET.fromstring(repomd).findall("r:data", ns) if d.get("type") == "primary"]
    if len(documents) != 1:
        raise ValueError("repository has no unique primary metadata")
    document = documents[0]
    checksum = document.find("r:checksum", ns)
    open_checksum = document.find("r:open-checksum", ns)
    expected_size = int(document.find("r:size", ns).text)
    expected_open_size = int(document.find("r:open-size", ns).text)
    if checksum.get("type") != "sha256" or open_checksum.get("type") != "sha256":
        raise ValueError("primary metadata requires SHA-256 checksums")
    if not (0 < expected_size <= 16 * 1024 * 1024 and 0 < expected_open_size <= MAX_PRIMARY):
        raise ValueError("primary metadata size exceeds the bounded audit")
    href = document.find("r:location", ns).get("href")
    url = relative_url(base, href)
    compressed = CLIENT.fetch(url, expected_size)
    if len(compressed) != expected_size or digest(compressed) != checksum.text:
        raise ValueError("compressed primary metadata checksum or size mismatch")
    if href.endswith(".gz"):
        with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
            raw = stream.read(expected_open_size + 1)
    elif href.endswith(".zst"):
        # zstd is a decoder only; package contents are never executed.
        with tempfile.TemporaryFile() as compressed_input:
            compressed_input.write(compressed)
            compressed_input.seek(0)
            process = subprocess.Popen(["zstd", "-dc"], stdin=compressed_input, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            deadline = threading.Timer(30, process.kill)
            deadline.start()
            try:
                raw = process.stdout.read(expected_open_size + 1)
                if len(raw) > expected_open_size:
                    process.kill()
                code = process.wait(timeout=30)
                if code != 0:
                    raise ValueError("bounded zstd metadata decoding failed")
            finally:
                deadline.cancel()
                if process.poll() is None:
                    process.kill()
                    process.wait()
                process.stdout.close()
    else:
        raise ValueError("unsupported primary metadata compression")
    if len(raw) != expected_open_size or digest(raw) != open_checksum.text:
        raise ValueError("open primary metadata checksum or size mismatch")
    root = ET.fromstring(raw)
    common = {"c": "http://linux.duke.edu/metadata/common", "rpm": "http://linux.duke.edu/metadata/rpm"}
    packages = root.findall("c:package", common)
    if len(packages) != int(root.get("packages")) or len(packages) != repository["rpm_count"]:
        raise ValueError("primary package count does not match immutable state")
    rows = []
    locations = set()
    for package in packages:
        version = package.find("c:version", common)
        checksum = package.find("c:checksum", common)
        relative = package.find("c:location", common).get("href")
        size = int(package.find("c:size", common).get("package"))
        arch = package.find("c:arch", common).text
        if checksum.get("type") != "sha256" or not CLIENT.SHA256.fullmatch(checksum.text):
            raise ValueError("RPM metadata requires a full SHA-256")
        if size <= 0:
            raise ValueError("RPM metadata declares a non-positive size")
        if arch not in ({"src", "nosrc"} if category == "source" else {"riscv64", "noarch"}):
            raise ValueError("repository contains an unexpected package architecture")
        url = relative_url(base, relative, rpm=True)
        if url in locations:
            raise ValueError("duplicate RPM metadata location")
        locations.add(url)
        sourcerpm = package.find("c:format/rpm:sourcerpm", common)
        rows.append({"name": package.find("c:name", common).text,
                     "epoch": version.get("epoch", "0"), "version": version.get("ver"),
                     "release": version.get("rel"), "arch": arch,
                     "filename": relative[9:], "url": url, "sha256": checksum.text, "size": size,
                     "sourcerpm": sourcerpm.text if sourcerpm is not None else None})
    return rows, {"repomd_url": repomd_url, "repomd_sha256": digest(repomd),
                  "primary_url": relative_url(base, href),
                  "primary_sha256": digest(compressed), "primary_open_sha256": digest(raw),
                  "primary_size": len(compressed), "primary_open_size": len(raw), "package_count": len(rows)}


def verify_file(record: dict) -> dict:
    url = record["url"]
    parsed = urllib.parse.urlsplit(url)
    fixed = urllib.parse.urlsplit(PUBLIC_ROOT)
    if parsed.scheme != fixed.scheme or parsed.netloc != fixed.netloc or parsed.query or parsed.fragment:
        raise ValueError("RPM URL is outside the fixed endpoint")
    request = urllib.request.Request(url, headers={"User-Agent": "openeuler-dashboard-published-audit/1"})
    opener = urllib.request.build_opener(CLIENT.NoRedirect)
    checksum = hashlib.sha256()
    count = 0
    with opener.open(request, timeout=30) as response:
        if response.status != 200 or response.geturl() != url:
            raise ValueError("RPM response is not HTTP 200 at its immutable URL")
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) != record["size"]:
            raise ValueError("RPM Content-Length differs from primary metadata")
        while True:
            block = response.read(min(1024 * 1024, record["size"] - count + 1))
            if not block:
                break
            count += len(block)
            if count > record["size"]:
                raise ValueError("RPM response exceeds its declared size")
            checksum.update(block)
    if count != record["size"] or checksum.hexdigest() != record["sha256"]:
        raise ValueError("RPM payload checksum or size differs from primary metadata; "
                         f"expected_size={record['size']} observed_size={count} "
                         f"expected_sha256={record['sha256']} observed_sha256={checksum.hexdigest()}")
    return {k: record[k] for k in ["filename", "url", "sha256", "size", "arch"]} | {"verified_at": now()}


def canonical_names(repo_root: Path) -> tuple[dict[str, str], list[dict]]:
    names: dict[str, list[str]] = {}
    for path in sorted((repo_root / "packages").glob("*/package.yaml")):
        if path.parent.name == "_template":
            continue
        if path.is_symlink():
            raise ValueError("package metadata cannot be a symlink")
        metadata = json.loads(path.read_text(encoding="utf-8"))
        package_id = metadata.get("package_id")
        name = metadata.get("rpm", {}).get("name")
        if package_id != path.parent.name or not CLIENT.PACKAGE_ID.fullmatch(package_id or "") or not name:
            raise ValueError("invalid canonical package metadata")
        names.setdefault(name, []).append(package_id)
    return {name: ids[0] for name, ids in names.items() if len(ids) == 1}, [
        {"reason": "ambiguous-rpm-name", "rpm_name": name, "package_ids": ids}
        for name, ids in names.items() if len(ids) != 1]


def collect(repo_root: Path, workers: int) -> dict:
    started = now()
    state_raw = CLIENT.fetch(CLIENT.STATE_URL, CLIENT.MAX_STATE_BYTES)
    state = CLIENT.validate_state(json.loads(state_raw))
    generation_state_url = PUBLIC_ROOT + "/generations/" + state["generation"] + "/state.json"
    generation_state = CLIENT.validate_state(json.loads(CLIENT.fetch(generation_state_url, CLIENT.MAX_STATE_BYTES)))
    if generation_state != state:
        raise ValueError("global and generation-specific states disagree")
    entries = {}
    provenance = {}
    for category in ["riscv64", "source"]:
        entries[category], provenance[category] = primary_entries(state["repositories"][category], category)
    names, gaps = canonical_names(repo_root)
    sources = {record["filename"]: record for record in entries["source"]}
    binaries: dict[str, list[dict]] = {}
    for record in entries["riscv64"]:
        source = sources.get(record["sourcerpm"])
        if not source or any(record[k] != source[k] for k in ["epoch", "version", "release"]):
            gaps.append({"reason": "binary-source-tuple-mismatch", "filename": record["filename"]})
            continue
        binaries.setdefault(record["sourcerpm"], []).append(record)
    results = {}
    failures = []
    all_records = entries["riscv64"] + entries["source"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(verify_file, record): record for record in all_records}
        for future in concurrent.futures.as_completed(futures):
            record = futures[future]
            try:
                results[record["url"]] = future.result()
            except Exception as error:
                failures.append({"reason": "file-verification-failed", "filename": record["filename"], "error": str(error)[:500]})
    gaps.extend(sorted(failures, key=lambda x: x["filename"]))
    packages: dict[str, dict] = {}
    for source in entries["source"]:
        package_id = names.get(source["name"])
        if not package_id:
            gaps.append({"reason": "unmatched-source-rpm-name", "rpm_name": source["name"]})
            continue
        source_result = results.get(source["url"])
        binary_results = [results[b["url"]] for b in binaries.get(source["filename"], []) if b["url"] in results]
        if not source_result or not binary_results:
            gaps.append({"reason": "no-verified-rpm-srpm-pair", "filename": source["filename"]})
            continue
        package = packages.setdefault(package_id, {"package_id": package_id, "rpm_name": source["name"], "versions": []})
        package["versions"].append({"epoch": source["epoch"], "version": source["version"], "release": source["release"],
                                    "source": source_result, "binaries": sorted(binary_results, key=lambda x: x["filename"])})
    # A moving global generation is not a coherent current publication snapshot.
    final_state = CLIENT.validate_state(json.loads(CLIENT.fetch(CLIENT.STATE_URL, CLIENT.MAX_STATE_BYTES)))
    if final_state != state:
        gaps.append({"reason": "global-generation-changed-during-audit"})
    source_names = {source["name"] for source in entries["source"]}
    main_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()
    return {"schema_version": 1, "kind": "dashboard-published-state", "started_at": started, "generated_at": now(),
            "repository": "yinjiayi/openeuler-riscv-packages", "main_sha": main_sha,
            "generation": state["generation"], "state_url": CLIENT.STATE_URL, "state_sha256": digest(state_raw),
            "generation_state_url": generation_state_url, "published_at": state["published_at"],
            "repositories": state["repositories"], "verified_repomd_sha256": {k: v["repomd_sha256"] for k, v in provenance.items()},
            "metadata": provenance, "coverage": {"status": "partial" if gaps else "complete",
                "source_packages": len(source_names), "matched_packages": len(source_names & names.keys()),
                "verified_packages": len(packages), "rpm_files": len(entries["riscv64"]), "srpm_files": len(entries["source"]),
                "verified_files": len(results), "verified_bytes": sum(result["size"] for result in results.values()), "gaps": gaps},
            "trust": {"transport": "operator-provided HTTP endpoint", "unsigned_rpms": True,
                "scope": "State-bound metadata, exact canonical RPM names, immutable links and full payload SHA-256; not installed-smoke, trusted-fleet, security or merge acceptance."},
            "verified_artifacts": sorted(results.values(), key=lambda x: x["url"]),
            "packages": sorted(packages.values(), key=lambda x: x["package_id"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6:
        parser.error("workers must be between 1 and 6")
    if args.output.exists():
        parser.error("output already exists; use a fresh evidence path")
    result = collect(args.repo_root.resolve(), args.workers)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["coverage"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
