#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- datamash
datamash --version | grep -F 'datamash (GNU datamash) 1.9'

actual=$(printf 'a\t1\na\t2\nb\t4\n' | datamash -s groupby 1 sum 2)
test "$actual" = $'a\t3\nb\t4'

actual=$(printf '%s\n' C V III IX XI | decorate -k1,1:roman)
test "$actual" = $'III\nV\nIX\nXI\nC'
