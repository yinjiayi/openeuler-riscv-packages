#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- diffutils
diff --version | grep -F 'diff (GNU diffutils) 3.12'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'alpha\nbeta\n' >"$smoke_dir/left"
printf 'alpha\ngamma\n' >"$smoke_dir/right"
cmp "$smoke_dir/left" "$smoke_dir/left"

set +e
diff -u "$smoke_dir/left" "$smoke_dir/right" >"$smoke_dir/delta"
diff_status=$?
set -e
test "$diff_status" -eq 1
grep -F -- '-beta' "$smoke_dir/delta"
grep -F -- '+gamma' "$smoke_dir/delta"
