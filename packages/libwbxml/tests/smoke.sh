#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libwbxml libwbxml-devel
pkg-config --print-errors --modversion libwbxml2 | grep -Fx '0.11.10'
command -v wbxml2xml >/dev/null
command -v xml2wbxml >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <wbxml/wbxml.h>

int main(void)
{
    const WB_UTINY *message = wbxml_errors_string(WBXML_OK);
    return message != 0 && message[0] != '\0' ? 0 : 1;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags libwbxml2) \
  "$smoke_dir/smoke.c" $(pkg-config --libs libwbxml2) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
