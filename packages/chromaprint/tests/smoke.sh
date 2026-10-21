#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- chromaprint libchromaprint libchromaprint-devel
fpcalc -version | grep -F 'fpcalc version 1.6.1'
pkg-config --modversion libchromaprint | grep -Fx '1.6.1'
rpm -q --provides libchromaprint | grep -F 'libchromaprint.so.1()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/chromaprint-smoke.c" <<'EOF'
#include <chromaprint.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    ChromaprintContext *ctx;
    int16_t sample;
    FILE *raw;
    int i;

    if (strcmp(chromaprint_get_version(), "1.6.1") != 0)
        return 1;
    ctx = chromaprint_new(CHROMAPRINT_ALGORITHM_DEFAULT);
    if (ctx == NULL || chromaprint_get_algorithm(ctx) != CHROMAPRINT_ALGORITHM_DEFAULT)
        return 2;
    if (!chromaprint_start(ctx, 11025, 1))
        return 3;
    raw = fopen("tone.s16le", "wb");
    if (raw == NULL)
        return 4;
    for (i = 0; i < 132300; i++) {
        sample = (int16_t)(((i % 101) - 50) * 500);
        if (fwrite(&sample, sizeof(sample), 1, raw) != 1)
            return 5;
        if (!chromaprint_feed(ctx, &sample, 1))
            return 6;
    }
    if (fclose(raw) != 0 || !chromaprint_finish(ctx))
        return 7;
    chromaprint_free(ctx);
    return 0;
}
EOF

cc $({ pkg-config --cflags libchromaprint; }) \
  "$smoke_dir/chromaprint-smoke.c" -o "$smoke_dir/chromaprint-smoke" \
  $({ pkg-config --libs libchromaprint; })
(
  cd "$smoke_dir"
  ./chromaprint-smoke
  fpcalc -format s16le -rate 11025 -channels 1 -length 10 -json tone.s16le \
    | grep -F '"fingerprint"'
)
