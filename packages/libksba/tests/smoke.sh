#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libksba libksba-devel
test "$(pkg-config --modversion ksba)" = 1.8.0

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/smoke.c" <<'EOF'
#include <ksba.h>
#include <stdio.h>

int main(void)
{
    const char *version = ksba_check_version(NULL);
    if (version == NULL || *version == '\0') {
        return 1;
    }
    puts(version);
    return 0;
}
EOF
gcc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs ksba) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
