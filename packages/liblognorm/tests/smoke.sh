#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblognorm liblognorm-devel liblognorm-utils liblognorm-help
lognormalizer -V 2>&1 | grep -F 'liblognorm version: 2.1.0'
pkg-config --modversion lognorm | grep -Fx '2.1.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/rules.rb" <<'EOF'
version=2
rule=:hello %name:word%
EOF
printf 'hello RVA23\n' | lognormalizer -r "$smoke_dir/rules.rb" -e json \
  >"$smoke_dir/classic.json"
grep -F '"name": "RVA23"' "$smoke_dir/classic.json"
printf 'hello RVA23\n' | lognormalizer -oturbo -r "$smoke_dir/rules.rb" -e json \
  >"$smoke_dir/turbo.json"
grep -F '"name": "RVA23"' "$smoke_dir/turbo.json"

cat >"$smoke_dir/liblognorm-smoke.c" <<'EOF'
#include <liblognorm.h>
#include <string.h>

int main(void) {
    ln_ctx context = ln_initCtx();
    if (context == NULL || strcmp(ln_version(), "2.1.0") != 0) {
        return 1;
    }
    return ln_exitCtx(context);
}
EOF
cc $({ pkg-config --cflags lognorm; }) "$smoke_dir/liblognorm-smoke.c" \
  -o "$smoke_dir/liblognorm-smoke" $({ pkg-config --libs lognorm; })
"$smoke_dir/liblognorm-smoke"
