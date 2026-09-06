#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libunwind libunwind-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libunwind.h>

int main(void)
{
    unw_context_t context;
    return unw_getcontext(&context) == 0 ? 0 : 1;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libunwind)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
