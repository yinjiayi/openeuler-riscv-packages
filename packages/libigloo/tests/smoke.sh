#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libigloo libigloo-devel
pkg-config --modversion igloo | grep -Fx '0.9.5'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <igloo/igloo.h>
#include <igloo/error.h>

int main(void) {
    const char *version = 0;
    int major = -1;
    int minor = -1;
    int patch = -1;

    if (igloo_version_get(&version, &major, &minor, &patch) != igloo_ERROR_NONE)
        return 1;
    if (version == 0 || major != 0 || minor != 9 || patch != 5)
        return 2;
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke" \
  $({ pkg-config --cflags --libs igloo; })
"$smoke_dir/smoke"
