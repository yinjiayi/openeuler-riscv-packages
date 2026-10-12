#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <cerf.h>
#include <math.h>

int main(void) {
  double value = dawson(1.0);
  return isfinite(value) && value > 0.53 && value < 0.54 ? 0 : 1;
}
EOF

cat >"$tmpdir/smoke.cpp" <<'EOF'
#include <cerf.h>
#include <cmath>

int main() {
  std::complex<double> value = w_of_z({1.0, 1.0});
  return std::isfinite(value.real()) && std::isfinite(value.imag()) ? 0 : 1;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" $(pkg-config --cflags --libs libcerf) -o "$tmpdir/smoke-c"
${CXX:-c++} ${CXXFLAGS:-} "$tmpdir/smoke.cpp" -lcerfcpp -o "$tmpdir/smoke-cpp"
"$tmpdir/smoke-c"
"$tmpdir/smoke-cpp"
