#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- bmon
test "$(rpm -q --qf '%{VERSION}\n' bmon)" = 4.0
bmon -V | grep -F 'bmon 4.0'
bmon -h | grep -F 'Usage: bmon'
