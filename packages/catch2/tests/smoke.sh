#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- catch2 catch2-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <catch2/catch_test_macros.hpp>
TEST_CASE("installed Catch2 runs") { REQUIRE(6 * 7 == 42); }
CPP
g++ -std=c++14 "$task_dir/smoke.cpp" -lCatch2Main -lCatch2 -o "$task_dir/smoke"
"$task_dir/smoke"
