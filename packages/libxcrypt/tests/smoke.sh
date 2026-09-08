#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libxcrypt libxcrypt-devel
test "$(pkg-config --modversion libxcrypt)" = 4.5.2

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/smoke.c" <<'EOF'
#define _GNU_SOURCE
#include <crypt.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    static const char setting[] = "$6$rounds=5000$openeuler$";
    struct crypt_data data = {0};
    char *hash = crypt_r("rva23", setting, &data);
    if (hash == NULL || strncmp(hash, setting, sizeof(setting) - 1) != 0) {
        return 1;
    }
    puts(hash);
    return 0;
}
EOF
gcc -Wall -Wextra -Werror "$smoke_dir/smoke.c" -lcrypt -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
