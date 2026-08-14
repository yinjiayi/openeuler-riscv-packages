#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- json-c json-c-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <json-c/json.h>
int main(void) {
    struct json_object *object = json_tokener_parse("{\"arch\":\"riscv64\"}");
    if (object == 0) return 1;
    json_object_put(object);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -ljson-c -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
