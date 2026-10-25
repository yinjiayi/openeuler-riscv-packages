#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- attr libattr libattr-devel

smoke_file=$(mktemp)
trap 'rm -f "$smoke_file"' EXIT
attribute_name=user.openeuler_riscv_smoke

setfattr -n "$attribute_name" -v rva23 "$smoke_file"
test "$(getfattr --only-values -n "$attribute_name" "$smoke_file")" = rva23
setfattr -x "$attribute_name" "$smoke_file"
if getfattr -n "$attribute_name" "$smoke_file" >/dev/null 2>&1; then
  echo 'extended attribute remained after removal' >&2
  exit 1
fi
