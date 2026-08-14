#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libatomic_ops libatomic_ops-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <atomic_ops.h>
int main(void) {
    volatile AO_t value = 0;
    AO_store(&value, 41);
    if (AO_fetch_and_add1(&value) != 41) return 1;
    return AO_load(&value) == 42 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -latomic_ops -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
