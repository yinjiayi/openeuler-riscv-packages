#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resolve and verify immutable snapshots of the supplemental RPM repository."""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib


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
MAX_PRIMARY_BYTES = 32 * 1024 * 1024
MAX_PRIMARY_OPEN_BYTES = 128 * 1024 * 1024
# Representable file size, not a package/aggregate artifact budget. Streaming
# verifies exactly the manifest-declared length without retaining RPM payloads.
MAX_FILE_SIZE = (1 << 63) - 1
RPM_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.~%-]*\.rpm$")
REPO_NS = "{http://linux.duke.edu/metadata/repo}"
COMMON_NS = "{http://linux.duke.edu/metadata/common}"
RPM_NS = "{http://linux.duke.edu/metadata/rpm}"


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


def load_upload_manifest(path: Path, state: dict[str, Any]) -> tuple[dict[str, Any], str]:
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_STATE_BYTES + 1)
        if len(raw) > MAX_STATE_BYTES:
            raise ValueError("upload manifest exceeds the size limit")
        manifest = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("exact upload manifest is missing or invalid") from error
    fields = {"schema_version", "generation", "package_id", "commit_sha", "run_id", "run_attempt", "artifacts"}
    if not isinstance(manifest, dict) or set(manifest) not in (fields, fields | {"kind", "status"}):
        raise ValueError("upload manifest has missing or unexpected fields")
    if "kind" in manifest and (manifest["kind"] != "rpm-repository-upload-batch" or manifest["status"] != "staged"):
        raise ValueError("upload manifest is not a staged RPM batch")
    for key in fields - {"artifacts"}:
        if type(manifest[key]) is not type(state[key]) or manifest[key] != state[key]:
            raise ValueError(f"upload manifest {key} does not match the published state")
    if state["generation"] != f"{state['package_id']}-{state['commit_sha']}-{state['run_id']}-{state['run_attempt']}":
        raise ValueError("generation does not bind the publication identity")
    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) < 2:
        raise ValueError("upload manifest must contain a binary and source RPM batch")
    names: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {"filename", "kind", "sha256", "size"}:
            raise ValueError("upload artifact has missing or unexpected fields")
        filename = artifact["filename"]
        if not isinstance(filename, str) or not RPM_FILENAME.fullmatch(filename) or filename in names:
            raise ValueError("upload artifact filename is unsafe or duplicated")
        if not isinstance(artifact["kind"], str) or artifact["kind"] not in {"binary", "source"}:
            raise ValueError("upload artifact kind is invalid")
        if not isinstance(artifact["sha256"], str) or not SHA256.fullmatch(artifact["sha256"]):
            raise ValueError("upload artifact SHA-256 is invalid")
        size = artifact["size"]
        if type(size) is not int or not 1 <= size <= MAX_FILE_SIZE:
            raise ValueError("upload artifact size is not a representable positive file size")
        names.add(filename)
    if {item["kind"] for item in artifacts} != {"binary", "source"}:
        raise ValueError("upload manifest requires both binary RPM and source RPM")
    return manifest, sha256_bytes(raw)


def xml_root(raw: bytes, expected: str) -> ET.Element:
    # ElementTree does not fetch external entities, but reject internal DTDs too.
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("repository XML must not contain a DTD or entity declaration")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as error:
        raise ValueError("repository XML is invalid") from error
    if root.tag != expected:
        raise ValueError("repository XML has an unexpected root or namespace")
    return root


def one(element: ET.Element, tag: str) -> ET.Element:
    found = element.findall(tag)
    if len(found) != 1:
        raise ValueError(f"repository XML requires exactly one {tag}")
    return found[0]


def integer(value: str | None, maximum: int, description: str) -> int:
    if value is None or not re.fullmatch(r"[0-9]{1,20}", value) or int(value) > maximum:
        raise ValueError(f"invalid or oversized {description}")
    return int(value)


