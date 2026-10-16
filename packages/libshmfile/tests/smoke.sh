#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libshmfile libshmfile-devel
rpm -V libshmfile libshmfile-devel
bash /usr/share/libshmfile/tests/run-tests.sh /
