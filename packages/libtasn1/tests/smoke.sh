#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtasn1 libtasn1-devel
asn1Parser --version | grep -F '4.21.0'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libtasn1.h>
int main(void) {
    const char *version = asn1_check_version(NULL);
    return version == 0 || version[0] == '\0';
}
EOF
cc "$smoke_dir/smoke.c" -ltasn1 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
