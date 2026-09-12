#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdisplay-info libdisplay-info-tools libdisplay-info-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libdisplay-info/cta-vic.h>

int main(void) {
    struct di_cta_vic vic = { .code = 16 };
    const struct di_cta_vic_video_format *format =
        di_cta_vic_video_format_from_vic(vic);
    if (!format) return 1;
    if (format->h_active != 1920 || format->v_active != 1080) return 2;
    if (format->interlaced) return 3;
    if (di_cta_vic_video_format_to_vic(format).code != vic.code) return 4;
    return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs libdisplay-info) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

if di-edid-decode </dev/null >"$smoke_dir/empty.log" 2>&1; then
  echo "di-edid-decode unexpectedly accepted empty input" >&2
  exit 5
fi
grep -F -- "di_edid_parse failed" "$smoke_dir/empty.log"
