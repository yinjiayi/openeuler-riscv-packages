#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- vtm
version_output=$(script --quiet --return --command 'vtm --version' /dev/null </dev/null 2>&1)
printf '%s\n' "$version_output"
grep -F -- 'v2026.07.30' <<<"$version_output"
