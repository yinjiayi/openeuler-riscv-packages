#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- wdiff diffutils
wdiff --version | grep -F 'wdiff (GNU wdiff) 1.2.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'alpha beta\n' >"$smoke_dir/old.txt"
printf 'alpha gamma\n' >"$smoke_dir/new.txt"

set +e
wdiff "$smoke_dir/old.txt" "$smoke_dir/new.txt" >"$smoke_dir/output.txt"
smoke_status=$?
set -e
test "$smoke_status" -eq 1
grep -F '[-beta-]' "$smoke_dir/output.txt"
grep -F '{+gamma+}' "$smoke_dir/output.txt"
