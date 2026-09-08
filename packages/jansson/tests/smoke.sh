#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jansson jansson-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <jansson.h>
#include <string.h>

int main(void) {
    json_error_t error;
    json_t *root = json_loads("{\"arch\":\"riscv64\",\"isa\":\"RVA23\"}", 0, &error);
    const char *arch;
    const char *isa;
    int result;
    if (root == NULL) return 1;
    arch = json_string_value(json_object_get(root, "arch"));
    isa = json_string_value(json_object_get(root, "isa"));
    result = arch == NULL || isa == NULL || strcmp(arch, "riscv64") != 0 || strcmp(isa, "RVA23") != 0;
    json_decref(root);
    return result;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs jansson) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
