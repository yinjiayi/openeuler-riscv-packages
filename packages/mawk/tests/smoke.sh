#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mawk
mawk -W version 2>&1 | grep -Fx 'mawk 1.3.4 20260302'

result=$(printf 'alpha 2\nbeta 3\n' | mawk '{sum += $2} END {print sum}')
test "$result" = '5'
