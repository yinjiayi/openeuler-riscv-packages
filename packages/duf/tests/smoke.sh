#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- duf
duf --version | grep -F 'duf 0.9.1'

json=$(duf --json)
printf '%s\n' "$json" | grep -F '"mount_point"'
