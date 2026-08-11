#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- doctest
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest/doctest.h>
TEST_CASE("installed doctest runs") { CHECK(6 * 7 == 42); }
CPP
g++ -std=c++11 "$task_dir/smoke.cpp" -o "$task_dir/smoke"
"$task_dir/smoke"
