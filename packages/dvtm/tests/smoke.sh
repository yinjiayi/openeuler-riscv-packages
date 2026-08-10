#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- dvtm
dvtm -v | grep -F 'dvtm-0.15'
test -x /usr/bin/dvtm-status