def checksum(element: ET.Element) -> str:
    if element.get("type") != "sha256" or not SHA256.fullmatch(element.text or ""):
        raise ValueError("repository metadata requires SHA-256 checksums")
    return str(element.text)


def decompress_zstd(payload: bytes) -> bytes:
    """Use the existing catalog dependency with bounded output, memory and time."""
    executable = shutil.which("zstd")
    if executable is None:
        raise ValueError("zstd is required to verify this repository's primary metadata")
    with tempfile.NamedTemporaryFile(prefix="rpm-publication-", suffix=".zst") as source:
        source.write(payload)
        source.flush()
        with subprocess.Popen(
            [executable, "-q", "-d", "-c", "-M128MB", "--", source.name],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ) as process:
            assert process.stdout is not None
            output = bytearray()
            deadline = time.monotonic() + 20
            try:
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ)
                    while True:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0 or not selector.select(remaining):
                            raise ValueError("primary zstd decompression exceeded its time limit")
                        block = os.read(process.stdout.fileno(), min(1024 * 1024, MAX_PRIMARY_OPEN_BYTES - len(output) + 1))
                        if not block:
                            break
                        output.extend(block)
                        if len(output) > MAX_PRIMARY_OPEN_BYTES:
                            raise ValueError("expanded primary metadata exceeds the verifier limit")
                if process.wait(timeout=max(0.01, deadline - time.monotonic())) != 0:
                    raise ValueError("primary metadata has invalid zstd data")
            except BaseException as error:
                process.kill()
                process.wait()
                if isinstance(error, (OSError, subprocess.TimeoutExpired)):
                    raise ValueError("primary zstd decompression failed or timed out") from error
                raise
    return bytes(output)


def load_primary(repository: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    base = repository["baseurl"]
    raw_repomd = fetch(base + "repodata/repomd.xml", MAX_REPOMD_BYTES)
    if sha256_bytes(raw_repomd) != repository["repomd_sha256"]:
        raise ValueError("repomd changed after the state verification")
    repomd = xml_root(raw_repomd, REPO_NS + "repomd")
    entries = [item for item in repomd.findall(REPO_NS + "data") if item.get("type") == "primary"]
    if len(entries) != 1:
        raise ValueError("repomd requires exactly one primary record")
    entry = entries[0]
    primary_href = one(entry, REPO_NS + "location").get("href", "")
    if not re.fullmatch(r"repodata/[A-Za-z0-9][A-Za-z0-9._+-]*\.xml(?:\.gz|\.zst)?", primary_href):
        raise ValueError("primary location is unsafe or its compression is unsupported")
    size = integer(one(entry, REPO_NS + "size").text, MAX_PRIMARY_BYTES, "primary size")
    expected_sha = checksum(one(entry, REPO_NS + "checksum"))
    compressed = fetch(base + primary_href, min(size, MAX_PRIMARY_BYTES))
    if len(compressed) != size or sha256_bytes(compressed) != expected_sha:
        raise ValueError("primary metadata size or SHA-256 mismatch")
    if primary_href.endswith(".gz"):
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
                raw = stream.read(MAX_PRIMARY_OPEN_BYTES + 1)
        except (OSError, EOFError) as error:
            raise ValueError("primary metadata has invalid gzip data") from error
    elif primary_href.endswith(".zst"):
        raw = decompress_zstd(compressed)
    else:
        raw = compressed
    if len(raw) > MAX_PRIMARY_OPEN_BYTES:
        raise ValueError("expanded primary metadata exceeds the verifier limit")
    for tag, actual in (("open-size", len(raw)), ("open-checksum", sha256_bytes(raw))):
        elements = entry.findall(REPO_NS + tag)
        if len(elements) > 1:
            raise ValueError(f"duplicate primary {tag}")
        if elements:
            expected = (integer(elements[0].text, MAX_PRIMARY_OPEN_BYTES, tag)
                        if tag == "open-size" else checksum(elements[0]))
            if expected != actual:
                raise ValueError(f"primary {tag} mismatch")
    primary = xml_root(raw, COMMON_NS + "metadata")
    packages = primary.findall(COMMON_NS + "package")
    count = integer(primary.get("packages"), 100000, "primary package count")
    if count != len(packages) or count != repository["rpm_count"]:
        raise ValueError("primary package count does not match the generation state")
    records: dict[str, Any] = {}
    for package in packages:
        href = one(package, COMMON_NS + "location").get("href", "")
        filename = href.removeprefix("Packages/")
        if not href.startswith("Packages/") or not RPM_FILENAME.fullmatch(filename) or filename in records:
            raise ValueError("primary RPM location is unsafe or duplicated")
        version = one(package, COMMON_NS + "version")
        identity = {
            "name": one(package, COMMON_NS + "name").text,
            "epoch": version.get("epoch"),
            "version": version.get("ver"),
            "release": version.get("rel"),
            "arch": one(package, COMMON_NS + "arch").text,
        }
        if any(not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9+_.~%^:-]{1,256}", value)
               for value in identity.values()):
            raise ValueError("primary package identity is invalid")
        integer(identity["epoch"], 4294967295, "package epoch")
        if identity["arch"] not in {"riscv64", "noarch", "src", "nosrc"}:
            raise ValueError("primary package architecture is unsupported")
        expected_filename = "{name}-{version}-{release}.{arch}.rpm".format(**identity)
        if filename != expected_filename:
            raise ValueError("primary filename does not match its package identity")
        format_element = one(package, COMMON_NS + "format")
        source_rpm = one(format_element, RPM_NS + "sourcerpm").text or ""
        if source_rpm and not RPM_FILENAME.fullmatch(source_rpm):
            raise ValueError("primary source RPM reference is unsafe")
        records[filename] = {
            "sha256": checksum(one(package, COMMON_NS + "checksum")),
            "size": integer(one(package, COMMON_NS + "size").get("package"), MAX_FILE_SIZE, "RPM size"),
            "identity": identity,
            "source_rpm": source_rpm,
        }
    return records, {"url": base + primary_href,
                     "sha256": expected_sha, "open_sha256": sha256_bytes(raw), "rpm_count": count}


