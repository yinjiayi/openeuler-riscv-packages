#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsoundio
rpm -V libsoundio
bash /usr/share/libsoundio/tests/run-contract.sh /
