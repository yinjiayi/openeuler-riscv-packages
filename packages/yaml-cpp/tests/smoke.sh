#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/parse.cpp" <<'EOF'
#include <iostream>
#include <yaml-cpp/yaml.h>
int main() { YAML::Node n = YAML::Load("target: RVA23"); std::cout << n["target"].as<std::string>() << '\n'; }
EOF
c++ "$tmpdir/parse.cpp" $(pkg-config --cflags --libs yaml-cpp) -o "$tmpdir/parse"
"$tmpdir/parse" | grep -Fx 'RVA23'
