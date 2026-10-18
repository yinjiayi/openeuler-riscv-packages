#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
unset CFLAGS CXXFLAGS MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEFILES
rpm -q hedley hedley-tests
rpm -V hedley hedley-tests
qa=$(mktemp -d)
trap 'find "$qa" -depth -delete' EXIT
cp /usr/include/hedley.h "$qa/"
cp -a /usr/share/hedley/qa/test "$qa/test"
make -C "$qa/test" all CC=gcc CXX=g++
test "$(find "$qa/test" -maxdepth 1 -type f -perm /111 | wc -l)" -eq 70
echo 'PASS hedley installed-header=70 original-default compile-link-only'
