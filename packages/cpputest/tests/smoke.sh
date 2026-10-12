#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.cpp" <<'EOF'
#include <CppUTest/CommandLineTestRunner.h>
#include <CppUTest/TestHarness.h>

TEST_GROUP(InstalledLibrary) {};
TEST(InstalledLibrary, AddsIntegers) { LONGS_EQUAL(4, 2 + 2); }

int main(int argc, char **argv) {
  return CommandLineTestRunner::RunAllTests(argc, argv);
}
EOF

${CXX:-c++} ${CXXFLAGS:-} "$tmpdir/smoke.cpp" ${LDFLAGS:-} -lCppUTest -o "$tmpdir/smoke"
"$tmpdir/smoke"
