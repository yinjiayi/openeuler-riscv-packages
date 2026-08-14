#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- recode recode-devel recode-help
recode --version | grep -F 'recode 3.7.15'

converted=$(printf '\351\n' | recode ISO-8859-1..UTF-8 | od -An -tx1 | tr -d ' \n')
test "$converted" = 'c3a90a'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/recode-smoke.c" <<'EOF'
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <recode.h>

int main(void) {
    RECODE_OUTER outer = recode_new_outer(0);
    if (outer == NULL) {
        return 1;
    }
    return recode_delete_outer(outer) ? 0 : 2;
}
EOF
cc "$smoke_dir/recode-smoke.c" -o "$smoke_dir/recode-smoke" -lrecode
"$smoke_dir/recode-smoke"
