#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liba53 liba53-devel
rpm -q --provides liba53 | grep -F 'liba53.so.1()(64bit)'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/a53-smoke.cpp" <<'EOF'
#include <a53.h>
#include <cstring>

int main() {
    u8 key[8] = {0x2b, 0xd6, 0x45, 0x9f, 0x82, 0xc5, 0xbc, 0x00};
    u8 expected[15] = {0x88, 0x9e, 0xea, 0xaf, 0x9e, 0xd1, 0xba, 0x1a,
                       0xbb, 0xd8, 0x43, 0x62, 0x32, 0xe4, 0x40};
    u8 downlink[15], uplink[15];
    A53_GSM(key, 64, 0x24f20f, downlink, uplink);
    return std::memcmp(downlink, expected, sizeof expected) != 0;
}
EOF
c++ "$smoke_dir/a53-smoke.cpp" -o "$smoke_dir/a53-smoke" \
  $({ pkg-config --cflags --libs liba53; })
"$smoke_dir/a53-smoke"
