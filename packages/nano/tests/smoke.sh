#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- nano
nano --version | grep -F "GNU nano, version 9.2"
test -x /usr/bin/nano
test -x /usr/bin/rnano
[ -f /usr/share/man/man1/nano.1.gz ] || [ -f /usr/share/man/man1/nano.1 ]
