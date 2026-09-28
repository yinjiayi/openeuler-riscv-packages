#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libfontenc libfontenc-devel
pkg-config --modversion fontenc | grep -Fx '1.1.9'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/fonts/fontenc.h>
#include <string.h>

int main(void) {
    FontEncPtr encoding = FontEncFind("iso8859-1", 0);
    FontMapPtr mapping = FontMapFind(encoding, FONT_ENCODING_UNICODE, 0, 0);
    const char *xlfd = "-misc-fixed-medium-r-normal--13-120-75-75-c-70-iso8859-1";
    char *name = FontEncFromXLFD(xlfd, strlen(xlfd));
    if (!encoding || !mapping || !name) return 1;
    if (strcmp(name, "iso8859-1") != 0) return 2;
    return FontEncRecode(0x41, mapping) == 0x41 ? 0 : 3;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs fontenc) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
