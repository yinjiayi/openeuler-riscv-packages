#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libstemmer libstemmer-devel
test "$(printf 'connections\n' | stemwords -l english)" = "connect"

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libstemmer.h>
#include <string.h>

int main(void) {
    struct sb_stemmer *stemmer = sb_stemmer_new("english", "UTF_8");
    const sb_symbol *word;
    int ok;
    if (stemmer == NULL)
        return 1;
    word = sb_stemmer_stem(stemmer, (const sb_symbol *)"connections", 11);
    ok = word != NULL && sb_stemmer_length(stemmer) == 7 &&
         memcmp(word, "connect", 7) == 0;
    sb_stemmer_delete(stemmer);
    return ok ? 0 : 2;
}
EOF

cc "$smoke_dir/smoke.c" -lstemmer -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
