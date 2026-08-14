#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read the schema-validated package build policy without a YAML dependency."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()
    package_dir = Path(args.package_dir)
    package = json.loads((package_dir / "package.yaml").read_text(encoding="utf-8"))
    package_id = package.get("package_id", "")
    if package_id != package_dir.name or not PACKAGE_ID.fullmatch(package_id):
        raise SystemExit("package id does not match the canonical directory name")
    build = package.get("build", {})
    profile = build.get("profile")
    if profile not in {"qemu-user", "needs-native-riscv"}:
        raise SystemExit("unknown build.profile")
    build_user = build.get("user", "root")
    if build_user not in {"root", "unprivileged"}:
        raise SystemExit("unknown build.user")
    timeout = build.get("timeout_minutes")
    if not isinstance(timeout, int) or not 5 <= timeout <= 360:
        raise SystemExit("invalid build.timeout_minutes")
    result = {
        "schema_version": 1,
        "package_id": package_id,
        "build_profile": profile,
        "build_user": build_user,
        "needs_native": profile == "needs-native-riscv",
        "native_reason": build.get("native_reason"),
        "timeout_minutes": timeout,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as handle:
            handle.write(f"needs_native={'true' if result['needs_native'] else 'false'}\n")
            handle.write(f"timeout_minutes={timeout}\n")
            handle.write(f"build_user={build_user}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
