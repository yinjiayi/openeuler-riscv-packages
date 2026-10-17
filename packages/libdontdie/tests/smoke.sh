#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdontdie
rpm -V libdontdie
bash /usr/share/libdontdie/tests/run-contract.sh /
