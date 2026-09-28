#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmicrohttpd libmicrohttpd-devel
test "$(pkg-config --modversion libmicrohttpd)" = 1.0.10

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
#include <microhttpd.h>
#include <string.h>

int main(void) {
  const char *version = MHD_get_version();
  if (!version || strcmp(version, "1.0.10") != 0)
    return 1;
  return MHD_is_feature_supported(MHD_FEATURE_TLS) == MHD_YES ? 0 : 1;
}
C

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libmicrohttpd) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
