#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bounded Docker cleanup for a host dedicated to one persistent Runner.

The program refuses to mutate Docker when any container is running. Once an
idle daemon is observed twice, it removes all stopped/created containers,
dangling volumes, unused custom networks, and only the repository-defined
``openeuler-builddeps:*`` derived images. It intentionally performs no global
image or build-cache prune, preserving the digest-pinned GHCR base image.
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
MAX_OUTPUT_BYTES = 1024 * 1024


class CleanupError(RuntimeError):
    """A fail-closed inventory or Docker operation failure."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker", type=Path, default=Path("/usr/bin/docker"))
    parser.add_argument("--max-objects", type=int, default=512)
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
    return lines(docker(command, "ps", "--quiet"), OBJECT, maximum, "running container")


def require_idle(command: Path, maximum: int) -> None:
    running = running_containers(command, maximum)
    if running:
        raise CleanupError(
            "running container detected on dedicated Runner host; refusing every cleanup mutation"
        )


def cleanup(command: Path, maximum: int) -> dict[str, int | bool]:
    if maximum < 1 or maximum > 4096:
        raise CleanupError("max-objects must be between 1 and 4096")
    if not command.is_absolute() or not command.is_file() or command.is_symlink():
        raise CleanupError("Docker command must be an absolute, regular, non-symlink file")

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
        result = cleanup(args.docker, args.max_objects)
    except (CleanupError, OSError, subprocess.SubprocessError, UnicodeError) as error:
        print(f"docker-cleanup: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
