#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmobi libmobi-devel
rpm -q --provides libmobi | grep -F 'libmobi.so.0()(64bit)'
mobitool -v | grep -F 'libmobi: 0.12'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libmobi-smoke.c" <<'EOF'
#include <mobi.h>
#include <string.h>

int main(void) {
    const char *version = mobi_version();
    return version == NULL || strcmp(version, "0.12") != 0;
}
EOF
cc "$smoke_dir/libmobi-smoke.c" -o "$smoke_dir/libmobi-smoke" \
  $({ pkg-config --cflags --libs libmobi; })
"$smoke_dir/libmobi-smoke"