def fetch_rpm_digest(url: str, size: int, deadline: float) -> str:
    # URLs are constructed only from validated immutable base URLs and quoted
    # manifest basenames. Never follow a metadata-supplied absolute RPM URL.
    parsed = urllib.parse.urlsplit(url)
    endpoint = urllib.parse.urlsplit(PUBLIC_ROOT)
    parts = parsed.path.split("/")
    if (
        parsed.scheme != endpoint.scheme or parsed.netloc != endpoint.netloc
        or parsed.query or parsed.fragment or len(parts) != 6
        or parts[:2] != ["", "generations"] or not GENERATION.fullmatch(parts[2])
        or parts[3] not in {"riscv64", "source"} or parts[4] != "Packages"
    ):
        raise ValueError("RPM URL is outside the fixed public endpoint")
    filename = urllib.parse.unquote(parts[5], errors="strict")
    if not RPM_FILENAME.fullmatch(filename) or urllib.parse.quote(filename, safe="+_.~-") != parts[5]:
        raise ValueError("RPM URL filename is not canonical")
    if type(size) is not int or not 1 <= size <= MAX_FILE_SIZE:
        raise ValueError("RPM download size is not a representable positive file size")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ValueError("publication verification exceeded its time limit")
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": "openeuler-riscv-rpm-repo-client/1"})
    digest = hashlib.sha256()
    received = 0
    try:
        with opener.open(request, timeout=min(20, remaining)) as response:
            if response.status != 200 or response.geturl() != url:
                raise ValueError("RPM response redirected or did not return HTTP 200")
            length = response.headers.get("Content-Length")
            if length is not None and integer(length, MAX_FILE_SIZE, "RPM Content-Length") != size:
                raise ValueError("RPM Content-Length does not match the upload manifest")
            while True:
                if time.monotonic() >= deadline:
                    raise ValueError("publication verification exceeded its time limit")
                chunk = response.read(min(1024 * 1024, size - received + 1))
                if not chunk:
                    break
                received += len(chunk)
                if received > size:
                    raise ValueError("RPM bytes exceed the upload manifest size")
                digest.update(chunk)
    except urllib.error.HTTPError as error:
        raise ValueError(f"RPM returned HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise ValueError("RPM download failed") from error
    if received != size:
        raise ValueError("RPM byte count does not match the upload manifest")
    return digest.hexdigest()


def verify_products(state: dict[str, Any], artifacts: list[dict[str, Any]],
                    records: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    sources = {item["filename"] for item in artifacts if item["kind"] == "source"}
    selected: list[dict[str, Any]] = []
    for artifact in artifacts:
        repository = "source" if artifact["kind"] == "source" else "riscv64"
        filename = artifact["filename"]
        record = records[repository].get(filename)
        if record is None:
            raise ValueError(f"uploaded {artifact['kind']} RPM is missing from primary metadata: {filename}")
        if record["sha256"] != artifact["sha256"] or record["size"] != artifact["size"]:
            raise ValueError(f"primary RPM differs from exact upload manifest: {filename}")
        source = record["identity"]["arch"] in {"src", "nosrc"}
        if source != (artifact["kind"] == "source"):
            raise ValueError(f"primary RPM kind does not match upload manifest: {filename}")
        if not source and record["source_rpm"] not in sources:
            raise ValueError(f"binary RPM does not reference an uploaded source RPM: {filename}")
        url = state["repositories"][repository]["baseurl"] + "Packages/" + urllib.parse.quote(filename, safe="+_.~-")
        selected.append({**artifact, "url": url, "identity": record["identity"], "source_rpm": record["source_rpm"]})
    # Sequential streaming requests bound socket/memory load even for large RPMs.
    deadline = time.monotonic() + 300
    for artifact in selected:
        if fetch_rpm_digest(artifact["url"], artifact["size"], deadline) != artifact["sha256"]:
            raise ValueError(f"physical RPM SHA-256 mismatch: {artifact['filename']}")
    return selected


def _verify_generation(args: argparse.Namespace) -> int:
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
    manifest, manifest_sha = load_upload_manifest(Path(args.upload_manifest), state)
    primary_records: dict[str, dict[str, Any]] = {}
    primary_evidence: dict[str, dict[str, Any]] = {}
    for repository in ("riscv64", "source"):
        records, evidence = load_primary(state["repositories"][repository])
        primary_records[repository] = records
        primary_evidence[repository] = evidence
    verified = verify_products(state, manifest["artifacts"], primary_records)
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
            "upload_manifest_sha256": manifest_sha,
            "verified_primary": primary_evidence,
            "verified_artifacts": verified,
            "verification_scope": "uploaded batch, not every historical package in the cumulative generation",
            "identity_source": "checksum-bound-primary; RPM headers and signatures were not independently queried",
            "trust": {
                "transport": "operator-provided HTTP endpoint",
                "authentication": "not established by same-endpoint checksums",
                "artifact_binding": "exact local upload manifest SHA-256 and size",
            },
            "status": "passed",
        },
    )
    return 0


def verify_generation(args: argparse.Namespace) -> int:
    if Path(args.output).resolve() == Path(args.upload_manifest).resolve():
        raise ValueError("verification output must not overwrite the upload manifest")
    try:
        return _verify_generation(args)
    except (ValueError, OSError, http.client.HTTPException, subprocess.TimeoutExpired, zlib.error) as error:
        # A failed retry must not leave a prior success receipt at this path.
        atomic_json(Path(args.output), {
            "schema_version": 1,
            "kind": "rpm-repository-publication-verification",
            "status": "failed",
            "checked_at": utc_now(),
            "reason": str(error),
        })
        raise ValueError(str(error)) from error


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
    verify_parser.add_argument(
        "--upload-manifest", default="artifacts/repository-publish/upload.json",
        help="exact staged upload evidence; defaults to the existing Package CI upload record",
    )
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
