#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- fftw fftw-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <fftw3.h>
int main(void) {
    fftw_complex in[4] = {{1,0}, {2,0}, {3,0}, {4,0}};
    fftw_complex out[4];
    fftw_plan plan = fftw_plan_dft_1d(4, in, out, FFTW_FORWARD, FFTW_ESTIMATE);
    if (plan == 0) return 1;
    fftw_execute(plan);
    fftw_destroy_plan(plan);
    return out[0][0] == 10.0 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -lfftw3 -lm -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
