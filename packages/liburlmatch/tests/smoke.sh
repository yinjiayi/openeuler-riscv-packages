#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- liburlmatch
rpm -V liburlmatch
test -s /usr/include/urlmatch.h
test -s /usr/lib64/liburlmatch.a
bash /usr/share/liburlmatch/tests/run-original-tests.sh /
