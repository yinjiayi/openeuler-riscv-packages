#!/usr/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 openEuler RISC-V package contributors
# Licensed under Apache License2.0; full text ships in the package.
# https://www.apache.org/licenses/LICENSE-2.0
# Distributed AS IS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.
set -euo pipefail
export LC_ALL=C LANG=C PATH=/usr/bin:/bin
unset LD_LIBRARY_PATH LD_PRELOAD LD_AUDIT
qa=/usr/share/libnghttp3-tests
test -f "$qa/SHA256SUMS"
(cd /; sha256sum -c "$qa/SHA256SUMS")
(cd /usr/share/licenses/libnghttp3/source-notices; sha256sum -c SHA256SUMS)
test "$(wc -l < /usr/share/licenses/libnghttp3/source-notices/SHA256SUMS)" -eq 151
bash "$qa/run-qa.sh" installed /usr/include /usr/lib64/libnghttp3.so.9.9.0 /usr/lib64/libnghttp3.a "$qa"
printf 'libnghttp3 installed payload and shared/static API: PASS\n'
