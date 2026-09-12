#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

next_day=$(dateadd 2024-02-28 +1d)
test "$next_day" = "2024-02-29"

span=$(datediff 2024-02-28 2024-03-01)
test "$span" = "2"
