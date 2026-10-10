#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Preserve only physical golden RPM/SRPM products, separate from log ingestion.

Successful phase claims must match the exact regular files, sizes and hashes.
Failure/native routing remains failure/native routing, never build acceptance.
No logs, commands, environment, repository configuration or source cache are
copied; the SRPM itself preserves build inputs for later inert inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import shutil
import stat
import sys

REPO = Path(__file__).resolve().parents[1]
FIXTURES = {"golden-success-hello", "golden-riscv-inline-asm", "golden-needs-native-kmod"}
SHA = re.compile(r"^[a-f0-9]{40}$")
# Input-parser safety bounds, not uploaded artifact/RPM byte budgets.
MAX_PHASE_BYTES = 1024 * 1024
MAX_TREE_DEPTH = 64


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_path(workspace: Path, path: Path, allow_missing: bool = False) -> bool:
    """Reject symlinks and non-directory ancestors inside the workspace."""
    current = workspace
    require(stat.S_ISDIR(current.lstat().st_mode), "workspace-not-regular-directory")
    parts = path.relative_to(workspace).parts
    for index, part in enumerate(parts):
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            require(allow_missing, "missing-required-path")
            return False
        require(not stat.S_ISLNK(mode), "symlink-input")
        if index != len(parts) - 1:
            require(stat.S_ISDIR(mode), "non-directory-ancestor")
    return True


def product_paths(workspace: Path, package_id: str) -> dict[str, Path]:
    result = {}
    work = workspace / "work" / package_id
    for tree in ("RPMS", "SRPMS"):
        root = work / tree
        if not safe_path(workspace, root, allow_missing=True):
            continue
        require(stat.S_ISDIR(root.lstat().st_mode), "product-tree-not-directory")
        def walk(directory: Path, depth: int) -> None:
            # Stream directory entries without imposing a product-count or
            # RPM-byte budget; recursion depth only protects path traversal.
            with os.scandir(directory) as scan:
                for entry in scan:
                    path = Path(entry.path)
                    require(depth + 1 <= MAX_TREE_DEPTH, "product-tree-depth-limit")
                    mode = path.lstat().st_mode
                    require(not stat.S_ISLNK(mode), "symlink-product-entry")
                    if stat.S_ISDIR(mode):
                        walk(path, depth + 1)
                    elif path.suffix == ".rpm":
                        require(stat.S_ISREG(mode), "non-regular-rpm")
                        result[path.relative_to(workspace).as_posix()] = path
        walk(root, 0)
    return result


def claim_path(value: str, package_id: str) -> str:
    require(isinstance(value, str), "invalid-artifact-path")
    parts = PurePosixPath(value).parts
    require(".." not in parts and "\\" not in value and "\x00" not in value,
            "unsafe-artifact-path")
    # Target container paths are /workspace/work/<id>/...; relative paths
    # are accepted solely in that same lexical subtree, never arbitrary hosts.
    relative = value[len("/workspace/"):] if value.startswith("/workspace/") else value
    parts = PurePosixPath(relative).parts
    require(len(parts) >= 4 and parts[:2] == ("work", package_id) and
            parts[2] in {"RPMS", "SRPMS"} and not relative.startswith("/") and
            relative == PurePosixPath(relative).as_posix() and
            relative.endswith(".rpm"), "artifact-path-outside-fixture")
    return relative


