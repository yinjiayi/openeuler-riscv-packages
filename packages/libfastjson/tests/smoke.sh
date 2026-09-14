#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libfastjson libfastjson-devel
test "$(pkg-config --modversion libfastjson)" = 1.2609.0

smoke_dir=$(mktemp -d)
trap 'rm -r -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <json.h>
#include <string.h>

int main(void)
{
    struct fjson_object *root;
    struct fjson_object *isa = NULL;
    struct fjson_object *ok = NULL;
    int passed;

    root = fjson_tokener_parse("{\"isa\":\"RVA23\",\"ok\":true}");
    passed = root != NULL &&
        fjson_object_object_get_ex(root, "isa", &isa) &&
        strcmp(fjson_object_get_string(isa), "RVA23") == 0 &&
        fjson_object_object_get_ex(root, "ok", &ok) &&
        fjson_object_get_boolean(ok);
    if (root != NULL)
        fjson_object_put(root);
    return passed ? 0 : 1;
}
EOF

read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libfastjson)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
    "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
