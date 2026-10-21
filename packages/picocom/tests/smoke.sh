#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail
rpm -q -- picocom picocom-tests lrzsz
test -x /usr/bin/picocom
/usr/bin/python3 -I -B /usr/libexec/picocom-tests/qa.py /
