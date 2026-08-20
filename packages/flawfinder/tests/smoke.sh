#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- flawfinder
flawfinder --version 2>&1 | grep -F 'Flawfinder version 2.0.20'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf '%s\n' '#include <string.h>' 'void f(char *d, const char *s) { strcpy(d, s); }' >"$smoke_dir/unsafe.c"
set +e
flawfinder --omittime --quiet --singleline "$smoke_dir/unsafe.c" >"$smoke_dir/result"
flawfinder_status=$?
set -e
test "$flawfinder_status" -ne 0
grep -F ':2:  [4] (buffer) strcpy:' "$smoke_dir/result"
