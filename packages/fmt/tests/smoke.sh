#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- fmt fmt-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <fmt/format.h>
#include <iostream>
int main() {
  std::cout << fmt::format("{} {}", "RISC-V", 64);
}
CPP
g++ -std=c++11 "$task_dir/smoke.cpp" -lfmt -o "$task_dir/smoke"
test "$("$task_dir/smoke")" = "RISC-V 64"
