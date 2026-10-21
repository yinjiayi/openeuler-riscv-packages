#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- variant-lite
test -r /usr/include/nonstd/variant.hpp
test -r /usr/lib64/cmake/variant-lite/variant-lite-config.cmake

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'CPP'
#define variant_CONFIG_SELECT_VARIANT 1
#include <nonstd/variant.hpp>

int main() {
  nonstd::variant<int, const char *> value(42);
  return nonstd::get<int>(value) == 42 && nonstd::holds_alternative<int>(value)
             ? 0
             : 1;
}
CPP
c++ -std=c++11 "$smoke_dir/smoke.cpp" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
