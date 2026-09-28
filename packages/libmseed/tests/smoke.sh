#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmseed libmseed-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/check.c" <<'EOF'
#include <libmseed.h>
#include <string.h>
int main(void) {
    char text[64];
    nstime_t time = ms_time2nstime(2004, 133, 7, 8, 9, 123456788);
    if (time == NSTERROR) return 1;
    if (!ms_nstime2timestr_n(time, text, sizeof(text), SEEDORDINAL,
                             NANO_MICRO_NONE)) return 2;
    return strcmp(text, "2004,133,07:08:09.123456788") == 0 ? 0 : 3;
}
EOF
cc "$smoke_dir/check.c" $(pkg-config --cflags --libs mseed) -o "$smoke_dir/check"
"$smoke_dir/check"
