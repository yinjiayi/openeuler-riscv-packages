#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- md4c md4c-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <md4c.h>

static int block(MD_BLOCKTYPE type, void *detail, void *userdata) {
    (void)type;
    (void)detail;
    ++*(int *)userdata;
    return 0;
}

static int span(MD_SPANTYPE type, void *detail, void *userdata) {
    (void)type;
    (void)detail;
    ++*(int *)userdata;
    return 0;
}

static int text(MD_TEXTTYPE type, const MD_CHAR *value, MD_SIZE size,
                void *userdata) {
    (void)type;
    (void)value;
    (void)size;
    ++*(int *)userdata;
    return 0;
}

int main(void) {
    static const MD_CHAR input[] = "# installed md4c\n";
    MD_PARSER parser = {0, MD_DIALECT_COMMONMARK, block, block,
                        span, span, text, 0, 0};
    int events = 0;
    return md_parse(input, sizeof(input) - 1, &parser, &events) != 0 ||
           events == 0;
}
EOF
read -r -a pc_flags <<<"$(pkg-config --cflags --libs md4c)"
cc "$smoke_dir/smoke.c" "${pc_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
printf '# installed md2html\n' | md2html | grep -F '<h1>installed md2html</h1>'
