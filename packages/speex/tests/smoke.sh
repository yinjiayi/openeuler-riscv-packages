#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- speex speex-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '#include <speex/speex.h>\nint main(void){void*s=speex_encoder_init(&speex_nb_mode);if(!s)return 1;speex_encoder_destroy(s);return 0;}\n' >"$d/a.c"
gcc "$d/a.c" -o "$d/a" $(pkg-config --cflags --libs speex)
"$d/a"
