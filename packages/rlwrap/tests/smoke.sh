#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- rlwrap
rlwrap --version | grep -F 'rlwrap 0.48'
test -x /usr/bin/rlwrap
test -f /usr/share/rlwrap/filters/README
