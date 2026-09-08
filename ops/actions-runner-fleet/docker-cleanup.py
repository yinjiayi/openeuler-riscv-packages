#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bounded Docker cleanup for a host dedicated to one persistent Runner.

The program recovers only fully identified dependency containers orphaned by a
prior job and otherwise refuses to mutate Docker when a container is running.
Once an idle daemon is observed twice, it removes all stopped/created
containers, dangling volumes, unused custom networks, and only the
repository-defined ``openeuler-builddeps:*`` derived images. It intentionally
performs no global image or build-cache prune, preserving the digest-pinned
GHCR base image.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


OBJECT = re.compile(r"^[a-f0-9]{12,64}$")
VOLUME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,254}$")
DERIVED_IMAGE = re.compile(r"^openeuler-builddeps:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$")
MANAGED_CONTAINER_NAME = re.compile(r"^/openeuler-builddeps-[1-9][0-9]*-[a-f0-9]{8}$")
MANAGED_IMAGE = re.compile(
    r"^ghcr\.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:[a-f0-9]{64}$"
)
MANAGED_LABEL = "io.openeuler.actions-runner.managed-builddeps"
MANAGED_VALUE = "v1"
MANAGED_COMMAND = ["/bin/bash", "-c", "while :; do sleep 3600; done"]
MAX_OUTPUT_BYTES = 1024 * 1024


