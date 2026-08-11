#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- utf8proc utf8proc-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <utf8proc.h>
int main(void) {
    const char *version = utf8proc_version();
    return version != 0 && version[0] != '\0' ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libutf8proc) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
