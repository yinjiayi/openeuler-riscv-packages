#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxmp libxmp-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <xmp.h>

int main(void) {
    xmp_context context = xmp_create_context();
    if (context == 0 || XMP_VER_MAJOR != 4)
        return 1;
    xmp_free_context(context);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lxmp -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
