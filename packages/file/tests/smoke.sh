#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- file file-libs file-devel file-help
file --version | grep -F 'file-5.48'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler RVA23\n' >"$smoke_dir/input.txt"
test "$(file -b --mime-type "$smoke_dir/input.txt")" = "text/plain"

cat >"$smoke_dir/libmagic-smoke.c" <<'EOF'
#include <magic.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    magic_t cookie = magic_open(MAGIC_MIME_TYPE);
    const char sample[] = "openEuler RVA23\n";
    const char *kind;
    if (cookie == NULL || magic_load(cookie, NULL) != 0) {
        return 1;
    }
    kind = magic_buffer(cookie, sample, sizeof(sample) - 1);
    if (kind == NULL || strcmp(kind, "text/plain") != 0) {
        magic_close(cookie);
        return 2;
    }
    puts(kind);
    magic_close(cookie);
    return 0;
}
EOF
cc $({ pkg-config --cflags libmagic; }) "$smoke_dir/libmagic-smoke.c" \
  -o "$smoke_dir/libmagic-smoke" $({ pkg-config --libs libmagic; })
test "$("$smoke_dir/libmagic-smoke")" = "text/plain"
