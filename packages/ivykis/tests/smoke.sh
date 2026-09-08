#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ivykis ivykis-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <iv.h>
int main(void) {
    iv_init();
    if (!iv_inited()) return 1;
    iv_deinit();
    return iv_inited() ? 1 : 0;
}
EOF
cc "$smoke_dir/smoke.c" -livykis -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
