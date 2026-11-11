#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- xsel
rpm -q -- xsel-tests
python3 -I -B /usr/libexec/xsel-tests/qa.py /
