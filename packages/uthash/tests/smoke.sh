#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- uthash
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdlib.h>
#include <uthash.h>
struct item {
    int id;
    UT_hash_handle hh;
};
int main(void) {
    struct item *table = 0;
    struct item *entry = malloc(sizeof(*entry));
    struct item *found = 0;
    int key = 23;
    if (entry == 0) return 1;
    entry->id = key;
    HASH_ADD_INT(table, id, entry);
    HASH_FIND_INT(table, &key, found);
    if (found != entry) return 1;
    HASH_DEL(table, entry);
    free(entry);
    return table == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
