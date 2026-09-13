#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- dos2unix
dos2unix --version 2>&1 | head -n 1 | grep -F 'dos2unix 7.5.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'first\r\nsecond\r\n' >"$smoke_dir/text"
dos2unix "$smoke_dir/text"
test "$(od -An -tx1 "$smoke_dir/text" | tr -d ' \n')" = '66697273740a7365636f6e640a'
unix2dos "$smoke_dir/text"
test "$(od -An -tx1 "$smoke_dir/text" | tr -d ' \n')" = '66697273740d0a7365636f6e640d0a'
