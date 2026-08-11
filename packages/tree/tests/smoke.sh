#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- tree tree-help
tree --version | grep -F 'tree v2.3.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
mkdir -p "$smoke_dir/root/alpha/beta"
printf 'RVA23\n' >"$smoke_dir/root/alpha/beta/payload.txt"
printf 'hidden\n' >"$smoke_dir/root/.hidden"

tree -afi --noreport "$smoke_dir/root" >"$smoke_dir/tree.txt"
grep -F "$smoke_dir/root/.hidden" "$smoke_dir/tree.txt"
grep -F "$smoke_dir/root/alpha/beta/payload.txt" "$smoke_dir/tree.txt"

tree -aJ --noreport "$smoke_dir/root" >"$smoke_dir/tree.json"
grep -E '"name"[[:space:]]*:[[:space:]]*"\.hidden"' "$smoke_dir/tree.json"
grep -E '"name"[[:space:]]*:[[:space:]]*"payload\.txt"' "$smoke_dir/tree.json"
