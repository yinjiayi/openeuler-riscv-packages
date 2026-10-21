#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.cpp" <<'EOF'
#include <cxxopts.hpp>

int main(int argc, char **argv) {
  cxxopts::Options options("installed-cxxopts");
  options.add_options()("count", "count", cxxopts::value<int>());
  const auto result = options.parse(argc, argv);
  return result["count"].as<int>() == 7 ? 0 : 1;
}
EOF

${CXX:-c++} ${CXXFLAGS:-} -std=c++11 "$tmpdir/smoke.cpp" -o "$tmpdir/smoke"
"$tmpdir/smoke" --count 7
