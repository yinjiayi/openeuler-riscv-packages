#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtermkey libtermkey-devel
rpm -q --provides libtermkey | grep -F 'libtermkey.so.1()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libtermkey-smoke.c" <<'EOF'
#include <string.h>
#include <termkey.h>

int main(void) {
    TermKey *termkey = termkey_new_abstract("xterm", TERMKEY_FLAG_UTF8);
    TermKeyKey key;
    char formatted[32];
    const char input[] = "A";
    if (termkey == 0)
        return 1;
    if (termkey_push_bytes(termkey, input, strlen(input)) != strlen(input))
        return 2;
    if (termkey_getkey(termkey, &key) != TERMKEY_RES_KEY)
        return 3;
    if (termkey_strfkey(termkey, formatted, sizeof(formatted), &key,
                        TERMKEY_FORMAT_VIM) == 0)
        return 4;
    termkey_destroy(termkey);
    return strcmp(formatted, "A") == 0 ? 0 : 5;
}
EOF
cc $({ pkg-config --cflags termkey; }) \
  "$smoke_dir/libtermkey-smoke.c" -o "$smoke_dir/libtermkey-smoke" \
  $({ pkg-config --libs termkey; })
"$smoke_dir/libtermkey-smoke"
