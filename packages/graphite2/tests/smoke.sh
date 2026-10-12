#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- graphite2 graphite2-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

if gr2fonttest >"$smoke_dir/gr2fonttest.log" 2>&1; then
  exit 1
fi
grep -F -- 'Usage:' "$smoke_dir/gr2fonttest.log" >/dev/null

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <graphite2/Font.h>

int main(void) {
    int major = 0;
    int minor = 0;
    int bugfix = 0;
    gr_engine_version(&major, &minor, &bugfix);
    return major == 1 && minor == 3 && bugfix == 15 ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" -lgraphite2 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
