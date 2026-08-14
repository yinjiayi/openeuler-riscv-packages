#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- zix zix-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <zix/digest.h>

#include <stddef.h>

int main(void) {
    static const char payload[] = "openEuler-RVA23";
    const size_t first = zix_digest(23U, payload, sizeof(payload) - 1U);
    const size_t second = zix_digest(23U, payload, sizeof(payload) - 1U);
    return first == second ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs zix-0) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
