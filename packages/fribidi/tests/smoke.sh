#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- fribidi fribidi-devel fribidi-help
fribidi --version | grep -F '1.0.16'
test "$(printf 'RVA23\n' | fribidi --nopad)" = 'RVA23'
pkg-config --modversion fribidi | grep -Fx '1.0.16'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/fribidi-smoke.c" <<'EOF'
#include <fribidi.h>
#include <stddef.h>

int main(void) {
    const FriBidiChar logical[] = {'R', 'V', 'A', '2', '3'};
    FriBidiChar visual[5] = {0};
    FriBidiParType direction = FRIBIDI_PAR_ON;
    size_t i;
    if (fribidi_log2vis(logical, 5, &direction, visual, NULL, NULL, NULL) == 0) {
        return 1;
    }
    for (i = 0; i < 5; ++i) {
        if (visual[i] != logical[i]) {
            return 2;
        }
    }
    return 0;
}
EOF
cc $({ pkg-config --cflags fribidi; }) "$smoke_dir/fribidi-smoke.c" \
  -o "$smoke_dir/fribidi-smoke" $({ pkg-config --libs fribidi; })
"$smoke_dir/fribidi-smoke"