class CleanupError(RuntimeError):
    """A fail-closed inventory or Docker operation failure."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker", type=Path, default=Path("/usr/bin/docker"))
    parser.add_argument("--max-objects", type=int, default=512)
    parser.add_argument("--managed-image-ref", required=True)
    return parser.parse_args()


def docker(command: Path, *arguments: str) -> str:
    completed = subprocess.run(
        [str(command), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    if len(completed.stdout) > MAX_OUTPUT_BYTES or len(completed.stderr) > MAX_OUTPUT_BYTES:
        raise CleanupError("Docker output exceeded the 1 MiB safety bound")
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace").strip()[-1000:]
        raise CleanupError(f"Docker command failed ({arguments[0]}): {message}")
    return completed.stdout.decode("utf-8", errors="strict")


def lines(value: str, pattern: re.Pattern[str], maximum: int, kind: str) -> list[str]:
    result = [item.strip() for item in value.splitlines() if item.strip()]
    if len(result) > maximum:
        raise CleanupError(f"{kind} inventory exceeds the {maximum}-object bound")
    if len(result) != len(set(result)):
        raise CleanupError(f"{kind} inventory contains duplicates")
    invalid = [item for item in result if pattern.fullmatch(item) is None]
    if invalid:
        raise CleanupError(f"{kind} inventory contains an unsafe identifier")
    return result


def running_containers(command: Path, maximum: int) -> list[str]:
    return lines(
        docker(command, "ps", "--no-trunc", "--quiet"),
        OBJECT,
        maximum,
        "running container",
    )


def require_idle(command: Path, maximum: int) -> None:
    running = running_containers(command, maximum)
    if running:
        raise CleanupError(
            "running container detected on dedicated Runner host; refusing every cleanup mutation"
        )


def managed_running_container(
    command: Path, container: str, managed_image_ref: str
) -> bool:
    raw = docker(command, "inspect", "--format", "{{json .}}", container)
    try:
        document = json.loads(raw)
    except json.JSONDecodeError as error:
        raise CleanupError("running container inspection is not valid JSON") from error
    if not isinstance(document, dict):
        raise CleanupError("running container inspection is not an object")
    config = document.get("Config")
    host = document.get("HostConfig")
    state = document.get("State")
    if not isinstance(config, dict) or not isinstance(host, dict) or not isinstance(state, dict):
        return False
    labels = config.get("Labels")
    return (
        document.get("Id") == container
        and isinstance(document.get("Name"), str)
        and MANAGED_CONTAINER_NAME.fullmatch(document["Name"]) is not None
        and config.get("Image") == managed_image_ref
        and config.get("Cmd") == MANAGED_COMMAND
        and isinstance(labels, dict)
        and labels.get(MANAGED_LABEL) == MANAGED_VALUE
        and host.get("AutoRemove") is False
        and state.get("Running") is True
    )


def recover_managed_running_containers(
    command: Path, maximum: int, managed_image_ref: str
) -> int:
    if MANAGED_IMAGE.fullmatch(managed_image_ref) is None:
        raise CleanupError("managed image must be the immutable repository build image")
    running = running_containers(command, maximum)
    if not running:
        return 0
    # Inspect every running container before the first mutation. One unknown
    # workload keeps the original fail-closed behavior for the whole host.
    identities = [
        managed_running_container(command, container, managed_image_ref)
        for container in running
    ]
    if not all(identities):
        raise CleanupError(
            "unrecognized running container detected on dedicated Runner host; "
            "refusing every cleanup mutation"
        )
    if running_containers(command, maximum) != running:
        raise CleanupError(
            "running container inventory changed during inspection; "
            "refusing every cleanup mutation"
        )
    docker(command, "rm", "--force", "--volumes", "--", *running)
    require_idle(command, maximum)
    return len(running)


def cleanup(command: Path, maximum: int, managed_image_ref: str) -> dict[str, int | bool]:
    if maximum < 1 or maximum > 4096:
        raise CleanupError("max-objects must be between 1 and 4096")
    if not command.is_absolute() or not command.is_file() or command.is_symlink():
        raise CleanupError("Docker command must be an absolute, regular, non-symlink file")

    recovered = recover_managed_running_containers(command, maximum, managed_image_ref)

    # A first check establishes an idle inventory. A second check immediately
    # before the first mutation narrows the race window without pretending the
    # Docker API provides a global transaction.
    require_idle(command, maximum)
    stopped = lines(
        docker(command, "ps", "--all", "--quiet"), OBJECT, maximum, "stopped container"
    )
    derived = lines(
        docker(
            command,
            "image",
            "ls",
            "--all",
            "--format",
            "{{.Repository}}:{{.Tag}}",
            "--filter",
            "reference=openeuler-builddeps:*",
        ),
        DERIVED_IMAGE,
        maximum,
        "derived image",
    )
    require_idle(command, maximum)

    if stopped:
        docker(command, "rm", "--force", "--volumes", "--", *stopped)

    # Recheck after container removal. A concurrently started, non-fleet
    # workload prevents all subsequent volume/network/image deletion.
    require_idle(command, maximum)
    volumes = lines(
        docker(command, "volume", "ls", "--quiet", "--filter", "dangling=true"),
        VOLUME,
        maximum,
        "dangling volume",
    )
    networks = lines(
        docker(command, "network", "ls", "--quiet", "--filter", "type=custom"),
        OBJECT,
        maximum,
        "custom network",
    )
    unused_networks: list[str] = []
    for network in networks:
        attached = docker(
            command, "network", "inspect", "--format", "{{len .Containers}}", network
        ).strip()
        if not attached.isdigit():
            raise CleanupError("custom network attachment count is invalid")
        if int(attached) == 0:
            unused_networks.append(network)

    require_idle(command, maximum)
    if volumes:
        docker(command, "volume", "rm", "--force", "--", *volumes)
    if unused_networks:
        docker(command, "network", "rm", "--", *unused_networks)
    if derived:
        docker(command, "image", "rm", "--force", "--", *derived)

    return {
        "schema_version": 1,
        "running_containers": False,
        "removed_managed_running_containers": recovered,
        "removed_containers": len(stopped),
        "removed_dangling_volumes": len(volumes),
        "removed_unused_networks": len(unused_networks),
        "removed_derived_images": len(derived),
        "global_image_prune": False,
        "global_build_cache_prune": False,
    }


def main() -> int:
    args = parse_args()
    try:
        result = cleanup(args.docker, args.max_objects, args.managed_image_ref)
    except (CleanupError, OSError, subprocess.SubprocessError, UnicodeError) as error:
        print(f"docker-cleanup: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
