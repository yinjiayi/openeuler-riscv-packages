#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-only
set -euo pipefail
rpm -q -- cowsay cowsay-tests
test -x /usr/bin/cowsay
test -L /usr/bin/cowthink
/usr/bin/python3 -I -B /usr/libexec/cowsay-tests/qa.py /
