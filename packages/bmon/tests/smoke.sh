#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- bmon
test "$(rpm -q --qf '%{VERSION}\n' bmon)" = 4.0
bmon -V | grep -F 'bmon 4.0'
set +e
output="$(bmon -h 2>&1)"
status=$?
set -e
test "$status" -eq 1
printf '%s\n' "$output" | grep -F 'Usage: bmon'
