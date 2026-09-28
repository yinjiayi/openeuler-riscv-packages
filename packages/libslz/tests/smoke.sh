#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libslz libslz-devel libslz-static
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/client.c" <<'EOF'
#include <slz.h>

int main(void) {
    struct slz_stream stream;
    return slz_init(&stream, 1, SLZ_FMT_ZLIB);
}
EOF
cc -Wall -Wextra -Werror "$smoke_dir/client.c" -lslz -o "$smoke_dir/client"
"$smoke_dir/client"

printf '%s\n' 'openEuler RISC-V SLZ installed smoke' >"$smoke_dir/input"
zenc -G "$smoke_dir/input" >"$smoke_dir/encoded"
zdec -G "$smoke_dir/encoded" >"$smoke_dir/decoded"
cmp "$smoke_dir/input" "$smoke_dir/decoded"
