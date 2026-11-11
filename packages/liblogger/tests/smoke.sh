#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q liblogger liblogger-devel liblogger-static
rpm -V liblogger liblogger-devel liblogger-static
bash /usr/share/liblogger/tests/run-contract.sh /
