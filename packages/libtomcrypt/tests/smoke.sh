#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtomcrypt libtomcrypt-devel
test "$(pkg-config --modversion libtomcrypt)" = 1.18.2
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libtomcrypt-smoke.c" <<'EOF'
#include <tomcrypt.h>

int main(void) {
    if (register_all_ciphers() != CRYPT_OK)
        return 1;
    if (register_all_hashes() != CRYPT_OK)
        return 2;
    if (find_cipher("aes") < 0)
        return 3;
    if (find_hash("sha256") < 0)
        return 4;
    return 0;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libtomcrypt)"
cc -Wall -Wextra -Werror "$smoke_dir/libtomcrypt-smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/libtomcrypt-smoke"
"$smoke_dir/libtomcrypt-smoke"
