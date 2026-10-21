#!/usr/bin/env bash
# SPDX-License-Identifier: CC0-1.0
set -euo pipefail
rpm -q -- nq nq-tests
python3 -I -B /usr/libexec/nq-tests/qa.py /
