#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
unset MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEFILES
rpm -q munit munit-tests
rpm -V munit munit-tests
qa=$(mktemp -d)
trap 'rm -f -- "$qa/example" "$qa/munit.c" "$qa/munit.h" "$qa/example.c" "$qa/Makefile" "$qa/results.log"; rmdir -- "$qa"' EXIT
cp /usr/include/munit.h /usr/share/munit/munit.c "$qa/"
cp /usr/share/munit/qa/example.c /usr/share/munit/qa/Makefile "$qa/"
make -C "$qa" CC=gcc CFLAGS='-O2 -std=c99 -g'
make -C "$qa" test > "$qa/results.log" 2>&1
cat "$qa/results.log"
grep -Fx '11 of 11 (100%) tests successful, 0 (0%) test skipped.' "$qa/results.log"
