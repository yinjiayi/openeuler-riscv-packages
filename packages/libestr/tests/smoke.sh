#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/check.c" <<'EOF'
#include <stdio.h>
#include <libestr.h>
int main(void) { es_str_t *s = es_newStrFromCStr("RVA23", 5); if (!s || es_strlen(s) != 5) return 1; es_deleteStr(s); puts(es_version()); }
EOF
cc "$tmpdir/check.c" $(pkg-config --cflags --libs libestr) -o "$tmpdir/check"
"$tmpdir/check" | grep -Fx '0.1.11'
