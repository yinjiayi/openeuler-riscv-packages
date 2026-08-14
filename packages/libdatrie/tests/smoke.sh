#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdatrie libdatrie-devel
test -x /usr/bin/trietool
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <datrie/trie.h>
int main(void) {
    AlphaMap *map = alpha_map_new();
    if (!map || alpha_map_add_range(map, 'a', 'z') != 0) return 1;
    Trie *trie = trie_new(map);
    if (!trie) return 2;
    AlphaChar key[] = {'r','v','a',0};
    TrieData data = 0;
    if (!trie_store(trie, key, 23) ||
        !trie_retrieve(trie, key, &data) || data != 23) return 3;
    trie_free(trie);
    alpha_map_free(map);
    return 0;
}
EOF
read -r -a datrie_flags <<<"$(pkg-config --cflags --libs datrie-0.2)"
gcc "$d/smoke.c" -o "$d/smoke" "${datrie_flags[@]}"
"$d/smoke"