def stage(workspace: Path, package_id: str, commit_sha: str, needs_native: bool,
          output: Path, manifest: dict) -> None:
    paths = product_paths(workspace, package_id)
    phase_path = workspace / "artifacts" / "golden" / package_id / "rpmbuild-phase-result.json"
    phase = None
    if safe_path(workspace, phase_path, allow_missing=True):
        require(stat.S_ISREG(phase_path.lstat().st_mode), "phase-not-regular-file")
        require(phase_path.stat().st_size <= MAX_PHASE_BYTES, "phase-input-size-limit")
        # Read at most the parser limit plus one byte, even if input grows
        # between lstat and read. Never hash/re-read arbitrary phase contents.
        with phase_path.open("rb") as handle:
            phase_bytes = handle.read(MAX_PHASE_BYTES + 1)
        require(len(phase_bytes) <= MAX_PHASE_BYTES, "phase-input-size-limit")
        phase = json.loads(phase_bytes.decode("utf-8"))
        sys.path.insert(0, str(REPO / "scripts"))
        validator = runpy.run_path(str(REPO / "scripts" / "validate-metadata"))
        schema = json.loads((REPO / "schemas" / "build-result.schema.json").read_text())
        require(not validator["schema_errors"](phase, schema, schema), "phase-schema-invalid")
        require(phase.get("kind") == "build-result" and
                phase.get("package_id") == package_id and
                phase.get("commit_sha") == commit_sha, "phase-identity-mismatch")
        manifest["phase_sha256"] = hashlib.sha256(phase_bytes).hexdigest()
        manifest["phase_status"] = phase["status"]
    if needs_native:
        require(not paths and (phase is None or phase["status"] == "needs-native-riscv"),
                "native-route-has-unexpected-products-or-build")
        manifest["product_evidence"] = "not-built-native-route"
        return
    require(phase is None or phase["status"] != "needs-native-riscv", "native-route-mismatch")
    verified = phase is not None and phase["status"] == "passed"
    if verified:
        require(phase["exit_code"] == 0 and phase["phase"] == "complete", "passed-phase-incomplete")
        claims = {}
        for claim in phase["artifacts"]:
            relative = claim_path(claim["path"], package_id)
            require(relative not in claims, "duplicate-artifact-claim")
            require(claim["kind"] == ("srpm" if relative.split("/")[2] == "SRPMS" else "rpm"),
                    "artifact-kind-mismatch")
            claims[relative] = claim
        require(set(claims) == set(paths) and
                {claim["kind"] for claim in claims.values()} == {"rpm", "srpm"},
                "passed-phase-products-missing-or-extra")
        for relative, source in paths.items():
            claim = claims[relative]
            require(source.stat().st_size == claim["size"] and
                    digest(source) == claim["sha256"], "physical-product-mismatch")
    manifest["product_evidence"] = "phase-matched-physical-products" if verified else "unverified-partial-or-no-build"
    for relative, source in sorted(paths.items()):
        source_sha = digest(source)
        size = source.stat().st_size
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination, follow_symlinks=False)
        require(destination.stat().st_size == size and digest(destination) == source_sha,
                "copied-product-mismatch")
        if verified:
            require(source_sha == claims[relative]["sha256"] and size == claims[relative]["size"],
                    "product-changed-during-copy")
        manifest["products"].append({"path": relative, "sha256": source_sha, "size": size,
                                     "kind": "srpm" if relative.split("/")[2] == "SRPMS" else "rpm"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--package-id", required=True, choices=sorted(FIXTURES))
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--needs-native", required=True, choices=("true", "false"))
    args = parser.parse_args()
    require(bool(SHA.fullmatch(args.commit_sha)), "invalid-commit-sha")
    workspace = Path(args.workspace).absolute()
    output = workspace / "artifacts" / "golden-products" / args.package_id
    safe_path(workspace, output.parent, allow_missing=True)
    # No recursive deletion or reuse: stale output requires operator isolation.
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 1, "kind": "golden-physical-product-manifest",
                "package_id": args.package_id, "commit_sha": args.commit_sha,
                "status": "failed", "phase_status": None, "phase_sha256": None,
                "product_evidence": "not-verified", "products": [],
                "boundary": "Physical retention only; not package installation or publication acceptance."}
    try:
        stage(workspace, args.package_id, args.commit_sha, args.needs_native == "true", output, manifest)
        manifest["status"] = "passed"
    except (ValueError, OSError, KeyError, TypeError):
        # Never echo arbitrary phase contents, command arguments or environment.
        manifest["message"] = "Golden physical product staging failed; inputs or products did not satisfy the retention contract."
    (output / "physical-products.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0 if manifest["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
