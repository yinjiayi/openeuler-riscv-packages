#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXvMC
test "$(pkg-config --modversion xvmc)" = '1.0.15'
test "$(pkg-config --modversion xvmc-wrapper)" = '1.0.15'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <dlfcn.h>
#include <X11/Xlib.h>
#include <X11/extensions/XvMClib.h>
#include <X11/extensions/vldXvMC.h>

int main(void)
{
    static const char *libraries[] = {"libXvMC.so.1", "libXvMCW.so.1"};
    for (unsigned int i = 0; i < sizeof(libraries) / sizeof(libraries[0]); i++) {
        void *handle = dlopen(libraries[i], RTLD_NOW);
        if (!handle || !dlsym(handle, "XvMCQueryVersion") ||
            !dlsym(handle, "XvMCCreateContext")) {
            return 1;
        }
        dlclose(handle);
    }
    return sizeof(XvMCContext) > 0 && XVMC_VLD != 0 ? 0 : 2;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xvmc xvmc-wrapper) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xvmc xvmc-wrapper) \
  -ldl -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
