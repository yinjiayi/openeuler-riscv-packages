#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcdada libcdada-devel
test -x /usr/bin/cdada-gen

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libcdada-smoke.c" <<'EOF'
#include <cdada/list.h>
#include <stdint.h>

int main(void) {
    uint32_t input = 42, output = 0;
    cdada_list_t *list = cdada_list_create(uint32_t);
    if (!list) return 1;
    if (cdada_list_push_back(list, &input) != CDADA_SUCCESS) return 2;
    if (cdada_list_size(list) != 1) return 3;
    if (cdada_list_first(list, &output) != CDADA_SUCCESS || output != 42) return 4;
    return cdada_list_destroy(list) == CDADA_SUCCESS ? 0 : 5;
}
EOF
cc "$smoke_dir/libcdada-smoke.c" -lcdada -o "$smoke_dir/libcdada-smoke"
"$smoke_dir/libcdada-smoke"
