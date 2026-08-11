#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmd libmd-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <md5.h>
#include <string.h>
int main(void) {
    char digest[MD5_DIGEST_STRING_LENGTH];
    return MD5Data((const unsigned char *)"abc", 3, digest) != 0 &&
           strcmp(digest, "900150983cd24fb0d6963f7d28e17f72") == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libmd) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
