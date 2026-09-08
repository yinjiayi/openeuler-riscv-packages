#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- popt popt-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <popt.h>
int main(void) {
    const char *argv[] = {"smoke", 0};
    poptContext context = poptGetContext("smoke", 1, argv, 0, 0);
    if (context == 0) return 1;
    poptFreeContext(context);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lpopt -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
