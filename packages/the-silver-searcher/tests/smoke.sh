#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- the_silver_searcher
ag --version | grep -F 'ag version 2.2.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

mkdir -p "$smoke_dir/src"
printf '%s\n' 'unrelated' 'openEuler RVA23' >"$smoke_dir/src/target.c"
printf '%s\n' 'unrelated' >"$smoke_dir/src/other.c"

ag --noaffinity --nocolor --nogroup --workers=1 --parallel \
  --cc 'openEuler[[:space:]]+RVA23' "$smoke_dir" | \
  grep -F 'openEuler RVA23'
ag --noaffinity --nocolor --workers=1 --parallel -l \
  'openEuler' "$smoke_dir" | grep -F 'target.c'
