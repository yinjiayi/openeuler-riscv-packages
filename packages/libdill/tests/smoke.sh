#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdill libdill-devel
pkg-config --exists libdill
rpm -q --qf '%{VERSION}\n' libdill | grep -Fx '2.14'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libdill-smoke.c" <<'EOF'
#include <libdill.h>

int main(void) {
    return now() < 0;
}
EOF
cc $(pkg-config --cflags libdill) "$smoke_dir/libdill-smoke.c" \
  -o "$smoke_dir/libdill-smoke" $(pkg-config --libs libdill)
"$smoke_dir/libdill-smoke"
