#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcyaml libcyaml-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cyaml/cyaml.h>

#include <string.h>

int main(void) {
    return cyaml_version_str != NULL && strcmp(cyaml_version_str, "1.4.2") == 0
               ? 0
               : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libcyaml) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
