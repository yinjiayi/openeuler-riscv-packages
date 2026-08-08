#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Enforce local, ordered, explicitly referenced package patch files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PATCH_DECLARATION = re.compile(r"^Patch(?P<number>[0-9]*):\s*(?P<name>\S+)\s*$", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    package_dir = Path(args.package_dir)
    errors: list[str] = []
    if not package_dir.is_dir() or not PACKAGE_ID.fullmatch(package_dir.name):
        errors.append("package directory or package id is invalid")

    patches_dir = package_dir / "patches"
    series_file = patches_dir / "series"
    spec_files = sorted(package_dir.glob("*.spec"))
    if len(spec_files) != 1:
        errors.append(f"expected exactly one SPEC, found {len(spec_files)}")

    listed: list[str] = []
    if not series_file.is_file():
        errors.append("patches/series is required, even when empty")
    else:
        for line_number, raw in enumerate(series_file.read_text(encoding="utf-8").splitlines(), 1):
            entry = raw.strip()
            if not entry or entry.startswith("#"):
                continue
            path = PurePosixPath(entry)
            if len(path.parts) != 1 or path.name != entry or not entry.endswith(".patch"):
                errors.append(f"series line {line_number} is not a local .patch basename")
                continue
            if entry in listed:
                errors.append(f"series contains duplicate patch {entry}")
            listed.append(entry)
            target = patches_dir / entry
            if not target.is_file() or target.is_symlink():
                errors.append(f"series patch is missing or a symlink: {entry}")

    present = sorted(path.name for path in patches_dir.glob("*.patch") if path.is_file()) if patches_dir.is_dir() else []
    for patch in present:
        if patch not in listed:
            errors.append(f"patch is not listed in patches/series: {patch}")

    declarations: dict[str, str] = {}
    spec_text = ""
    if len(spec_files) == 1:
        spec_text = spec_files[0].read_text(encoding="utf-8")
        for match in PATCH_DECLARATION.finditer(spec_text):
            name = PurePosixPath(match.group("name")).name
            declarations[name] = match.group("number") or "0"
        for patch in listed:
            if patch not in declarations:
                errors.append(f"SPEC does not declare patch: {patch}")
        autosetup = re.search(r"(?m)^%autosetup\b([^\n]*)$", spec_text)
        autosetup_applies = bool(autosetup and not re.search(r"(?:^|\s)-N(?:\s|$)", autosetup.group(1)))
        if listed and "%autopatch" not in spec_text and not re.search(r"(?m)^%patch(?:\s|[0-9])", spec_text) and not autosetup_applies:
            errors.append("SPEC declares patches but does not apply them with %autosetup, %autopatch, or %patch")

    result = {
        "schema_version": 1,
        "package_id": package_dir.name,
        "status": "passed" if not errors else "failed",
        "series": listed,
        "patch_count": len(listed),
        "errors": errors,
    }
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    for error in errors:
        print(f"patch policy: {error}", file=sys.stderr)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
