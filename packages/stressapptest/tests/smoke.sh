#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- stressapptest
test -x /usr/bin/stressapptest
