#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblo liblo-tools liblo-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lo/lo.h>
#include <string.h>

int main(void) {
    lo_address address = lo_address_new("127.0.0.1", "9000");
    if (!address) return 1;
    if (lo_address_get_protocol(address) != LO_UDP) return 2;
    if (strcmp(lo_address_get_port(address), "9000") != 0) return 3;
    lo_address_free(address);
    return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs liblo) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
