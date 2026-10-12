#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcdio-paranoia libcdio-paranoia-devel
cd-paranoia --version
test "$(pkg-config --modversion libcdio_paranoia)" = "10.2+2.0.2"
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <cdio/paranoia/paranoia.h>

#include <stdio.h>
#include <string.h>

int main(void)
{
    const char *version = cdio_paranoia_version();
    if (version == NULL || strstr(version, "10.2") == NULL) {
        return 1;
    }
    puts(version);
    return 0;
}
EOF
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs libcdio_paranoia) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
