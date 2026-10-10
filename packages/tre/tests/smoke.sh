#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- tre agrep tre-devel tre-help
agrep --version | grep -F '0.9.0'
test "$(printf 'RVA23\n' | agrep -1 'RVA24')" = 'RVA23'
pkg-config --modversion tre | grep -Fx '0.9.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/tre-smoke.c" <<'EOF'
#include <tre/tre.h>

int main(void) {
    regex_t expression;
    regmatch_t match;
    int status;
    if (tre_regcomp(&expression, "RVA[0-9]+", REG_EXTENDED) != REG_OK) {
        return 1;
    }
    status = tre_regexec(&expression, "openEuler-RVA23", 1, &match, 0);
    tre_regfree(&expression);
    if (status != REG_OK) {
        return 2;
    }
    return match.rm_so == 10 && match.rm_eo == 15 ? 0 : 3;
}
EOF
cc $({ pkg-config --cflags tre; }) "$smoke_dir/tre-smoke.c" \
  -o "$smoke_dir/tre-smoke" $({ pkg-config --libs tre; })
"$smoke_dir/tre-smoke"
