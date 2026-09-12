#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmicrodns libmicrodns-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <microdns/microdns.h>

int main(void) {
    char message[128] = {0};
    if (MDNS_PORT != 5353) return 1;
    if (mdns_strerror(0, message, sizeof(message)) >= 0) return 2;
    return message[0] == '\0' ? 0 : 3;
}
EOF

${CC:-cc} ${CFLAGS:-} "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs microdns) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
