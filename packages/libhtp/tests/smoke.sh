#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libhtp libhtp-devel
test "$(pkg-config --modversion htp)" = 0.5.53

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <htp/htp.h>
#include <htp/htp_config.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    htp_cfg_t *cfg = htp_config_create();
    if (cfg == NULL) return 1;
    const char *version = htp_get_version();
    int ok = version != NULL && strcmp(version, "LibHTP v0.5.53") == 0;
    htp_config_destroy(cfg);
    return ok ? 0 : 2;
}
EOF
read -r -a pkg_config_flags <<<"$(pkg-config --cflags --libs htp)"
cc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  "${pkg_config_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
