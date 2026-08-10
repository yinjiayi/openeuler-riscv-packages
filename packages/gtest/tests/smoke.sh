#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gtest gtest-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <vector>
TEST(InstalledGoogleTest, Runs) { EXPECT_EQ(6 * 7, 42); }
TEST(InstalledGoogleMock, Runs) {
  EXPECT_THAT((std::vector<int>{6, 7}), ::testing::ElementsAre(6, 7));
}
CPP
g++ -std=c++14 "$task_dir/smoke.cpp" -lgmock -lgtest_main -lgtest -pthread -o "$task_dir/smoke"
"$task_dir/smoke"
