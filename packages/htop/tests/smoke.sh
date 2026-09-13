#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- htop
htop --version | grep -F "htop 3.5.2"
test -x /usr/bin/htop
[ -f /usr/share/man/man1/htop.1.gz ] || [ -f /usr/share/man/man1/htop.1 ]
