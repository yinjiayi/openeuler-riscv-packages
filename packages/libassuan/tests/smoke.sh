#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libassuan9 libassuan-devel
test "$(pkg-config --modversion libassuan)" = 3.0.2

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/smoke.c" <<'EOF'
#include <assuan.h>

int main(void)
{
    assuan_context_t context = NULL;
    if (assuan_new(&context) != 0 || context == NULL) {
        return 1;
    }
    assuan_release(context);
    return 0;
}
EOF
gcc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs libassuan) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
