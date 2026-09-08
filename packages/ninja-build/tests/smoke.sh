#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ninja-build
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/build.ninja" <<'EOF'
rule emit
  command = printf 'riscv64-RVA23\n' > $out
build target.txt: emit
default target.txt
EOF
ninja -C "$smoke_dir"
test "$(cat "$smoke_dir/target.txt")" = "riscv64-RVA23"
