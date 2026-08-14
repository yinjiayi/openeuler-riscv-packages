#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- fast-float
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cc" <<'EOF'
#include <fast_float/fast_float.h>
int main() {
    const char text[] = "3.5";
    double value = 0;
    const auto result = fast_float::from_chars(text, text + 3, value);
    return result.ec == std::errc() && value == 3.5 ? 0 : 1;
}
EOF
c++ -std=c++17 "$smoke_dir/smoke.cc" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
