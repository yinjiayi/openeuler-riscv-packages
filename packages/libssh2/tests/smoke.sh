#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libssh2 libssh2-devel
test "$(rpm -q --qf '%{VERSION}' libssh2)" = '1.11.1'
test -e "$(rpm --eval '%{_libdir}')/libssh2.so.1"
test "$(pkg-config --modversion libssh2)" = '1.11.1'
test -f /usr/include/libssh2.h

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libssh2.h>

int main(void) {
    if (libssh2_init(LIBSSH2_INIT_NO_CRYPTO) != 0)
        return 1;
    libssh2_exit();
    return 0;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libssh2)"
cc "$smoke_dir/smoke.c" "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
