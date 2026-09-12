#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- zvbi zvbi-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libzvbi.h>

int main(void) {
    unsigned int major = 0;
    unsigned int minor = 0;
    unsigned int micro = 0;
    vbi_decoder *decoder;

    vbi_version(&major, &minor, &micro);
    if (major != 0 || minor != 2 || micro != 45)
        return 1;
    decoder = vbi_decoder_new();
    if (decoder == 0)
        return 2;
    vbi_decoder_delete(decoder);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lzvbi -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
