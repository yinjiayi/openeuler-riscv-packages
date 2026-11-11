#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q -- ii ii-tests
rpm -V -- ii ii-tests
exec python3 -I -B /usr/libexec/ii-tests/qa.py /
