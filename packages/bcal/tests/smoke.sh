#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- bcal
test "$(rpm -q --qf '%{VERSION}\n' bcal)" = 2.5
bcal -h 2>&1 | grep -F 'usage: bcal'
bcal -m 10 mb | grep -Fx '10000000 B'
