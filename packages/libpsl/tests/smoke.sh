#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpsl libpsl-utils libpsl-devel libpsl-help
psl --version | grep -F 'psl 0.23.3'
test "$(psl --use-builtin-data --is-public-suffix --batch com)" = '1'
test "$(psl --use-builtin-data --print-reg-domain --batch www.example.com)" = 'example.com'
pkg-config --modversion libpsl | grep -Fx '0.23.3'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libpsl-smoke.c" <<'EOF'
#include <libpsl.h>
#include <string.h>

int main(void) {
    const psl_ctx_t *ctx = psl_builtin();
    const char *domain;
    if (ctx == NULL || !psl_is_public_suffix(ctx, "com")) {
        return 1;
    }
    domain = psl_registrable_domain(ctx, "www.example.com");
    return domain != NULL && strcmp(domain, "example.com") == 0 ? 0 : 2;
}
EOF
cc $({ pkg-config --cflags libpsl; }) "$smoke_dir/libpsl-smoke.c" \
  -o "$smoke_dir/libpsl-smoke" $({ pkg-config --libs libpsl; })
"$smoke_dir/libpsl-smoke"
