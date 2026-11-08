#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- xdo xdo-tests
exec /usr/bin/python3 -I -B /usr/libexec/xdo-tests/qa.py /
