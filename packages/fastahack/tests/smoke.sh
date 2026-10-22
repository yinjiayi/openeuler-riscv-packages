#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$(rpm -q --qf '%{VERSION}' fastahack)" = 1.0.0
rpm -V fastahack
bash /usr/share/fastahack/tests/run-contract.sh /
