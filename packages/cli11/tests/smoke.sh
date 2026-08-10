#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cli11
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <CLI/CLI.hpp>
int main() {
  CLI::App app{"smoke"};
  int value = 0;
  app.add_option("--value", value)->required();
  const char *argv[] = {"smoke", "--value", "42"};
  app.parse(3, const_cast<char **>(argv));
  return value == 42 ? 0 : 1;
}
CPP
g++ -std=c++14 "$task_dir/smoke.cpp" -o "$task_dir/smoke"
"$task_dir/smoke"
