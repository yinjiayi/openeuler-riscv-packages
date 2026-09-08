#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libzip libzip-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
pkg-config --exact-version=1.11.4 libzip
ziptool -n "$smoke_dir/smoke.zip" add smoke.txt libzip-smoke
test -s "$smoke_dir/smoke.zip"
test "$(ziptool "$smoke_dir/smoke.zip" cat 0)" = libzip-smoke
