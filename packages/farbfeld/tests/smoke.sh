#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- farbfeld farbfeld-tests
python3 -I -B /usr/share/farbfeld/qa.py /usr/bin
