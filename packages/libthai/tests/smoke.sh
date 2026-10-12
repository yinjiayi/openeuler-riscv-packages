#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libthai libthai-devel
test -s /usr/share/libthai/thbrk.tri
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <thai/thctype.h>

int main(void) {
    return th_isthai(0xa1) ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libthai) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
