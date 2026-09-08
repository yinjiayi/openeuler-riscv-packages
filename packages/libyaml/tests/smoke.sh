#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libyaml libyaml-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <yaml.h>
int main(void) {
    yaml_parser_t parser;
    if (!yaml_parser_initialize(&parser)) return 1;
    yaml_parser_delete(&parser);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lyaml -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
