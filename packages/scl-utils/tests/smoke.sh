#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- scl-utils
test -x /usr/bin/scl
/usr/bin/scl --help 2>&1 | grep -F 'usage: scl'
