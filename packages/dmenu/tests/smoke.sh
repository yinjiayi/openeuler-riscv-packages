#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dmenu dmenu-tests
exec python3 -I -B /usr/libexec/dmenu-tests/qa.py /
