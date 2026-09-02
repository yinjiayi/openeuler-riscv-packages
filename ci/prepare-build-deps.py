#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create an unshared, per-run OCI image containing audited BuildRequires."""

from __future__ import annotations

import argparse
import configparser
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import uuid

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CAPABILITY = re.compile(r"^[A-Za-z0-9_+.:()/%{}~<>= -]+$")
IMAGE_REF = re.compile(r"^ghcr\.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:[a-f0-9]{64}$")
DERIVED_TAG = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")
DNF_NETWORK_OPTIONS = [
    "--setopt=retries=20",
    "--setopt=timeout=60",
    "--setopt=minrate=1",
    "--setopt=max_parallel_downloads=1",
]
BUILD_USERS = {"root", "unprivileged"}
BASELINE_ANCHORS = frozenset({"bash", "rpm", "rpm-build", "gcc", "gcc-c++", "make", "python3"})
TARGET_BUILD_USER = "rpmbuild"
TARGET_BUILD_UID = 10001
TARGET_BUILD_GID = 10001
RUNNER_MANAGED_LABEL = "io.openeuler.actions-runner.managed-builddeps"
RUNNER_MANAGED_VALUE = "v1"
SUPPLEMENTAL_STATE_URL = "http://2.27.148.101:38080/state.json"
SUPPLEMENTAL_REPO_KEYS = {
    "name",
    "baseurl",
    "enabled",
    "gpgcheck",
    "repo_gpgcheck",
    "metadata_expire",
    "skip_if_unavailable",
    "module_hotfixes",
}


