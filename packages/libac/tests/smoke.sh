#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libac libac-devel
rpm -V libac libac-devel
test "$(rpm -qf --qf '%{NAME}\n' /usr/lib64/libac.so.2.0.0)" = libac
test "$(rpm -qf --qf '%{NAME}\n' /usr/include/libac.h)" = libac-devel
test "$(readlink /usr/lib64/libac.so.2)" = libac.so.2.0.0
test "$(readlink /usr/lib64/libac.so)" = libac.so.2.0.0
for file in COPYING COPYING.GPL2 COPYING.APACHE2 random_r.c twalk_r.c tdestroy.c; do
    test -s "/usr/share/licenses/libac/$file"
done
bash /usr/share/libac/tests/run-contract.sh
