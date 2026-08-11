#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libidn libidn-devel libidn-help
idn --version | grep -F 'idn (GNU Libidn) 1.44'
test "$(CHARSET=UTF-8 idn --quiet --idna-to-ascii 'bücher.example')" = \
  'xn--bcher-kva.example'
test "$(CHARSET=UTF-8 idn --quiet --idna-to-unicode 'xn--bcher-kva.example')" = \
  'bücher.example'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libidn-smoke.c" <<'EOF'
#include <idna.h>
#include <idn-free.h>
#include <string.h>

int main(void) {
    const char input[] = "\x62\xc3\xbc\x63\x68\x65\x72\x2e\x65\x78\x61\x6d\x70\x6c\x65";
    char *output = NULL;
    int rc = idna_to_ascii_8z(input, &output, 0);
    if (rc != IDNA_SUCCESS || output == NULL) {
        return 1;
    }
    rc = strcmp(output, "xn--bcher-kva.example") == 0 ? 0 : 2;
    idn_free(output);
    return rc;
}
EOF
cc $({ pkg-config --cflags libidn; }) "$smoke_dir/libidn-smoke.c" \
  -o "$smoke_dir/libidn-smoke" $({ pkg-config --libs libidn; })
"$smoke_dir/libidn-smoke"
