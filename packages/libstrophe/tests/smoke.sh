#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libstrophe libstrophe-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '#include <strophe.h>\nint main(void){xmpp_ctx_t*c=xmpp_ctx_new(0,0);if(!c)return 1;xmpp_ctx_free(c);return 0;}\n' >"$d/a.c"
gcc "$d/a.c" -o "$d/a" $(pkg-config --cflags --libs libstrophe)
"$d/a"
