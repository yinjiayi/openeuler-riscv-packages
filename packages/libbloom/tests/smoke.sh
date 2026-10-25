#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libbloom libbloom-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <bloom.h>
#include <string.h>

int main(void) {
    struct bloom filter = {0};
    const char *key = "openEuler-riscv64-RVA23";
    int length = (int)strlen(key);
    if (bloom_init2(&filter, 1000, 0.01) != 0) return 1;
    if (bloom_check(&filter, key, length) != 0) return 2;
    if (bloom_add(&filter, key, length) != 0) return 3;
    if (bloom_check(&filter, key, length) != 1) return 4;
    if (bloom_reset(&filter) != 0) return 5;
    if (bloom_check(&filter, key, length) != 0) return 6;
    bloom_free(&filter);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lbloom -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
