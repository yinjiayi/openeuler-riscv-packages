#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libbgpdump libbgpdump-devel
bgpdump -T
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/check.c" <<'EOF'
#include <bgpdump_lib.h>
int main(void) {
    BGPDUMP *(*volatile open_fn)(const char *) = bgpdump_open_dump;
    void (*volatile close_fn)(BGPDUMP *) = bgpdump_close_dump;
    return open_fn == 0 || close_fn == 0;
}
EOF
cc "$smoke_dir/check.c" -lbgpdump -o "$smoke_dir/check"
"$smoke_dir/check"
