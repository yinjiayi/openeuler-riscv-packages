#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- range-v3
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <range/v3/view/iota.hpp>
int main() {
  int sum = 0;
  for (int value : ranges::views::iota(1, 5)) sum += value;
  return sum == 10 ? 0 : 1;
}
CPP
g++ -std=c++14 "$task_dir/smoke.cpp" -o "$task_dir/smoke"
"$task_dir/smoke"
