#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
rpm -q -- xssstate xssstate-tests
echo 'c4b6f504a6a8eb247bc60960bd65cbf9631c008449a1d71ac4c55e34be1c6011  /usr/share/xssstate/qa/xssstate-1.1.tar.gz' | sha256sum -c -
exec python3 -I -B /usr/libexec/xssstate-tests/qa.py ''
