#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libnewuoa
rpm -V libnewuoa
bash /usr/share/libnewuoa/tests/run-checks.sh
