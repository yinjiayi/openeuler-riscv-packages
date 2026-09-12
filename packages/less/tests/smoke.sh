#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- less
less --version | head -n 1 | grep -Fx 'less 704 (PCRE2 regular expressions)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler-riscv64-RVA23-less-smoke\n' >"$smoke_dir/input"
TERM=dumb less -F -X "$smoke_dir/input" >"$smoke_dir/output"
grep -Fx 'openEuler-riscv64-RVA23-less-smoke' "$smoke_dir/output"
