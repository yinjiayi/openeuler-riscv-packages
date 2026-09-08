#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Feed one short-lived Runner token through an inherited environment only.

The token is read from standard input, is never accepted as an argument, and
is not copied to a file. The child gets the value only as the Runner's
documented secret environment input. The official Runner removes that variable
from its environment and registers it with its log secret masker.
"""

from __future__ import annotations

import argparse
import ctypes
import os
from pathlib import Path
import pwd
import re
import signal
import sys


BASE = Path("/opt/openeuler-actions-runner")
REPOSITORY_URL = "https://github.com/yinjiayi/openeuler-riscv-packages"
LABELS = (
    "oe-rva23-qemu,ubuntu-26.04,openeuler-24.03-lts-sp3,"
    "rva23-qemu,trusted-main-only"
)
NAME = re.compile(r"^oe-rva23-qemu-(20[1-9]|2[1-4][0-9]|250)$")
SECRET = re.compile(rb"^[A-Za-z0-9_+=./-]{10,512}$")
LONG_LIVED_PREFIXES = (b"ghp_", b"gho_", b"ghu_", b"ghs_", b"ghr_", b"github_pat_")
PR_SET_DUMPABLE = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the fixed Runner configuration operation with a token read from stdin."
    )
    parser.add_argument("purpose", choices=("register", "remove"))
    parser.add_argument("--user", required=True)
    parser.add_argument("--name", required=True)
    return parser.parse_args()


def read_secret() -> bytearray:
    raw = sys.stdin.buffer.readline(514)
    if len(raw) > 513 or (len(raw) == 513 and not raw.endswith(b"\n")):
        raise ValueError("credential exceeds 512 bytes")
    if raw.endswith(b"\n"):
        raw = raw[:-1]
    if raw.endswith(b"\r"):
        raw = raw[:-1]
    if not raw or not SECRET.fullmatch(raw):
        raise ValueError("credential is empty or contains unsupported characters")
    if raw.startswith(LONG_LIVED_PREFIXES):
        raise ValueError("long-lived GitHub access tokens are not accepted")
    return bytearray(raw)


def disable_core_dumps() -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(PR_SET_DUMPABLE, 0, 0, 0, 0) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


def validate_target(name: str, user: str) -> tuple[Path, pwd.struct_passwd]:
    if not NAME.fullmatch(name):
        raise ValueError("runner name is outside the managed fleet")
    account = pwd.getpwnam(user)
    if account.pw_uid == 0 or user != "oegha":
        raise ValueError("runner service account must be the non-root oegha user")
    runner_dir = BASE / name
    if runner_dir.resolve() != runner_dir or not runner_dir.is_dir():
        raise ValueError("runner directory is missing or not canonical")
    config = runner_dir / "config.sh"
    if config.is_symlink() or not config.is_file() or not os.access(config, os.X_OK):
        raise ValueError("config.sh is missing, non-executable, or a symlink")
    return runner_dir, account


def child_argv(purpose: str, runner_dir: Path, name: str) -> list[str]:
    config = str(runner_dir / "config.sh")
    if purpose == "remove":
        return [config, "remove", "--unattended"]
    return [
        config,
        "--unattended",
        "--url",
        REPOSITORY_URL,
        "--name",
        name,
        "--work",
        "_work",
        "--labels",
        LABELS,
        "--disableupdate",
    ]


def scan_for_persisted_secret(runner_dir: Path, secret: bytearray) -> bool:
    candidates: list[Path] = []
    for name in (
        ".runner",
        ".credentials",
        ".credentials_rsaparams",
        ".env",
        ".path",
        ".service",
    ):
        candidates.append(runner_dir / name)
    diag = runner_dir / "_diag"
    if diag.is_dir():
        candidates.extend(path for path in diag.iterdir() if path.is_file() and not path.is_symlink())
    needle = bytes(secret)
    for candidate in candidates:
        try:
            if candidate.is_symlink() or not candidate.is_file() or candidate.stat().st_size > 16 * 1024 * 1024:
                continue
            if needle in candidate.read_bytes():
                return True
        except OSError:
            return True
    return False


def execute(purpose: str, runner_dir: Path, account: pwd.struct_passwd, name: str, secret: bytearray) -> int:
    argv = child_argv(purpose, runner_dir, name)
    pid = os.fork()
    if pid == 0:
        try:
            os.chdir(runner_dir)
            os.umask(0o077)
            os.initgroups(account.pw_name, account.pw_gid)
            os.setgid(account.pw_gid)
            os.setuid(account.pw_uid)
            disable_core_dumps()
            token = secret.decode("ascii")
            environment = {
                "ACTIONS_RUNNER_INPUT_TOKEN": token,
                "HOME": str(runner_dir / "_state" / "home"),
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "LOGNAME": account.pw_name,
                "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "USER": account.pw_name,
            }
            os.execve(argv[0], argv, environment)
        except BaseException as error:  # pragma: no cover - last-resort child failure
            print(f"credential-exec: child setup failed: {type(error).__name__}", file=sys.stderr)
            os._exit(126)
    _, status = os.waitpid(pid, 0)
    if os.WIFSIGNALED(status):
        return 128 + os.WTERMSIG(status)
    if not os.WIFEXITED(status):
        return 125
    return os.WEXITSTATUS(status)


def main() -> int:
    args = parse_args()
    secret = bytearray()
    try:
        disable_core_dumps()
        runner_dir, account = validate_target(args.name, args.user)
        secret = read_secret()
        result = execute(args.purpose, runner_dir, account, args.name, secret)
        if scan_for_persisted_secret(runner_dir, secret):
            print("credential-exec: credential persistence guard failed", file=sys.stderr)
            return 78
        return result
    except (KeyError, OSError, ValueError) as error:
        print(f"credential-exec: {error}", file=sys.stderr)
        return 64
    finally:
        for index in range(len(secret)):
            secret[index] = 0


if __name__ == "__main__":
    sys.exit(main())
