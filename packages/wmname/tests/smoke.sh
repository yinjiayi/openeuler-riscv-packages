#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q -- wmname wmname-tests
rpm -V -- wmname wmname-tests
exec python3 -I -B /usr/libexec/wmname-tests/qa.py /
