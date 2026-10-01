#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libgcrypt libgcrypt-devel
test "$(pkg-config --modversion libgcrypt)" = 1.12.2
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <gcrypt.h>

int main(void)
{
    if (!gcry_check_version("1.12.2")) {
        return 1;
    }
    gcry_control(GCRYCTL_INITIALIZATION_FINISHED, 0);
    return 0;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libgcrypt)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
