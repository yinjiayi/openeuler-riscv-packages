#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dhex dhex-tests
test -x /usr/bin/dhex
test -f /usr/libexec/dhex-tests/qa.py
/usr/bin/python3 -I -B /usr/libexec/dhex-tests/qa.py /
