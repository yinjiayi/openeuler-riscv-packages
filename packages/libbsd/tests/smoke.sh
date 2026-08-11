#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libbsd libbsd-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <bsd/string.h>
#include <string.h>
int main(void) {
    char output[16];
    return strlcpy(output, "riscv64", sizeof(output)) == 7 &&
           strcmp(output, "riscv64") == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libbsd) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
