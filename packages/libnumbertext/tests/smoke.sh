#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libnumbertext libnumbertext-devel
pkg-config --modversion libnumbertext | grep -Fx '1.0.11'
spellout -l en 123 | grep -Fx 'one hundred twenty-three'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libnumbertext-smoke.cxx" <<'EOF'
#include <Numbertext.hxx>
#include <string>

int main() {
    Numbertext converter;
    converter.set_prefix("/usr/share/libnumbertext/");
    if (!converter.load("en"))
        return 1;

    std::string value = "42";
    if (!converter.numbertext(value, "en"))
        return 2;
    return value == "forty-two" ? 0 : 3;
}
EOF

g++ "$smoke_dir/libnumbertext-smoke.cxx" -o "$smoke_dir/libnumbertext-smoke" \
  $({ pkg-config --cflags --libs libnumbertext; })
"$smoke_dir/libnumbertext-smoke"

readelf -d /usr/lib64/libnumbertext-1.0.so.0 | \
  grep -F 'Library soname: [libnumbertext-1.0.so.0]'
