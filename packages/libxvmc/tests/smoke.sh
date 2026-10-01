#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXvMC
for module in xvmc xvmc-wrapper; do
  module_version=$(pkg-config --print-errors --modversion "$module")
  printf '%s version: %s\n' "$module" "$module_version"
  test "$module_version" = '1.0.15'
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <dlfcn.h>
#include <stdio.h>
#include <X11/Xlib.h>
#include <X11/extensions/XvMClib.h>
#include <X11/extensions/vldXvMC.h>

int main(void)
{
    static const struct {
        const char *library;
        const char *symbols[2];
    } checks[] = {
        {"libXvMC.so.1", {"XvMCQueryVersion", "XvMCListSurfaceTypes"}},
        {"libXvMCW.so.1", {"XvMCQueryVersion", "XvMCCreateContext"}}
    };
    for (unsigned int i = 0; i < sizeof(checks) / sizeof(checks[0]); i++) {
        void *handle = dlopen(checks[i].library, RTLD_NOW);
        if (!handle) {
            fprintf(stderr, "%s: %s\n", checks[i].library, dlerror());
            return 1;
        }
        for (unsigned int j = 0; j < 2; j++) {
            if (!dlsym(handle, checks[i].symbols[j])) {
                fprintf(stderr, "%s: missing %s\n", checks[i].library,
                        checks[i].symbols[j]);
                dlclose(handle);
                return 1;
            }
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
