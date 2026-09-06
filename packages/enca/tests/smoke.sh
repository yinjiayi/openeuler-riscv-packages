#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- enca enca-devel
enca --version | grep -F '1.22'
enca --list converters | grep -Fx 'librecode'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <enca.h>

#include <stdio.h>
#include <string.h>

int main(void) {
    EncaEncoding encoding = enca_parse_encoding_name("UTF-8");
    const char *name;

    if (!enca_charset_is_known(encoding.charset)) {
        fputs("libenca did not recognize UTF-8\n", stderr);
        return 1;
    }

    /* The iconv spelling is optional when configure rejects target iconv. */
    name = enca_charset_name(encoding.charset, ENCA_NAME_STYLE_ENCA);
    if (name == NULL || strcmp(name, "UTF-8") != 0) {
        fprintf(stderr, "unexpected canonical UTF-8 name: %s\n",
                name == NULL ? "(null)" : name);
        return 1;
    }

    return 0;
}
EOF
read -r -a pc_flags <<<"$(pkg-config --cflags --libs enca)"
cc "$smoke_dir/smoke.c" "${pc_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
