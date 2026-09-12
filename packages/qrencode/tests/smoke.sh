#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- qrencode qrencode-devel qrencode-help
qrencode --version | grep -F 'qrencode version 4.1.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
qrencode --output="$smoke_dir/code.png" 'openEuler RVA23'
test -s "$smoke_dir/code.png"
signature=$(od -An -tx1 -N8 "$smoke_dir/code.png" | tr -d ' \n')
test "$signature" = '89504e470d0a1a0a'

cat >"$smoke_dir/qrencode-smoke.c" <<'EOF'
#include <qrencode.h>

int main(void) {
    QRcode *code = QRcode_encodeString("openEuler RVA23", 0, QR_ECLEVEL_M,
                                       QR_MODE_8, 1);
    if (code == 0 || code->width <= 0 || code->data == 0) {
        return 1;
    }
    QRcode_free(code);
    return 0;
}
EOF
cc $({ pkg-config --cflags libqrencode; }) \
  "$smoke_dir/qrencode-smoke.c" -o "$smoke_dir/qrencode-smoke" \
  $({ pkg-config --libs libqrencode; })
"$smoke_dir/qrencode-smoke"
