#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libhpptools
bash /usr/share/libhpptools/tests/run-tests.sh
