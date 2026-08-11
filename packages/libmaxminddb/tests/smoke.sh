#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmaxminddb libmaxminddb-devel
mmdblookup --version
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <maxminddb.h>
int main(void) {
    const char *version = MMDB_lib_version();
    return version != 0 && version[0] != '\0' ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libmaxminddb) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
