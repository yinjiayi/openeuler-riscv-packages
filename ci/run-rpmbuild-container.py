#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run network-enabled rpmbuild under a fail-closed per-package user policy.

``root`` preserves the historical build identity for packages whose complete
upstream checks require root capabilities. ``unprivileged`` first hands the
fresh generated work tree to the fixed ``rpmbuild`` identity and then runs all
RPM phases, including ``%check``, as that identity. Dependency installation is
always a separate root-only operation in ``prepare-build-deps.py``.
"""

from __future__ import annotations

import argparse
import grp
import json
import os
import pathlib
import pwd
import re
import shutil
import stat
import subprocess
import sys
from typing import Optional, Sequence


PACKAGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
DERIVED_IMAGE = re.compile(
    r"^openeuler-builddeps:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$"
)
BUILD_USERS = {"root", "unprivileged"}
POSITIVE_SECONDS = re.compile(r"^[1-9][0-9]*$")
TARGET_USER = "rpmbuild"
TARGET_UID = 10001
TARGET_GID = 10001
EVIDENCE_FILES = (
    "ownership-handoff.json",
    "build-identity.json",
    "rpmbuild-phase-result.json",
)


class ContractError(RuntimeError):
    """A build-identity or path contract was not satisfied."""


def positive_seconds(value: str) -> int:
    """Parse a canonical positive decimal timeout without accepting signs."""
    if not POSITIVE_SECONDS.fullmatch(value):
        raise argparse.ArgumentTypeError("timeout seconds must be a positive decimal integer")
    return int(value)


def write_json(path: pathlib.Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def require_regular_directory(path: pathlib.Path, label: str) -> pathlib.Path:
    if path.is_symlink():
        raise ContractError(f"{label} must not be a symlink: {path}")
    path.mkdir(parents=True, exist_ok=True)
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise ContractError(f"{label} is not a directory: {path}")
    return path


def require_exact_child(path: pathlib.Path, parent: pathlib.Path, label: str) -> pathlib.Path:
    resolved = path.resolve()
    expected_parent = parent.resolve()
    try:
        resolved.relative_to(expected_parent)
    except ValueError as error:
        raise ContractError(f"{label} must remain below {expected_parent}: {resolved}") from error
    if resolved == expected_parent:
        raise ContractError(f"{label} must not equal its parent: {resolved}")
    return resolved


def docker_limits(*, network: str) -> list[str]:
    if network not in {"bridge", "none"}:
        raise ContractError(f"unsupported build container network: {network}")
    return [
        "--platform",
        "linux/riscv64",
        "--network",
        network,
        "--memory",
        "6g",
        "--cpus",
        "2",
        "--pids-limit",
        "1024",
        "--security-opt",
        "no-new-privileges",
    ]


def common_mounts(
    repo_root: pathlib.Path,
    work_dir: pathlib.Path,
    package_id: str,
) -> list[str]:
    return [
        "-v",
        f"{repo_root}:/workspace:ro",
        "-v",
        f"{work_dir}:/workspace/work/{package_id}:rw",
        "-w",
        "/workspace",
    ]


def require_real_directory(path: pathlib.Path, label: str) -> pathlib.Path:
    """Reject symlinked paths before changing their host-side permissions."""

    if path.is_symlink() or not path.is_dir():
        raise ContractError(f"{label} must be a regular directory: {path}")
    return path


def grant_other_access(path: pathlib.Path, *, readable: bool) -> None:
    """Set the exact other-mode bits needed for container or host readback."""

    mode = path.lstat().st_mode
    if stat.S_ISDIR(mode):
        other_mode = stat.S_IXOTH | (stat.S_IROTH if readable else 0)
    elif stat.S_ISREG(mode):
        other_mode = stat.S_IROTH
        if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            other_mode |= stat.S_IXOTH
    else:
        raise ContractError(f"workspace input is not a regular file or directory: {path}")
    os.chmod(path, (stat.S_IMODE(mode) & ~0o007) | other_mode)


def grant_root_workspace_traversal(repo_root: pathlib.Path) -> None:
    """Let root-build test identities traverse only the fixed mount parents."""

    repository = require_real_directory(repo_root, "repository root")
    work_parent = require_real_directory(repo_root / "work", "work parent directory")
    grant_other_access(repository, readable=False)
    grant_other_access(work_parent, readable=False)


def workspace_tree_entries(root: pathlib.Path) -> list[pathlib.Path]:
    """List a regular input tree without ever following a checkout symlink."""

    def walk_error(error: OSError) -> None:
        raise ContractError(f"unable to inspect workspace input: {error.filename}") from error

    entries: list[pathlib.Path] = []
    for current, directories, files in os.walk(
        root, topdown=True, followlinks=False, onerror=walk_error
    ):
        current_path = pathlib.Path(current)
        current_mode = current_path.lstat().st_mode
        if not stat.S_ISDIR(current_mode) or stat.S_ISLNK(current_mode):
            raise ContractError(f"workspace input must not be a symlink: {current_path}")
        entries.append(current_path)
        directories.sort()
        for name in directories:
            candidate = current_path / name
            mode = candidate.lstat().st_mode
            if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
                raise ContractError(f"workspace input must not be a symlink: {candidate}")
        for name in sorted(files):
            candidate = current_path / name
            mode = candidate.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ContractError(f"workspace input must not be a symlink: {candidate}")
            if not stat.S_ISREG(mode):
                raise ContractError(
                    f"workspace input is not a regular file or directory: {candidate}"
                )
            entries.append(candidate)
    return entries


def grant_unprivileged_workspace_access(
    repo_root: pathlib.Path, package_id: str
) -> None:
    """Expose only build inputs, never runner state or unrelated package trees."""

    packages_dir = require_real_directory(repo_root / "packages", "packages directory")
    work_parent = require_real_directory(repo_root / "work", "work parent directory")
    input_trees = (
        require_real_directory(repo_root / "ci", "CI scripts directory"),
        require_real_directory(repo_root / "scripts", "repository scripts directory"),
        require_real_directory(
            packages_dir / package_id, "selected package directory"
        ),
    )
    require_real_directory(repo_root, "repository root")

    # Validate every permitted tree before changing a single host-side mode.
    accessible_entries = [
        entry for root in input_trees for entry in workspace_tree_entries(root)
    ]

    # The container needs to address these known children but must not list the
    # repository root or the complete package inventory.
    grant_other_access(repo_root, readable=False)
    grant_other_access(packages_dir, readable=False)
    grant_other_access(work_parent, readable=False)
    for entry in accessible_entries:
        grant_other_access(entry, readable=True)


def unprivileged_prepare_command(
    image: str,
    repo_root: pathlib.Path,
    work_dir: pathlib.Path,
    package_id: str,
) -> list[str]:
    container_work = f"/workspace/work/{package_id}"
    return [
        "docker",
        "run",
        "--rm",
        *docker_limits(network="none"),
        "--user",
        "0:0",
        *common_mounts(repo_root, work_dir, package_id),
        image,
        "ci/run-rpmbuild-container.py",
        "prepare",
        "--work-dir",
        container_work,
        "--result-dir",
        f"{container_work}/.ci-result",
    ]


def build_command(
    image: str,
    repo_root: pathlib.Path,
    work_dir: pathlib.Path,
    artifact_dir: pathlib.Path,
    package_id: str,
    commit_sha: str,
    build_user: str,
    build_timeout_seconds: int,
) -> list[str]:
    if build_user not in BUILD_USERS:
        raise ContractError(f"unsupported build user policy: {build_user}")
    if (
        isinstance(build_timeout_seconds, bool)
        or not isinstance(build_timeout_seconds, int)
        or build_timeout_seconds < 1
    ):
        raise ContractError("build timeout seconds must be a positive integer")
    container_work = f"/workspace/work/{package_id}"
    if build_user == "root":
        run_uid_gid = "0:0"
        result_dir = "/evidence"
        extra_mounts = ["-v", f"{artifact_dir}:/evidence:rw"]
        user_environment = ["-e", "HOME=/root", "-e", "USER=root", "-e", "LOGNAME=root"]
    else:
        run_uid_gid = f"{TARGET_UID}:{TARGET_GID}"
        result_dir = f"{container_work}/.ci-result"
        extra_mounts = []
        user_environment = [
            "-e",
            f"HOME={container_work}/home",
            "-e",
            f"USER={TARGET_USER}",
            "-e",
            f"LOGNAME={TARGET_USER}",
        ]
    return [
        "docker",
        "run",
        "--rm",
        *docker_limits(network="bridge"),
        "--user",
        run_uid_gid,
        "-e",
        "OE_RVA23_PROBE=passed",
        "-e",
        "OE_BUILD_NETWORK=enabled",
        *user_environment,
        *common_mounts(repo_root, work_dir, package_id),
        *extra_mounts,
        image,
        "ci/run-rpmbuild-container.py",
        "exec",
        "--build-user",
        build_user,
        "--work-dir",
        container_work,
        "--result-dir",
        result_dir,
        "--identity-output",
        f"{result_dir}/build-identity.json",
        "--",
        "scripts/build-rpm",
        "--package-dir",
        f"packages/{package_id}",
        "--repo-root",
        "/workspace",
        "--work-dir",
        f"work/{package_id}",
        "--result",
        f"{result_dir}/rpmbuild-phase-result.json",
        "--commit-sha",
        commit_sha,
        "--timeout",
        str(build_timeout_seconds),
        "--skip-install-smoke",
        "--expected-arch",
        "riscv64",
    ]


def target_identity() -> tuple[pwd.struct_passwd, grp.struct_group]:
    try:
        user = pwd.getpwnam(TARGET_USER)
        group = grp.getgrgid(TARGET_GID)
    except KeyError as error:
        raise ContractError("derived image does not contain the fixed rpmbuild identity") from error
    if user.pw_uid != TARGET_UID or user.pw_gid != TARGET_GID:
        raise ContractError(
            f"{TARGET_USER} identity drifted: observed {user.pw_uid}:{user.pw_gid}, "
            f"expected {TARGET_UID}:{TARGET_GID}"
        )
    if group.gr_gid != TARGET_GID or group.gr_name != TARGET_USER:
        raise ContractError(
            f"{TARGET_USER} group drifted: observed {group.gr_name}:{group.gr_gid}, "
            f"expected {TARGET_USER}:{TARGET_GID}"
        )
    return user, group


def ownership_entries(root: pathlib.Path) -> list[pathlib.Path]:
    entries = [root]
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = pathlib.Path(current)
        for name in sorted(directories + files):
            candidate = current_path / name
            mode = candidate.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ContractError(f"ownership handoff refuses symlink entry: {candidate}")
            entries.append(candidate)
    return entries


def handoff_ownership(path: pathlib.Path) -> int:
    entries = ownership_entries(path)
    # The service UMask is deliberately 0077. Keep the work tree writable only
    # by the fixed build UID while allowing the host runner to collect public
    # build evidence and RPMs after ownership has changed.
    for entry in entries:
        grant_other_access(entry, readable=True)
    for entry in entries:
        os.chown(entry, TARGET_UID, TARGET_GID, follow_symlinks=False)
    return len(entries)


def prepare_mode(args: argparse.Namespace) -> int:
    if os.geteuid() != 0 or os.getegid() != 0:
        raise ContractError("ownership handoff must run as container root")
    target_identity()
    work_dir = require_regular_directory(pathlib.Path(args.work_dir), "work directory")
    result_dir = require_exact_child(
        pathlib.Path(args.result_dir), work_dir, "result directory"
    )
    require_regular_directory(result_dir, "result directory")
    record = {
        "schema_version": 1,
        "kind": "rpmbuild-ownership-handoff",
        "status": "passed",
        "preparation_uid": os.geteuid(),
        "preparation_gid": os.getegid(),
        "target_user": TARGET_USER,
        "target_uid": TARGET_UID,
        "target_gid": TARGET_GID,
        "host_readback_policy": (
            "files are other-readable; directories are other-readable and "
            "searchable; other-write is denied"
        ),
        "work_entries_before_record": len(ownership_entries(work_dir)),
    }
    write_json(result_dir / "ownership-handoff.json", record)
    handoff_ownership(work_dir)
    return 0


def directory_evidence(
    path: pathlib.Path,
    label: str,
    expected: Optional[tuple[int, int]],
) -> dict[str, object]:
    mode = path.lstat().st_mode
    metadata = path.stat()
    if not stat.S_ISDIR(mode):
        raise ContractError(f"{label} is not a regular directory: {path}")
    if expected and (metadata.st_uid, metadata.st_gid) != expected:
        raise ContractError(
            f"{label} ownership is {metadata.st_uid}:{metadata.st_gid}, "
            f"expected {expected[0]}:{expected[1]}"
        )
    if not os.access(path, os.R_OK | os.W_OK | os.X_OK):
        raise ContractError(f"{label} is not readable, writable, and searchable by the build user")
    return {
        "path": str(path),
        "uid": metadata.st_uid,
        "gid": metadata.st_gid,
        "mode": stat.S_IMODE(mode),
    }


def exec_mode(args: argparse.Namespace) -> int:
    effective_uid = os.geteuid()
    effective_gid = os.getegid()
    if args.build_user == "root":
        if effective_uid != 0 or effective_gid != 0:
            raise ContractError("root build policy did not receive UID/GID 0:0")
        observed_user = pwd.getpwuid(effective_uid).pw_name
        expected_owner = None
    elif args.build_user == "unprivileged":
        user, _ = target_identity()
        if effective_uid == 0 or effective_gid == 0:
            raise ContractError("unprivileged rpmbuild must never run as root")
        if effective_uid != TARGET_UID or effective_gid != TARGET_GID:
            raise ContractError(
                f"rpmbuild identity is {effective_uid}:{effective_gid}, "
                f"expected {TARGET_UID}:{TARGET_GID}"
            )
        observed_user = user.pw_name
        expected_owner = (TARGET_UID, TARGET_GID)
    else:
        raise ContractError(f"unsupported build user policy: {args.build_user}")

    work_dir = pathlib.Path(args.work_dir)
    result_dir = pathlib.Path(args.result_dir)
    if not args.command or args.command[0] != "scripts/build-rpm":
        raise ContractError("build wrapper may execute only scripts/build-rpm")
    if "--offline" in args.command:
        raise ContractError("rpmbuild invocation must allow verified network source retrieval")
    if os.environ.get("OE_BUILD_NETWORK") != "enabled":
        raise ContractError("network-enabled build policy was not reported by the container")
    previous_umask = os.umask(0o022)
    identity = {
        "schema_version": 1,
        "kind": "rpmbuild-execution-identity",
        "status": "passed",
        "build_user_policy": args.build_user,
        "user": observed_user,
        "uid": effective_uid,
        "gid": effective_gid,
        "is_root": effective_uid == 0,
        "umask": "0022",
        "previous_umask": f"{previous_umask:04o}",
        "network_access_policy": "enabled",
        "work_directory": directory_evidence(work_dir, "work directory", expected_owner),
        "result_directory": directory_evidence(
            result_dir, "result directory", expected_owner
        ),
    }
    write_json(pathlib.Path(args.identity_output), identity)
    os.execv(args.command[0], args.command)
    raise AssertionError("os.execv returned unexpectedly")


def copy_unprivileged_evidence(
    result_dir: pathlib.Path,
    artifact_dir: pathlib.Path,
    *,
    require_complete: bool,
) -> None:
    missing: list[str] = []
    for name in EVIDENCE_FILES:
        source = result_dir / name
        try:
            mode = source.lstat().st_mode
        except FileNotFoundError:
            missing.append(name)
            continue
        except OSError as error:
            raise ContractError(
                f"generated build evidence is unreadable: {source}: {error}"
            ) from error
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise ContractError(f"generated build evidence is not a regular file: {source}")
        shutil.copyfile(source, artifact_dir / name, follow_symlinks=False)
    if require_complete and missing:
        raise ContractError(
            "successful unprivileged build is missing required evidence: "
            + ", ".join(missing)
        )


def run_mode(args: argparse.Namespace) -> int:
    if not PACKAGE_ID.fullmatch(args.package_id):
        raise ContractError("package id is not canonical")
    if not COMMIT_SHA.fullmatch(args.commit_sha):
        raise ContractError("commit SHA must be exactly 40 lowercase hexadecimal characters")
    if not DERIVED_IMAGE.fullmatch(args.image):
        raise ContractError("build image must be the local, per-run BuildRequires image")
    if args.build_user not in BUILD_USERS:
        raise ContractError(f"unsupported build user policy: {args.build_user}")

    repo_root = pathlib.Path(args.repo_root).resolve()
    package_dir = repo_root / "packages" / args.package_id
    if package_dir.is_symlink() or not (package_dir / "package.yaml").is_file():
        raise ContractError("package directory is absent from the exact checked-out repository")
    work_dir = pathlib.Path(args.work_dir).resolve()
    expected_work = (repo_root / "work" / args.package_id).resolve()
    if work_dir != expected_work:
        raise ContractError(f"work directory must equal {expected_work}: {work_dir}")
    artifact_dir = pathlib.Path(args.artifact_dir).resolve()
    expected_artifacts = (repo_root / "artifacts" / "build").resolve()
    if artifact_dir != expected_artifacts:
        raise ContractError(f"artifact directory must equal {expected_artifacts}: {artifact_dir}")
    require_regular_directory(work_dir, "work directory")
    require_regular_directory(artifact_dir, "artifact directory")

    if args.build_user == "unprivileged":
        grant_unprivileged_workspace_access(repo_root, args.package_id)
        result_dir = work_dir / ".ci-result"
        if result_dir.is_symlink():
            raise ContractError("target result directory must not be a symlink")
        if result_dir.exists():
            shutil.rmtree(result_dir)
        result_dir.mkdir(mode=0o755)
        preparation = subprocess.run(
            unprivileged_prepare_command(
                args.image, repo_root, work_dir, args.package_id
            ),
            check=False,
        )
        if preparation.returncode != 0:
            copy_unprivileged_evidence(
                result_dir, artifact_dir, require_complete=False
            )
            return preparation.returncode
    else:
        grant_root_workspace_traversal(repo_root)
        result_dir = artifact_dir

    completed = subprocess.run(
        build_command(
            args.image,
            repo_root,
            work_dir,
            artifact_dir,
            args.package_id,
            args.commit_sha,
            args.build_user,
            args.build_timeout_seconds,
        ),
        check=False,
    )
    if args.build_user == "unprivileged":
        copy_unprivileged_evidence(
            result_dir,
            artifact_dir,
            require_complete=completed.returncode == 0,
        )
    return completed.returncode


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="mode", required=True)

    run_parser = subparsers.add_parser("run", help="orchestrate the policy-selected build")
    run_parser.add_argument("--image", required=True)
    run_parser.add_argument("--package-id", required=True)
    run_parser.add_argument("--repo-root", required=True)
    run_parser.add_argument("--work-dir", required=True)
    run_parser.add_argument("--artifact-dir", required=True)
    run_parser.add_argument("--commit-sha", required=True)
    run_parser.add_argument("--build-user", required=True, choices=sorted(BUILD_USERS))
    run_parser.add_argument(
        "--build-timeout-seconds", required=True, type=positive_seconds
    )

    prepare_parser = subparsers.add_parser(
        "prepare", help="hand fresh generated trees from root to the fixed target user"
    )
    prepare_parser.add_argument("--work-dir", required=True)
    prepare_parser.add_argument("--result-dir", required=True)

    exec_parser = subparsers.add_parser(
        "exec", help="verify the policy-selected identity and exec scripts/build-rpm"
    )
    exec_parser.add_argument("--build-user", required=True, choices=sorted(BUILD_USERS))
    exec_parser.add_argument("--work-dir", required=True)
    exec_parser.add_argument("--result-dir", required=True)
    exec_parser.add_argument("--identity-output", required=True)
    exec_parser.add_argument("command", nargs=argparse.REMAINDER)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    if args.mode == "run":
        return run_mode(args)
    if args.mode == "prepare":
        return prepare_mode(args)
    if args.mode == "exec":
        if args.command and args.command[0] == "--":
            args.command = args.command[1:]
        return exec_mode(args)
    raise AssertionError(f"unhandled mode: {args.mode}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
