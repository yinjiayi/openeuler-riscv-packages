#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- google-crc32c google-crc32c-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/crc32c-smoke.cc" <<'EOF'
#include <cstdint>
#include <crc32c/crc32c.h>

int main() {
    const std::uint8_t input[] = "123456789";
    return crc32c_value(input, sizeof(input) - 1) == UINT32_C(0xe3069283) ? 0 : 1;
}
EOF
c++ -std=c++11 "$smoke_dir/crc32c-smoke.cc" -lcrc32c -o "$smoke_dir/crc32c-smoke"
"$smoke_dir/crc32c-smoke"
