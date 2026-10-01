#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- pixman pixman-devel
test "$(pkg-config --modversion pixman-1)" = "0.46.4"

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <pixman.h>
#include <stddef.h>
#include <stdint.h>

int main(void) {
    uint32_t pixel = 0;
    pixman_color_t red = {0xffff, 0, 0, 0xffff};
    pixman_rectangle16_t rect = {0, 0, 1, 1};
    pixman_image_t *image = pixman_image_create_bits(
        PIXMAN_a8r8g8b8, 1, 1, &pixel, sizeof(pixel));
    if (image == NULL)
        return 1;
    if (!pixman_image_fill_rectangles(PIXMAN_OP_SRC, image, &red, 1, &rect)) {
        pixman_image_unref(image);
        return 2;
    }
    pixman_image_unref(image);
    return pixel == 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs pixman-1) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
