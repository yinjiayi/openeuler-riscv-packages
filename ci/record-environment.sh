#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

output=${1:-artifacts/environment.json}
mkdir -p "$(dirname "$output")"

CI_ENV_HOSTNAME="$(hostname 2>/dev/null || true)"
CI_ENV_IP="$(hostname -I 2>/dev/null | awk '{$1=$1; print}' || true)"
CI_ENV_UNAME="$(uname -a 2>/dev/null || true)"
CI_ENV_CPU="$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || true)"
CI_ENV_MEMORY="$(free -b 2>/dev/null | awk '/^Mem:/ {print $2 " total, " $7 " available"}' || true)"
CI_ENV_DISK="$(df -Pk . 2>/dev/null | tail -n 1 | awk '{print $2 " KiB total, " $4 " KiB available"}' || true)"
CI_ENV_DOCKER="$(docker version --format '{{.Server.Version}}' 2>/dev/null || true)"
CI_ENV_GIT="$(git --version 2>/dev/null || true)"
CI_ENV_COMMIT="$(git rev-parse HEAD 2>/dev/null || true)"
CI_ENV_BRANCH="$(git symbolic-ref --short -q HEAD 2>/dev/null || true)"
CI_ENV_DIRTY="$(git status --porcelain 2>/dev/null | wc -l | awk '{$1=$1; print}' || true)"
export CI_ENV_HOSTNAME CI_ENV_IP CI_ENV_UNAME CI_ENV_CPU CI_ENV_MEMORY
export CI_ENV_DISK CI_ENV_DOCKER CI_ENV_GIT CI_ENV_COMMIT CI_ENV_BRANCH CI_ENV_DIRTY

python3 - "$output" <<'PY'
import datetime
import json
import os
import sys

payload = {
    "schema_version": 1,
    "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "hostname": os.environ.get("CI_ENV_HOSTNAME", ""),
    "ip": os.environ.get("CI_ENV_IP", ""),
    "uname": os.environ.get("CI_ENV_UNAME", ""),
    "cpu_count": os.environ.get("CI_ENV_CPU", ""),
    "memory": os.environ.get("CI_ENV_MEMORY", ""),
    "disk": os.environ.get("CI_ENV_DISK", ""),
    "docker": os.environ.get("CI_ENV_DOCKER", ""),
    "git": os.environ.get("CI_ENV_GIT", ""),
    "commit": os.environ.get("CI_ENV_COMMIT", ""),
    "branch": os.environ.get("CI_ENV_BRANCH", ""),
    "dirty_paths": int(os.environ.get("CI_ENV_DIRTY") or 0),
}
with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
PY
