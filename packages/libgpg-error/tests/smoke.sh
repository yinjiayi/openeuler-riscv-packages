#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libgpg-error libgpg-error-devel
gpg-error --version
test "$(pkg-config --modversion gpg-error)" = 1.61

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/smoke.c" <<'EOF'
#include <gpg-error.h>
#include <stdio.h>

int main(void)
{
    gpg_error_t error = gpg_error(GPG_ERR_INV_VALUE);
    const char *message = gpg_strerror(error);
    if (message == NULL || *message == '\0') {
        return 1;
    }
    puts(message);
    return 0;
}
EOF
gcc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs gpg-error) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
