#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- catatonit
test "$(rpm -q --qf '%{VERSION}\n' catatonit)" = 0.2.1
catatonit -V | grep -F 'tini version 0.2.1_catatonit'
catatonit -h 2>&1 | grep -F 'usage: catatonit'
