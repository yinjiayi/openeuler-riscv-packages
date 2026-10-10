#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bats
bats --version | grep -Fx 'Bats 1.14.0'
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/rva23.bats" <<'EOF'
@test "RVA23 package executes tests" {
  run printf '%s\n' RVA23
  [ "$status" -eq 0 ]
  [ "$output" = RVA23 ]
}
EOF
bats --tap "$tmpdir/rva23.bats" | grep -Fx 'ok 1 RVA23 package executes tests'
