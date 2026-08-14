#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""List active QEMU-buildable packages for repository backfill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages-dir", default="packages")
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()
    packages: list[str] = []
    skipped: list[dict[str, str]] = []
    for directory in sorted(Path(args.packages_dir).iterdir(), key=lambda path: path.name):
        if not directory.is_dir() or not PACKAGE_ID.fullmatch(directory.name):
            continue
        metadata_path = directory / "package.yaml"
        if not metadata_path.is_file():
            continue
        value = json.loads(metadata_path.read_text(encoding="utf-8"))
        reason = ""
        if directory.name.startswith("golden-"):
            reason = "fixed evaluation fixture, not a public package"
        elif value.get("maintenance", {}).get("status") == "retired":
            reason = "retired"
        elif value.get("build", {}).get("profile") == "needs-native-riscv":
            reason = "requires unavailable native RISC-V validation"
        if reason:
            skipped.append({"package_id": directory.name, "reason": reason})
        else:
            packages.append(directory.name)
    if not packages:
        raise SystemExit("no active QEMU-buildable packages were found")
    if len(packages) > 256:
        raise SystemExit("package count exceeds the GitHub Actions matrix limit")
    document = {
        "schema_version": 1,
        "kind": "rpm-repository-backfill-plan",
        "packages": packages,
        "package_count": len(packages),
        "skipped": skipped,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as stream:
            stream.write("packages=" + json.dumps(packages, separators=(",", ":")) + "\n")
    print(f"selected {len(packages)} packages; skipped {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
