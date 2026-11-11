#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libecoli
rpm -V libecoli
bash /usr/share/libecoli/run-tests.sh
