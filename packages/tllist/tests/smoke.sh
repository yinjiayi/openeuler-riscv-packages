#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- tllist
pkg-config --modversion tllist | grep -Fx '1.1.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <tllist.h>

int main(void) {
    tll(int) values = tll_init();
    tll_push_back(values, 17);
    tll_push_front(values, 9);
    if (tll_length(values) != 2 || tll_front(values) != 9 ||
        tll_back(values) != 17)
        return 1;
    tll_free(values);
    return 0;
}
EOF
read -r -a pc_flags <<<"$(pkg-config --cflags tllist)"
cc "$smoke_dir/smoke.c" "${pc_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
