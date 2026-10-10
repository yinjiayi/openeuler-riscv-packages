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
import uuid

PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CAPABILITY = re.compile(r"^[A-Za-z0-9_+.:()/%{}~<>= -]+$")
IMAGE_REF = re.compile(r"^ghcr\.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:[a-f0-9]{64}$")
DERIVED_TAG = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")
DNF_TRANSACTION_CONTAINER_PATH = "/usr/local/libexec/openeuler-run-dnf-transaction"
DNF_TRANSACTION_BUDGET_SECONDS = 3300
DNF_ATTEMPT_TIMEOUTS_SECONDS = "2100,1100"
DNF_RETRY_DELAY_SECONDS = 10
DNF_KILL_AFTER_SECONDS = 10
BUILD_USERS = {"root", "unprivileged"}
BASELINE_ANCHORS = frozenset({"bash", "rpm", "rpm-build", "gcc", "gcc-c++", "make", "python3"})
TARGET_BUILD_USER = "rpmbuild"
TARGET_BUILD_UID = 10001
TARGET_BUILD_GID = 10001
RUNNER_MANAGED_LABEL = "io.openeuler.actions-runner.managed-builddeps"
RUNNER_MANAGED_VALUE = "v1"
RUNNER_MANAGED_NETWORK_LABEL = "io.openeuler.actions-runner.managed-builddeps-network"
RUNNER_SESSION_LABEL = "io.openeuler.actions-runner.builddeps-session"
DOCKER_ID = re.compile(r"^[a-f0-9]{64}$")
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


def root_exec(container: str, *argv: str) -> list[str]:
    """Build an explicit root-only docker exec command."""

    return ["docker", "exec", "--user", "0:0", container, *argv]


def docker_json(argv: list[str], description: str) -> dict[str, object]:
    """Return one fail-closed Docker inspection document."""

    raw = run(argv, capture=True)
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"{description} inspection is not valid JSON") from error
    if not isinstance(document, dict):
        raise SystemExit(f"{description} inspection is not an object")
    return document


def require_docker_id(value: object, description: str) -> str:
    identifier = str(value or "")
    if not DOCKER_ID.fullmatch(identifier):
        raise SystemExit(f"{description} is not a full Docker object ID")
    return identifier


def inspect_network(identifier: str) -> dict[str, object]:
    return docker_json(
        ["docker", "network", "inspect", "--format", "{{json .}}", identifier],
        "Docker network",
    )


def inspect_container(identifier: str) -> dict[str, object]:
    return docker_json(
        ["docker", "inspect", "--format", "{{json .}}", identifier],
        "dependency container",
    )


def validate_managed_network(
    document: dict[str, object],
    *,
    expected_id: str,
    expected_name: str,
    expected_internal: bool,
    expected_session: str,
    expected_containers: set[str],
) -> dict[str, object]:
    """Validate one per-run bridge and return its safe evidence projection."""

    network_id = require_docker_id(document.get("Id"), "Docker network ID")
    labels = document.get("Labels")
    containers = document.get("Containers")
    if (
        network_id != expected_id
        or document.get("Name") != expected_name
        or document.get("Driver") != "bridge"
        or document.get("Scope") != "local"
        or document.get("Internal") is not expected_internal
        or document.get("Attachable") is not False
        or document.get("Ingress") is not False
        or not isinstance(labels, dict)
        or labels.get(RUNNER_MANAGED_NETWORK_LABEL) != RUNNER_MANAGED_VALUE
        or labels.get(RUNNER_SESSION_LABEL) != expected_session
        or not isinstance(containers, dict)
        or set(containers) != expected_containers
    ):
        raise SystemExit("per-run dependency network identity or isolation is invalid")
    return {
        "id": network_id,
        "name": expected_name,
        "driver": "bridge",
        "scope": "local",
        "internal": expected_internal,
        "attachable": False,
        "ingress": False,
        "exclusive_container_count": len(expected_containers),
        "session": expected_session,
    }


