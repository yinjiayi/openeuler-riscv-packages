#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create a regular-file-only, checksum-bound RPM repository upload batch."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
from typing import Any


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
RPM_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+_.~%-]*\.rpm$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def reset_output(path: Path) -> None:
    if path == Path(path.anchor) or path.is_symlink():
        raise ValueError("unsafe upload staging directory")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--run-attempt", required=True, type=int)
    args = parser.parse_args()
    if not PACKAGE_ID.fullmatch(args.package_id) or not COMMIT_SHA.fullmatch(args.commit_sha):
        parser.error("package id or exact commit SHA is invalid")
    if args.run_id < 1 or args.run_attempt < 1:
        parser.error("run id and attempt must be positive integers")
    artifact_root = Path(args.artifact_root).resolve()
    output = Path(args.output_dir).absolute()
    reset_output(output)
    payload_dir = output / "payload"
    payload_dir.mkdir()
    generation = f"{args.package_id}-{args.commit_sha}-{args.run_id}-{args.run_attempt}"
    records: list[dict[str, Any]] = []
    names: set[str] = set()
    for tree, kind in (("RPMS", "binary"), ("SRPMS", "source")):
        root = artifact_root / "work" / args.package_id / tree
        if not root.is_dir() or root.is_symlink():
            parser.error(f"sanitized build artifact is missing {tree}")
        for current, directories, files in os.walk(root, topdown=True, followlinks=False):
            current_path = Path(current)
            safe_dirs: list[str] = []
            for name in sorted(directories):
                candidate = current_path / name
                if stat.S_ISDIR(candidate.lstat().st_mode) and not candidate.is_symlink():
                    safe_dirs.append(name)
                else:
                    parser.error(f"non-directory entry in sanitized RPM tree: {candidate}")
            directories[:] = safe_dirs
            for filename in sorted(files):
                source = current_path / filename
                if source.is_symlink() or not stat.S_ISREG(source.lstat().st_mode):
                    parser.error(f"non-regular entry in sanitized RPM tree: {source}")
                if not RPM_FILENAME.fullmatch(filename) or filename in names:
                    parser.error(f"unsafe or duplicated RPM filename: {filename}")
                names.add(filename)
                destination = payload_dir / filename
                shutil.copyfile(source, destination, follow_symlinks=False)
                os.chmod(destination, 0o644)
                records.append(
                    {
                        "filename": filename,
                        "kind": kind,
                        "sha256": sha256_file(destination),
                        "size": destination.stat().st_size,
                    }
                )
    if not any(record["kind"] == "binary" for record in records):
        parser.error("sanitized build artifact contains no binary RPM")
    if not any(record["kind"] == "source" for record in records):
        parser.error("sanitized build artifact contains no source RPM")
    ready = {
        "schema_version": 1,
        "generation": generation,
        "package_id": args.package_id,
        "commit_sha": args.commit_sha,
        "run_id": args.run_id,
        "run_attempt": args.run_attempt,
        "artifacts": sorted(records, key=lambda item: item["filename"]),
    }
    atomic_json(output / ".ready", ready)
    atomic_json(
        output / "publish-evidence.json",
        {**ready, "kind": "rpm-repository-upload-batch", "status": "staged"},
    )
    print(generation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
