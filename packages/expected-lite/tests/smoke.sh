#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- expected-lite
test -r /usr/include/nonstd/expected.hpp
test -r /usr/lib64/cmake/expected-lite/expected-lite-config.cmake

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'CPP'
#define nsel_CONFIG_SELECT_EXPECTED 1
#include <nonstd/expected.hpp>

int main() {
  nonstd::expected<int, int> success(7);
  nonstd::expected<int, int> failure(nonstd::unexpect, 3);
  return success.has_value() && success.value() == 7 &&
                 !failure.has_value() && failure.error() == 3
             ? 0
             : 1;
}
CPP
c++ -std=c++11 "$smoke_dir/smoke.cpp" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
