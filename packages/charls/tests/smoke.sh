#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- CharLS CharLS-devel
pkg-config --modversion charls | grep -Fx '2.4.4'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/charls-smoke.c" <<'EOF'
#include <stdint.h>
#include <string.h>
#include <charls/charls.h>

int main(void) {
    int32_t major = 0;
    int32_t minor = 0;
    int32_t patch = 0;

    charls_get_version_number(&major, &minor, &patch);
    if (major != 2 || minor != 4 || patch != 4)
        return 1;
    return strcmp(charls_get_version_string(), "2.4.4") == 0 ? 0 : 2;
}
EOF
cc "$smoke_dir/charls-smoke.c" -o "$smoke_dir/charls-smoke" \
  $({ pkg-config --cflags --libs charls; })
"$smoke_dir/charls-smoke"
