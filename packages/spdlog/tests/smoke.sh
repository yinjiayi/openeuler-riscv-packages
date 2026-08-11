#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- spdlog spdlog-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <spdlog/spdlog.h>
int main() {
  spdlog::set_pattern("%v");
  spdlog::info("openEuler RISC-V");
  return 0;
}
CPP
g++ -std=c++11 "$task_dir/smoke.cpp" -lspdlog -pthread -o "$task_dir/smoke"
"$task_dir/smoke"
