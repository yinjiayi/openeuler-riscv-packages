#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- wget2 wget2-libs wget2-devel
wget2 --version | grep -F -- 'GNU Wget2 2.2.1' >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <wget.h>

int main(void) {
    wget_global_init(0);
    wget_global_deinit();
    return 0;
}
EOF

cc $(pkg-config --cflags libwget) "$smoke_dir/smoke.c" \
  $(pkg-config --libs libwget) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
