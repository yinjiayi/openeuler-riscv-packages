#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcap-ng libcap-ng-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cap-ng.h>
int main(void) {
    capng_clear(CAPNG_SELECT_BOTH);
    return capng_have_capabilities(CAPNG_SELECT_BOTH) == CAPNG_NONE ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libcap-ng) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
