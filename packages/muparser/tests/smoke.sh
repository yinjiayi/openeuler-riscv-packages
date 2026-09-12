#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- muparser muparser-devel
rpm -q --provides muparser | grep -F 'libmuparser.so.2()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/muparser-smoke.cpp" <<'EOF'
#include <cmath>
#include <muParser.h>

int main() {
    mu::Parser parser;
    parser.SetExpr("sqrt(81)+2^3");
    return std::fabs(parser.Eval() - 17.0) < 1e-12 ? 0 : 1;
}
EOF
c++ $({ pkg-config --cflags muparser; }) \
  "$smoke_dir/muparser-smoke.cpp" -o "$smoke_dir/muparser-smoke" \
  $({ pkg-config --libs muparser; })
"$smoke_dir/muparser-smoke"
