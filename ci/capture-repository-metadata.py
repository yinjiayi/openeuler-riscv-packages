#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Retain complete supplemental metadata, not RPM payload or installation proof.

This is an evidence-only consumer of an already resolved generation. It never
selects a repository, updates a resolution, installs a decoder, or executes RPMs.
"""

from __future__ import annotations

import argparse
import bz2
import configparser
import hashlib
import importlib.util
import json
import lzma
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("metadata_rpm_client", ROOT / "ci/rpm-repo-client.py")
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)
REPO_NS = "http://linux.duke.edu/metadata/repo"
COMMON_NS = "http://linux.duke.edu/metadata/common"
FILES_NS = "http://linux.duke.edu/metadata/filelists"
MAX_COMPRESSED = 16 * 1024 * 1024
MAX_OPEN = 64 * 1024 * 1024
RPM_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.~-]*$")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def no_duplicate_keys(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def json_bytes(raw: bytes) -> dict:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys)
    require(isinstance(value, dict), "JSON evidence must be an object")
    return value


def local_bytes(path: Path, maximum: int = CLIENT.MAX_STATE_BYTES) -> bytes:
    require(path.is_file() and not path.is_symlink(), "input must be a regular file")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "local evidence exceeds its parser limit")
    return raw


def integer(value: str | None, maximum: int, *, zero: bool = False) -> int:
    require(isinstance(value, str) and bool(re.fullmatch(r"0|[1-9][0-9]{0,19}", value)),
            "invalid metadata integer")
    number = int(value)
    require((0 if zero else 1) <= number <= maximum, "metadata integer outside parser limits")
    return number


def xml_root(raw: bytes, tag: str) -> ET.Element:
    # No DTD/entity expansion, alternate encodings, or external resource lookup.
    text = raw.decode("utf-8")
    require("\x00" not in text and not re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, re.I),
            "DTD/entities or non UTF-8 XML are not allowed")
    declaration = re.match(r"\ufeff?\s*<\?xml\s+([^?]*)\?>", text)
    if declaration:
        encoding = re.search(r"encoding\s*=\s*['\"]([^'\"]+)['\"]", declaration[1], re.I)
        require(not encoding or encoding[1].lower() in {"utf-8", "utf8"}, "XML encoding must be UTF-8")
    root = ET.fromstring(raw)
    require(root.tag == tag, "unexpected XML root or namespace")
    return root


def one(element: ET.Element, tag: str) -> ET.Element:
    values = element.findall(tag)
    require(len(values) == 1, "missing or duplicate XML field")
    return values[0]


def metadata_url(base: str, href: str) -> str:
    value = urllib.parse.urlsplit(href)
    require(not (value.scheme or value.netloc or value.query or value.fragment) and
            bool(re.fullmatch(r"repodata/[A-Za-z0-9][A-Za-z0-9._+-]*", href)) and
            ".." not in href.split("/"), "unsafe metadata location")
    return base + href


def decompress(raw: bytes, href: str, expected: int) -> bytes:
    if href.endswith(".gz"):
        decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
        result = decoder.decompress(raw, expected + 1)
        require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and len(result) == expected,
                "open gzip metadata size/stream mismatch")
        return result
    elif href.endswith(".bz2"):
        decoder = bz2.BZ2Decompressor()
        result = decoder.decompress(raw, max_length=expected + 1)
        require(decoder.eof and not decoder.unused_data and len(result) == expected,
                "open bzip2 metadata size/stream mismatch")
        return result
    elif href.endswith(".xz"):
        decoder = lzma.LZMADecompressor(memlimit=128 * 1024 * 1024)
        result = decoder.decompress(raw, max_length=expected + 1)
        require(decoder.eof and not decoder.unused_data and len(result) == expected,
                "open xz metadata size/stream mismatch")
        return result
    elif href.endswith(".zst"):
        # Optional, fixed system decoder only: no PATH lookup or installation.
        decoder = Path("/usr/bin/zstd")
        require(decoder.is_file() and os.access(decoder, os.X_OK),
                "zstd metadata requires the preinstalled /usr/bin/zstd decoder")
        with tempfile.TemporaryFile() as source:
            source.write(raw)
            source.seek(0)
            process = subprocess.Popen([str(decoder), "-dc", "--memory=128MB"], stdin=source,
                                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            timer = threading.Timer(30, process.kill)
            timer.start()
            try:
                result = process.stdout.read(expected + 1)
                if len(result) > expected:
                    process.kill()
                require(process.wait(timeout=30) == 0, "zstd metadata decoding failed")
            finally:
                timer.cancel()
                if process.poll() is None:
                    process.kill()
                    process.wait()
                process.stdout.close()
        require(len(result) == expected, "open metadata size mismatch")
        return result
    else:
        raise ValueError("unsupported metadata compression; nothing was skipped")


def identity(package: ET.Element, namespace: str, *, primary: bool) -> tuple:
    prefix = "{" + namespace + "}"
    name = one(package, prefix + "name").text if primary else package.get("name")
    arch = one(package, prefix + "arch").text if primary else package.get("arch")
    version = one(package, prefix + "version")
    epoch = version.get("epoch", "0")
    ver, rel = version.get("ver"), version.get("rel")
    require(isinstance(name, str) and bool(RPM_NAME.fullmatch(name)), "invalid RPM name")
    require(isinstance(epoch, str) and bool(re.fullmatch(r"0|[1-9][0-9]*", epoch)), "invalid RPM epoch")
    for value in (ver, rel):
        require(isinstance(value, str) and 0 < len(value) <= 1024 and
                not any(c.isspace() or ord(c) < 32 for c in value), "invalid RPM version/release")
    return name, epoch, ver, rel, arch


def joined_namespace(primary: bytes, filelists: bytes, category: str, expected_count: int) -> dict:
    p = xml_root(primary, "{" + COMMON_NS + "}metadata")
    f = xml_root(filelists, "{" + FILES_NS + "}filelists")
    primary_packages = p.findall("{" + COMMON_NS + "}package")
    files_packages = f.findall("{" + FILES_NS + "}package")
    require(len(p) == len(primary_packages) and len(f) == len(files_packages),
            "unexpected metadata record type")
    for root, packages in ((p, primary_packages), (f, files_packages)):
        require(integer(root.get("packages"), 2**63 - 1, zero=True) == len(packages) == expected_count,
                "metadata package count differs from immutable state")
    packages, nevras, locations = {}, set(), set()
    for package in primary_packages:
        require(package.get("type") == "rpm", "primary package is not RPM metadata")
        checksum = one(package, "{" + COMMON_NS + "}checksum")
        pkgid = checksum.text
        require(checksum.get("type") == "sha256" and checksum.get("pkgid") == "YES" and
                isinstance(pkgid, str) and bool(CLIENT.SHA256.fullmatch(pkgid)), "invalid primary pkgid")
        key = identity(package, COMMON_NS, primary=True)
        require(key[-1] in ({"src", "nosrc"} if category == "source" else {"riscv64", "noarch"}),
                "unexpected repository architecture")
        location = one(package, "{" + COMMON_NS + "}location").get("href")
        require(isinstance(location, str) and bool(re.fullmatch(r"Packages/[A-Za-z0-9][A-Za-z0-9+_.~%-]*\.rpm", location))
                and "%" not in location, "unsafe RPM metadata location")
        require(pkgid not in packages and key not in nevras and location not in locations,
                "duplicate primary pkgid, NEVRA, or location")
        integer(one(package, "{" + COMMON_NS + "}size").get("package"), 2**63 - 1)
        packages[pkgid] = key
        nevras.add(key)
        locations.add(location)
    seen, file_count = set(), 0
    for package in files_packages:
        pkgid = package.get("pkgid")
        require(pkgid in packages and pkgid not in seen, "orphan or duplicate filelists pkgid")
        require(identity(package, FILES_NS, primary=False) == packages[pkgid], "primary/filelists NEVRA mismatch")
        seen.add(pkgid)
        paths = set()
        for item in package:
            if item.tag == "{" + FILES_NS + "}version":
                continue
            require(item.tag == "{" + FILES_NS + "}file" and item.get("type", "file") in
                    {"file", "dir", "ghost"}, "unexpected filelists item")
            path = item.text
            require(isinstance(path, str) and path.startswith("/") and "\\" not in path and
                    not any(ord(c) < 32 for c in path) and ".." not in path.split("/") and
                    "." not in path.split("/") and "//" not in path and
                    (path == "/" or not path.endswith("/")) and path not in paths,
                    "unsafe, noncanonical, or duplicate filelists path")
            paths.add(path)
        file_count += len(paths)
    require(seen == set(packages), "incomplete primary/filelists pkgid join")
    joined = [[pkgid, *packages[pkgid]] for pkgid in sorted(packages)]
    return {"package_count": len(packages), "file_count": file_count,
            "identity_join": "unique-pkgid-and-identical-NEVRA",
            "identity_join_sha256": sha(json.dumps(joined, separators=(",", ":")).encode()),
            "coverage": "complete"}


def validate_repo(raw: bytes, baseurl: str, enabled: bool) -> None:
    parser = configparser.ConfigParser(interpolation=None, strict=True)
    parser.read_string(raw.decode("utf-8"))
    require(not parser.defaults() and parser.sections() == ["openeuler-riscv-project"],
            "unexpected supplemental repository sections")
    section = dict(parser["openeuler-riscv-project"])
    expected = {"name": "openEuler RISC-V project packages (immutable generation)" if enabled else
                "openEuler RISC-V project packages (unavailable)", "baseurl": baseurl,
                "enabled": "1" if enabled else "0", "gpgcheck": "0", "repo_gpgcheck": "0",
                "metadata_expire": "never", "skip_if_unavailable": "0" if enabled else "1",
                "module_hotfixes": "1"}
    require(section == expected, "repo settings do not match the resolved generation or disabled fallback")


def validate_resolution(resolution: dict) -> bool:
    common = {"schema_version", "kind", "status", "resolved_at", "state_url", "state_sha256",
              "generation", "repositories", "verified_repomd_sha256", "trust"}
    enabled = resolution.get("status") == "passed"
    require(set(resolution) == (common if enabled else common | {"reason", "fallback"}) and
            type(resolution.get("schema_version")) is int and resolution.get("schema_version") == 1 and
            resolution.get("kind") == "supplemental-repository-resolution" and
            resolution.get("state_url") == CLIENT.STATE_URL and
            isinstance(resolution.get("resolved_at"), str), "invalid resolution evidence")
    if enabled:
        require(isinstance(resolution.get("state_sha256"), str) and
                bool(CLIENT.SHA256.fullmatch(resolution["state_sha256"])), "invalid resolved state checksum")
        require(resolution["trust"] == {"transport": "operator-provided HTTP endpoint", "rpm_gpgcheck": False,
                "controls": ["fixed endpoint", "no redirects", "immutable generation URL", "state-bound repomd SHA-256"]},
                "unexpected resolved repository trust policy")
    else:
        require(resolution.get("status") == "unavailable" and resolution.get("reason") == "endpoint-unavailable" and
                resolution.get("state_sha256") is None and resolution.get("generation") is None and
                resolution.get("repositories") == {} and resolution.get("verified_repomd_sha256") == {} and
                resolution.get("fallback") == {"active_repository_ids": ["openeuler-rva23"],
                                               "supplemental_repository_enabled": False} and
                resolution["trust"] == {"transport": "official openEuler HTTPS repository", "rpm_gpgcheck": True,
                "controls": ["supplemental repository explicitly disabled", "official repository only",
                             "official repository GPG verification retained"]}, "invalid official-only fallback")
    return enabled


def capture(args: argparse.Namespace) -> dict:
    for value in (args.package_commit, args.tooling_commit):
        require(bool(CLIENT.COMMIT_SHA.fullmatch(value)), "context requires full commit SHAs")
    require(bool(CLIENT.PACKAGE_ID.fullmatch(args.package_id)), "invalid context package id")
    run_id = integer(str(args.run_id), 10**20 - 1)
    attempt = integer(str(args.run_attempt), 10**10 - 1)
    resolution_raw, repo_raw, overlay_raw = (local_bytes(path) for path in (args.resolution, args.repo_file, args.overlay))
    resolution, overlay = json_bytes(resolution_raw), json_bytes(overlay_raw)
    require(set(overlay) == {"schema_version", "kind", "status", "package_id", "package_commit_sha",
                            "package_tree_sha", "tooling_commit_sha"} and type(overlay["schema_version"]) is int and overlay["schema_version"] == 1 and
            overlay["kind"] == "protected-main-package-overlay" and overlay["status"] == "passed" and
            overlay["package_id"] == args.package_id and overlay["package_commit_sha"] == args.package_commit and
            overlay["tooling_commit_sha"] == args.tooling_commit and
            isinstance(overlay["package_tree_sha"], str) and bool(CLIENT.COMMIT_SHA.fullmatch(overlay["package_tree_sha"])),
            "context does not match the exact package/tooling overlay")
    enabled = validate_resolution(resolution)
    generation = resolution["generation"]
    if enabled:
        require(isinstance(generation, str) and bool(CLIENT.GENERATION.fullmatch(generation)), "invalid resolved generation")
    validate_repo(repo_raw, CLIENT.PUBLIC_ROOT + "/" if not enabled else
                  CLIENT.PUBLIC_ROOT + "/generations/" + generation + "/riscv64/", enabled)
    destination = args.output_dir
    require(not destination.exists() and not destination.is_symlink(), "capture requires a fresh output directory")
    destination.mkdir(parents=True, exist_ok=False)
    files = {}

    def store(name: str, raw: bytes, url: str | None = None) -> None:
        with (destination / name).open("xb") as stream:
            stream.write(raw)
        files[name] = {"sha256": sha(raw), "bytes": len(raw)}
        if url:
            # CLIENT.fetch enforces exact URL + HTTP 200 and no redirects.
            # Never retain arbitrary response headers (e.g. cookies/auth data).
            files[name].update(url=url, http_status=200)

    store("resolution.json", resolution_raw)
    store("openeuler-riscv-project.repo", repo_raw)
    store("tooling-overlay.json", overlay_raw)
    context = {"repository": "yinjiayi/openeuler-riscv-packages", "package_id": args.package_id,
               "package_commit_sha": args.package_commit, "tooling_commit_sha": args.tooling_commit,
               "package_tree_sha": overlay["package_tree_sha"], "run_id": run_id, "run_attempt": attempt,
               "capture_helper_sha256": sha(Path(__file__).read_bytes()),
               "repo_client_sha256": sha((ROOT / "ci/rpm-repo-client.py").read_bytes())}
    store("context.json", (json.dumps(context, indent=2, sort_keys=True) + "\n").encode())
    repositories = {}
    if enabled:
        url = CLIENT.PUBLIC_ROOT + "/generations/" + generation + "/state.json"
        raw = CLIENT.fetch(url, CLIENT.MAX_STATE_BYTES)
        require(sha(raw) == resolution["state_sha256"], "immutable state bytes differ from resolved state checksum")
        state = CLIENT.validate_state(json_bytes(raw))
        require(state["generation"] == generation and state["repositories"] == resolution["repositories"] and
                {k: v["repomd_sha256"] for k, v in state["repositories"].items()} == resolution["verified_repomd_sha256"],
                "immutable state differs from approved resolution")
        store("state.json", raw, url)
        for category in ("riscv64", "source"):
            repository = state["repositories"][category]
            url = repository["baseurl"] + "repodata/repomd.xml"
            repomd = CLIENT.fetch(url, CLIENT.MAX_REPOMD_BYTES)
            require(sha(repomd) == repository["repomd_sha256"], "repomd checksum differs from immutable state")
            root = xml_root(repomd, "{" + REPO_NS + "}repomd")
            store(category + "-repomd.xml", repomd, url)
            opened = {}
            for kind in ("primary", "filelists"):
                entries = [item for item in root.findall("{" + REPO_NS + "}data") if item.get("type") == kind]
                require(len(entries) == 1, "missing or duplicate required metadata type")
                entry = entries[0]
                checksum = one(entry, "{" + REPO_NS + "}checksum")
                open_checksum = one(entry, "{" + REPO_NS + "}open-checksum")
                for check in (checksum, open_checksum):
                    require(check.get("type") == "sha256" and isinstance(check.text, str) and
                            bool(CLIENT.SHA256.fullmatch(check.text)), "metadata requires SHA-256 checksums")
                size = integer(one(entry, "{" + REPO_NS + "}size").text, MAX_COMPRESSED)
                open_size = integer(one(entry, "{" + REPO_NS + "}open-size").text, MAX_OPEN)
                href = one(entry, "{" + REPO_NS + "}location").get("href")
                require(isinstance(href, str), "missing metadata location")
                url = metadata_url(repository["baseurl"], href)
                compressed = CLIENT.fetch(url, size)
                require(len(compressed) == size and sha(compressed) == checksum.text,
                        "compressed metadata checksum or size mismatch")
                raw = decompress(compressed, href, open_size)
                require(sha(raw) == open_checksum.text, "open metadata checksum mismatch")
                store(category + "-" + kind + ".compressed", compressed, url)
                store(category + "-" + kind + ".xml", raw)
                opened[kind] = raw
            repositories[category] = joined_namespace(opened["primary"], opened["filelists"], category, repository["rpm_count"])
    receipt = {"schema_version": 1, "kind": "supplemental-repository-metadata-capture",
               "status": "passed" if enabled else "not-applicable", "captured_at": CLIENT.utc_now(),
               "reason": "complete-enabled-generation-metadata" if enabled else "supplemental-repository-explicitly-disabled",
               "generation": generation, "context": context, "files": files, "repositories": repositories,
               "claim_boundary": "metadata-only; no RPM payload, build, install, publication, or merge acceptance"}
    CLIENT.atomic_json(destination / "receipt.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("resolution", "repo-file", "overlay", "output-dir"):
        parser.add_argument("--" + name, required=True, type=Path)
    for name in ("package-id", "package-commit", "tooling-commit", "run-id", "run-attempt"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    try:
        result = capture(args)
    except (ValueError, OSError, ET.ParseError, EOFError, zlib.error, lzma.LZMAError, subprocess.SubprocessError) as error:
        parser.exit(1, "repository-metadata-capture: " + str(error) + "\n")
    print(result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
