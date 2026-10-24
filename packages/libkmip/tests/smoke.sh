#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libkmip
rpm -V libkmip
bash /usr/share/libkmip/run-tests.sh
