#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libucl libucl-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

printf 'answer = 42;\n' >"$smoke_dir/input.ucl"
ucl_tool --in "$smoke_dir/input.ucl" --format json >"$smoke_dir/output.json"
grep -Eq '"answer"[[:space:]]*:[[:space:]]*42' "$smoke_dir/output.json"

cat >"$smoke_dir/libucl-smoke.c" <<'EOF'
#include <ucl.h>

int main(void) {
    struct ucl_parser *parser = ucl_parser_new(0);
    const ucl_object_t *root;
    const ucl_object_t *answer;

    if (parser == NULL)
        return 1;
    if (!ucl_parser_add_string(parser, "answer = 42;", 12))
        return 2;
    root = ucl_parser_get_object(parser);
    answer = ucl_object_lookup(root, "answer");
    if (answer == NULL || ucl_object_toint(answer) != 42)
        return 3;
    ucl_object_unref(root);
    ucl_parser_free(parser);
    return 0;
}
EOF

cc "$smoke_dir/libucl-smoke.c" -o "$smoke_dir/libucl-smoke" -lucl
"$smoke_dir/libucl-smoke"
