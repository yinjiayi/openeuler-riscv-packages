#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v pigz >/dev/null
command -v unpigz >/dev/null
pigz --version | grep -F 'pigz 2.8'

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
printf 'openEuler-riscv64-RVA23\n' >"$tmpdir/input"
pigz -c "$tmpdir/input" >"$tmpdir/input.gz"
unpigz -c "$tmpdir/input.gz" >"$tmpdir/output"
cmp "$tmpdir/input" "$tmpdir/output"
