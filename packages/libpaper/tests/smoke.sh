#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpaper libpaper-devel
paper --help >/dev/null
paper --all | grep -E '^a4[[:space:]]'
