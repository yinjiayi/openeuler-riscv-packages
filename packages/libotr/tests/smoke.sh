#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libotr libotr-devel
test "$(pkg-config --modversion libotr)" = "4.1.1"
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libotr/proto.h>

#include <stdio.h>
#include <string.h>

int main(void)
{
    const char *version = otrl_version();
    if (version == NULL || strcmp(version, "4.1.1") != 0) {
        return 1;
    }
    puts(version);
    return 0;
}
EOF
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs libotr) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