def validate_container_networks(
    document: dict[str, object],
    *,
    expected_id: str,
    expected_name: str,
    expected_session: str,
    expected_networks: dict[str, str] | None,
) -> str:
    """Require the exact container identity, session, and network endpoints."""

    container_id = require_docker_id(document.get("Id"), "dependency container ID")
    config = document.get("Config")
    host_config = document.get("HostConfig")
    network_settings = document.get("NetworkSettings")
    if (
        container_id != expected_id
        or document.get("Name") != f"/{expected_name}"
        or not isinstance(config, dict)
        or not isinstance(config.get("Labels"), dict)
        or config["Labels"].get(RUNNER_MANAGED_LABEL) != RUNNER_MANAGED_VALUE
        or config["Labels"].get(RUNNER_SESSION_LABEL) != expected_session
        or not isinstance(host_config, dict)
        or not isinstance(network_settings, dict)
        or not isinstance(network_settings.get("Networks"), dict)
    ):
        raise SystemExit("dependency container identity is invalid")
    networks = network_settings["Networks"]
    if expected_networks is None:
        if host_config.get("NetworkMode") != "none" or set(networks) - {"none"}:
            raise SystemExit("networkless dependency container has an external endpoint")
        return container_id
    if set(networks) != set(expected_networks):
        raise SystemExit("dependency container has unexpected network endpoints")
    for name, network_id in expected_networks.items():
        endpoint = networks.get(name)
        if not isinstance(endpoint, dict) or endpoint.get("NetworkID") != network_id:
            raise SystemExit("dependency container network ID does not match its endpoint")
    return container_id


def recover_created_network_id(
    raw_id: str,
    *,
    expected_name: str,
    expected_internal: bool,
    expected_session: str,
) -> str:
    """Recover a successful create whose stdout was not a full network ID."""

    if DOCKER_ID.fullmatch(raw_id):
        return raw_id
    document = inspect_network(expected_name)
    recovered_id = require_docker_id(document.get("Id"), "recovered Docker network ID")
    validate_managed_network(
        document,
        expected_id=recovered_id,
        expected_name=expected_name,
        expected_internal=expected_internal,
        expected_session=expected_session,
        expected_containers=set(),
    )
    return recovered_id


def recover_created_container_id(
    raw_id: str,
    *,
    expected_name: str,
    expected_image: str,
    expected_network_mode: str,
    expected_network_name: str,
    expected_session: str,
) -> str:
    """Recover a successful create only through its exact labelled identity."""

    if DOCKER_ID.fullmatch(raw_id):
        return raw_id
    document = inspect_container(expected_name)
    recovered_id = require_docker_id(document.get("Id"), "recovered dependency container ID")
    config = document.get("Config")
    host_config = document.get("HostConfig")
    state = document.get("State")
    if (
        document.get("Name") != f"/{expected_name}"
        or not isinstance(config, dict)
        or config.get("Image") != expected_image
        or not isinstance(config.get("Labels"), dict)
        or config["Labels"].get(RUNNER_MANAGED_LABEL) != RUNNER_MANAGED_VALUE
        or config["Labels"].get(RUNNER_SESSION_LABEL) != expected_session
        or not isinstance(host_config, dict)
        or host_config.get("NetworkMode") not in {expected_network_mode, expected_network_name}
        or not isinstance(state, dict)
        or state.get("Running") is not False
    ):
        raise SystemExit("created dependency container recovery identity is invalid")
    return recovered_id


def cleanup_docker_resources(
    container_id: str,
    *,
    container_created: bool,
    started: bool,
    network_ids: list[str],
) -> list[str]:
    """Attempt exact cleanup and return the commands that did not succeed."""

    failures: list[str] = []
    commands: list[tuple[str, list[str]]] = []
    if started:
        commands.append(("container-stop", ["docker", "stop", "--time", "5", container_id]))
    if container_created:
        commands.append(("container-remove", ["docker", "rm", "--force", container_id]))
    commands.extend(
        (f"network-remove:{network_id}", ["docker", "network", "rm", network_id])
        for network_id in network_ids
    )
    for description, argv in commands:
        try:
            completed = subprocess.run(argv, check=False, text=True)
        except (OSError, subprocess.SubprocessError):
            failures.append(description)
            continue
        if completed.returncode != 0:
            failures.append(description)
    return failures


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


