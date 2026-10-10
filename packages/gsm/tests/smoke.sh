#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gsm gsm-devel
rpm -q --provides gsm | grep -F 'libgsm.so.1()(64bit)'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/gsm-smoke.c" <<'EOF'
#include <gsm.h>
int main(void) {
    gsm encoder = gsm_create(), decoder = gsm_create();
    gsm_signal input[160], output[160];
    gsm_byte frame[33];
    int nonzero = 0;
    if (!encoder || !decoder) return 1;
    for (int i = 0; i < 160; ++i) input[i] = (gsm_signal)((i % 80 - 40) * 128);
    gsm_encode(encoder, input, frame);
    if ((frame[0] >> 4) != GSM_MAGIC) return 2;
    if (gsm_decode(decoder, frame, output) != 0) return 3;
    for (int i = 0; i < 160; ++i) nonzero |= output[i];
    gsm_destroy(encoder);
    gsm_destroy(decoder);
    return nonzero == 0;
}
EOF
cc "$smoke_dir/gsm-smoke.c" -o "$smoke_dir/gsm-smoke" \
  $({ pkg-config --cflags --libs gsm; })
"$smoke_dir/gsm-smoke"
