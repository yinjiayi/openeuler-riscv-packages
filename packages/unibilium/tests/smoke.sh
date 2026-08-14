#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- unibilium unibilium-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <unibilium.h>
int main(void) {
    unibi_term *term = unibi_dummy();
    if (term == 0) return 1;
    unibi_destroy(term);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lunibilium -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
