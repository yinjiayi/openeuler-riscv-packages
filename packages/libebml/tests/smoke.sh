#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libebml libebml-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.cpp" <<'EOF'
#include <ebml/EbmlId.h>
#include <ebml/EbmlVersion.h>
#include <iostream>

int main() {
    const libebml::EbmlId id(0x1A45DFA3u, 4);
    libebml::binary bytes[4] = {};
    id.Fill(bytes);
    if (LIBEBML_VERSION != 0x010406 || id.GetLength() != 4 ||
        bytes[0] != 0x1a || bytes[1] != 0x45 ||
        bytes[2] != 0xdf || bytes[3] != 0xa3 ||
        libebml::EbmlCodeVersion.empty()) return 1;
    std::cout << "libebml-installed-api-ok\n";
    return 0;
}
EOF

g++ -std=c++14 "$smoke_dir/smoke.cpp" $(pkg-config --cflags --libs libebml) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" | grep -Fx 'libebml-installed-api-ok'
