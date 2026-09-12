#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- optional-lite
test -r /usr/include/nonstd/optional.hpp
test -r /usr/lib64/cmake/optional-lite/optional-lite-config.cmake

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'CPP'
#define optional_CONFIG_SELECT_OPTIONAL 1
#include <nonstd/optional.hpp>

int main() {
  nonstd::optional<int> value(7);
  nonstd::optional<int> empty;
  return value.has_value() && value.value() == 7 && !empty.has_value() ? 0 : 1;
}
CPP
c++ -std=c++11 "$smoke_dir/smoke.cpp" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
