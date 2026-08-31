#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtsm libtsm-devel
pkg-config --modversion libtsm | grep -Fx '4.7.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libtsm-smoke.c" <<'EOF'
#include <libtsm.h>

int main(void) {
    struct tsm_screen *screen = NULL;
    int rc = tsm_screen_new(&screen, NULL, NULL);

    if (rc < 0 || screen == NULL)
        return 1;
    if (tsm_screen_resize(screen, 80, 24) < 0)
        return 2;
    if (tsm_screen_get_width(screen) != 80 ||
        tsm_screen_get_height(screen) != 24)
        return 3;
    tsm_screen_unref(screen);
    return 0;
}
EOF

cc "$smoke_dir/libtsm-smoke.c" -o "$smoke_dir/libtsm-smoke" \
  $({ pkg-config --cflags --libs libtsm; })
"$smoke_dir/libtsm-smoke"
