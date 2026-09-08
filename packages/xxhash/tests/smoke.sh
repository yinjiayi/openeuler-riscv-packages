#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- xxhash xxhash-devel
test "$(printf abc | xxhsum -H0 | awk '{print $1}')" = "32d153ff"
