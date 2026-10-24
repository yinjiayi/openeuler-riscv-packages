#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH
rpm -q libgtextutils libgtextutils-devel
rpm -V libgtextutils libgtextutils-devel
test -s /usr/share/licenses/libgtextutils/COPYING
library=$(readlink -f /usr/lib64/libgtextutils-0.7.so.0)
test "$(rpm -qf --qf '%{NAME}' "$library")" = libgtextutils
test "$(pkg-config --modversion gtextutils)" = 0.7
bash /usr/share/libgtextutils/tests/run-installed-tests.sh
