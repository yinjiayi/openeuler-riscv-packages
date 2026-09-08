#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpaper libpaper-devel
paper --help >/dev/null 2>&1
paper --all | grep -E '^A4:[[:space:]]+210x297[[:space:]]+mm$'
