#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxdg-basedir libxdg-basedir-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <basedir.h>

#include <string.h>

int main(void) {
    xdgHandle handle;
    const char *cache;
    int ok;

    if (xdgInitHandle(&handle) == NULL)
        return 1;
    cache = xdgCacheHome(&handle);
    ok = cache != NULL && strstr(cache, "xdg-cache") != NULL;
    xdgWipeHandle(&handle);
    return ok ? 0 : 2;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libxdg-basedir) -o "$smoke_dir/smoke"
XDG_CACHE_HOME="$smoke_dir/xdg-cache" "$smoke_dir/smoke"
