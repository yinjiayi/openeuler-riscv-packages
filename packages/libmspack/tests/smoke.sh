#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libmspack libmspack-devel
test "$(pkg-config --modversion libmspack)" = 0.11alpha
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <mspack.h>

int main(void)
{
    return mspack_version(MSPACK_VER_LIBRARY) > 0 ? 0 : 1;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs libmspack)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
