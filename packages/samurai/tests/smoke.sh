#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- samurai samurai-tests
test -x /usr/bin/samu
test -f /usr/libexec/samurai-tests/qa.py
/usr/bin/python3 -I -B /usr/libexec/samurai-tests/qa.py /
