#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- expat expat-devel
xmlwf -v
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <expat.h>
#include <string.h>
int main(void) {
    const char xml[] = "<root><child/></root>";
    XML_Parser parser = XML_ParserCreate(NULL);
    if (parser == NULL) return 1;
    int ok = XML_Parse(parser, xml, (int)strlen(xml), XML_TRUE);
    XML_ParserFree(parser);
    return ok == XML_STATUS_OK ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -lexpat -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
