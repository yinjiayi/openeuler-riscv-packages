#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v cdb >/dev/null
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
printf 'key openEuler-riscv64-RVA23\n' | cdb -c -m "$tmpdir/test.cdb"
cdb -q -m "$tmpdir/test.cdb" key | grep -Fx 'openEuler-riscv64-RVA23'
cdb -s "$tmpdir/test.cdb" | grep -F 'records'
