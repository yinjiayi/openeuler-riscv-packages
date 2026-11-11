#!/bin/bash
# SPDX-License-Identifier: MIT
set -euo pipefail
rpm -q jshon jshon-tests
rpm -V jshon jshon-tests
exec python3 -I -B /usr/libexec/jshon-tests/qa.py /