def run(argv: list[str], *, capture: bool = False) -> str:
    completed = subprocess.run(
        argv,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return completed.stdout if capture else ""


def run_with_retries(
    argv: list[str],
    *,
    attempts: int = 3,
    delays: tuple[int, ...] = (5, 15),
) -> int:
    """Run a networked dependency transaction with bounded cache-preserving retries."""
    if attempts < 1 or not delays or any(delay < 0 for delay in delays):
        raise ValueError("retry policy is invalid")
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(1, attempts + 1):
        print(f"dependency install attempt {attempt}/{attempts}", flush=True)
        last = subprocess.run(argv, check=False, text=True)
        if last.returncode == 0:
            return attempt
        if attempt < attempts:
            delay = delays[min(attempt - 1, len(delays) - 1)]
            print(
                f"dependency install attempt {attempt} failed with exit {last.returncode}; "
                f"retrying after {delay}s with the same DNF cache",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(delay)
    assert last is not None
    raise subprocess.CalledProcessError(last.returncode, argv)


def root_exec(container: str, *argv: str) -> list[str]:
    """Build an explicit root-only docker exec command."""

    return ["docker", "exec", "--user", "0:0", container, *argv]


def build_user_provision_commands(container: str) -> list[list[str]]:
    """Return the fail-closed commands that create the fixed build identity."""

    return [
        root_exec(
            container,
            "groupadd",
            "--gid",
            str(TARGET_BUILD_GID),
            TARGET_BUILD_USER,
        ),
        root_exec(
            container,
            "useradd",
            "--uid",
            str(TARGET_BUILD_UID),
            "--gid",
            str(TARGET_BUILD_GID),
            "--create-home",
            "--home-dir",
            "/var/lib/rpmbuild",
            "--shell",
            "/sbin/nologin",
            TARGET_BUILD_USER,
        ),
    ]


def rpm_manifest(container: str) -> list[str]:
    output = run(
        root_exec(
            container,
            "rpm",
            "-qa",
            "--qf", "%{NAME}\\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\\t%{ARCH}\\n",
        ),
        capture=True,
    )
    return sorted(line for line in output.splitlines() if line)


def rpm_baseline_evidence(
    package_id: str,
    base_image: str,
    manifest: list[str],
) -> dict[str, object]:
    malformed = [entry for entry in manifest if entry.count("\t") != 2]
    names = {
        entry.split("\t", 1)[0]
        for entry in manifest
        if entry.count("\t") == 2 and entry.split("\t", 1)[0]
    }
    missing = sorted(BASELINE_ANCHORS - names)
    valid = bool(manifest) and not malformed and not missing
    manifest_bytes = (("\n".join(manifest) + "\n") if manifest else "").encode("utf-8")
    return {
        "schema_version": 1,
        "kind": "dependency-rpm-baseline",
        "package_id": package_id,
        "phase": "dependency-prepare",
        "status": "passed" if valid else "failed",
        "classification": "none" if valid else "failure:infrastructure",
        "reason": "validated-live-rpm-baseline" if valid else "base-image-rpm-baseline-invalid",
        "base_image": base_image,
        "rpm_manifest_before_count": len(manifest),
        "rpm_manifest_before_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "required_anchors": sorted(BASELINE_ANCHORS),
        "missing_anchors": missing,
        "malformed_entry_count": len(malformed),
        "network_install_started": False,
        "network_phase": "disconnected-before-install",
        "message": (
            "The locked base image exposes a non-empty live RPM baseline."
            if valid
            else "base-image-rpm-baseline-invalid: the locked base image has an empty, "
                 "malformed, or incomplete live RPM baseline; "
                 "dependency networking and installation were refused."
        ),
    }


def write_json_atomic(path: pathlib.Path, payload: dict[str, object]) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def validate_supplemental_repository(
    evidence: dict[str, object], repository_text: str
) -> tuple[bool, dict[str, object]]:
    if evidence.get("kind") != "supplemental-repository-resolution":
        raise ValueError("supplemental repository evidence has the wrong kind")
    if evidence.get("state_url") != SUPPLEMENTAL_STATE_URL:
        raise ValueError("supplemental repository evidence has the wrong state URL")

    parser = configparser.ConfigParser(interpolation=None, strict=True)
    try:
        parser.read_string(repository_text)
    except configparser.Error as error:
        raise ValueError("supplemental repository file is not valid INI") from error
    if parser.sections() != ["openeuler-riscv-project"]:
        raise ValueError("supplemental repository file has unexpected sections")
    repository = parser["openeuler-riscv-project"]
    if set(repository) != SUPPLEMENTAL_REPO_KEYS:
        raise ValueError("supplemental repository file has unexpected settings")
    if (
        repository.get("gpgcheck") != "0"
        or repository.get("repo_gpgcheck") != "0"
        or repository.get("metadata_expire") != "never"
        or repository.get("module_hotfixes") != "1"
    ):
        raise ValueError("supplemental repository file changed its fixed RPM trust policy")

    status = evidence.get("status", "passed")
    if status == "passed":
        generation = str(evidence.get("generation", ""))
        state_sha = str(evidence.get("state_sha256", ""))
        repositories = evidence.get("repositories")
        if (
            not re.fullmatch(
                r"(?:bootstrap-[0-9]{8}T[0-9]{6}Z|[a-z0-9-]+-[0-9a-f]{40}-[1-9][0-9]*-[1-9][0-9]*)",
                generation,
            )
            or not re.fullmatch(r"[0-9a-f]{64}", state_sha)
            or not isinstance(repositories, dict)
        ):
            raise ValueError("verified supplemental repository evidence is invalid")
        binary = repositories.get("riscv64")
        if not isinstance(binary, dict):
            raise ValueError("verified supplemental repository evidence lacks riscv64 metadata")
        expected_baseurl = binary.get("baseurl")
        repomd_sha = binary.get("repomd_sha256")
        if (
            not isinstance(expected_baseurl, str)
            or not re.fullmatch(r"[0-9a-f]{64}", str(repomd_sha or ""))
            or repository.get("baseurl") != expected_baseurl
            or repository.get("enabled") != "1"
            or repository.get("skip_if_unavailable") != "0"
        ):
            raise ValueError("supplemental repository file does not match verified evidence")
        return True, {
            "status": "passed",
            "state_url": evidence["state_url"],
            "state_sha256": state_sha,
            "generation": generation,
            "baseurl": expected_baseurl,
            "repomd_sha256": repomd_sha,
            "rpm_gpgcheck": False,
        }

    fallback = evidence.get("fallback")
    if (
        status != "unavailable"
        or evidence.get("reason") != "endpoint-unavailable"
        or evidence.get("generation") is not None
        or evidence.get("state_sha256") is not None
        or evidence.get("repositories") != {}
        or fallback
        != {
            "active_repository_ids": ["openeuler-rva23"],
            "supplemental_repository_enabled": False,
        }
        or repository.get("baseurl") != "http://2.27.148.101:38080/"
        or repository.get("enabled") != "0"
        or repository.get("skip_if_unavailable") != "1"
    ):
        raise ValueError("unavailable supplemental repository fallback is invalid")
    return False, {
        "status": "unavailable",
        "state_url": evidence["state_url"],
        "enabled": False,
        "reason": "endpoint-unavailable",
        "fallback_repository_ids": ["openeuler-rva23"],
        "rpm_gpgcheck": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-image", required=True)
    parser.add_argument("--package-dir", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--derived-tag", required=True)
    parser.add_argument("--supplemental-repo-file", required=True)
    parser.add_argument("--supplemental-evidence", required=True)
    parser.add_argument("--build-user", required=True, choices=sorted(BUILD_USERS))
    args = parser.parse_args()

    root = pathlib.Path.cwd().resolve()
    package_dir = pathlib.Path(args.package_dir).resolve()
    work_dir = pathlib.Path(args.work_dir).resolve()
    output = pathlib.Path(args.output).resolve()
    supplemental_repo = pathlib.Path(args.supplemental_repo_file).resolve()
    supplemental_evidence_path = pathlib.Path(args.supplemental_evidence).resolve()
    package_id = package_dir.name
    if not PACKAGE_ID.fullmatch(package_id) or package_dir.parent != root / "packages":
        raise SystemExit("package directory is outside packages/ or has a noncanonical id")
    if not IMAGE_REF.fullmatch(args.base_image):
        raise SystemExit("base image must be the approved GHCR repository at an immutable digest")
    if not DERIVED_TAG.fullmatch(args.derived_tag):
        raise SystemExit("derived image tag is unsafe")
    if not supplemental_repo.is_file() or supplemental_repo.is_symlink():
        raise SystemExit("supplemental repository file must be a regular non-symlink file")
    if not supplemental_evidence_path.is_file() or supplemental_evidence_path.is_symlink():
        raise SystemExit("supplemental repository evidence must be a regular non-symlink file")
    supplemental_evidence = json.loads(supplemental_evidence_path.read_text(encoding="utf-8"))
    repository_text = supplemental_repo.read_text(encoding="utf-8")
    try:
        supplemental_available, supplemental_record = validate_supplemental_repository(
            supplemental_evidence, repository_text
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error
    work_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    plan_path = output.parent / "dependency-plan.json"
    baseline_path = output.parent / "rpm-baseline.json"

    # Planning runs with no network. Only the package, trusted shared scripts,
    # and dedicated output/work directories are mounted.  The evidence mount
    # deliberately lives outside /workspace: that tree is a read-only bind,
    # so Docker cannot create a previously absent nested mountpoint below it.
    run(
        [
            "docker", "run", "--rm", "--platform", "linux/riscv64", "--network", "none",
            "--memory", "2g", "--cpus", "2", "--pids-limit", "512",
            "--security-opt", "no-new-privileges",
            "--user", "0:0",
            "-v", f"{root}:/workspace:ro",
            "-v", f"{work_dir}:/workspace/work/{package_id}:rw",
            "-v", f"{output.parent}:/evidence:rw",
            "-w", "/workspace",
            args.base_image,
            "scripts/build-rpm", "--package-dir", f"packages/{package_id}",
            "--repo-root", "/workspace",
            "--work-dir", f"work/{package_id}",
            "--result", f"/evidence/{plan_path.name}",
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
    install_attempts = 0
    try:
        run([
            "docker", "create", "--platform", "linux/riscv64", "--name", container,
            "--label", f"{RUNNER_MANAGED_LABEL}={RUNNER_MANAGED_VALUE}",
            "--network", "none",
            "--memory", "6g", "--cpus", "2", "--pids-limit", "1024",
            "--security-opt", "no-new-privileges",
            "--mount", f"type=bind,src={supplemental_repo},dst=/etc/yum.repos.d/openeuler-riscv-project.repo,readonly",
            "--user", "0:0",
            args.base_image, "/bin/bash", "-c", "while :; do sleep 3600; done",
        ])
        run(["docker", "start", container])
        started = True
        dependency_uid = int(run(root_exec(container, "id", "-u"), capture=True).strip())
        dependency_gid = int(run(root_exec(container, "id", "-g"), capture=True).strip())
        if dependency_uid != 0 or dependency_gid != 0:
            raise SystemExit("dependency installation container is not running as root")
        before = rpm_manifest(container)
        baseline = rpm_baseline_evidence(package_id, args.base_image, before)
        write_json_atomic(baseline_path, baseline)
        if baseline["status"] != "passed":
            raise SystemExit(str(baseline["message"]))
        # The container is created without a network.  Only a validated live
        # RPM baseline permits connection to the fixed bridge and the audited
        # DNF transaction below.
        run(["docker", "network", "connect", "bridge", container])
        baseline["network_install_started"] = True
        baseline["network_phase"] = "connected-before-install"
        write_json_atomic(baseline_path, baseline)
        enabled_repositories = ["--enablerepo=openeuler-rva23"]
        if supplemental_available:
            enabled_repositories.append("--enablerepo=openeuler-riscv-project")
        executed_install_argv = [
            "dnf", "-y", "--setopt=install_weak_deps=False", *DNF_NETWORK_OPTIONS,
            "--disablerepo=*", *enabled_repositories, "install", "--", *dependencies,
        ]
        if dependencies:
            install_attempts = run_with_retries(root_exec(container, *executed_install_argv))
        if args.build_user == "unprivileged":
            for command in build_user_provision_commands(container):
                run(command)
            observed_build_uid = int(
                run(root_exec(container, "id", "-u", TARGET_BUILD_USER), capture=True).strip()
            )
            observed_build_gid = int(
                run(root_exec(container, "id", "-g", TARGET_BUILD_USER), capture=True).strip()
            )
            if observed_build_uid != TARGET_BUILD_UID or observed_build_gid != TARGET_BUILD_GID:
                raise SystemExit("fixed rpmbuild identity does not match the required UID/GID")
        else:
            observed_build_uid = 0
            observed_build_gid = 0
        after = rpm_manifest(container)
        run(root_exec(container, "dnf", "clean", "all"))
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
        "supplemental_repository": supplemental_record,
        "build_requires": dependencies,
        "planned_install_argv": planned_argv,
        "executed_install_argv": executed_install_argv,
        "dependency_install_attempts": install_attempts,
        "rpm_manifest_before": before,
        "rpm_manifest_after": after,
        "rpm_delta_added": added,
        "dependency_install_identity": {
            "uid": dependency_uid,
            "gid": dependency_gid,
            "is_root": True,
        },
        "target_build_identity": {
            "policy": args.build_user,
            "user": TARGET_BUILD_USER if args.build_user == "unprivileged" else "root",
            "uid": observed_build_uid,
            "gid": observed_build_gid,
            "is_root": args.build_user == "root",
        },
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "ephemeral": True,
        "published": False,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.derived_tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
