#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libshrinkwrap
rpm -V libshrinkwrap
bash /usr/share/libshrinkwrap/tests/run-tests.sh /
