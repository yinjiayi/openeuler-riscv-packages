#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- most
test "$(printf 'openEuler-most-stdin\n' | most)" = openEuler-most-stdin
test -n "$(most /usr/share/doc/most/most.txt)"
test -f /usr/share/man/man1/most.1.gz
