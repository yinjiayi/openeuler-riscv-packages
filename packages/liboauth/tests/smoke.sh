#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liboauth liboauth-devel
rpm -q --provides liboauth | grep -F 'liboauth.so.0()(64bit)'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/oauth-smoke.c" <<'EOF'
#include <oauth.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char input[] = "RISC V?&";
    char *escaped = oauth_url_escape(input);
    char *decoded;
    size_t length = 0;
    if (!escaped || strcmp(escaped, "RISC%20V%3F%26") != 0) return 1;
    decoded = oauth_url_unescape(escaped, &length);
    if (!decoded || length != strlen(input) || strcmp(decoded, input) != 0) return 2;
    free(decoded);
    free(escaped);
    return 0;
}
EOF
cc "$smoke_dir/oauth-smoke.c" -o "$smoke_dir/oauth-smoke" \
  $({ pkg-config --cflags --libs oauth; })
"$smoke_dir/oauth-smoke"
