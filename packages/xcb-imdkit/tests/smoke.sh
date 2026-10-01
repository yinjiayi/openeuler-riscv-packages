#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- xcb-imdkit xcb-imdkit-devel
rpm -q --whatprovides 'pkgconfig(xcb-imdkit)'
test "$(pkg-config --modversion xcb-imdkit)" = '1.0.9'
rpm -ql xcb-imdkit-devel | grep -Fx '/usr/include/xcb-imdkit/encoding.h'
rpm -ql xcb-imdkit-devel | grep -E '/cmake/XCBImdkit/XCBImdkitConfig\.cmake$'

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <xcb-imdkit/encoding.h>

#include <stdlib.h>
#include <string.h>

int main(void) {
    static const char input[] = "xcb-imdkit \xe4\xbd\xa0\xe5\xa5\xbd";
    size_t compound_length = 0;
    size_t utf8_length = 0;
    char *compound;
    char *roundtrip;
    int result;

    xcb_compound_text_init();
    compound = xcb_utf8_to_compound_text(input, strlen(input),
                                         &compound_length);
    if (compound == NULL || compound_length == 0) {
        free(compound);
        return 1;
    }

    roundtrip = xcb_compound_text_to_utf8(compound, compound_length,
                                          &utf8_length);
    result = roundtrip != NULL && utf8_length == strlen(input) &&
             memcmp(roundtrip, input, utf8_length) == 0
                 ? 0
                 : 1;
    free(roundtrip);
    free(compound);
    return result;
}
EOF

cc=${CC:-cc}
read -r -a user_cflags <<<"${CFLAGS:-}"
read -r -a package_cflags <<<"$(pkg-config --cflags xcb-imdkit)"
read -r -a user_ldflags <<<"${LDFLAGS:-}"
read -r -a package_libs <<<"$(pkg-config --libs xcb-imdkit)"
"$cc" "${user_cflags[@]}" "${package_cflags[@]}" "$tmpdir/smoke.c" \
    "${user_ldflags[@]}" "${package_libs[@]}" -o "$tmpdir/smoke"
"$tmpdir/smoke"
