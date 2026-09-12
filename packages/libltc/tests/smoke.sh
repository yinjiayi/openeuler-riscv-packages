#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libltc libltc-devel
rpm -q --provides libltc | grep -F 'libltc.so.11()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libltc-smoke.c" <<'EOF'
#include <ltc.h>

int main(void) {
    LTCEncoder *encoder = ltc_encoder_create(48000.0, 25.0, LTC_TV_625_50, 0);
    if (encoder == 0)
        return 1;
    ltc_encoder_free(encoder);
    return 0;
}
EOF
cc $({ pkg-config --cflags ltc; }) \
  "$smoke_dir/libltc-smoke.c" -o "$smoke_dir/libltc-smoke" \
  $({ pkg-config --libs ltc; })
"$smoke_dir/libltc-smoke"
