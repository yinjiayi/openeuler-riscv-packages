#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jbig2dec jbig2dec-devel
jbig2dec --version | grep -Fx 'jbig2dec 0.20'
test "$(pkg-config --modversion jbig2dec)" = '0.20'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdint.h>
#include <stddef.h>
#include <jbig2.h>

int main(void) {
    Jbig2Ctx *ctx;
    if (JBIG2_VERSION_MAJOR != 0 || JBIG2_VERSION_MINOR != 20) return 1;
    ctx = jbig2_ctx_new(NULL, 0, NULL, NULL, NULL);
    if (ctx == NULL) return 2;
    jbig2_ctx_free(ctx);
    return 0;
}
EOF
read -r -a pkgconf_flags <<<"$(pkg-config --cflags --libs jbig2dec)"
cc "$smoke_dir/smoke.c" "${pkgconf_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
