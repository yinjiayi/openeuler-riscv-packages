#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libspng libspng-devel
pkg-config --modversion spng | grep -Fx '0.7.4'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libspng-smoke.c" <<'EOF'
#include <spng.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    static const unsigned char png_signature[8] = {
        0x89, 'P', 'N', 'G', '\r', '\n', 0x1a, '\n'
    };
    unsigned char pixel[4] = {0x12, 0x34, 0x56, 0xff};
    struct spng_ihdr ihdr = {
        .width = 1,
        .height = 1,
        .bit_depth = 8,
        .color_type = SPNG_COLOR_TYPE_TRUECOLOR_ALPHA,
        .compression_method = 0,
        .filter_method = 0,
        .interlace_method = 0,
    };
    spng_ctx *ctx = spng_ctx_new(SPNG_CTX_ENCODER);
    void *png;
    size_t png_size = 0;
    int error = 0;
    int ok;

    if (ctx == NULL || strcmp(spng_version_string(), "0.7.4") != 0)
        return 1;
    if (spng_set_option(ctx, SPNG_ENCODE_TO_BUFFER, 1) != 0 ||
        spng_set_ihdr(ctx, &ihdr) != 0 ||
        spng_encode_image(ctx, pixel, sizeof(pixel), SPNG_FMT_PNG,
                          SPNG_ENCODE_FINALIZE) != 0)
        return 2;
    png = spng_get_png_buffer(ctx, &png_size, &error);
    ok = png != NULL && error == 0 && png_size > sizeof(png_signature) &&
         memcmp(png, png_signature, sizeof(png_signature)) == 0;
    free(png);
    spng_ctx_free(ctx);
    return ok ? 0 : 3;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs spng)"
cc "$smoke_dir/libspng-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libspng-smoke"
"$smoke_dir/libspng-smoke"
