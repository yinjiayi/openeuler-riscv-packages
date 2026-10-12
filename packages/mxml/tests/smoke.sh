#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mxml mxml-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <mxml.h>

#include <stdlib.h>
#include <string.h>

int main(void) {
    mxml_node_t *xml = mxmlNewXML("1.0");
    mxml_node_t *root = mxmlNewElement(xml, "openEuler");
    char *text = mxmlSaveAllocString(xml, NULL);
    const int ok = root != NULL && text != NULL && strstr(text, "openEuler") != NULL;
    free(text);
    mxmlDelete(xml);
    return ok ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs mxml4) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
