#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtomcrypt libtomcrypt-devel
test "$(pkg-config --modversion libtomcrypt)" = 1.18.2
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <tomcrypt.h>

int main(void)
{
    unsigned char digest[32];
    const unsigned char input[] = "openEuler";
    register_hash(&sha256_desc);
    if (sha256(input, sizeof(input) - 1, digest) != CRYPT_OK) {
        return 1;
    }
    return digest[0] == 0 ? 1 : 0;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libtomcrypt)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
