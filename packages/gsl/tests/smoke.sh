#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gsl gsl-devel gsl-help
gsl-config --version | grep -Fx '2.8'
pkg-config --modversion gsl | grep -Fx '2.8'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/gsl-smoke.c" <<'EOF'
#include <gsl/gsl_sf_bessel.h>
#include <math.h>

int main(void) {
    const double value = gsl_sf_bessel_J0(0.0);
    return fabs(value - 1.0) < 1.0e-14 ? 0 : 1;
}
EOF
cc $({ pkg-config --cflags gsl; }) "$smoke_dir/gsl-smoke.c" \
  -o "$smoke_dir/gsl-smoke" $({ pkg-config --libs gsl; })
"$smoke_dir/gsl-smoke"
