#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- uchardet uchardet-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf 'openEuler riscv64 RVA23 ASCII smoke\n' >"$smoke_dir/input.txt"
test "$(uchardet "$smoke_dir/input.txt")" = "ASCII"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <uchardet/uchardet.h>
#include <string.h>

int main(void) {
    static const char input[] = "openEuler riscv64 RVA23 ASCII smoke\n";
    uchardet_t detector = uchardet_new();
    const char *charset;
    int failed;
    if (detector == NULL)
        return 1;
    failed = uchardet_handle_data(detector, input, sizeof(input) - 1);
    uchardet_data_end(detector);
    charset = uchardet_get_charset(detector);
    failed = failed || charset == NULL || strcmp(charset, "ASCII") != 0;
    uchardet_delete(detector);
    return failed;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs uchardet) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
