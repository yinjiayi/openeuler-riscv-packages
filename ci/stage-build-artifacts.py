#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stage a build artifact from regular evidence files and RPMs only."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import stat
from typing import Iterator


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVIDENCE_SUFFIXES = {".json", ".log"}
RPM_TREES = ("RPMS", "SRPMS")


def regular_entries(
    root: pathlib.Path,
    excluded: list[dict[str, str]],
    errors: list[dict[str, str]],
) -> Iterator[pathlib.Path]:
    """Yield regular entries without following directory symlinks."""

    def record_walk_error(error: OSError) -> None:
        errors.append(
            {
                "path": str(error.filename or root),
                "reason": "unreadable-directory",
                "message": str(error),
            }
        )

    for current, directories, files in os.walk(
        root, topdown=True, followlinks=False, onerror=record_walk_error
    ):
        current_path = pathlib.Path(current)
        safe_directories: list[str] = []
        for name in sorted(directories):
            candidate = current_path / name
            try:
                mode = candidate.lstat().st_mode
            except OSError as error:
                errors.append(
                    {"path": str(candidate), "reason": "unreadable-entry", "message": str(error)}
                )
                continue
            if stat.S_ISDIR(mode):
                safe_directories.append(name)
            else:
                excluded.append({"path": str(candidate), "reason": "non-directory-tree-entry"})
        directories[:] = safe_directories
        for name in sorted(files):
            candidate = current_path / name
            try:
                mode = candidate.lstat().st_mode
            except OSError as error:
                errors.append(
                    {"path": str(candidate), "reason": "unreadable-entry", "message": str(error)}
                )
                continue
            if not stat.S_ISREG(mode):
                excluded.append({"path": str(candidate), "reason": "non-regular-file"})
                continue
            yield candidate


def reset_output(output: pathlib.Path, sources: tuple[pathlib.Path, ...]) -> None:
    if output.is_symlink():
        output.unlink()
    resolved_output = output.resolve()
    if resolved_output == pathlib.Path(resolved_output.anchor):
        raise ValueError("refusing to stage into a filesystem root")
    for source in sources:
        source = source.resolve()
        if resolved_output == source or source in resolved_output.parents:
            raise ValueError("output directory must be outside every input tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)


def copy_regular(source: pathlib.Path, destination: pathlib.Path, errors: list[dict[str, str]]) -> bool:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination, follow_symlinks=False)
    except OSError as error:
        errors.append({"path": str(source), "reason": "copy-failed", "message": str(error)})
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    if args.package_id and not PACKAGE_ID.fullmatch(args.package_id):
        parser.error("package id is not canonical")

    artifact_dir = pathlib.Path(args.artifact_dir).resolve()
    work_dir = pathlib.Path(args.work_dir).resolve()
    output_dir = pathlib.Path(args.output_dir).absolute()
    reset_output(output_dir, (artifact_dir, work_dir))

    included: list[str] = []
    excluded: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []

    if artifact_dir.is_dir():
        for source in regular_entries(artifact_dir, excluded, errors):
            relative = source.relative_to(artifact_dir)
            if relative.as_posix() == "archive-manifest.json":
                excluded.append({"path": str(source), "reason": "reserved-output-name"})
                continue
            if source.suffix not in EVIDENCE_SUFFIXES:
                excluded.append({"path": str(source), "reason": "not-structured-evidence-or-log"})
                continue
            destination = output_dir / "artifacts" / "build" / relative
            if copy_regular(source, destination, errors):
                included.append(destination.relative_to(output_dir).as_posix())
    else:
        excluded.append({"path": str(artifact_dir), "reason": "missing-artifact-directory"})

    if args.package_id:
        for tree in RPM_TREES:
            source_root = work_dir / tree
            if not source_root.is_dir():
                continue
            for source in regular_entries(source_root, excluded, errors):
                if source.suffix != ".rpm":
                    excluded.append({"path": str(source), "reason": "not-an-rpm"})
                    continue
                relative = source.relative_to(source_root)
                destination = output_dir / "work" / args.package_id / tree / relative
                if copy_regular(source, destination, errors):
                    included.append(destination.relative_to(output_dir).as_posix())

    manifest = {
        "schema_version": 1,
        "kind": "package-ci-build-artifact-manifest",
        "package_id": args.package_id or None,
        "status": "failed" if errors else "passed",
        "policy": "regular .json/.log evidence and regular .rpm products only",
        "included_files": sorted(included),
        "excluded_entries": sorted(excluded, key=lambda entry: (entry["path"], entry["reason"])),
        "errors": errors,
    }
    manifest_path = output_dir / "artifacts" / "build" / "archive-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
