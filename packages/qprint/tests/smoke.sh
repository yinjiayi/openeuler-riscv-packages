#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q -- qprint qprint-tests make python3
test -x /usr/bin/qprint
/usr/bin/python3 -I -B /usr/libexec/qprint-tests/qa.py --installed /
