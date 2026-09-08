#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- yajl yajl-devel
printf '{"arch":"riscv64","isa":"RVA23"}\n' | json_verify
printf '{"arch":"riscv64"}\n' | json_reformat | grep -F '"arch": "riscv64"'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <yajl/yajl_parse.h>
int main(void) {
    yajl_handle parser = yajl_alloc(0, 0, 0);
    if (parser == 0) return 1;
    yajl_free(parser);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs yajl) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
