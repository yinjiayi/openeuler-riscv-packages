#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- SDL2_image SDL2_image-devel
pkg-config --exists 'SDL2_image = 2.8.8'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

printf '%s' 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=' \
  | base64 --decode >"$smoke_dir/pixel.png"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <SDL_image.h>

int main(int argc, char **argv) {
    const SDL_version *version = IMG_Linked_Version();
    SDL_Surface *image;
    if (argc != 2) return 1;
    if (version == NULL || version->major != 2 || version->minor != 8 || version->patch != 8) return 2;
    image = IMG_Load(argv[1]);
    if (image == NULL) return 3;
    return image->w == 1 && image->h == 1 ? 0 : 4;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs SDL2_image) \
  -o "$smoke_dir/pkgconfig-smoke"
SDL_VIDEODRIVER=dummy "$smoke_dir/pkgconfig-smoke" "$smoke_dir/pixel.png"
