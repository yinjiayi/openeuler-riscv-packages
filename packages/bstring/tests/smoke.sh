#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
work="$(mktemp -d /tmp/bstring-smoke.XXXXXXXX)"
python3 /usr/share/bstring-tests/run-qa.py --phase installed \
  --prefix /usr --libdir lib64 --work-dir "$work/qa"
