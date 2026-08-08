#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create an unshared, per-run OCI image containing audited BuildRequires."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys
import uuid

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CAPABILITY = re.compile(r"^[A-Za-z0-9_+.:()/%{}~<>= -]+$")
IMAGE_REF = re.compile(r"^ghcr\.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:[a-f0-9]{64}$")
DERIVED_TAG = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")


def run(argv: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(
        argv,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return completed.stdout if capture else ""


def rpm_manifest(container: str) -> list[str]:
    output = run(
        [
            "docker", "exec", container, "rpm", "-qa",
            "--qf", "%{NAME}\\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\\t%{ARCH}\\n",
        ],
        capture=True,
    )
    return sorted(line for line in output.splitlines() if line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-image", required=True)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--derived-tag", required=True)
    args = parser.parse_args()

    root = pathlib.Path.cwd().resolve()
    package_dir = pathlib.Path(args.package_dir).resolve()
    work_dir = pathlib.Path(args.work_dir).resolve()
    output = pathlib.Path(args.output).resolve()
    package_id = package_dir.name
    if not PACKAGE_ID.fullmatch(package_id) or package_dir.parent != root / "packages":
        raise SystemExit("package directory is outside packages/ or has a noncanonical id")
    if not IMAGE_REF.fullmatch(args.base_image):
        raise SystemExit("base image must be the approved GHCR repository at an immutable digest")
    if not DERIVED_TAG.fullmatch(args.derived_tag):
        raise SystemExit("derived image tag is unsafe")
    work_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    plan_path = output.parent / "dependency-plan.json"

    # Planning runs with no network. Only the package, trusted shared scripts,
    # and dedicated output/work directories are mounted.
    run(
        [
            "docker", "run", "--rm", "--platform", "linux/riscv64", "--network", "none",
            "--memory", "2g", "--cpus", "2", "--pids-limit", "512",
            "--security-opt", "no-new-privileges",
            "-v", f"{root}:/workspace:ro",
            "-v", f"{work_dir}:/workspace/work/{package_id}:rw",
            "-v", f"{output.parent}:/workspace/artifacts/dependencies:rw",
            "-w", "/workspace",
            args.base_image,
            "scripts/build-rpm", "--package-dir", f"packages/{package_id}",
            "--repo-root", "/workspace",
            "--work-dir", f"work/{package_id}",
            "--result", f"artifacts/dependencies/{plan_path.name}",
            "--plan", "--offline", "--expected-arch", "riscv64",
        ]
    )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    dependencies = plan.get("dependency_plan", {}).get("build_requires")
    planned_argv = plan.get("dependency_plan", {}).get("install_argv")
    if not isinstance(dependencies, list):
        raise SystemExit("dependency plan did not contain dependency_plan.build_requires")
    for dependency in dependencies:
        if (
            not isinstance(dependency, str)
            or not dependency
            or dependency.startswith("-")
            or "\n" in dependency
            or not CAPABILITY.fullmatch(dependency)
        ):
            raise SystemExit(f"unsafe BuildRequires capability: {dependency!r}")
    expected_argv = ["dnf", "-y", "--setopt=install_weak_deps=False", "install", "--"] + dependencies
    if planned_argv != expected_argv:
        raise SystemExit("dependency plan install_argv does not match the reviewed DNF contract")

    container = f"openeuler-builddeps-{os.getpid()}-{uuid.uuid4().hex[:8]}"
    started = False
    try:
        run([
            "docker", "create", "--platform", "linux/riscv64", "--name", container,
            "--memory", "6g", "--cpus", "2", "--pids-limit", "1024",
            "--security-opt", "no-new-privileges",
            args.base_image, "/bin/bash", "-c", "while :; do sleep 3600; done",
        ])
        run(["docker", "start", container])
        started = True
        before = rpm_manifest(container)
        if dependencies:
            run([
                "docker", "exec", container, "dnf", "-y",
                "--setopt=install_weak_deps=False", "--disablerepo=*",
                "--enablerepo=openeuler-rva23", "install", "--", *dependencies,
            ])
        after = rpm_manifest(container)
        run(["docker", "exec", container, "dnf", "clean", "all"])
        image_id = run(["docker", "commit", container, args.derived_tag], capture=True).strip()
    finally:
        if started:
            subprocess.run(["docker", "stop", "--time", "5", container], check=False)
        subprocess.run(["docker", "rm", "--force", container], check=False)

    before_set = set(before)
    added = [entry for entry in after if entry not in before_set]
    payload = {
        "schema_version": 1,
        "package_id": package_id,
        "base_image": args.base_image,
        "derived_image_id": image_id,
        "derived_tag": args.derived_tag,
        "repository": "https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/",
        "build_requires": dependencies,
        "planned_install_argv": planned_argv,
        "executed_install_argv": [
            "dnf", "-y", "--setopt=install_weak_deps=False", "--disablerepo=*",
            "--enablerepo=openeuler-rva23", "install", "--", *dependencies,
        ],
        "rpm_manifest_before": before,
        "rpm_manifest_after": after,
        "rpm_delta_added": added,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "ephemeral": True,
        "published": False,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.derived_tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
