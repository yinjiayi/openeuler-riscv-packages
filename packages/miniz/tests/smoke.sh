#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- miniz miniz-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <miniz.h>

#include <string.h>

int main(void) {
    static const unsigned char input[] = "openEuler RVA23 miniz smoke";
    unsigned char compressed[128];
    unsigned char restored[128];
    mz_ulong compressed_size = sizeof(compressed);
    mz_ulong restored_size = sizeof(restored);

    if (compress(compressed, &compressed_size, input, sizeof(input)) != MZ_OK) {
        return 1;
    }
    if (uncompress(restored, &restored_size, compressed, compressed_size) != MZ_OK) {
        return 2;
    }
    return restored_size == sizeof(input) && memcmp(restored, input, sizeof(input)) == 0 ? 0 : 3;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs miniz) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
