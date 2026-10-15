#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH
rpm -q libgse libgse-devel
rpm -V libgse libgse-devel
for license in COPYING.LESSER COPYING.GPL3 COPYING.BSD; do
    test -s "/usr/share/licenses/libgse/$license"
done
library=$(readlink -f /usr/lib64/libgse.so.0)
test "$(rpm -qf --qf '%{NAME}' "$library")" = libgse
test "$(rpm -qf --qf '%{NAME}' /usr/include/gse/encap.h)" = libgse-devel
test "$(rpm -qf --qf '%{NAME}' /usr/lib64/pkgconfig/gse.pc)" = libgse-devel
# Upstream tag1.2.1 retains this internal version; do not rewrite the source.
test "$(pkg-config --modversion gse)" = 1.2.0
bash /usr/share/libgse/tests/run-contract.sh
