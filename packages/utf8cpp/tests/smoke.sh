#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- utf8cpp
grep -Fq 'set(PACKAGE_VERSION "4.2.0")' \
  /usr/share/utf8cpp/cmake/utf8cppConfigVersion.cmake

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'EOF'
#include <utf8cpp/utf8.h>

#include <string>

int main() {
    const std::string valid = "openEuler \xE5\xBC\x80\xE6\x94\xBE";
    const std::string invalid = "\xC0\xAF";
    return utf8::is_valid(valid.begin(), valid.end()) &&
                   !utf8::is_valid(invalid.begin(), invalid.end())
               ? 0
               : 1;
}
EOF
c++ -std=c++17 "$smoke_dir/smoke.cpp" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
