#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsamplerate libsamplerate-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <math.h>
#include <samplerate.h>
int main(void) {
    float in[4] = {0.0f, 0.25f, -0.25f, 0.0f}, out[8] = {0};
    SRC_DATA d = {.data_in=in, .data_out=out, .input_frames=4,
                  .output_frames=8, .src_ratio=2.0, .end_of_input=1};
    if (src_simple(&d, SRC_SINC_FASTEST, 1) != 0) return 1;
    return d.output_frames_gen > 0 ? 0 : 2;
}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(pkg-config --cflags --libs samplerate) -lm
"$d/smoke"
