#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- erfa erfa-devel
pkg-config --modversion erfa | grep -Fx '2.0.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/erfa-smoke.c" <<'EOF'
#include <math.h>
#include <erfa.h>

int main(void) {
    double djm0;
    double djm;

    if (eraCal2jd(2000, 1, 1, &djm0, &djm) != 0)
        return 1;
    if (fabs(djm0 - 2400000.5) > 1e-9)
        return 2;
    return fabs(djm - 51544.0) > 1e-9 ? 3 : 0;
}
EOF
cc "$smoke_dir/erfa-smoke.c" -o "$smoke_dir/erfa-smoke" \
  $({ pkg-config --cflags --libs erfa; })
"$smoke_dir/erfa-smoke"
