#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxmlb libxmlb-devel libxmlb-tests
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf '<root><item>expected</item></root>\n' > "$smoke_dir/sample.xml"
xb-tool compile "$smoke_dir/sample.xmlb" "$smoke_dir/sample.xml"
query_output=$(xb-tool query "$smoke_dir/sample.xmlb" 'root/item')
printf '%s\n' "$query_output" | grep -F 'RESULT:'
printf '%s\n' "$query_output" | grep -F 'expected'

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <xmlb.h>
#include <glib.h>

int main(void) {
    XbSilo *silo = xb_silo_new();
    if (silo == NULL) return 1;
    g_object_unref(silo);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs xmlb) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
