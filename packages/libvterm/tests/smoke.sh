#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libvterm libvterm-devel
rpm -q --provides libvterm | grep -F 'libvterm.so.0()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf '\033[31mRVA23\033[0m' | vterm-dump >"$smoke_dir/dump"
test -s "$smoke_dir/dump"

cat >"$smoke_dir/libvterm-smoke.c" <<'EOF'
#include <vterm.h>

int main(void) {
    VTerm *terminal = vterm_new(24, 80);
    VTermScreen *screen;
    if (terminal == 0)
        return 1;
    screen = vterm_obtain_screen(terminal);
    vterm_screen_reset(screen, 1);
    vterm_free(terminal);
    return 0;
}
EOF
cc $({ pkg-config --cflags vterm; }) \
  "$smoke_dir/libvterm-smoke.c" -o "$smoke_dir/libvterm-smoke" \
  $({ pkg-config --libs vterm; })
"$smoke_dir/libvterm-smoke"
