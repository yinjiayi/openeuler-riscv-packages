#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXmu
pkg-config --modversion xmu | grep -Fx '1.3.1'
pkg-config --modversion xmuu | grep -Fx '1.3.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xmu/CharSet.h>
#include <X11/Xmu/Converters.h>

int main(void)
{
    void (*volatile converter)(XrmValue *, Cardinal *, XrmValuePtr, XrmValuePtr)
        = XmuCvtStringToBackingStore;
    return converter == 0 || XmuCompareISOLatin1("AbC", "aBc") != 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xmu xmuu) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xmu xmuu) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
