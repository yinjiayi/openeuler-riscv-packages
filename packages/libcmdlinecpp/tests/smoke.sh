#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libcmdlinecpp
rpm -V libcmdlinecpp
bash /usr/share/libcmdlinecpp/tests/run-checks.sh
