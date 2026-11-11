#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libinjection
rpm -q -- libinjection-devel libinjection-static libinjection-tests
rpm -V libinjection libinjection-devel libinjection-static libinjection-tests
cd /tmp
bash /usr/share/libinjection/tests/run-tests.sh /usr/lib64
