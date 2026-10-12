#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXxf86vm
module_version=$(pkg-config --print-errors --modversion xxf86vm)
printf 'xxf86vm version: %s\n' "$module_version"
test "$module_version" = '1.1.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <dlfcn.h>
#include <X11/Xlib.h>
#include <X11/extensions/xf86vmode.h>

int main(void)
{
    void *handle = dlopen("libXxf86vm.so.1", RTLD_NOW);
    if (!handle || !dlsym(handle, "XF86VidModeQueryVersion") ||
        !dlsym(handle, "XF86VidModeGetAllModeLines")) {
        return 1;
    }
    dlclose(handle);
    return sizeof(XF86VidModeModeLine) > 0 ? 0 : 2;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xxf86vm) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xxf86vm) \
  -ldl -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
