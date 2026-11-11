#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q -- swarp swarp-tests
rpm -V -- swarp swarp-tests
exec python3 -I -B /usr/libexec/swarp-tests/qa.py /
