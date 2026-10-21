#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

printf 'alpha\nbeta\n' >"$tmpdir/base"
printf 'alpha\nbeta\ngamma\n' >"$tmpdir/new"

rdiff signature "$tmpdir/base" "$tmpdir/signature"
rdiff delta "$tmpdir/signature" "$tmpdir/new" "$tmpdir/delta"
rdiff patch "$tmpdir/base" "$tmpdir/delta" "$tmpdir/restored"
cmp "$tmpdir/new" "$tmpdir/restored"
