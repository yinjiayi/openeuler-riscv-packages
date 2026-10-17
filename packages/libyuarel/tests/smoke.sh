#!/usr/bin/bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
rpm -q libyuarel libyuarel-devel
rpm -V libyuarel libyuarel-devel
test -s /usr/share/licenses/libyuarel/LICENSE
/usr/bin/bash /usr/share/libyuarel/run-tests.sh
