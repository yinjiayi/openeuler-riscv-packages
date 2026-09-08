#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cjson cjson-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cjson/cJSON.h>
int main(void) {
    cJSON *object = cJSON_Parse("{\"arch\":\"riscv64\"}");
    cJSON *arch;
    int ok;
    if (object == 0) return 1;
    arch = cJSON_GetObjectItemCaseSensitive(object, "arch");
    ok = cJSON_IsString(arch) && arch->valuestring != 0;
    cJSON_Delete(object);
    return ok ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libcjson) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
