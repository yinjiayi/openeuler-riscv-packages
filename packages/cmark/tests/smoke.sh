#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cmark cmark-libs cmark-devel cmark-help
test "$(printf '%s\n' '**RVA23**' | cmark)" = '<p><strong>RVA23</strong></p>'
pkg-config --modversion libcmark | grep -Fx '0.31.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/cmark-smoke.c" <<'EOF'
#include <cmark.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    const char input[] = "**RVA23**\n";
    char *html = cmark_markdown_to_html(input, sizeof(input) - 1, CMARK_OPT_DEFAULT);
    int rc = 0;
    if (html == NULL || strcmp(html, "<p><strong>RVA23</strong></p>\n") != 0) {
        rc = 1;
    }
    free(html);
    return rc;
}
EOF
cc $({ pkg-config --cflags libcmark; }) "$smoke_dir/cmark-smoke.c" \
  -o "$smoke_dir/cmark-smoke" $({ pkg-config --libs libcmark; })
"$smoke_dir/cmark-smoke"
