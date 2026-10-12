#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- psmisc

fuser_bin=$(command -v fuser)
killall -V >/dev/null
prtstat -V >/dev/null
pslog -V >/dev/null
pstree -V >/dev/null
"$fuser_bin" -V >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
touch "$smoke_dir/open-file"
exec 9<"$smoke_dir/open-file"
"$fuser_bin" "$smoke_dir/open-file" >"$smoke_dir/fuser.out" 2>&1
grep -Eq "(^|[^0-9])$$([^0-9]|$)" "$smoke_dir/fuser.out"
