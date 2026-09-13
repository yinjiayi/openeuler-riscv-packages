#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cproto
test -x /usr/bin/cproto
smoke_out=$(mktemp)
trap 'rm -f "$smoke_out"' EXIT
printf 'int helper(void) { return 0; }\\n' | cproto >"$smoke_out"
grep -F 'helper' "$smoke_out"
