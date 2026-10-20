#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q -- tabbed tabbed-tests
rpm -V -- tabbed tabbed-tests
exec python3 -I -B /usr/libexec/tabbed-tests/qa.py /
