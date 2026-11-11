#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- snooze snooze-tests
test -x /usr/bin/snooze
python3 -I -B /usr/libexec/snooze-tests/qa.py /usr/bin/snooze /
