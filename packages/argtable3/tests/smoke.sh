#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- argtable3 argtable3-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <argtable3.h>

int main(void) {
    char *argv[] = {"smoke", "--flag"};
    arg_lit_t *flag = arg_lit0("f", "flag", "set the flag");
    arg_end_t *end = arg_end(4);
    void *table[] = {flag, end};
    int errors = arg_parse(2, argv, table);
    int ok = errors == 0 && flag != 0 && flag->count == 1;
    arg_freetable(table, sizeof(table) / sizeof(table[0]));
    return ok ? 0 : 1;
}
EOF
read -r -a pkg_flags <<<"$(pkg-config --cflags --libs argtable3)"
cc "$smoke_dir/smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
