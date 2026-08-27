#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- yyjson yyjson-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <stdlib.h>
#include <string.h>
#include <yyjson.h>
int main(void) {
    yyjson_doc *doc = yyjson_read("{\"isa\":\"RVA23\",\"ok\":true}", 26, 0);
    if (!doc) return 1;
    yyjson_val *root = yyjson_doc_get_root(doc);
    const char *isa = yyjson_get_str(yyjson_obj_get(root, "isa"));
    int ok = isa && strcmp(isa, "RVA23") == 0 && yyjson_get_bool(yyjson_obj_get(root, "ok"));
    yyjson_doc_free(doc);
    return ok ? 0 : 2;
}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(pkg-config --cflags --libs yyjson)
"$d/smoke"
