#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- findutils findutils-help
find --version
xargs --version

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

mkdir -p "$smoke_dir/a" "$smoke_dir/b"
: >"$smoke_dir/a/one"
: >"$smoke_dir/b/two"

count=$(find "$smoke_dir" -type f -print0 | xargs -0 -n1 printf '%s\n' | wc -l)
test "$count" -eq 2
