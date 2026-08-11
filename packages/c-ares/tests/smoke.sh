#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- c-ares c-ares-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <ares.h>
#include <stdio.h>
int main(void) {
    int version = 0;
    if (ares_library_init(ARES_LIB_INIT_ALL) != ARES_SUCCESS) return 1;
    if (ares_version(&version) == NULL || version == 0) return 2;
    ares_library_cleanup();
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lcares -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
