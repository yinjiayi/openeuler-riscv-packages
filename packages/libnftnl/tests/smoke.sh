#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libnftnl libnftnl-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libnftnl/table.h>

#include <string.h>

int main(void) {
    struct nftnl_table *table = nftnl_table_alloc();
    const char *name;

    if (table == NULL)
        return 1;
    nftnl_table_set_str(table, NFTNL_TABLE_NAME, "b26");
    name = nftnl_table_get_str(table, NFTNL_TABLE_NAME);
    if (name == NULL || strcmp(name, "b26") != 0) {
        nftnl_table_free(table);
        return 2;
    }
    nftnl_table_free(table);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libnftnl) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
