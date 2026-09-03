#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- fping
fping -v | grep -F '5.5'
test "$(fping -g 192.0.2.1 192.0.2.2 | wc -l)" -eq 2
