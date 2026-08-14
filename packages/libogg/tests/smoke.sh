#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libogg libogg-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <ogg/ogg.h>

int main(void) {
    ogg_sync_state sync;
    ogg_stream_state stream;
    if (ogg_sync_init(&sync) != 0) return 1;
    if (ogg_stream_init(&stream, 23) != 0) {
        ogg_sync_clear(&sync);
        return 2;
    }
    if (ogg_stream_clear(&stream) != 0) return 3;
    return ogg_sync_clear(&sync) == 0 ? 0 : 4;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs ogg) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