def rpm_manifest_from_image(base_image: str) -> list[str]:
    """Read the immutable image RPM baseline in a networkless one-shot container."""

    output = run(
        [
            "docker", "run", "--rm", "--pull", "never",
            "--platform", "linux/riscv64", "--network", "none", "--read-only",
            "--memory", "1g", "--cpus", "2", "--pids-limit", "256",
            "--security-opt", "no-new-privileges", "--user", "0:0",
            base_image,
            "rpm", "-qa", "--qf", "%{NAME}\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\t%{ARCH}\n",
        ],
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
        "network_phase": "network-absent-before-install",
        "network_install_completed": False,
        "message": (
            "The locked base image exposes a non-empty live RPM baseline."
            if valid
            else "base-image-rpm-baseline-invalid: the locked base image has an empty, "
                 "malformed, or incomplete live RPM baseline; "
                 "dependency egress and installation were refused."
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
    dnf_transaction_runner = root / "ci" / "run-dnf-transaction"
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
    if not dnf_transaction_runner.is_file() or dnf_transaction_runner.is_symlink():
        raise SystemExit("bounded DNF transaction runner must be a regular non-symlink file")
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
    transaction_path = output.parent / "dnf-transaction.json"

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

    # Prove the immutable base image's live RPM state in a separate one-shot
    # container whose network mode can remain `none` for its entire lifetime.
    # The long-lived dependency container is created only after this gate.
    before = rpm_manifest_from_image(args.base_image)
    baseline = rpm_baseline_evidence(package_id, args.base_image, before)
    write_json_atomic(baseline_path, baseline)
    if baseline["status"] != "passed":
        raise SystemExit(str(baseline["message"]))

    enabled_repositories = ["--enablerepo=openeuler-rva23"]
    if supplemental_available:
        enabled_repositories.append("--enablerepo=openeuler-riscv-project")
    planned_network_install_argv = [
        "dnf", "-y", "--setopt=install_weak_deps=False",
        "--disablerepo=*", *enabled_repositories, "install", "--", *dependencies,
    ]

    session = uuid.uuid4().hex
    container = f"openeuler-builddeps-{os.getpid()}-{session[:8]}"
    egress_network = f"openeuler-builddeps-egress-{os.getpid()}-{session[:8]}"
    container_id = ""
    container_created = False
    started = False
    live_network_ids: list[str] = []
    install_attempts = 0
    executed_install_argv: list[str] | None = None
    egress_record: dict[str, object] | None = None
    primary_error: BaseException | None = None
    try:
        if dependencies:
            egress_network_id = run([
                "docker", "network", "create", "--driver", "bridge",
                "--label", f"{RUNNER_MANAGED_NETWORK_LABEL}={RUNNER_MANAGED_VALUE}",
                "--label", f"{RUNNER_SESSION_LABEL}={session}",
                egress_network,
            ], capture=True).strip()
            egress_network_id = recover_created_network_id(
                egress_network_id,
                expected_name=egress_network,
                expected_internal=False,
                expected_session=session,
            )
            live_network_ids.append(egress_network_id)
            egress_record = validate_managed_network(
                inspect_network(egress_network_id),
                expected_id=egress_network_id,
                expected_name=egress_network,
                expected_internal=False,
                expected_session=session,
                expected_containers=set(),
            )
            dependency_network = egress_network_id
        else:
            dependency_network = "none"
        container_id = run([
            "docker", "create", "--platform", "linux/riscv64", "--name", container,
            "--label", f"{RUNNER_MANAGED_LABEL}={RUNNER_MANAGED_VALUE}",
            "--label", f"{RUNNER_SESSION_LABEL}={session}",
            "--network", dependency_network,
            "--memory", "6g", "--cpus", "2", "--pids-limit", "1024",
            "--security-opt", "no-new-privileges",
            "--mount", f"type=bind,src={supplemental_repo},dst=/etc/yum.repos.d/openeuler-riscv-project.repo,readonly",
            "--mount", f"type=bind,src={dnf_transaction_runner},dst={DNF_TRANSACTION_CONTAINER_PATH},readonly",
            "--mount", f"type=bind,src={output.parent},dst=/evidence",
            "--user", "0:0",
            args.base_image, "/bin/bash", "-c", "while :; do sleep 3600; done",
        ], capture=True).strip()
        container_id = recover_created_container_id(
            container_id,
            expected_name=container,
            expected_image=args.base_image,
            expected_network_mode=dependency_network,
            expected_network_name=egress_network if dependencies else "none",
            expected_session=session,
        )
        container_created = True
        run(["docker", "start", container_id])
        started = True
        if dependencies:
            validate_container_networks(
                inspect_container(container_id),
                expected_id=container_id,
                expected_name=container,
                expected_session=session,
                expected_networks={egress_network: egress_network_id},
            )
            egress_record = validate_managed_network(
                inspect_network(egress_network_id),
                expected_id=egress_network_id,
                expected_name=egress_network,
                expected_internal=False,
                expected_session=session,
                expected_containers={container_id},
            )
        else:
            validate_container_networks(
                inspect_container(container_id),
                expected_id=container_id,
                expected_name=container,
                expected_session=session,
                expected_networks=None,
            )
        dependency_uid = int(run(root_exec(container_id, "id", "-u"), capture=True).strip())
        dependency_gid = int(run(root_exec(container_id, "id", "-g"), capture=True).strip())
        if dependency_uid != 0 or dependency_gid != 0:
            raise SystemExit("dependency installation container is not running as root")
        baseline["session"] = session
        if dependencies:
            baseline["egress_network"] = egress_record
            baseline["network_install_started"] = True
            baseline["network_phase"] = "exclusive-egress-verified-before-install"
            write_json_atomic(baseline_path, baseline)
            run(root_exec(
                container_id,
                "python3",
                DNF_TRANSACTION_CONTAINER_PATH,
                "--evidence", "/evidence/dnf-transaction.json",
                "--budget-seconds", str(DNF_TRANSACTION_BUDGET_SECONDS),
                "--attempt-timeouts-seconds", DNF_ATTEMPT_TIMEOUTS_SECONDS,
                "--retry-delay-seconds", str(DNF_RETRY_DELAY_SECONDS),
                "--kill-after-seconds", str(DNF_KILL_AFTER_SECONDS),
                "--",
                *planned_network_install_argv,
            ))
            transaction_record = json.loads(transaction_path.read_text(encoding="utf-8"))
            if (
                transaction_record.get("kind") != "dnf-transaction"
                or transaction_record.get("status") != "passed"
                or transaction_record.get("exit_code") != 0
                or not isinstance(transaction_record.get("attempts"), list)
                or not transaction_record["attempts"]
            ):
                raise SystemExit("bounded DNF transaction evidence is invalid or incomplete")
            executed_install_argv = transaction_record.get("command")
            if not isinstance(executed_install_argv, list) or not all(
                isinstance(item, str) for item in executed_install_argv
            ):
                raise SystemExit("bounded DNF transaction command evidence is invalid")
            install_attempts = len(transaction_record["attempts"])
            run(["docker", "network", "disconnect", egress_network_id, container_id])
            validate_container_networks(
                inspect_container(container_id),
                expected_id=container_id,
                expected_name=container,
                expected_session=session,
                expected_networks={},
            )
            validate_managed_network(
                inspect_network(egress_network_id),
                expected_id=egress_network_id,
                expected_name=egress_network,
                expected_internal=False,
                expected_session=session,
                expected_containers=set(),
            )
            run(["docker", "network", "rm", egress_network_id])
            live_network_ids.remove(egress_network_id)
            egress_record["removed_after_install"] = True
            baseline["egress_network"] = egress_record
            baseline["network_install_completed"] = True
            baseline["network_phase"] = "disconnected-after-install"
            baseline["dependency_install_attempts"] = install_attempts
            write_json_atomic(baseline_path, baseline)
        else:
            baseline["network_phase"] = "network-not-required-empty-dependency-set"
            write_json_atomic(baseline_path, baseline)
        if args.build_user == "unprivileged":
            for command in build_user_provision_commands(container_id):
                run(command)
            observed_build_uid = int(
                run(root_exec(container_id, "id", "-u", TARGET_BUILD_USER), capture=True).strip()
            )
            observed_build_gid = int(
                run(root_exec(container_id, "id", "-g", TARGET_BUILD_USER), capture=True).strip()
            )
            if observed_build_uid != TARGET_BUILD_UID or observed_build_gid != TARGET_BUILD_GID:
                raise SystemExit("fixed rpmbuild identity does not match the required UID/GID")
        else:
            observed_build_uid = 0
            observed_build_gid = 0
        after = rpm_manifest(container_id)
        run(root_exec(container_id, "dnf", "clean", "all"))
        image_id = run(["docker", "commit", container_id, args.derived_tag], capture=True).strip()
    except BaseException as error:
        primary_error = error
        raise
    finally:
        cleanup_failures = cleanup_docker_resources(
            container_id,
            container_created=container_created,
            started=started,
            network_ids=list(reversed(live_network_ids)),
        )
        if cleanup_failures:
            message = "exact dependency Docker cleanup failed: " + ", ".join(cleanup_failures)
            if primary_error is None:
                raise SystemExit(message)
            print(message, file=sys.stderr, flush=True)

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
        "dependency_install_transaction": transaction_record if dependencies else None,
        "network_lifecycle": {
            "session": session,
            "phase": baseline["network_phase"],
            "egress_network": baseline.get("egress_network"),
            "network_install_started": baseline["network_install_started"],
            "network_install_completed": baseline["network_install_completed"],
        },
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
