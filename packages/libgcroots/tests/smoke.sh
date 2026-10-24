#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH
rpm -q libgcroots libgcroots-devel
rpm -V libgcroots libgcroots-devel
test -s /usr/share/licenses/libgcroots/COPYING
test -s /usr/share/licenses/libgcroots/COPYING.GPL3
library=$(readlink -f /usr/lib64/libgcroots.so.0)
test "$(rpm -qf --qf '%{NAME}' "$library")" = libgcroots
test "$(pkg-config --modversion gcroots)" = 0.3.2
bash /usr/share/libgcroots/tests/run-contract.sh
