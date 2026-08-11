#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpng libpng-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <png.h>
#include <stdio.h>

int main(void) {
    png_structp writer;
    png_infop info;
    if (png_access_version_number() != PNG_LIBPNG_VER) return 1;
    writer = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (writer == NULL) return 2;
    info = png_create_info_struct(writer);
    if (info == NULL) {
        png_destroy_write_struct(&writer, NULL);
        return 3;
    }
    png_destroy_write_struct(&writer, &info);
    puts(PNG_LIBPNG_VER_STRING);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libpng) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" | grep -Fx '1.6.58'
