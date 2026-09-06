#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsoxr libsoxr-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '#include <soxr.h>\nint main(void){soxr_error_t e=0;soxr_t s=soxr_create(48000,44100,1,&e,0,0,0);if(!s||e)return 1;soxr_delete(s);return 0;}\n' >"$d/a.c"
gcc "$d/a.c" -o "$d/a" $(pkg-config --cflags --libs soxr)
"$d/a"
