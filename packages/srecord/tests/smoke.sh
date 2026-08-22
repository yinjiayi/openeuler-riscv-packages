#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- srecord srecord-devel libgcrypt-devel
for tool in srec_cat srec_cmp srec_info; do
  command -v "$tool"
  "$tool" -version 2>&1 | grep -F 'version 1.65.0'
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

srec_cat -generate 0 16 -constant 0xAA \
  -Output "$smoke_dir/image.srec" -Motorola
srec_info "$smoke_dir/image.srec" >"$smoke_dir/info.txt"
grep -F 'Data:   0000 - 000F' "$smoke_dir/info.txt"
srec_cat "$smoke_dir/image.srec" -Motorola \
  -Output "$smoke_dir/image.hex" -Intel
srec_cmp "$smoke_dir/image.srec" -Motorola \
  "$smoke_dir/image.hex" -Intel
grep -E '^S[0-9]' "$smoke_dir/image.srec"
grep -E '^:' "$smoke_dir/image.hex"

cat >"$smoke_dir/consumer.cc" <<'EOF'
#include <srecord/adler16.h>

int main() {
    srecord::adler16 checksum;
    checksum.next('a');
    return checksum.get() == 0x6262 ? 0 : 1;
}
EOF
g++ -std=c++17 -Wall -Wextra -Werror "$smoke_dir/consumer.cc" \
  -lsrecord -lgcrypt -o "$smoke_dir/consumer"
"$smoke_dir/consumer"
