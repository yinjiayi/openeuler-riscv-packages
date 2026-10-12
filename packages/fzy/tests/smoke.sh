#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

result=$(printf 'alpha\nbeta\ngamma\n' | fzy --show-matches=alp)
test "$result" = "alpha"
