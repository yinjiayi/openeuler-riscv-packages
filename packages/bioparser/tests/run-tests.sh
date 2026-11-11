#!/bin/bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
root=""
case "${1:-}" in
  --staged) test "$#" -eq 2; root="$2"; test -d "$root/usr/include/bioparser" ;;
  "") test "$#" -eq 0; rpm -V bioparser bioparser-tests ;;
  *) exit 2 ;;
esac
qa="$root/usr/share/bioparser/qa"
test -f "$qa/SHA256SUMS"
(cd "$qa" && sha256sum --check --strict SHA256SUMS)
test "$(find "$qa/tests" -maxdepth 1 -name '*_test.cpp' -type f | wc -l)" -eq 6
test "$(find "$qa/tests/data" -type f | wc -l)" -eq 10
test "$(find "$qa/biosoup/include/biosoup" -type f | wc -l)" -eq 5
unset CPATH CPLUS_INCLUDE_PATH C_INCLUDE_PATH LIBRARY_PATH LD_LIBRARY_PATH CMAKE_PREFIX_PATH CMAKE_MODULE_PATH
while IFS='=' read -r key _; do
  case "$key" in GTEST_*) unset "$key" ;; esac
done < <(env)
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
cmake -S "$qa" -B "$tmp/build" \
  -Dbioparser_DIR="$root/usr/lib64/cmake/bioparser" \
  -DEXPECTED_INCLUDE="$root/usr/include" \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_CXX_FLAGS="-UNDEBUG"
cmake --build "$tmp/build" --parallel 2
"$tmp/build/original_suite" --gtest_filter='*' --gtest_output="xml:$tmp/results.xml"
python3 "$qa/check-results.py" "$tmp/results.xml"
"$tmp/build/installed_consumer" "$qa/tests/data/sample.fasta" "$qa/tests/data/sample.fasta.gz"
