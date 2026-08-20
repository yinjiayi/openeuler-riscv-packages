#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jsmn
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <jsmn/jsmn.h>

int main(void) {
    const char json[] = "{\"ok\":true}";
    jsmn_parser parser;
    jsmntok_t tokens[3];
    jsmn_init(&parser);
    return jsmn_parse(&parser, json, sizeof(json) - 1, tokens, 3) == 3 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
