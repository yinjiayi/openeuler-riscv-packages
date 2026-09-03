#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cwalk cwalk-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cwalk.h>
#include <string.h>

int main(void) {
    char output[32];
    size_t length = cwk_path_normalize("/srv/../opt//repo", output, sizeof(output));
    return length == strlen("/opt/repo") && strcmp(output, "/opt/repo") == 0 ? 0 : 1;
}
EOF
read -r -a pkg_flags <<<"$(pkg-config --cflags --libs cwalk)"
cc "$smoke_dir/smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
