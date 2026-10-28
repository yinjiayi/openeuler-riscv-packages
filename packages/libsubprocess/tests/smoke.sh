#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_PRELOAD LD_LIBRARY_PATH
test -r /usr/include/cpp-subprocess/subprocess.hpp
test -r /usr/lib64/cmake/subprocess/subprocess-config.cmake
test -r /usr/lib64/cmake/subprocess/subprocess-version.cmake
test -r /usr/lib64/cmake/subprocess/subprocess-targets.cmake
qa=/usr/share/libsubprocess-tests
(cd "$qa"; sha256sum -c SHA256SUMS)
license=/usr/share/licenses/libsubprocess
if test ! -d "$license"; then license=/usr/share/licenses/libsubprocess-2.5; fi
test -r "$license/LICENSE.MIT"
test -r "$license/Apache-2.0.txt"
(cd "$license/source-notices"; sha256sum -c SHA256SUMS)
test "$(wc -l < "$license/source-notices/SHA256SUMS")" -eq 27
bash "$qa/run-qa.sh" /usr
printf '%s\n' "libsubprocess installed header/CMake consumer: 10 additive groups; original10CTest ran only during target build."
