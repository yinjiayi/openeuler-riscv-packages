#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libnpy
rpm -V libnpy
bash /usr/share/libnpy/run-tests.sh
