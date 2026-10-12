#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblqr liblqr-devel
test "$(pkg-config --modversion lqr-1)" = 0.4.3

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/resize.c" <<'EOF'
#include <lqr.h>
#include <glib.h>

int main(void) {
    guchar *pixels = g_malloc0(8 * 8 * 3);
    LqrCarver *carver;
    int result = 0;
    for (int i = 0; i < 8 * 8 * 3; ++i) pixels[i] = (guchar)i;
    carver = lqr_carver_new(pixels, 8, 8, 3);
    if (carver == NULL) { g_free(pixels); return 1; }
    if (lqr_carver_init(carver, 1, 0.0f) != LQR_OK) result = 2;
    if (result == 0 && lqr_carver_resize(carver, 7, 8) != LQR_OK) result = 3;
    if (result == 0 && (lqr_carver_get_width(carver) != 7 ||
                        lqr_carver_get_height(carver) != 8)) result = 4;
    lqr_carver_destroy(carver);
    return result;
}
EOF
read -r -a lqr_flags <<< "$(pkg-config --cflags --libs lqr-1)"
cc -std=c99 "$smoke_dir/resize.c" "${lqr_flags[@]}" -o "$smoke_dir/resize"
"$smoke_dir/resize"
