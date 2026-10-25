#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libgrapheme libgrapheme-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <grapheme.h>
#include <stdint.h>

int main(void)
{
    const char combined[] = "a\xcc\x81" "b";
    uint_least32_t cp = 0;
    if (grapheme_next_character_break_utf8(combined, sizeof(combined) - 1) != 3)
        return 1;
    if (grapheme_decode_utf8("A", 1, &cp) != 1 || cp != 'A')
        return 2;
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  "$smoke_dir/smoke.c" -lgrapheme -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
