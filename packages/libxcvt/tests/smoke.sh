#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxcvt
pkg-config --modversion libxcvt | grep -Fx '0.1.3'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cvt 1920 1200 75 >"$smoke_dir/modeline.txt"
grep -F 'Modeline "1920x1200_75.00"' "$smoke_dir/modeline.txt"
grep -F '245.25' "$smoke_dir/modeline.txt"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libxcvt/libxcvt.h>
#include <stdlib.h>

int main(void)
{
    struct libxcvt_mode_info *mode =
        libxcvt_gen_mode_info(1920, 1200, 75.0f, false, false);
    if (mode == NULL)
        return 1;
    int result = mode->hdisplay != 1920 || mode->vdisplay != 1200 ||
                 mode->dot_clock == 0 || mode->htotal <= mode->hdisplay ||
                 mode->vtotal <= mode->vdisplay;
    free(mode);
    return result;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags libxcvt) \
  "$smoke_dir/smoke.c" $(pkg-config --libs libxcvt) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
