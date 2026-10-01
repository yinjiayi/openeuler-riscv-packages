#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libunistring libunistring-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdint.h>
#include <unistr.h>

int main(void) {
  const uint8_t text[] = {'A', 0xc3, 0xa9, 0};
  return u8_strlen(text) == 2 ? 0 : 1;
}
EOF

cc -Wall -Werror "$smoke_dir/smoke.c" -o "$smoke_dir/smoke" -lunistring
"$smoke_dir/smoke"
