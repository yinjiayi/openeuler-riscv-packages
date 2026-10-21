#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- giflib giflib-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <gif_lib.h>

int main(int argc, char **argv) {
    int error = 0;
    GifFileType *gif;
    if (argc != 2 || GIFLIB_MAJOR < 6)
        return 1;
    gif = EGifOpenFileName(argv[1], 0, &error);
    if (gif == NULL)
        return 2;
    if (EGifPutScreenDesc(gif, 1, 1, 8, 0, NULL) == GIF_ERROR)
        return 3;
    return EGifCloseFile(gif, &error) == GIF_ERROR;
}
EOF

cc "$smoke_dir/smoke.c" -lgif -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/api.gif"
giftext "$smoke_dir/api.gif" >/dev/null
