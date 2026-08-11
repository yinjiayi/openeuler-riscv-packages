#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- bzip2 bzip2-libs bzip2-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler riscv64 RVA23\n' >"$smoke_dir/input"
bzip2 -k "$smoke_dir/input"
bzip2 -dc "$smoke_dir/input.bz2" >"$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <bzlib.h>
int main(void) {
    return BZ2_bzlibVersion() == 0;
}
EOF
cc "$smoke_dir/smoke.c" -lbz2 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
