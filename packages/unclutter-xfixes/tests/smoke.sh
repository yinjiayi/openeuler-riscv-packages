#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- unclutter-xfixes unclutter-xfixes-tests
exec /usr/bin/python3 -I -B /usr/libexec/unclutter-xfixes-tests/qa.py /
