#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- which which-help
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

mkdir -p "$smoke_dir/first" "$smoke_dir/second"
printf '#!/usr/bin/env sh\nexit 0\n' >"$smoke_dir/first/rva23-tool"
printf '#!/usr/bin/env sh\nexit 0\n' >"$smoke_dir/second/rva23-tool"
chmod 0755 "$smoke_dir/first/rva23-tool" "$smoke_dir/second/rva23-tool"

test "$(PATH="$smoke_dir/first:$smoke_dir/second:/usr/bin" /usr/bin/which rva23-tool)" = \
  "$smoke_dir/first/rva23-tool"
PATH="$smoke_dir/first:$smoke_dir/second:/usr/bin" /usr/bin/which --all rva23-tool \
  >"$smoke_dir/all.txt"
printf '%s\n%s\n' "$smoke_dir/first/rva23-tool" "$smoke_dir/second/rva23-tool" \
  >"$smoke_dir/expected.txt"
cmp "$smoke_dir/expected.txt" "$smoke_dir/all.txt"
/usr/bin/which --version | grep -F 'GNU which v2.25'
