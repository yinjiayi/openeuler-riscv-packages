#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libunarr libunarr-devel
pkg-config --exists libunarr

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libunarr-smoke.c" <<'EOF'
#include <stdio.h>
#include <string.h>
#include <unarr.h>

int main(void) {
    static const unsigned char input[] = {0x11, 0x22, 0x33, 0x44};
    unsigned char output[sizeof(input)] = {0};
    ar_stream *stream = ar_open_memory(input, sizeof(input));

    if (stream == NULL)
        return 1;
    if (ar_read(stream, output, sizeof(output)) != sizeof(output)) {
        ar_close(stream);
        return 2;
    }
    if (memcmp(input, output, sizeof(input)) != 0) {
        ar_close(stream);
        return 3;
    }
    if (ar_tell(stream) != (off64_t)sizeof(input) ||
        !ar_seek(stream, 0, SEEK_SET)) {
        ar_close(stream);
        return 4;
    }
    ar_close(stream);
    return 0;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libunarr)"
cc "$smoke_dir/libunarr-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libunarr-smoke"
"$smoke_dir/libunarr-smoke"
